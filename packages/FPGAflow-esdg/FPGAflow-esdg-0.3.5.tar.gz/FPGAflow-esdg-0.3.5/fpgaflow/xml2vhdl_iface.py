# -*- coding: utf8 -*-
"""

*********************
``xml2vhdl_iface.py``
*********************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``xml2vhdl_iface.py`` is a module to handle interfacing and executing of external ``xml2vhdl`` generation
script.

The ``git`` repository for ``xml2vhdl`` can be found at:
`Bitbucket.org <https://bitbucket.org/ricch/xml2vhdl.git>`_.
See `XML2VHDL Read the Docs <https://xml2vhdl.readthedocs.io>`_ for documentation.

"""
import helpers.customlogging as log
import helpers.version as my_version
import helpers.funcs as funcs

import os

logger = log.config_logger(name=__name__)
LOGLEVEL = log.LogLevelsConsts

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(0, 1, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class Xml2Vhdl(object):
    """Xml2Vhdl object used to configure the required arguments for generating VHDL from XML.

    The Xml2VhdlGenerate class is defined external to this project and is used only if ``xml2vhdl_support`` is
    enabled. this requires :ref:`settings_git` or :ref:`settings_subversion` has a reference to ``xml2vhdl``.

    The ``git`` repository for ``xml2vhdl`` can be found at:
    `Bitbucket.org <https://bitbucket.org/ricch/xml2vhdl.git>`_.
    See `XML2VHDL Read the Docs <https://xml2vhdl.readthedocs.io>`_ for documentation.

    Keyword Args:
        **log (bool, optional): Default value: ``False``
        **input_folder (str, or list of str): Default value: ``list()``
        **path (str, or list of str): Default value: ``list()``
        **bus_library (str): Default value: ``'axi4_lib'``
        **slave_library (str): Default value: ``'work'``
        **bus_definition_number (int): Default value: ``0``
        **relative_output_path (str): Default value: ``'../vhdl/generated'``
        **vhdl_output (str): Default value: ``False``
        **xml_output (str): Default value: ``False``
        **attributes (bool): Links to the ``xml_help`` attribute. Default value: ``False``
        **relocate_path (str): Default value: ``''``
        **constant (str, or list of str): Default value: ``list()``
        **tb (bool): Default value: ``False``
        **top (str): Links to the ``vhdl_top`` attribute. Default value: ``''``
        **vhdl_record_name (str): Default value: ``'t_axi4lite_mmap_slaves'``
        **zip (bool): Default value: ``False``

    Attributes:
        log bool: Prints version and history log to pass to ``Xml2VhdlGenerate`` using the ``-l`` argument.
        input_folder list(): List of input folders to pass to ``Xml2VhdlGenerate`` using the ``-d`` argument.
        path list(): List of paths to linked XML file to pass to ``Xml2VhdlGenerate`` using
            the ``-p`` argument.
        bus_library (str): Bus library to pass to ``Xml2VhdlGenerate`` using the ``-b`` argument.
        slave_library (str): Slave library to pass to ``Xml2VhdlGenerate`` using the ``-s`` argument.
        bus_definition_number (int): Bus definition number to pass to ``Xml2VhdlGenerate`` using the
            ``-n`` argument.
        relative_output_path (str): Relative output path to pass to ``Xml2VhdlGenerate`` using the
            ``--relative_output_path`` argument.
        vhdl_output (str): VHDL output path to pass to ``Xml2VhdlGenerate`` using the
            ``-v`` argument.
        xml_output (str): XML output path to pass to ``Xml2VhdlGenerate`` using the
            ``-x`` argument.
        xml_help bool: Prints supported XML attributes to pass to ``Xml2VhdlGenerate``
            using the ``-a`` argument.
        relocate_path (str): Relocate path to pass to ``Xml2VhdlGenerate`` using the
            ``--relocate_path`` argument.
        constant list(): List of constant(s) to substitute the specified constant value in the XML file,
            passed to ``Xml2VhdlGenerate`` using the ``-c`` argument.
        tb bool: Option to generate simple test-bench, passed to ``Xml2VhdlGenerate``
            using the ``--tb`` argument.
        vhdl_top: Top-level IC name for VHDL generation. Passed to ``Xml2VhdlGenerate`` using the
            ``-t`` argument.
        vhdl_record_name str: VHDL record name containing slaves memory-map. Passed to `Xml2VhdlGenerate``
            using the ``-r`` argument.
        zip bool: Option to generate ``BRAM`` hex init file, passed to ``Xml2VhdlGenerate``
            using the ``--zip`` argument.

    todo:
        * Consider moving :mod:`projectflow.Xml2Vhdl` to ``xml2vhdl``.

    """
    def __init__(self, **kwargs):
        global xml2vhdl
        import xml2vhdl as xml2vhdl
        self.logger = log.config_logger(name=__name__, class_name=self.__class__.__name__)
        self.set_bool(attr='log', value=funcs.get_kwarg('log', kwargs, False))
        self.add_to_path(attr='input_file', add_paths=funcs.get_kwarg('input_file', kwargs, list()))
        self.add_to_path(attr='input_folder', add_paths=funcs.get_kwarg('input_folder', kwargs, list()))
        self.add_to_path(attr='path', add_paths=funcs.get_kwarg('path', kwargs, list()))
        self.set_library(lib=funcs.get_kwarg('bus_library', kwargs, 'axi4_lib'), lib_type='bus')
        self.set_library(lib=funcs.get_kwarg('slave_library', kwargs, 'work'), lib_type='slave')
        self.set_bus_definition_number(number=funcs.get_kwarg('bus_definition_number', kwargs, 0))
        self.set_relative_output_path(path=funcs.get_kwarg('relative_output_path', kwargs, '../vhdl/generated'))
        self.set_vhdl_output(path=funcs.get_kwarg('vhdl_output', kwargs, False))
        self.set_xml_output(path=funcs.get_kwarg('xml_output', kwargs, False))
        self.set_bool(attr='xml_help', value=funcs.get_kwarg('attributes', kwargs, False))
        self.set_relocate_path(path=funcs.get_kwarg('relocate_path', kwargs, ''))
        self.add_to_path(attr='constant', add_paths=funcs.get_kwarg('constant', kwargs, list()))
        self.set_bool(attr='tb', value=funcs.get_kwarg('tb', kwargs, False))
        self.set_vhdl_top(top=funcs.get_kwarg('top', kwargs, ''))
        self.set_vhdl_record_name(name=funcs.get_kwarg('vhdl_record_name', kwargs, 't_axi4lite_mmap_slaves'))
        self.set_bool(attr='zip', value=funcs.get_kwarg('zip', kwargs, False))

    def add_to_path(self, **kwargs):
        """Adds to existing path list to corresponding attribute.

        Keyword Args:
            **attr (str): attribute to add path(s) to.
            **add_paths (str or list of str): path(s) where to find source files for generation.
                Default value: ``list()``

        Returns:
            bool: ``True`` when successful, ``False`` when unsuccessful.

        """
        attr = funcs.get_kwarg('attr', kwargs, None)
        add_paths = funcs.get_kwarg('add_paths', kwargs, list())

        if not attr:
            self.logger.critical('Attribute No Provided.')
            return False

        if hasattr(self, attr):
            self.logger.debug('Adding to: {attr}'.format(attr=attr))
            temp_input_path = getattr(self, attr)
        else:
            self.logger.debug('Creating: {attr}'.format(attr=attr))
            temp_input_path = list()

        if isinstance(add_paths, (list, )):
            temp_input_path.extend(add_paths)
        elif isinstance(add_paths, (str, )):
            temp_input_path.append(add_paths)
        else:
            self.logger.critical('Unsupported type when adding to "{attr}": {path} is: {type}'
                                 .format(attr=attr, path=add_paths, type=type(add_paths)))
            return False

        setattr(self, attr, temp_input_path)
        return True

    def set_bool(self, **kwargs):
        """sets boolean value to corresponding attribute

        Keyword Args:
            **attr (str):  attribute to assign boolean value.
            **value (bool, optional): Default value: ``False``

        Returns:
            bool: ``True`` when successful, ``False`` when unsuccessful.

        """
        attr = funcs.get_kwarg('attr', kwargs, None)
        value = funcs.get_kwarg('value', kwargs, False)

        if not attr:
            self.logger.critical('Attribute No Provided.')
            return False

        if isinstance(value, (bool, )):
            setattr(self, attr, value)
            return True
        else:
            self.logger.critical('Unsupported type when adding to "{attr}": {value} is: {type}'
                                 .format(attr=attr, path=value, type=type(value)))
            return False

    def set_library(self, lib, lib_type='bus'):
        """Sets the bus library

        Args:
            lib (str): VHDL library used to define and handle XML generated bus connections.
            lib_type (str, optional): Library to set. Valid values are: ``'bus'`` and ``'slave'``.
                Default value: ``'bus'``

        Returns:
            None

        """
        if lib_type == 'bus':
            setattr(self, 'bus_library', lib)
        elif lib_type == 'slave':
            setattr(self, 'slave_library', lib)
        else:
            logger.critical('Unsupported Library Type: {lib_type}. Defaulting to "bus"'
                            .format(lib_type=lib_type))
            setattr(self, 'bus_library', lib)

    def set_bus_definition_number(self, number=0, **kwargs):
        """Sets the bus definition number

        Args:
            number (int): Bus definition number. Valid values are: ``0``, ``1``, ``2``.
                where:

                * ``0``: ``axi4lite``

                * ``1``: ``wishbone (16 bit)``

                * ``2``: ``wishbone (32 bit)``

                Default value: ``0``

        Keyword Args:

        Returns:
            None

        """
        if isinstance(number, (int, )):
            if number > 2:
                self.logger.critical('Unsupported {attr}: {number}. Defaulting to: 0'
                                     .format(attr='bus_definition_number', number=number))
                setattr(self, 'bus_definition_number', 0)
            else:
                setattr(self, 'bus_definition_number', number)
        else:
            self.logger.critical('Unsupported type when adding to "{attr}": {number} is: {type}'
                                 .format(attr='bus_definition_number', number=number, type=type(number)))
            self.logger.critical('\tDefaulting "{attr}": {number}'
                                 .format(attr='bus_definition_number', number=0))
            setattr(self, 'bus_definition_number', 0)

    def set_relative_output_path(self, path, **kwargs):
        """Sets the relative output path

        Args:
            path (str): relative path where to store generated files.

        Keyword Args:

        Returns:
            None

        """
        setattr(self, 'relative_output_path', path)

    def set_vhdl_output(self, path, **kwargs):
        """Sets the VHDL output path

        Args:
            path (str): path where to store generated VHDL files.

        Keyword Args:

        Returns:
            None

        """
        setattr(self, 'vhdl_output', path)

    def set_xml_output(self, path, **kwargs):
        """Sets the XML output path

        Args:
            path (str): path where to store generated XML files.

        Keyword Args:

        Returns:
            None

        """
        setattr(self, 'xml_output', path)

    def set_relocate_path(self, path, **kwargs):
        """Sets the XML output path

        Args:
            path (str): path where to store generated XML files.

        Keyword Args:

        Returns:
            None

        """
        setattr(self, 'relocate_path', path)

    def set_vhdl_top(self, top, **kwargs):
        """Sets the VHDL Top-level name

        Args:
            top (str): Name of top-level to assign to generated IC top-level.

        Keyword Args:

        Returns:
            None

        """
        setattr(self, 'vhdl_top', top)

    def set_vhdl_record_name(self, name, **kwargs):
        """Sets the VHDL record name

        Args:
            name (str): Name of VHDL record containing slaves memory-map.

        Keyword Args:

        Returns:
            None

        """
        setattr(self, 'vhdl_record_name', name)

    def get_log(self):
        """Gets the log

        Returns:
             bool: log attribute value if successful, otherwise ``False``

        """
        return getattr(self, 'log', False)

    def get_input_file(self):
        """Gets the input files(s)

        Returns:
             list of str: input files(s) if successful, otherwise ``False``

        """
        return getattr(self, 'input_file', False)

    def get_input_folder(self):
        """Gets the input folder(s)

        Returns:
             list of str: input folders(s) if successful, otherwise ``False``

        """
        return getattr(self, 'input_folder', False)

    def get_path(self):
        """Gets the path(s)

        Returns:
             list of str: path(s) if successful, otherwise ``False``

        """
        return getattr(self, 'path', False)

    def get_bus_library(self):
        """Gets the bus library

        Returns:
             str: bus library if successful, otherwise ``False``

        """
        return getattr(self, 'bus_library', False)

    def get_slave_library(self):
        """Gets the slave library

        Returns:
             str: slave library if successful, otherwise ``False``

        """
        return getattr(self, 'slave_library', False)

    def get_bus_definition_number(self):
        """Gets the bus definition number

        Returns:
             int: bus definition number if successful, otherwise ``False``

        """
        return getattr(self, 'bus_definition_number', False)

    def get_relative_output_path(self):
        """Gets the relative output path

        Returns:
             str: relative output path if successful, otherwise ``False``

        """
        return getattr(self, 'relative_output_path', False)

    def get_vhdl_output_path(self):
        """Gets the VHDL output path

        Returns:
             str: VHDL output path if successful, otherwise ``False``

        """
        return getattr(self, 'vhdl_output_path', False)

    def get_xml_output_path(self):
        """Gets the XML output path

        Returns:
             str: XML output path if successful, otherwise ``False``

        """
        return getattr(self, 'xml_output_path', False)

    def get_xml_help(self):
        """Gets the xml_help

        Returns:
             bool: xml_help attribute value if successful, otherwise ``False``

        """
        return getattr(self, 'xml_help', False)

    def get_relocate_path(self):
        """Gets the relocate_path

        Returns:
             bool: relocate_path attribute value if successful, otherwise ``False``

        """
        return getattr(self, 'relocate_path', False)

    def get_constant(self):
        """Gets the constant(s)

        Returns:
             list of str: constant(s) if successful, otherwise ``False``

        """
        return getattr(self, 'constant', False)

    def get_tb(self):
        """Gets the tb

        Returns:
             bool: tb attribute value if successful, otherwise ``False``

        """
        return getattr(self, 'tb', False)

    def get_vhdl_top(self):
        """Gets the VHDL top-level name

        Returns:
             str: VHDL top-level name if successful, otherwise ``False``

        """
        return getattr(self, 'vhdl_top', False)

    def get_vhdl_record_name(self):
        """Gets the VHDL record name

        Returns:
             str: VHDL record name if successful, otherwise ``False``

        """
        return getattr(self, 'vhdl_record_name', False)

    def get_zip(self):
        """Gets the zip

        Returns:
             bool: zip attribute value if successful, otherwise ``False``

        """
        return getattr(self, 'zip', False)

    def report_info(self):
        """Reports relevant object attributes

        Returns:
             None

        """
        self.logger.info('-' * 80)

        if self.get_log():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='log', value=True))

        if self.get_input_file():
            for path in self.get_input_file():
                self.logger.info('\t--{attr} {value} \\'
                                 .format(attr='input_file', value=path))

        if self.get_input_folder():
            for path in self.get_input_folder():
                self.logger.info('\t--{attr} {value} \\'
                                 .format(attr='input_folder', value=path))
        if self.get_path():
            for path in self.get_path():
                self.logger.info('\t--{attr} {value} \\'
                                 .format(attr='path', value=path))

        if self.get_bus_library():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='bus_library', value=self.get_bus_library()))

        if self.get_slave_library():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='slave_library', value=self.get_slave_library()))

        if self.get_bus_definition_number():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='bus_definition_number', value=self.get_bus_definition_number()))

        if self.get_xml_help():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='xml_help', value=True))

        if self.get_relocate_path():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='relocate_path', value=self.get_relocate_path()))

        if self.get_constant():
            for path in self.get_constant():
                self.logger.info('\t--{attr} {value} \\'
                                 .format(attr='constant', value=path))

        if self.get_tb():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='tb', value=True))

        if self.get_vhdl_top():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='top', value=self.get_vhdl_top()))

        if self.get_vhdl_record_name():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='vhdl_record_name', value=self.get_vhdl_record_name()))

        if self.get_zip():
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='zip', value=True))

        if self.get_relative_output_path():
            self.logger.info('\t--{attr} {value}'
                             .format(attr='relative_output_path', value=self.get_relative_output_path()))
        else:
            self.logger.info('\t--{attr} {value} \\'
                             .format(attr='vhdl_output_path', value=self.get_vhdl_output_path()))
            self.logger.info('\t--{attr} {value}'
                             .format(attr='xml_output_path', value=self.get_xml_output_path()))

    def generate_vhdl(self, working_dir):
        """Generates VHDL from XML

        Args:
            working_dir (str): Path to XML2VHDL Working Directory.

        Returns:
             None

        """
        self.logger.info('Running XML2VHDL Using:')
        self.report_info()
        cwd = os.getcwd()
        os.chdir(working_dir)
        xml2vhdl.Xml2VhdlGenerate(self)
        os.chdir(cwd)
        self.logger.info('Completed XML2VHDL Generation')


if __name__ == '__main__':
    pass
else:
    logger.info(__str__)

