# -*- coding: utf8 -*-
"""

********************
``helpers/funcs.py``
********************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``funcs.py`` is a helpers module to provide functions commonly used throughout.

"""
import os
import shutil
import re
import version as my_version
import customlogging as log
logger = log.config_logger(name=__name__)

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(0, 1, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class Const(object):
    """Allows attributes to be treated like constants where they can be set one time only.

    Raises:
        ConstError if attribute already exists.

    """
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Cannot Reassign Attribute: {}.{}".format(self.__class__.__name__, name)
        self.__dict__[name] = value


def set_kwargs(obj, kwargs):
    """Sets attributes to specified existing object.


    Args:
        obj (str): name of the object to assign attribute(s).
        kwargs (dict): dictionary of key, values, where key is the attribute and value is the vaule to assign

    Returns:
        None

    """
    if kwargs:
        for k, v in kwargs.iteritems():
            setattr(obj, k, v)


def get_kwarg(arg, kwargs, default):
    """Finds arg in kwargs and returns the value. If arg is not found return the provided default value.

    Args:
        arg (str): Name of argument to extract
        kwargs (dict): Dictionary of keys, values to find and return ``arg`` value from.
        default: The value to assign if ``arg`` is not a key in ``kwargs``

    Returns:
        ``default``

    """
    if arg in kwargs:
        return kwargs[arg]
    else:
        return default


def validate_file(f, touch=False):
    """Checks the given file exists on the file-system. If touch is True, create the file if it is missing.

    Args:
        f (str): Full path, including file name, of the file to validate.
        touch (bool, optional): If set creates an empty file if not found on the file-system.
            Default value: ``False``

    Returns:
        ``True`` on success, ``False`` otherwise.

    """
    basedir = os.path.dirname(f)
    if os.path.exists(f):
        logger.info('Found File: {}'
                    .format(f))
        return True
    else:
        logger.critical('File Missing on System: {}'
                        .format(f))
        if touch:
            logger.info('Creating File: {}'
                        .format(f))
            if not os.path.exists(basedir):
                os.makedirs(basedir)
            with open(f, 'a'):
                os.utime(f, None)
            return True
        else:
            return False


def replace_tag_with_attr_value(obj, tag):
    """Replaces a ``<TAG>`` with a corresponding attribute value.

    Looks for ``<TAG>`` (enclosed in <>) in tag string passed to the function, and if found returns a
    string with the tag replaced by the value as ``obj.<TAG>`` attribute.

    If the attribute exists but is not populated with a value an "empty" string ``''`` is returned.
    This allows all <TAG> options in the layout configuration to be optional.

    Args:
        obj (obj): Object to assign replaced ``<TAG>`` as attribute.
        tag (str): string to check for sub-strings enclosed in ``<>``.

    Returns:
        (str): An empty string if corresponding attribute for the ``<TAG>`` is **not** found; or the
        corresponding attribute if found; or the original ``<TAG>`` if anything else.

    """
    if '<' in tag and '>' in tag:
        attribute_tag = strip_tag(tag)
        obj.logger.debug('Processing {tag}: {attribute_tag}'
                         .format(tag=tag, attribute_tag=attribute_tag))
    else:
        obj.logger.debug('Not a Valid Tag: {tag}'
                         .format(tag=tag))
        return tag

    if hasattr(obj, attribute_tag):
        if not getattr(obj, attribute_tag):
            obj.logger.critical('Attribute Not Found: {attribute_tag}'
                                .format(attribute_tag=attribute_tag))
            return ''
        else:
            obj.logger.debug('Valid Tag {tag}: {attribute_tag}'
                             .format(tag=tag, attribute_tag=attribute_tag))

            resolved_attr = str(getattr(obj, attribute_tag))
            obj.logger.debug('Resolved Attribute from Tag: {resolved_attr}'
                             .format(resolved_attr=resolved_attr))
            return re.sub('(<[^>]+>)', resolved_attr, tag)
    else:
        obj.logger.critical('Attribute Not Found: {attribute_tag}'
                            .format(attribute_tag=attribute_tag))
    return tag


def strip_tag(tag):
    """Removes the ``<`` and ``>`` from tag and returns the lowercase string enclosed.

    Args:
        tag (str): UPPERCASE tag enclosed in ``<`` and ``>``

    Returns:
        (str): lowercase ``TAG`` with ``<`` and ``>`` stripped.

    """
    stripped_tag = (tag[tag.find('<') + 1:tag.find('>')]).lower()
    return stripped_tag


def readfile_as_list(full_path):
    """Takes a full-path to file and returns the contents as a list.

    Args:
        full_path (str): Full path, including file name, of the file to read from.

    Returns:
        (list): Line-by-line list of file contents.

    """
    if os.path.isfile(full_path):
        with open(full_path) as f:
            return f.readlines()
    else:
        logger.critical('File Does Not Exist on File-System: {file}'
                         .format(file=full_path))
        return False

def writefile_as_list(full_path, contents):
    """Takes a list and writes contents line-by-line to file.

    Args:
        full_path (str): Full path, including file name, of the file to write.
        contents (list): Line-by-line list of contents to write.

    Returns:
        None

    """

    if os.path.isfile(full_path):
        logger.warning('Overwriting: {f}'
                       .format(f=full_path))
    else:
        logger.info('Writing: {f}'
                    .format(f=full_path))

    with open(full_path, 'w') as f:
        for line in contents:
            f.write('{line}\n'.format(line=line.rstrip()))


def copy_files_from_dir(src_path, dst_path):
    """Copy files from source directory to destination directory.

    Uses ``shutil.copy2`` to copy files recursively from one directory to another directory.

    Args:
        src_path (str): Full-path of the source directory.
        dst_path (str): Full-path of the destination directory.

    Returns:
        None

    """
    files = list()
    for root, subpaths, filenames in os.walk(src_path):
        for f in filenames:
            files.append(os.path.join(root, f))

    for f in files:
        logger.info('\t{f}'.format(f=f))
        shutil.copy2(f, dst_path)


def clean_path(**kwargs):
    """Cleans given path, by removing and recreating empty path.


    Keyword Args:
        **path (str): Absolute path to clean.

    Returns:
        None

    """
    path = get_kwarg('path', kwargs, False)

    if path and path != "":
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path)

