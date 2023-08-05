import os
import sys
import inspect
import pkg_resources
import importlib
import json

import wx

from . import action
from . import errors
# from . import preferences
from .utils import jsonutil
from .utils.command import StatusFlags
from .menubar import MenuDescription

import logging
log = logging.getLogger(__name__)


def get_editors():
    editors = []
    for entry_point in pkg_resources.iter_entry_points('sawx.editors'):
        mod = entry_point.load()
        log.debug(f"get_edtiors: Found module {entry_point.name}")
        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj) and SawxEditor in obj.__mro__[1:]:
                # only use subclasses of SawxEditor, not the
                # SawxEditor base class itself
                log.debug(f"get_editors: Found editor class {name}")
                editors.append(obj)
    return editors


def find_editor_class_for_file(file_metadata):
    """Find the "best" editor for a given MIME type string.

    First attempts all editors with exact matches for the MIME string,
    and if no exact matches are found, returns through the list to find
    one that can edit that class of MIME.
    """
    editors = get_editors()
    log.debug(f"finding editors using {editors}")
    for editor in editors:
        if editor.can_edit_file_exact(file_metadata):
            return editor
    for editor in editors:
        if editor.can_edit_file_generic(file_metadata):
            return editor
    raise errors.UnsupportedFileType(f"No editor available for {file_metadata}")

def find_editor_class_by_name(name):
    """Find the editor class given its class name

    Returns the SawxEditor subclass whose `name` class attribute matches
    the given string.
    """
    editors = get_editors()
    log.debug(f"finding editors using {editors}")
    for editor in editors:
        if editor.name == name:
            return editor
        if name in editor.compatibility_names:
            return editor
    raise errors.EditorNotFound(f"No editor named {name}")


