import os
import types
import io as BytesIO
import uuid

import numpy as np
import jsonpickle

# Enthought library imports.
from .utils.events import EventHandler
from .utils.command import UndoStack
from .utils import jsonutil
from .utils.nputil import to_numpy
from .templates import get_template

import logging
log = logging.getLogger(__name__)


class BaseDocument:

    # Class properties

    json_expand_keywords = {}

    metadata_extension = ".omnivore"

    def __init__(self, raw_bytes=b""):
        self.uri = ""
        self.mime = "application/octet-stream"
        self.name = ""
        self.undo_stack = UndoStack()
        self.raw_bytes = to_numpy(raw_bytes)
        self.uuid = str(uuid.uuid4())
        self.document_id = -1
        self.change_count = 0
        self.global_resource_cleanup_functions = []
        self.permute = None
        self.segments = []
        self.baseline_document = None
        self.extra_metadata = {}

        # events
        self.recalc_event = EventHandler(self, True)
        self.structure_changed_event = EventHandler(self, True)
        self.byte_values_changed_event = EventHandler(self, True)  # and possibly style, but size of array remains unchanged

        self.byte_style_changed_event = EventHandler(self, True)  # only styling info may have changed, not any of the data byte values

    @property
    def can_revert(self):
        return self.uri != ""

    @property
    def menu_name(self):
        if self.uri:
            return "%s (%s)" % (self.name, self.uri)
        return self.name

    @property
    def root_name(self):
        name, _ = os.path.splitext(self.name)
        return name

    @property
    def extension(self):
        _, ext = os.path.splitext(self.name)
        return ext

    @property
    def is_on_local_filesystem(self):
        path = self.filesystem_path()
        return bool(path)

    @classmethod
    def get_blank(cls):
        return cls(raw_bytes=b"")

    def __str__(self):
        return f"Document: id={self.document_id}, mime={self.metadata.mime}, {self.metadata.uri}"

    def __len__(self):
        return np.alen(self.raw_bytes)

    def __getitem__(self, val):
        return self.raw_bytes[val]

    @property
    def dirty(self):
        return self.undo_stack.is_dirty()

    def to_bytes(self):
        return self.raw_bytes.tostring()

    def load_permute(self, editor):
        if self.permute:
            self.permute.load(self, editor)

    def filesystem_path(self):
        try:
            fs_, relpath = fs.opener.opener.parse(self.uri)
            if fs_.hassyspath(relpath):
                return fs_.getsyspath(relpath)
        except fs.errors.FSError:
            pass
        return None

    @property
    def bytestream(self):
        return BytesIO.BytesIO(self.raw_bytes)

    # serialization

    def load_metadata_before_editor(self, guess):
        extra = self.load_extra_metadata_before_editor(guess)
        self.restore_extra_from_dict(extra)
        self.extra_metadata = extra

    def load_extra_metadata_before_editor(self, guess):
        ext = self.metadata_extension
        return guess.json_metadata.get(ext, dict())

    def calc_unserialized_template(self, template):
        try:
            text = get_template(template)
        except OSError:
            log.debug("no template for %s" % template)
            e = {}
        else:
            e = jsonutil.unserialize(template, text)
        return e

    def get_filesystem_extra_metadata_uri(self):
        """ Get filename of file used to store extra metadata
        """
        return None

    def get_metadata_for(self, task):
        """Return extra metadata for the particular task

        """
        # Each task has its own section in the metadata so they can save stuff
        # without fear of stomping on another task's data. Also, when saving,
        # they can overwrite their task stuff without changing an other task's
        # info so that other task's stuff can be re-saved even if that task
        # wasn't used in this editing session.
        try:
            return self.extra_metadata[task.editor_id]
        except KeyError:
            log.info("%s not in task specific metadata; falling back to old metadata storage" % task.editor_id)

        # For compatibility with pre-1.0 versions of Sawx which stored
        # metadata for all tasks in the root directory
        return self.extra_metadata

    def init_extra_metadata_dict(self, editor):
        """ Creates new metadata dictionary for metadata to be serialized

        The returned dict includes all the current document properties and all
        the task specific metadata in the originally loaded document.

        The task specific metadata will be replaced by values in the current
        task.
        """
        mdict = {}
        known = set(editor.task.known_editor_ids)
        for k, v in self.extra_metadata.items():
            if k in known:
                mdict[k] = dict(v)
        self.serialize_extra_to_dict(mdict)
        return mdict

    def store_task_specific_metadata(self, editor, mdict, task_dict):
        # FIXME: should handle all tasks that have changed in this edit
        # session, not just the one that is being saved.
        task_name = editor.task.editor_id
        mdict[task_name] = task_dict
        mdict["last_task_id"] = task_name

    def serialize_extra_to_dict(self, mdict):
        """Save extra metadata to a dict so that it can be serialized
        """
        mdict["document uuid"] = self.uuid
        if self.baseline_document is not None:
            mdict["baseline document"] = self.baseline_document.metadata.uri

    def restore_extra_from_dict(self, e):
        log.debug("restoring extra metadata: %s" % str(e))
        if 'document uuid' in e:
            self.uuid = e['document uuid']
        # if 'baseline document' in e:
        #     try:
        #         self.load_baseline(e['baseline document'])
        #     except DocumentError:
        #         pass
        if 'last_task_id' in e:
            self.last_task_id = e['last_task_id']

    def load_baseline(self, uri, confirm_callback=None):
        log.debug(f"loading baseline data from {uri}")
        if confirm_callback is None:
            confirm_callback = lambda a,b: True
        try:
            guess = FileGuess(uri)
        except Exception as e:
            log.error("Problem loading baseline file %s: %s" % (uri, str(e)))
            raise DocumentError(str(e))
        raw_bytes = guess.numpy
        difference = len(raw_bytes) - len(self)
        if difference > 0:
            if confirm_callback("Truncate baseline data by %d bytes?" % difference, "Baseline Size Difference"):
                raw_bytes = raw_bytes[0:len(self)]
            else:
                raw_bytes = []
        elif difference < 0:
            if confirm_callback("Pad baseline data with %d zeros?" % (-difference), "Baseline Size Difference"):
                raw_bytes = np.pad(raw_bytes, (0, -difference), "constant", constant_values=0)
            else:
                raw_bytes = []
        if len(raw_bytes) > 0:
            self.init_baseline(guess.metadata, raw_bytes)
        else:
            self.del_baseline()

    def save_to_uri(self, uri, editor, saver=None, save_metadata=True):
        # Have to use a two-step process to write to the file: open the
        # filesystem, then open the file.  Have to open the filesystem
        # as writeable in case this is a virtual filesystem (like ZipFS),
        # otherwise the write to the actual file will fail with a read-
        # only filesystem error.
        raw_bytes = self.calc_raw_bytes_to_save(editor, saver)

        if uri.startswith("file://"):
            # FIXME: workaround to allow opening of file:// URLs with the
            # ! character
            uri = uri.replace("file://", "")
        fs, relpath = opener.parse(uri, writeable=True)
        fh = fs.open(relpath, 'wb')
        log.debug("saving to %s" % uri)
        fh.write(raw_bytes)
        fh.close()
        fs.close()

        if save_metadata:
            self.save_metadata_to_uri(uri, editor)

    def save_metadata_to_uri(self, uri, editor):
        mdict = self.calc_metadata_to_save(editor)
        ext = self.metadata_extension
        if mdict:
            fs, relpath = opener.parse(uri + ext, writeable=True)
            log.debug("saving extra metadata to %s" % relpath)
            jsonpickle.set_encoder_options("json", sort_keys=True, indent=4)
            raw_bytes = jsonpickle.dumps(mdict)
            text = jsonutil.collapse_json(raw_bytes, 8, self.json_expand_keywords)
            header = editor.get_extra_metadata_header()
            fh = fs.open(relpath, 'w')
            fh.write(header)
            fh.write(text)
            fh.close()
            fs.close()

    def calc_raw_bytes_to_save(self, editor, saver):
        if saver is None:
            raw_bytes = self.raw_bytes.tostring()
        else:
            raw_bytes = saver(self, editor)
        return raw_bytes

    def calc_metadata_to_save(self, editor):
        mdict = self.init_extra_metadata_dict(editor)
        task_metadata = dict()
        editor.to_metadata_dict(task_metadata, self)
        self.store_task_specific_metadata(editor, mdict, task_metadata)
        return mdict

    def save_next_to_on_filesystem(self, ext, data, mode="w"):
        path = self.filesystem_path()
        if not path:
            raise RuntimeError("Not on local filesystem")
        dirname = os.path.dirname(path)
        if dirname:
            if not ext.startswith("."):
                ext = "." + ext
            basename = self.root_name + ext
            filename = os.path.join(dirname, basename)
            with open(filename, mode) as fh:
                fh.write(data)
        else:
            raise RuntimeError(f"Unable to determine path of {path}")
        return basename

    #### Cleanup functions

    def add_cleanup_function(self, func):
        # Prevent same function from being added multiple times
        if func not in self.global_resource_cleanup_functions:
            self.global_resource_cleanup_functions.append(func)

    def global_resource_cleanup(self):
        for f in self.global_resource_cleanup_functions:
            log.debug("Calling cleanup function %s" % f)
            f()
