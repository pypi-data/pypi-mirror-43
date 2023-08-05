import os
import sys
import glob
import json
import pkg_resources

import jsonpickle
from datetime import datetime

import appdirs
from .templates import template_subdirs

import logging
log = logging.getLogger(__name__)


config_base_dir = None
log_dir = None
log_file_ext = None
cache_dir = None
user_data_dir = None

def setup_file_persistence(app_name):
    global config_base_dir, log_dir, log_file_ext, cache_dir, user_data_dir

    dirname = appdirs.user_config_dir(app_name)
    config_base_dir = dirname
    template_subdirs[0:0] = [get_config_subdir("templates")]

    # Make sure it exists!
    if not os.path.exists(config_base_dir):
        os.makedirs(config_base_dir)

    dirname = appdirs.user_log_dir(app_name)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    log_dir = dirname

    log_file_ext = "-%s" % datetime.now().strftime("%Y%m%d-%H%M%S")

    dirname = appdirs.user_cache_dir(app_name)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    cache_dir = dirname

    dirname = appdirs.user_data_dir(app_name)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    user_data_dir = dirname

    # Prevent py2exe from creating a dialog box on exit saying that there
    # are error messages.  It thinks that anything written to stderr is an
    # error, and the python logging module redirects everything to stderr.
    # Instead, redirect stderr to a log file in the user log directory
    frozen = getattr(sys, 'frozen', False)
    if frozen in ('dll', 'windows_exe', 'console_exe'):
        # redirect py2exe stderr/stdout to log file
        log = get_log_file_name("py2exe")
        oldlog = sys.stdout
        sys.stdout = open(log, 'w')
        if hasattr(oldlog, "saved_text"):
            sys.stdout.write("".join(oldlog.saved_text))
        sys.stderr = sys.stdout

        # The logging module won't redirect to the new stderr without help
        handler = logging.StreamHandler(sys.stderr)
        logger = logging.getLogger('')
        logger.addHandler(handler)
    else:
        log = get_log_file_name("log")
        handler = logging.FileHandler(log)
        formatter = logging.Formatter("%(levelname)s:%(name)s:%(msg)s")
        handler.setFormatter(formatter)
        logger = logging.getLogger('')
        logger.addHandler(handler)

def get_log_file_name(log_file_name_base, ext=""):
    filename = log_file_name_base + log_file_ext
    if ext:
        if not ext.startswith("."):
            filename += "."
        filename += ext
    else:
        filename += ".log"
    filename = os.path.join(log_dir, filename)
    return filename

def save_log(text, log_file_name_base, ext=""):
    filename = get_log_file_name(log_file_name_base, ext)

    try:
        with open(filename, "w") as fh:
            fh.write(text)
    except IOError:
        log.error("Failed writing %s to %s" % (log_file_name_base, filename))

def get_config_subdir(subdir):
    dirname = os.path.join(config_base_dir, subdir)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

def get_config_dir_filename(storage_type, json_name):
    return os.path.join(config_base_dir, json_name + "." + storage_type)

def get_file_config_data(subdir, filename, default_on_error=None, mode='r'):
    try:
        file_path = get_config_dir_filename(subdir, filename)
        with open(file_path, mode) as fh:
            data = fh.read()
        return data
    except IOError:
        # file not found
        return default_on_error

def save_file_config_data(subdir, filename, data, mode='w'):
    file_path = get_config_dir_filename(subdir, filename)
    with open(file_path, mode) as fh:
        fh.write(data)

def get_json_data(json_name, default_on_error=None):
    raw = get_file_config_data("json", json_name)
    if raw is None:
        return default_on_error
    try:
        json_data = jsonpickle.decode(raw)
        try:
            # new format is a list with a format identifier as the first ntry
            if json_data[0] == "format=v2":
                decoded = json_data[1]
        except KeyError:
            # deprecated format was a dictionary, and was creating an xtra
            # layer of indirection by encoding the jsonpickle as another thing
            json_data = json.loads(raw)
            encoded = json_data[json_name]
            decoded = jsonpickle.decode(encoded)
        return decoded
    except ValueError:
        # bad JSON format
        log.error("Bad JSON format in preferences file: %s" % json_name)
        return default_on_error

def save_json_data(json_name, data):
    json_data = ["format=v2", data]
    encoded = jsonpickle.encode(json_data)
    save_file_config_data("json", json_name, encoded)

def get_bson_data(bson_name):
    import bson

    raw = get_file_config_data("bson", bson_name, mode='rb')
    if raw is not None and len(raw) > 0:
        bson_data = bson.loads(raw)
        data = bson_data[bson_name]
    else:
        raise IOError("Blank BSON data")
    return data

def save_bson_data(bson_name, data):
    import bson

    bson_data = {bson_name: data}
    raw = bson.dumps(bson_data)
    save_file_config_data("bson", bson_name, raw, mode='wb')

def get_user_dir(subdir):
    dirname = os.path.join(user_data_dir, subdir)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

def get_user_dir_filename(subdir, json_name):
    return os.path.join(get_user_dir(subdir), json_name)

def get_user_data(subdir, filename, default_on_error=None, mode='r'):
    try:
        file_path = get_user_dir_filename(subdir, filename)
        with open(file_path, mode) as fh:
            data = fh.read()
        return data
    except IOError:
        # file not found
        return default_on_error

def save_user_data(subdir, filename, data, mode='w'):
    file_path = get_user_dir_filename(subdir, filename)
    with open(file_path, mode) as fh:
        fh.write(data)

def get_available_user_data(subdir):
    config_dir = get_user_dir(subdir)
    globname = os.path.join(config_dir, "*")
    available = [os.path.basename(a) for a in glob.glob(globname)]
    return available

def get_text_user_data(subdir, filename, default_on_error=None):
    return get_user_data(subdir, filename, default_on_error, 'r')

def save_text_user_data(subdir, filename, data):
    return save_user_data(subdir, filename, data)

def get_binary_user_data(subdir, filename, default_on_error=None):
    return get_user_data(subdir, filename, default_on_error, 'rb')

def save_binary_user_data(subdir, filename, data):
    return save_user_data(subdir, filename, data, 'wb')


def restore_from_last_time():
    modules = []
    for entry_point in pkg_resources.iter_entry_points('sawx.remember'):
        mod = entry_point.load()
        log.debug(f"restore_from_last_time: Found module {entry_point.name}")
        try:
            restore = getattr(mod, 'restore_from_last_time')
        except AttributeError:
            log.warning(f"restore_from_last_time: no restore function in module {entry_point.name}")
        else:
            restore()
            modules.append(mod)
    return modules


def remember_for_next_time(modules):
    for mod in modules:
        log.debug(f"remember_for_next_time: {mod}")
        try:
            remember = getattr(mod, 'remember_for_next_time')
        except AttributeError:
            log.warning(f"remember_for_next_time: no remember function in module {mod}")
        else:
            remember()