class SawxEditor:
    name = "sawx_base_editor"
    pretty_name = "Sawx Framework Base Editor"

    # list of alternate names for this editor, for compatibility with task_ids
    # from Sawx 1.0
    compatibility_names = []

    menubar_desc = [
        ["File",
            ["New",
                "new_blank_file",
                None,
                "new_file_from_template",
            ],
            "open_file",
            ["Open Recent",
                "open_recent",
            ],
            None,
            "save_file",
            "save_as",
            None,
            "quit",
        ],
        ["Edit",
            "undo",
            "redo",
            None,
            "copy",
            "cut",
            "paste",
            None,
            "prefs",
        ],
        ["Help",
            "about",
        ],
    ]

    keybinding_desc = {
        "new_file": "Ctrl+N",
        "open_file": "Ctrl+O",
        "save_file" : "Ctrl+S",
        "save_as" : "Shift+Ctrl+S",
        "cut": "Ctrl+X",
        "copy": "Ctrl+C",
        "paste": "Ctrl+V",
    }

    toolbar_desc = [
        "open_file", "save_file", None, "undo", "redo", None, "copy", "cut", "paste"
    ]

    statusbar_desc = [
        ["main", -1],
        ["debug", -1],
    ]

    module_search_order = ["sawx.actions"]

    extra_metadata_file_extensions = []

    tool_bitmap_size = (24, 24)

    preferences_module = "sawx.preferences"

    preferences = None

    # if an editor is marked as transient, it will be replaced if it's the
    # active frame when a new frame is added.
    transient = False

    @property
    def is_dirty(self):
        return False

    @property
    def can_copy(self):
        return False

    @property
    def can_paste(self):
        return False

    @property
    def can_undo(self):
        return self.document is not None and self.document.undo_stack.can_undo()

    @property
    def can_redo(self):
        return self.document is not None and self.document.undo_stack.can_redo()

    @property
    def best_file_save_dir(self):
        attempts = []
        if self.last_saved_uri:
            # try most recent first
            attempts.append(self.last_saved_uri)
        if self.last_loaded_uri:
            # try directory of last loaded file next
            attempts.append(self.last_loaded_uri)
        if self.document and self.document.uri:
            # path of current file is the final try
            attempts.append(self.document.uri)

        print(("attempts for best_file_save_dir: %s" % str(attempts)))
        dirpath = ""
        for uri in attempts:
            uri_dir = os.path.dirname(uri)
            if os.path.exists(uri_dir):
                dirpath = uri_dir
                break

        return dirpath

    @property
    def title(self):
        uri = self.last_saved_uri or self.last_loaded_uri
        if uri:
            return os.path.basename(uri)
        return self.pretty_name

    @property
    def is_transient(self):
        return self.transient or self.__class__ == SawxEditor

    def __init__(self, action_factory_lookup=None):
        self.tab_name = self.pretty_name
        self.frame = None
        if action_factory_lookup is None:
            action_factory_lookup = {}
        self.action_factory_lookup = action_factory_lookup
        self.last_loaded_uri = None
        self.last_saved_uri = None
        self.document = None
        self.extra_metadata = {}
        if self.__class__.preferences is None:
            self.create_preferences()

    @classmethod
    def create_preferences(cls):
        mod = importlib.import_module(cls.preferences_module)
        fallback_cls = None
        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj):
                mro_names = [str(s) for s in obj.__mro__]
                if "SawxFrameworkPreferences" in mro_names[0]:
                    fallback_cls = obj
                for obj_name in mro_names[1:]:
                    if "SawxFrameworkPreferences" in obj_name:
                        cls.preferences = obj()
                        break
        if cls.preferences is None:
            if fallback_cls:
                cls.preferences = fallback_cls()
            else:
                raise RuntimeError("No preference module {self.preferences_module}")

    def prepare_destroy(self):
        print(f"prepare_destroy: {self.tab_name}")
        self.control = None
        self.frame = None

    def create_control(self, parent):
        return wx.StaticText(parent, -1, "Base class for Sawx editors")

    def create_event_bindings(self):
        pass

    def load(self, path, file_metadata, args=None):
        pass

    def load_success(self, path, file_metadata):
        self.last_loaded_uri = path
        from sawx.actions import open_recent
        open_recent.open_recent.append(path)
        self.tab_name = os.path.basename(path)
        self.frame.status_message(f"loaded {path} {file_metadata}", True)

    #### popup menu utilities

    def show_popup(self, popup_menu_desc, popup_data=None):
        valid_id_map = {}
        menu = MenuDescription("popup", popup_menu_desc, self, valid_id_map, popup_data=popup_data)
        menu.sync_with_editor(valid_id_map)
        action_id = self.control.GetPopupMenuSelectionFromUser(menu.menu)
        if action_id == wx.ID_NONE:
            log.debug("show_popup: cancelled")
        else:
            action_key, action = valid_id_map[action_id]
            log.debug(f"show_popup: id={action_id}, action_key='{action_key}' action={action}")
            try:
                wx.CallAfter(action.perform, action_key)
            except AttributeError:
                log.warning(f"no perform method for {action}")


    #### command processing

    def undo(self):
        undo = self.document.undo_stack.undo(self)
        self.process_flags(undo.flags)

    def redo(self):
        undo = self.document.undo_stack.redo(self)
        self.process_flags(undo.flags)

    def end_batch(self):
        self.document.undo_stack.end_batch()

    def process_command(self, command, batch=None):
        """Process a single command and immediately update the UI to reflect
        the results of the command.
        """
        f = StatusFlags()
        undo = self.process_batch_command(command, f, batch)
        if undo.flags.success:
            self.process_flags(f)
        return undo

    def process_batch_command(self, command, f, batch=None):
        """Process a single command but don't update the UI immediately.
        Instead, update the batch flags to reflect the changes needed to
        the UI.
        
        """
        undo = self.document.undo_stack.perform(command, self, batch)
        f.add_flags(undo.flags, command)
        return undo

    def process_flags(self, flags):
        """Perform the UI updates given the StatusFlags or BatchFlags flags
        
        """
        log.debug("processing flags: %s" % str(flags))
        d = self.document
        visible_range = False

        if flags.message:
            self.task.status_bar.message = flags.message

        if flags.rebuild_ui:
            log.debug(f"process_flags: rebuild_ui")
            d.recalc_event(flags=flags)
        if flags.refresh_needed:
            log.debug(f"process_flags: refresh_needed")
            d.recalc_event(flags=flags)


    #### metadata

    def load_extra_metadata(self, path, default_metadata):
        self.extra_metadata.update(default_metadata)
        for ext in self.extra_metadata_file_extensions:
            mpath = path + "." + ext
            try:
                fh = open(mpath, 'r')
                text = fh.read()
            except IOError:
                log.debug(f"load_extra_metadata: no metadata found at {mpath}")
                pass
            else:
                try:
                    metadata = jsonutil.unserialize(mpath, text)
                except ValueError as e:
                    log.error(f"invalid data in {mpath}: {e}")
                    metadata = {}
                self.extra_metadata.update(metadata)

    @property
    def editor_metadata(self):
        m = self.extra_metadata.get(self.name, {})
        return m

    def get_editor_specific_metadata(self, keyword):
        """Get the metadata for the keyword that is specific to this editor
        class.

        E.g. if there is a layout stored in the metadata, it will be in
        metadata[self.name]['layout']:

        {
            "omnivore.byte_edit": {
                "layout": {
                    "sidebars": [ ... ],
                    "tile_manager": { .... },
                }
        }
        """
        try:
            layout_dict = metadata[self.name][keyword]
        except KeyError:
            layout_dict = {}
        return layout_dict

    @classmethod
    def can_edit_file_exact(cls, file_metadata):
        return False

    @classmethod
    def can_edit_file_generic(cls, file_metadata):
        return False

    @classmethod
    def can_edit_file(cls, file_metadata):
        return cls.can_edit_file_exact(file_metadata) or cls.can_edit_file_generic(file_metadata)

    def calc_usable_action(self, action_key):
        try:
            action_factory = self.action_factory_lookup[action_key]
        except KeyError:
            action_factory = action.find_action_factory(self.module_search_order, action_key)
            self.action_factory_lookup[action_key] = action_factory
        return action_factory(self, action_key)
