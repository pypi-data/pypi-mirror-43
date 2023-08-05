# -*- coding: utf8 -*-
"""

************************
``helpers/arguments.py``
************************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``arguments.py`` is a helpers module provided to define and configure the argument passing and parsing for the
main modules.


"""
import os
import yaml
import argparse

import customlogging as log
logger = log.config_logger(name=__name__)

import version as my_version
rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(0, 8, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class Arguments(object):
    """Creates arguments for passing files and configuration data to the script.

    A Class which configures and retrieves Arguments for use by a python script. Dictionaries
    retrieved from YAML files are added as attributes to this class with no sub-processing.
    Information including the filename of each YAML file parsed is also added as an attribute.

    See :ref:`arguments`

    Attributes:

        config (dict): the parsed dictionary of the ``config.yml`` passed using to script ``--config``
        settings (dict): the parsed dictionary of the ``settings.yml`` passed to script using ``--settings``
        checkout_enabled (bool): set ``True`` using optional ``--checkout_enabled``, otherwise ``False``
        dev_flag (bool): set ``True`` using optional ``--dev``, otherwise ``False``
        open_gui (str): Valid values: ``'fpga'``, ``'sim'``. Using optional ``--open_gui``, otherwise ``None``
        clean (list of str): Valid values: ``'all'``, ``'fpga'``, ``'ip'``, ``'precompiled_sim'``, ``'sim'``.
            Using optiona ``clean``, otherwise: ``None``

    """
    def __init__(self):
        self.logger = log.config_logger(name=__name__, class_name=self.__class__.__name__)
        _parser = self._create_parser()
        self._add_arguments(_parser)
        args = self._get_args(_parser)
        for k in vars(args):
            self.logger.info('Processed Argument: --{arg}'
                             .format(arg=k))

        log.sect_break(self.logger)
        self.logger.info('Loading Arguments from Command Line...')
        log.sect_break(self.logger)
        self._import_from_yaml(args)
        try:
            self._vunit_args(self.settings, self.settings_file)
        except AttributeError:
            self.logger.warning("Settings Missing. Using Default Options for VUnit.")

    def __repr__(self):
        return "{self.__class__.__name__}()".format(self=self)

    def __str__(self):
        return "{} is a {self.__class__.__name__} object".format(__name__, self=self)

    @staticmethod
    def _create_parser():
        """

        Creates an ``argparse`` object

        :return:
        """
        return argparse.ArgumentParser()

    @staticmethod
    def _add_arguments(parser):
        """Adds Arguments to provide to python script, using the argparse module.

        Args:
            parser (obj): ``argparse`` object

        Returns:
            None

        """
        parser.add_argument("--config",
                            dest="config",
                            type=argparse.FileType('r'),
                            default="./config.yml",
                            required=True,
                            help="YAML File Defining Project")
        parser.add_argument("--settings",
                            dest="settings",
                            type=argparse.FileType('r'),
                            required=True,
                            help="YAML File Defining Settings for Top-Level")
        parser.add_argument("--checkout_enabled",
                            dest="checkout_disabled",
                            action="store_false",
                            help="Enables Checkout When Creating RepoFlow Objects")
        parser.add_argument("--dev",
                            dest="dev_flag",
                            action="store_true",
                            help="Development Flag for Executing Script in PyCharm")
        parser.add_argument("--headless",
                            dest="headless",
                            action="store_true",
                            help="Headless Flag for Forcing GUI Based Options to False. Used to Ensure"
                                 "Continuous Integration Environments Execute Unimpeded by "
                                 "External User Input")
        parser.add_argument("--open_gui",
                            dest="open_gui",
                            choices=['fpga', 'sim'],
                            action="store",
                            default=None,
                            help="Opens Project in Specified Tool After Generating Project")
        parser.add_argument("--clean",
                            dest="clean",
                            choices=['all', 'fpga', 'ip', 'precompiled_sim', 'sim'],
                            nargs="*",
                            action="append",
                            default=None,
                            help="Cleans the Projects Specified Output Prior to Generating Project.")

    @staticmethod
    def _get_args(parser):
        """Fetches the arguments from a argparse object

        Args:
            parser (obj): argparse object

        Returns:
            None

        """
        args = parser.parse_args()
        return args

    def _import_from_yaml(self, args):
        """Imports attributes from ``yml`` file.

        Imports attributes from YAML Files defined by ``_ARG_FILELIST`` which have been passed to via
        Argument(s) attribute names match the corresponding arg name, and a reference containing the
        absolute path to the YAML file is also stored in an attribute named ``<arg>_file``

        Args:
            settings (dict):
            config (dict):

        returns:
            None

        """
        for arg in vars(args):
            attr = getattr(args, arg)
            if hasattr(attr, 'read'):
                name_attr = '{}'.format(arg)
                fname_attr = '{}_file'.format(arg)
                self.logger.info('Processing:                   --{}'
                                 .format(name_attr))
                self.logger.info('Filepath Reference Attribute: {}'
                                 .format(fname_attr))
                try:
                    abspath = os.path.abspath(attr.name)
                    contents = yaml.load(attr)
                    attr.close()
                    setattr(self, fname_attr, abspath)
                    self.logger.info('Path:                         {}'
                                     .format(abspath))
                    setattr(self, name_attr, contents)
                except AttributeError as e:
                    self.logger.error('Error Importing {} YAML File from Argument. File '
                                      '(Probably) Not a YAML File'
                                      .format(fname_attr))
                    self.logger.error('\t{}.'
                                      .format(e))
                    log.errorexit(self.logger)
            else:
                self.logger.info('Processing:                   --{}'
                                 .format(arg))
                setattr(self, arg, getattr(args, arg))

    def _vunit_args(self, settings, settings_file, vunit_args_id='vunit_args', headless=False):
        """Sets up VUnit Arguments to pass from settings.

        Replicates the passing of arguments from the command line.

        Args:
            settings (dict) Settings retrieved from YAML settings file
            settings_file (str): Absolute path of settings files used.
            vunit_args_id (str, optional): Key in settings dict representing VUnit arguments.
                Default value: ``'vunit_args'``

        Returns:
            None

        """
        supported_vunit_args = ['version', 'log_level',  'output_path', 'test_patterns',
                                'list', 'files', 'keep_compiling', 'num_threads',
                                'elaborate', 'verbose', 'xunit_xml', 'coverage',
                                'unique_sim', 'exit_0', 'no_color']

        if vunit_args_id in settings:
            self.logger.info("Appending VUnit Arguments using '{vunit_args}:' Key from Settings File: {file}"
                             .format(vunit_args=vunit_args_id,
                                     file=settings_file))
            for key, value in settings[vunit_args_id].items():
                if key in supported_vunit_args:
                    self.logger.debug("Setting VUnit Arg: {key}:{value}"
                                      .format(key=key, value=value))
                    setattr(self, key, value)
                    if key == 'version' and value:
                        self.logger.warning("Settings YAML File is Configuring VUnit to Only return Version")
                    elif key == 'list' and value:
                        self.logger.warning("Settings YAML File is Configuring VUnit to Only List Test-Cases")
                        self.logger.warning("\tOnly Test Cases Matching 'test_patterns' are Listed")
                    elif key == 'files' and value:
                        self.logger.warning("Settings YAML File is Configuring VUnit to Only List "
                                            "Compile Ordered Files")
                else:
                    if key == 'clean':
                        self.logger.critical('"vunit_args: {key}" is a Depreciated VUnit Option in Settings '
                                             'File: {settings}'
                                             .format(key=key, settings=settings_file))
                        self.logger.critical('\tInstead Use Argument: "--clean sim"')
                    elif key == 'clean_precompiled_libs':
                        self.logger.critical('"vunit_args: {key}" is a Depreciated VUnit Option in Settings '
                                             'File: {settings}'
                                             .format(key=key, settings=settings_file))
                        self.logger.critical('\tInstead Use Argument: "--clean precompiled_sim"')
                    elif key == 'gui':
                        self.logger.critical('"vunit_args: {key}" is a Depreciated VUnit Option in Settings '
                                             'File: {settings}'
                                             .format(key=key, settings=settings_file))
                        self.logger.critical('\tInstead Use Argument: "--open_gui sim"')
                    else:
                        self.logger.critical('"vunit_args: {key}: {value}" is an Unsupported VUnit Option in '
                                             'Settings File: {settings}'
                                             .format(key=key, value=value, settings=settings_file))
        else:
            self.logger.warning("VUnit Arguments '{vunit_args}' Missing from Settings. "
                                "Using Default Options"
                                .format(vunit_args=vunit_args_id))

