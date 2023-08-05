import importlib

import wx

from . import art
from . import errors

import logging
log = logging.getLogger(__name__)


global_action_ids = {
    "about": wx.ID_ABOUT,
    "quit": wx.ID_EXIT,
    "prefs": wx.ID_PREFERENCES,
    "new_file": wx.ID_NEW,
    "open_file": wx.ID_OPEN,
    "save_file": wx.ID_SAVE,
    "save_as": wx.ID_SAVEAS,
    "copy": wx.ID_COPY,
    "cut": wx.ID_CUT,
    "paste": wx.ID_PASTE,
    "undo": wx.ID_UNDO,
    "redo": wx.ID_REDO,
}


def get_action_id(action_key):
    global global_action_ids

    try:
        id = global_action_ids[action_key]
    except KeyError:
        id = wx.NewId()
        global_action_ids[action_key] = id
    return id

found_modules = {}
ignore_modules = set()

def find_action_factory_in_module(mod_root, action_key):
    """Given a module name, search for the action using heuristics matching
    based on the action name.

    First, the module mod_root.action_key is searched for the class named
    action_key. If not found, the action_key is shortened in successive steps,
    breaking up the action name by underscores. If it is not found in any of
    those steps, it is searched for in mod_root.__init__.

    For example, if the module is "sawx.actions" and the action
    key is "file_save_as", the lookup order will be:

        sawx.actions.file_save_as.py
        sawx.actions.file_save.py
        sawx.actions.file.py
        sawx.actions.__init__.py
    """
    global found_modules, ignore_modules

    action_key_parts = action_key.split("_")
    modules = []
    while bool(action_key_parts):
        modules.append("." + "_".join(action_key_parts))
        action_key_parts.pop()
    modules.append("")
    for ext in modules:
        mod_name = f"{mod_root}{ext}"
        if mod_name in ignore_modules:
            log.debug(f"ignoring {mod_name}")
            continue
        try:
            mod = found_modules[mod_name]
            log.debug(f"found previously discovered {mod_name}")
        except KeyError:
            try:
                spec = importlib.util.find_spec(mod_name)
            except Exception as e:
                log.error(f"syntax error in module {mod_name}: {e}")
                import traceback
                log.error(traceback.format_exc())
                ignore_modules.add(mod_name)
                continue
            else:
                if spec is None:
                    log.debug(f"non-existent module {mod_name}")
                    ignore_modules.add(mod_name)
                    continue
            try:
                mod = importlib.import_module(mod_name)
            except Exception as e:
                log.error(f"error loading module {mod_name}: {e}")
                import traceback
                log.error(traceback.format_exc())
                ignore_modules.add(mod_name)
                continue
            else:
                log.debug(f"found module {mod_name}")
                found_modules[mod_name] = mod

        try:
            factory = mod.action_factory
        except AttributeError:
            log.debug(f"no callable action_factory in {mod_name}")
        else:
            log.debug(f"found callable action_factory in {mod_name}")
            return factory
        log.debug(f"searching in {mod_name} for '{action_key}'")
        try:
            factory = getattr(mod, action_key)
        except AttributeError:
            log.debug(f"no callable {action_key} in {mod_name}")
        else:
            log.debug(f"found callable {action_key} in {mod_name}")
            return factory

def find_action_factory(module_search_order, action_key):
    """Search for the action given its key.

    The module search order is a list of module names. Within each of those
    module names, the action is searched for using some heuristics based on the
    action name. See `find_action_factory_in_module` for more details.

    If no action is found, KeyError is raised.
    """
    for mod in module_search_order:
        action_factory = find_action_factory_in_module(mod, action_key)
        if action_factory is not None:
            return action_factory
    else:
        raise KeyError(f"no action factory found for {action_key} in {module_search_order}")

