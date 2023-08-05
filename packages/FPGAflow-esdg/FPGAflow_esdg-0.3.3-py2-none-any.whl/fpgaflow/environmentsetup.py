# -*- coding: utf8 -*-
"""

***********************
``environmentsetup.py``
***********************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``environmentsetup.py`` is a module provided to configure the host environment for each project, setting up
environment variables which persist during the execution of the script which defined paths and license
references for each tool using the the flow. Specific values are extracted from the corresponding
``settings.yml`` YAML file and the tool installation  structure is determined from the ``config.yml`` YAML
file, each passed to the module via :mod:`arguments` (see :ref:`arguments`).

Todo:
    * Add ``breathe`` configuration to :meth:`ProjectEnvironment.configure_documentation_tool`

"""
import helpers.customlogging as log
import helpers.version as my_version
import helpers.arguments as arguments
import helpers.funcs as funcs

import fpgavendor_iface as fpgavendor_iface

import os

logger = log.config_logger(name=__name__)
LOGLEVEL = log.LogLevelsConsts

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(1, 0, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class ProjectEnvironment(object):
    """
    An object containing attributes defining the environment variables required for processing a project.

    Specific values are extracted from the corresponding ``settings.yml`` YAML file and the tool installation
    structure is determined from the ``config.yml`` YAML file, each passed to the module via
    :mod:`arguments` (see :ref:`arguments`).

    """
    def __init__(self, **kwargs):
        self.logger = log.config_logger(name=__name__, class_name=self.__class__.__name__)
        funcs.set_kwargs(self, kwargs)
        args = arguments.Arguments()
        setattr(self, 'args', args)
        for attr in vars(args):
            self.logger.debug('Promoting Attribute: {attr}: {value}'
                              .format(attr=attr, value=getattr(args, attr)))
            if attr == 'clean':
                clean = list()
                if isinstance(getattr(args, attr), list):
                    for c in getattr(args, attr):
                        if isinstance(c, list):
                            for cc in c:
                                clean.append(cc)
                        else:
                            clean.append(c)
                self.logger.error('clean: {clean}'.format(clean=clean))
                setattr(self, attr, clean)
            else:
                setattr(self, attr, getattr(args, attr))

        log.sect_break(self.logger)

        self.set_args_from_dict(key='environment',
                                subkey='required',
                                dictionary=self.config,
                                from_envvars=True)

        self.set_args_from_dict(key='environment',
                                subkey='exclude_keywords',
                                dictionary=self.config,
                                from_envvars=False)

        self.set_args_from_dict(key='repository',
                                dictionary=self.config,
                                from_envvars=False)

        self.set_args_from_dict(key='documentation',
                                dictionary=self.config,
                                from_envvars=False)

        log.sect_break(self.logger)
        self.logger.info('Processing Settings...')
        log.sect_break(self.logger)
        self.logger.debug('Processing Category from List of Valid Categories: {self.categories}'
                          .format(self=self))
        for cat in self.categories:
            if cat in list(self.settings.keys()):
                self.logger.info('Found Valid Category in Settings: {cat}'
                                 .format(cat=cat))
                setattr(self, 'category', cat)
                setattr(self, 'layout', cat + '_layout')

        self.set_args_from_dict(key=self.category,
                                dictionary=self.settings,
                                from_envvars=False)

        self.set_args_from_dict(key='documentation',
                                dictionary=self.settings,
                                from_envvars=False)

        for field in self.required:
            self.logger.debug('Processing Mandatory Field: {field}'
                              .format(field=field))
            attr = getattr(self, field, None)
            if attr:
                self.logger.debug('  {field}: {value}'
                                  .format(field=field, value=attr))
            else:
                log.mand_missing(self, field)

        if self.language in self.supported_languages:
            self.logger.info('Documentation Language: {self.language}'.format(self=self))
        else:
            self.logger.critical('Unsupported Documentation Language: {self.language}'
                                 .format(self=self))
            self.logger.critical('\tSupported Languages: {self.supported_languages}'
                                 .format(self=self))
            self.language = self.supported_languages[0]
            self.logger.critical('\tDefaulting to: {self.language}'
                                 .format(self=self))

        self.logger.info('Successfully Parsed Settings File to Complete Project Configuration')
        log.sect_break(self.logger)
        self.configure_modelsim_environment()
        self.configure_fpga_vendor_tool()
        self.configure_documentation_tool()
        log.sect_break(self.logger)

        self.logger.info('Processed Project Environment')
        log.sect_break(self.logger)

    def __repr__(self):
        return "{self.__class__.__name__}()".format(self=self)

    def __str__(self):
        return "{} is a {self.__class__.__name__} object".format(__name__, self=self)

    def check_if_supported(self, **kwargs):
        """Checks if value in ``settings.yml`` is supported in ``config.yml``

        Checks value against a list of ``supported_values`` and exits with error if not found with
        reference to the full-path of the failing ``settings.yml`` YAML used.

        Keyword Args:
            **value (str): Default value: ``None``
            **supported_values (list of str): Default value: ``list()``
            **settings_fileref (str): Full path, including filename, of settings file used.
                Default value: ``None``

        Returns:
            None

        """
        value = funcs.get_kwarg('value', kwargs, None)
        supported_values = funcs.get_kwarg('supported_values', kwargs, list())
        settings_fileref = funcs.get_kwarg('settings_fileref', kwargs, None)

        if value in supported_values:
            self.logger.debug('Using: {value}'
                              .format(value=value))
        else:
            self.logger.error('Unsupported: {value}'
                              .format(value=value))
            self.logger.error('Supported Values: {supported}'
                              .format(supported=supported_values))
            self.logger.error('Check: {settings_file}'
                              .format(settings_file=settings_fileref))
            log.errorexit(self.logger)

    def set_attr_from_path(self, **kwargs):
        """Sets an attribute: ``name`` containing a full-path, without file name.

        Keyword Args:
            **name (str): Name of the attribute to set. Default value: ``None``
            **path (str): Full path, excluding any filenames, of reference to attribute.
                Default value: ```None``
            **create_if_missing (bool, optional): If ``True`` Creates the directory structure on the
                file-system, using ``os.makedirs()``. If the directory structure does **not** exist on the
                file-system. Default value: ``False``
            **force_attr (bool, optional): If ``True`` Creates the attribute even if the directory structure
                does **not** exist on the file-system. Default value: ``False``

        Returns:
            None

        """
        name = funcs.get_kwarg('name', kwargs, None)
        path = funcs.get_kwarg('path', kwargs, None)
        create_if_missing = funcs.get_kwarg('create_if_missing', kwargs, False)
        force_attr = funcs.get_kwarg('force_attr', kwargs, False)

        if os.path.exists(path):
            self.logger.debug('Parsed:  {path}'
                              .format(path=path))
            setattr(self, name, path)
        else:
            self.logger.critical('Path Missing on File-System: {path}'
                                 .format(path=path))
            if create_if_missing:
                self.logger.warning('Creating Path on File-System: {path}'
                                    .format(path=path))
                os.makedirs(path)

            if force_attr:
                setattr(self, name, path)

    def set_args_from_dict(self, **kwargs):
        """Sets arguments from a dictionary.

        Creates attributes from a dictionary based on ``key`` or ``key[subkey]``, from
        the item or items in list found in ``dictionary[key]`` or ``dictionary[key][subkey]``.
        If using: ``from_envvars=True`` the attribute will be sourced from the system environment
        variable.

        Keyword Args:
            **key (str): Name of the dictionary key to process. Default value: ``None``
            **subkey (str, optional): Name of the dictionary sub-key to process. Default value: ``None``
            **dictionary (dict): Dictionary to extract ``[key]`` or ``[key][subkey]`` value from.
                Default value: ``dict()``
            **from_envvars (bool, optional): If ``True`` gets the value from the corresponding system
                environment variable. Default value: ``False``

        Returns:
            None

        """
        key = funcs.get_kwarg('key', kwargs, None)
        subkey = funcs.get_kwarg('subkey', kwargs, None)
        dictionary = funcs.get_kwarg('dictionary', kwargs, dict())
        from_envvars = funcs.get_kwarg('from_envvars', kwargs, False)

        if key in list(dictionary.keys()):
            self.logger.info('Setting Up {key}...'
                             .format(key=key.capitalize()))
            if from_envvars:
                if subkey:
                    self.setattr_from_envvar(envs=dictionary[key][subkey])
                else:
                    self.setattr_from_envvar(envs=dictionary[key])
            else:
                if subkey:
                    if isinstance(dictionary[key][subkey], (dict,)):
                        for k, v in dictionary[key][subkey].iteritem():
                            self.logger.debug('Adding Attribute {self.__class__.__name__}.{k} => {v}'
                                              .format(self=self, k=k, v=v))
                            setattr(self, k, v)
                    else:
                        self.logger.debug('Adding Attribute {self.__class__.__name__}.{k} => {v}'
                                          .format(self=self, k=subkey, v=dictionary[key][subkey]))
                        setattr(self, subkey, dictionary[key][subkey])
                else:
                    if isinstance(dictionary[key], (dict,)):
                        for k, v in dictionary[key].iteritems():
                            self.logger.debug('Adding Attribute {self.__class__.__name__}.{k} => {v}'
                                              .format(self=self, k=k, v=v))
                            setattr(self, k, v)
                    else:
                        self.logger.debug('Adding Attribute {self.__class__.__name__}.{k} => {v}'
                                          .format(self=self, k=key, v=dictionary[key]))
                        setattr(self, key, dictionary[key])

    def setattr_from_envvar(self, **kwargs):
        """Sets attribute from system environment variable.

        Gets the value from corresponding `$envs`` and sets attribute matching the system environment variable
        name with the value retrieved.

        Keyword Args:
            **envs (str): Name of the system environment variable to process. Default value: ``None``

        Returns:
            None

        """
        envs = funcs.get_kwarg('envs', kwargs, None)

        if isinstance(envs, (list, tuple, set, frozenset)):
            for env in envs:
                self.set_envattr(env=env)
        else:
            self.set_envattr(env=envs)

    def set_path_environ(self, **kwargs):
        """Sets system environment ``$path`` variable.

        This performs the equivalent of running:

        .. code-block:: bash

           setenv env path

        If ``$env`` already exists it will append to the existing value:

        .. code-block:: bash

           setenv env path:${env}

        Keyword Args:
            **env (str): Name of the system environment variable name. Default value: ``None``
            **path (str): System environment variable value. Default value: ``None``
            **delimiter (str, optional): Delimiter to use between multiple environment variable values
                Default value: ``':'``
            **overwrite (bool, optional): If ``True`` overwrite existing value instead of appending.
                Default value: ``False``

        Returns:
            None

        """
        env = funcs.get_kwarg('env', kwargs, None)
        path = funcs.get_kwarg('path', kwargs, None)
        delimiter = funcs.get_kwarg('delimiter', kwargs, ':')
        overwrite = funcs.get_kwarg('overwrite', kwargs, None)

        try:
            temp_env = os.environ[env.upper()]
            self.logger.debug('Adding:  {env} {value}'
                              .format(env=env.upper(), value=path))
            if overwrite:
                temp_env = None
        except KeyError:
            temp_env = None
            self.logger.debug('Setting: {env} {value}'
                              .format(env=env.upper(), value=path))

        self.logger.debug('Old Env: {env}'
                          .format(env=temp_env))

        if temp_env:
            temp_list = temp_env.split(delimiter)
            self.logger.debug('Processing Existing Environment Variable Value:')
            for i in temp_list:
                self.logger.debug('\t{i}'
                                  .format(i=i))
            if path in temp_list:
                self.logger.warning('{path} Already Set in: ${env}'
                                    .format(path=path, env=env.upper()))
                self.logger.warning('\tMoving to First Reference')
                temp_list.remove(path)
                temp_env = '{delimiter}'.format(delimiter=delimiter).join(temp_list)
                self.logger.debug('Re-ordered: {env}'
                                  .format(env=temp_env))
            temp_env = '{path}{delimiter}{env}'.format(path=path, delimiter=delimiter, env=temp_env)
        else:
            temp_env = '{path}'.format(path=path)

        self.logger.debug('Updated: {value}'
                          .format(value=temp_env))

        os.environ[env.upper()] = temp_env
        temp_env = os.environ[env.upper()]
        self.logger.info('Updated: ${env} {value}'.format(env=env.upper(), value=temp_env))

    def set_envattr(self, **kwargs):
        """Checks to see if the attribute already exists before setting.

        Keyword Args:
            **env (str): Name of the system environment variable to check. Default value: ``None``

        Returns:
            None
        """
        env = funcs.get_kwarg('env', kwargs, None)

        if hasattr(self, env.lower()):
            self.logger.crtical('Attribute Already Set: {}'
                                .format(env.lower()))
        else:
            setattr(self, env.lower(), self.get_envvar(variable_name=env))

    def get_envvar(self, **kwargs):
        """Method to get system environment variable using ``os.environ``

        If the system environment variable does **not** exist :meth:`customlogging.errorexit` is called.

        Keyword Args:
            **variable_name (str): Name of the system environment variable to get from system.
                Default value: ``None``

        Returns:
            (str): The retrieved system environment variable.

        """
        variable_name = funcs.get_kwarg('variable_name', kwargs, None)

        try:
            resolved_name = os.environ[variable_name]
            self.logger.info('\t${:<24}{}'
                             .format(variable_name, resolved_name))
            return resolved_name
        except KeyError:
            self.logger.error('Environment Variable Not Set: {name}'
                              .format(name=variable_name.upper()))
            self.logger.error('\tFor Linux Add Environment Variable Using:')
            self.logger.error('\t\tsetenv {name} <VALUE>'
                              .format(name=variable_name.upper()))
            self.logger.error('\tWhere <VALUE> is the Variable Value')
            log.errorexit(self.logger)

    def add_environment_variable(self, **kwargs):
        """Adds a system environment variable for the running script.

        If the system environment variable already exists this will add the new value as the first value
        and append the old value using ``':'`` as a delimiter.

        Keyword Args:
            **name (str): Name of the system environment variable to create/append. Default value: ``None``
            **value (str): Value to assign to the system environment variable. Default value: ``None``
            **overwrite (bool, optional): Default value: ``False``

        Returns:
            None

        """
        name = funcs.get_kwarg('name', kwargs, None)
        value = funcs.get_kwarg('value', kwargs, None)
        overwrite = funcs.get_kwarg('overwrite', kwargs, False)

        self.logger.debug('Setting: {name} -> {value}'
                          .format(name=name.upper(), value=value))
        self.set_path_environ(env=name.upper(), path=value, overwrite=overwrite)

    def configure_modelsim_environment(self):
        """Configures and validates the system environment variables for running ``modelsim``

        Returns:
            None

        """
        self.logger.info('Setting Up Simulation Environment...')
        self.check_if_supported(value=self.sim_vendor,
                                supported_values=self.config['simulation']['supported_vendors'],
                                settings_fileref=self.settings_file)
        self.logger.info('Simulator: {vendor}'
                         .format(vendor=self.sim_vendor.capitalize()))

        self.check_if_supported(value=self.sim_version,
                                supported_values=self.config['simulation'][self.sim_vendor]['supported_tools'],
                                settings_fileref=self.settings_file)
        self.logger.info('Using Version: {version}'
                         .format(version=self.sim_version))

        self.configure_license(config_dict=self.config['simulation'][self.sim_vendor]['license'])

        try:
            self.configure_mode(mode=self.sim_mode,
                                config_dict=self.config['simulation'][self.sim_vendor]['mode'],
                                mode_type='sim')
        except AttributeError:
            setattr(self, 'sim_mode', 32)
            self.logger.info('Sim Mode Defaulting to: {mode}'
                             .format(mode=self.sim_mode))
            self.configure_mode(mode=self.sim_mode,
                                config_dict=self.config['simulation'][self.sim_vendor]['mode'],
                                mode_type='sim')

        self.configure_paths(config_dict=self.config['simulation'][self.sim_vendor]['paths'])

        setattr(self, 'sim_version', self.sim_vendor + '_' + self.sim_version.replace('/', '_'))
        self.logger.info('Renamed Simulation Version for Build Referencing: {self.sim_version}'
                         .format(self=self))

        self.logger.info('Successfully Configured Simulation Environment')
        log.sect_break(self.logger)

    def configure_fpga_vendor_tool(self):
        """Configures and validates the system environment variables for running the `FPGA` vendor tool.

        Returns:
            None

        """
        self.logger.info('Setting Up FPGA Vendor Environment...')
        self.check_if_supported(value=self.vendor,
                                supported_values=self.config['fpga']['supported_vendors'],
                                settings_fileref=self.settings_file)
        self.logger.info('FPGA Vendor: {vendor}'
                         .format(vendor=self.vendor.capitalize()))

        self.check_if_supported(value=self.tool_version,
                                supported_values=self.config['fpga'][self.vendor]['tools'],
                                settings_fileref=self.settings_file)
        self.logger.info('Using Version: {version}'
                         .format(version=self.tool_version))

        self.configure_license(config_dict=self.config['fpga'][self.vendor]['license'])

        try:
            self.configure_mode(mode=self.tool_mode,
                                config_dict=self.config['fpga'][self.vendor]['mode'],
                                mode_type='tool')
        except AttributeError:
            tool_mode = self.config['fpga'][self.vendor]['mode']['supported_modes'][0]
            self.logger.debug('Setting Tool Mode: {mode}'
                              .format(mode=tool_mode))
            setattr(self, 'tool_mode', tool_mode)
            self.logger.info('Tool Mode Defaulting to: {mode}'
                             .format(mode=self.tool_mode))
            self.configure_mode(mode=self.tool_mode,
                                config_dict=self.config['fpga'][self.vendor]['mode'],
                                mode_type='tool')

        self.configure_paths(config_dict=self.config['fpga'][self.vendor]['paths'])

        setattr(self, 'tool_version', fpgavendor_iface.resolve_tool_version(tool_version=self.tool_version,
                                                                            vendor=self.vendor))

        self.logger.info('Renamed Tool Version for Build Referencing: {self.tool_version}'
                         .format(self=self))

        self.logger.info('Successfully Configured FPGA Vendor Tool Environment')
        log.sect_break(self.logger)

    def configure_documentation_tool(self):
        """Configures and validates the system environment variables for running documentation tools.

        Supports the following automatic documentation generation tools:

        * ``doxygen``
        * ``breathe``
        * ``sphinx``

        Returns:
            None

        """
        self.logger.info('Setting Up Documentation Environment...')
        self.logger.info('Configuring Doxygen...')
        self.check_if_supported(value=self.doxy_version,
                                supported_values=self.config['documentation']['doxygen']['supported_tools'],
                                settings_fileref=self.settings_file)
        self.logger.info('\tUsing Version: {version}'
                         .format(version=self.doxy_version))
        self.configure_paths(config_dict=self.config['documentation']['doxygen']['paths'])

        self.logger.info('Configuring Dot...')
        self.check_if_supported(value=self.dot_version,
                                supported_values=self.config['documentation']['dot']['supported_tools'],
                                settings_fileref=self.settings_file)
        self.logger.info('\tUsing Version: {version}'
                         .format(version=self.dot_version))
        self.configure_paths(config_dict=self.config['documentation']['dot']['paths'])

        self.logger.info('Configuring Breathe...')
        # \TODO Configure Breathe Here...

        self.logger.info('Configuring Sphinx...')
        self.check_if_supported(value=self.sphinx_version,
                                supported_values=self.config['documentation']['sphinx']['supported_tools'],
                                settings_fileref=self.settings_file)
        self.logger.info('\tUsing Version: {version}'
                         .format(version=self.sphinx_version))
        self.configure_paths(config_dict=self.config['documentation']['sphinx']['paths'])

    def configure_license(self, **kwargs):
        """Configures license environment variables.

        Gets configuration from ``config.yml`` YAML file (see :ref:`configuration`).

        Keyword Args:
            **license_settings (dict): The license settings from configuration dictionary.
                Default value: ``None``

        Returns:
            None

        """
        license_settings = funcs.get_kwarg('config_dict', kwargs, None)

        if isinstance(license_settings, (dict,)):
            for k, v in license_settings.iteritems():
                self.logger.info('Setting License: {k}: {v}'
                                 .format(k=k, v=v))
                setattr(self, k, v)
                if isinstance(v, (list,)):
                    for i in v:
                        self.add_environment_variable(name=k, value=i)
                else:
                    self.add_environment_variable(name=k, value=v)

    def configure_mode(self, **kwargs):
        """Configure tool execution mode.

        Provides support for running the tools in 32 or 64 bit modes as well as referencing libraries not
        supported by the host operating system distribution.

        Keyword Args:
            **mode (str): Default value: ``None``
            **mode_config (dict): Dictionary defining the mode of running the tool being configured.
                Default value: ``None``
            **mode_type (str): Default value: ``sim``
        Returns:
            None

        """
        mode = funcs.get_kwarg('mode', kwargs, None)
        mode_config = funcs.get_kwarg('config_dict', kwargs, None)
        mode_type = funcs.get_kwarg('mode_type', kwargs, 'sim')

        try:
            if mode in mode_config['supported_modes']:
                self.logger.info('{mode_type} Mode: {mode}'
                                 .format(mode_type=mode_type.capitalize(),
                                         mode=mode))
            else:
                mode = mode_config['supported_modes'][0]
                self.logger.debug('Setting Mode to: {mode}'
                                  .format(mode=mode))
                setattr(self, mode_type.lower() + '_mode', mode)
                self.logger.warning('Unsupported {mode_type} Defaulting to: {mode}'
                                    .format(mode_type=mode_type.capitalize(),
                                            mode=mode))
                self.logger.warning('\tSupported {mode_type} Modes: {modes}'
                                    .format(mode_type=mode_type.capitalize(),
                                            modes=mode_config['supported_modes']))

            self.add_environment_variable(name=mode_config['env_name'], value=mode, overwrite=True)
            ld_library_path = mode_config['ld_library_path_' + str(mode)]
        except TypeError:
            ld_library_path = mode_config['ld_library_path']

        try:
            if isinstance(ld_library_path, (list,)):
                for p in ld_library_path:
                    self.add_environment_variable(name='ld_library_path', value=p, overwrite=False)
        except KeyError:
            self.logger.info('No Additional LD_LIBRARY_PATH References to Add. Skipping')

    def configure_paths(self, **kwargs):
        """Configures system environment paths required for tool execution.

        Keyword Args:
            **paths_config (dict): Dictionary defining the paths and values for the tool being configured.
                Default value: ``None``

        Returns:
            None

        """
        paths_config = funcs.get_kwarg('config_dict', kwargs, None)

        try:
            root_path = funcs.replace_tag_with_attr_value(self, paths_config['root_path'])
            root_name = paths_config['root_name']
            self.logger.debug('Root Path: {path}'
                              .format(path=root_path))
            self.logger.debug('Root Name: {name}'
                              .format(name=root_name))

            self.set_attr_from_path(name=root_name,
                                    path=root_path,
                                    create_if_missing=False)
            self.add_environment_variable(name=root_name, value=root_path, overwrite=True)

            additional_paths = paths_config.get('additional_paths', None)
            if isinstance(additional_paths, (dict,)):
                for k, v in additional_paths.iteritems():
                    self.logger.info('Setting Additional Path Environment Variables: ${k}'
                                     .format(k=k.upper()))
                    if isinstance(v, (list,)):
                        attr_value = list()
                        for i in v:
                            resolved_path = funcs.replace_tag_with_attr_value(self, i)
                            resolved_path = os.path.join(root_path, resolved_path)
                            attr_value.append(resolved_path)
                        self.set_attr_from_path(name=k,
                                                path=resolved_path,
                                                create_if_missing=False)
                        self.add_environment_variable(name=k, value=resolved_path, overwrite=False)
                        self.logger.debug('Set Attribute: {attr}: {value}'
                                          .format(attr=k, value=attr_value))
                    else:
                        resolved_path = funcs.replace_tag_with_attr_value(self, v)
                        resolved_path = os.path.join(root_path, resolved_path)
                        self.set_attr_from_path(name=k,
                                                path=resolved_path,
                                                create_if_missing=False)
                        self.add_environment_variable(name=k, value=resolved_path, overwrite=True)
                        self.logger.debug('Set Attribute: {attr}: {value}'
                                          .format(attr=k, value=resolved_path))

            add_to_path = paths_config.get('add_to_path', list())
            if isinstance(add_to_path, (list,)):
                for i in add_to_path:
                    resolved_path = funcs.replace_tag_with_attr_value(self, i)
                    resolved_path = os.path.join(root_path, resolved_path)
                    self.set_attr_from_path(name='path',
                                            path=resolved_path,
                                            create_if_missing=False)
                    self.add_environment_variable(name='path', value=resolved_path, overwrite=False)
            else:
                resolved_path = funcs.replace_tag_with_attr_value(self, add_to_path)
                resolved_path = os.path.join(root_path, resolved_path)
                self.set_attr_from_path(name='path',
                                        path=resolved_path,
                                        create_if_missing=False)
                self.add_environment_variable(name='path', value=resolved_path, overwrite=True)

            external_references = paths_config.get('external_references', None)
            if isinstance(external_references, (dict,)):
                for k, v in external_references.iteritems():
                    self.logger.info('Setting External Reference Attributes: {k}'
                                     .format(k=k.lower()))
                    if isinstance(v, (list,)):
                        attr_value = list()
                        for i in v:
                            resolved_path = funcs.replace_tag_with_attr_value(self, i)
                            resolved_path = os.path.join(root_path, resolved_path)
                            attr_value.append(resolved_path)
                        self.set_attr_from_path(name=k,
                                                path=resolved_path,
                                                create_if_missing=False,
                                                force_attr=True)
                        setattr(self, k, attr_value)
                        self.logger.debug('Set Attribute: {attr}: {value}'
                                          .format(attr=k, value=attr_value))
                    else:
                        resolved_path = funcs.replace_tag_with_attr_value(self, v)
                        resolved_path = os.path.join(root_path, resolved_path)
                        self.set_attr_from_path(name=k,
                                                path=resolved_path,
                                                create_if_missing=False,
                                                force_attr=True)
                        self.logger.debug('Set Attribute: {attr}: {value}'
                                          .format(attr=k, value=resolved_path))
        except KeyError:
            pass

        try:
            internal_references = paths_config['internal_references']
            root_path = os.path.abspath('./')
            self.logger.debug('Internal Path: {path}'
                              .format(path=root_path))
            if isinstance(internal_references, (dict,)):
                for k, v in internal_references.iteritems():
                    self.logger.info('Setting Internal Reference Attributes: {k}'
                                     .format(k=k.lower()))
                    if isinstance(v, (list,)):
                        attr_value = list()
                        for i in v:
                            resolved_path = funcs.replace_tag_with_attr_value(self, i)
                            resolved_path = os.path.join(root_path, resolved_path)
                            attr_value.append(resolved_path)
                        self.set_attr_from_path(name=k,
                                                path=resolved_path,
                                                create_if_missing=False,
                                                force_attr=True)
                        setattr(self, k, attr_value)
                        self.logger.debug('Set Attribute: {attr}: {value}'
                                          .format(attr=k, value=attr_value))
                    else:
                        resolved_path = funcs.replace_tag_with_attr_value(self, v)
                        resolved_path = os.path.abspath(os.path.join(root_path, resolved_path))

                        self.set_attr_from_path(name=k,
                                                path=resolved_path,
                                                create_if_missing=False,
                                                force_attr=True)
                        self.logger.debug('Set Attribute: {attr}: {value}'
                                          .format(attr=k, value=resolved_path))
        except KeyError:
            pass


if __name__ == '__main__':
    logger.info("environmentsetup {} {}"
                .format(__version__, version.revision))
    log.sect_break(logger)

    project = ProjectEnvironment()

else:
    logger.info(__str__)