class SawxAction:
    name = "base action"

    def __init__(self, editor, action_key):
        self.editor = editor
        self.popup_data = None  # set by MenuDescription if action is in a popup menu
        self.init_from_editor()

    def calc_name(self, action_key):
        return self.name

    def calc_icon_name(self, action_key):
        return action_key

    def perform(self, action_key):
        raise AttributeError(f"no perform method defined for {self}")

    def calc_menu_sub_keys(self, action_key):
        """Return any dynamically created action_keys

        Actions that create multiple entries in the menubar/toolbar must create
        unique action_keys here."""
        raise AttributeError("this action has no dynamically created sub-actions")

    def append_to_menu(self, menu, id, action_key):
        menu.Append(id, self.calc_name(action_key))

    def append_to_toolbar(self, tb, id, action_key):
        name = self.calc_name(action_key)
        tb.AddTool(id, name, self.calc_bitmap(action_key), wx.NullBitmap, wx.ITEM_NORMAL, name, f"{action_key} id={id} '{name}'", None)

    def calc_bitmap(self, action_key):
        icon_name = self.calc_icon_name(action_key)
        return art.get_bitmap(icon_name, self.editor.tool_bitmap_size)

    def init_from_editor(self):
        pass

    def calc_enabled(self, action_key):
        return True

    def sync_menu_item_from_editor(self, action_key, menu_item):
        state = self.calc_enabled(action_key)
        menu_item.Enable(state)

    def sync_tool_item_from_editor(self, action_key, toolbar_control, id):
        state = self.calc_enabled(action_key)
        toolbar_control.EnableTool(id, state)


class SawxActionRadioMixin:
    def append_to_menu(self, menu, id, action_key):
        menu.AppendCheckItem(id, self.calc_name(action_key))

    def append_to_toolbar(self, tb, id, action_key):
        name = self.calc_name(action_key)
        tb.AddTool(id, name, self.calc_bitmap(action_key), wx.NullBitmap, wx.ITEM_RADIO, name, f"{action_key} id={id} '{name}'", None)


class SawxRadioAction(SawxActionRadioMixin, SawxAction):
    def calc_checked(self, action_key):
        """Return checked state of item

        If the item passed into this function is different than the item from
        the source, raise `RecreateDynamicMenuBar` error to force recalculation
        of the whole menubar.
        """
        raise NotImplementedError

    def sync_menu_item_from_editor(self, action_key, menu_item):
        if self.calc_enabled(action_key):
            state = self.calc_checked(action_key)
            log.debug(f"{action_key}: checked={state}")
            menu_item.Enable(True)
            menu_item.Check(state)
        else:
            menu_item.Enable(False)


class SawxActionListMixin:
    prefix = "_prefix_name_"

    empty_list_name = "No Items"

    def init_prefix(self):
        self.prefix_count = len(self.prefix)

    def init_from_editor(self):
        self.init_prefix()
        self.current_list = self.calc_list_items()

    def calc_list_items(self):
        return []

    def get_index(self, action_key):
        return int(action_key[self.prefix_count:])

    def get_item(self, action_key):
        return self.current_list[self.get_index(action_key)] if self.current_list else None

    def calc_name(self, action_key):
        if len(self.current_list) == 0:
            return self.empty_list_name
        return str(self.get_item(action_key))

    def calc_menu_sub_keys(self, action_key):
        if len(self.current_list) == 0:
            return [self.prefix + "empty"]
        return [f"{self.prefix}{i}" for i in range(len(self.current_list))]


class SawxListAction(SawxActionListMixin, SawxAction):
    def sync_menu_item_from_editor(self, action_key, menu_item):
        if self.current_list:
            state = self.calc_enabled(action_key)
            menu_item.Enable(state)
        else:
            if self.calc_list_items():
                raise errors.RecreateDynamicMenuBar
            menu_item.Enable(False)

    def perform(self, action_key):
        raise NotImplementedError


class SawxRadioListAction(SawxActionListMixin, SawxActionRadioMixin, SawxAction):

    def calc_checked_list_item(self, action_key, index, item):
        """Return checked state of item

        If the item passed into this function is different than the item from
        the source, raise `RecreateDynamicMenuBar` error to force recalculation
        of the whole menubar.
        """
        raise NotImplementedError

    def sync_menu_item_from_editor(self, action_key, menu_item):
        if self.current_list:
            state = self.calc_enabled(action_key)
            if state:
                index = self.get_index(action_key)
                item = self.current_list[index]
                checked = self.calc_checked_list_item(action_key, index, item)
                log.debug(f"{action_key}: checked={state}, {item}")
            else:
                checked = False
            menu_item.Enable(state)
            menu_item.Check(checked)
        else:
            if self.calc_list_items():
                raise errors.RecreateDynamicMenuBar
            menu_item.Enable(False)

    def perform(self, action_key):
        raise NotImplementedError
