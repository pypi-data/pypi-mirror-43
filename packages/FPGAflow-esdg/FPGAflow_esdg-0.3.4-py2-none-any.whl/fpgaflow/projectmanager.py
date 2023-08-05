# -*- coding: utf8 -*-
"""

*********************
``projectmanager.py``
*********************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``projectmanager.py`` is a module provided to setup, validate and execute source-code retrieval from
externally hosted repositories. Project specific values are extracted from the corresponding ``settings.yml``
YAML file and the projects structure is determined from the ``config.yml`` YAML file, each passed to the
module via :mod:`arguments` (see :ref:`arguments`).

Todo:
    * Add ``git`` support for cloning projects.
    * ``echo $PASSWORD | git svn clone $REMOTE_URL --stdlayout
      --preserve-empty-dirs --username=$REPO_USERNAME $LOCAL_PATH``
      where ``$REMOTE_URL`` doesn't include ``$sub_path`` value as this is determined using ``--stdlayout``
    * Allow projects to be hosted by a mixture of ``git`` and ``SVN``
    * Check if :meth:`ProjectDependency._layout_tag_attr_replace` can be safely replaced by
      :meth:`funcs.replace_tag_with_attr_value`

"""
import helpers.customlogging as log
import helpers.version as my_version
import environmentsetup as projectenvironment
import fpgavendor_iface as fpgavendor_iface
import helpers.funcs as funcs

import importlib
import sys
import os
import re
import posixpath
import urlparse
import getpass
import yaml

logger = log.config_logger(name=__name__)
LOGLEVEL = log.LogLevelsConsts

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(1, 2, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class RepoFlow(projectenvironment.ProjectEnvironment):
    """
    Parses the project settings file for repository_config key and processes locations found under the key.
    This provides enough information to construct the local working_copy path using ``repo_root`` inherited
    from :obj:`projectenvironment.ProjectEnvironment` and the URL of the remote repository.

    Inherits: projectenvironment.ProjectEnvironment (obj): Inherited RepoFlow object.
    See :obj:`projectenvironment.projectenvironment`.

    Username is assumed to be the same for each repository location (using self.repo_username inherited
    from projectenvironment.ProjectEnvironment)

    """
    def __init__(self, **kwargs):
        super(RepoFlow, self).__init__()
        setattr(self, 'repo_root', self.repo_root.replace('//', '/'))
        self.logger.info('REPO_ROOT: {self.repo_root}'.format(self=self))
        self.logger.info('REPO_USERNAME: {self.repo_username}'.format(self=self))

        try:
            self.logger.info('BITBUCKET_USERNAME: {self.bitbucket_username}'.format(self=self))
            bitbucket_username = self.bitbucket_username
        except AttributeError:
            bitbucket_username = ''
        log.sect_break(self.logger)

        repository_config = self.settings['repository_config']

        self.repo_types = list()
        if 'subversion' in repository_config:
            self.logger.info('Settings Contains Subversion Repository')
            self.repo_types.append('subversion')
        if 'git' in repository_config:
            self.logger.info('Settings Contains Git Repository')
            self.repo_types.append('git')
        else:
            self.logger.critical('Unknown Repository Type in Settings File: {self.settings_file}'
                                 .format(self=self))

        self.dependencies = list()
        for repo_type in self.repo_types:
            repository_config = self.settings['repository_config'][repo_type]
            self.dependencies.extend(self.process_repository_config(repository_config=repository_config,
                                                                    bitbucket_username=bitbucket_username))

        xml2vhdl_support = False
        for depend in self.dependencies:
            if depend.name == 'xml2vhdl':
                self.logger.info('Processing Environment for inclusion of "{depend.name}"...'
                                 .format(depend=depend))
                python_paths = [os.path.join(depend.scripts_dir, 'python', depend.name)]
                if os.path.exists(python_paths[0]):
                    for path in python_paths:
                        self.logger.info('Updating sys.path with: {path}'
                                         .format(path=path))
                        sys.path.append(path)
                        xml2vhdl_support = True
                        xml2vhdl_path = path
                else:
                    self.logger.critical('Can Not Update sys.path. Missing: {python_path}. '
                                         .format(python_path=python_paths[0]))

        setattr(self, 'xml2vhdl_support', xml2vhdl_support)
        setattr(self, 'xml2vhdl_path', xml2vhdl_path)

        log.sect_break(self.logger)
        self.logger.info('Processed Project Dependencies')
        log.sect_break(self.logger)

    def __repr__(self):
        return "{self.__class__.__name__}()".format(self=self)

    def __str__(self):
        return "{} is a {self.__class__.__name__} object".format(__name__, self=self)

    def process_repository_config(self, **kwargs):
        """Process repository configuration for current project

        Keyword Args:
            **repository_config (dict): Dictionary of Repository Configuration for Repository Type extracted
                from ``settings.yml`` YAML file.
            **repo_type (str): The type of repository to operate on. Valid values are: ``'subversion'`` and
                ``'git'```. Default value: ``'subversion'``
            **bitbucket_username (str, optional): The ``username`` to access ``bitbucket`` repository.
                Default value = ``''``

        Returns:
            (list of obj): A list of processed :class:`ProjectDependency` objects.

        """
        repository_config = funcs.get_kwarg('repository_config', kwargs, dict())
        repo_type = funcs.get_kwarg('repo_type', kwargs, 'subversion')
        bitbucket_username = funcs.get_kwarg('bitbucket_username', kwargs, '')
        dependencies = list()

        if isinstance(repository_config, (dict,)):
            for key, value in repository_config.items():
                self.logger.info('Processing Dependency: {name}'
                                 .format(name=key))

                if isinstance(value, (dict,)):
                    if key == self.name:
                        top_level = True
                    else:
                        top_level = False

                if value['enabled']:
                    try:
                        board_name = self.board
                    except AttributeError:
                        board_name = None

                    try:
                        board_settings = self.board_settings
                    except AttributeError:
                        board_settings = None

                    try:
                        family = self.family
                    except AttributeError:
                        family = None

                    try:
                        device = self.device
                    except AttributeError:
                        device = None

                    try:
                        vunit_default = value['vunit_default']
                    except KeyError:
                        vunit_default = False

                    try:
                        required_vhdl_libs = value['required_vhdl_libs']
                    except KeyError:
                        required_vhdl_libs = list()

                    url = value['url']
                    remote_path = self.construct_remote_path(**value)

                    try:
                        remote_rev = value['rev']
                    except KeyError:
                        remote_rev = ''

                    local_path = self.construct_local_path(root=self.repo_root,
                                                           path=value['path'])

                    category = self.get_category_from_path(supported_categories=self.categories,
                                                           category_mapping=self.category_mapping,
                                                           path=value['path'])

                    value.update(name=key)
                    if category == 'library':
                        cat_mapping = self.category_mapping
                        value.update(contrib_lib=self.get_contrib_lib_from_path(name=key,
                                                                                category_mapping=cat_mapping,
                                                                                path=value['path']))
                    else:
                        value.update(contrib_lib=None)

                    required_fields_dict = dict()

                    for attr in self.config['repository']['required']:
                        if attr in value:
                            required_fields_dict.update({attr: value[attr]})
                            self.logger.debug('\tUsing Attribute from Dependency: {attr}'
                                              .format(attr=attr))
                        else:
                            required_fields_dict.update({attr: getattr(self, attr)})
                            self.logger.debug('\tUsing Inherited Attribute: {attr}'
                                              .format(attr=attr))

                    dependencies.append(ProjectDependency(repo_root=self.repo_root,
                                                          name=key,
                                                          category=category,
                                                          url=url,
                                                          local_path=local_path,
                                                          remote_path=remote_path,
                                                          remote_rev=remote_rev,
                                                          required_vhdl_libs=required_vhdl_libs,
                                                          vunit_default=vunit_default,
                                                          top_level=top_level,
                                                          board_name=board_name,
                                                          board_settings=board_settings,
                                                          family=family,
                                                          device=device,
                                                          lib_append_categories=self.lib_append_categories,
                                                          bitbucket_username=bitbucket_username,
                                                          repo_config_dict=self.config['repository'],
                                                          tag_replacement_dict=required_fields_dict))

                    if not self.checkout_disabled:
                        self.logger.debug('Checking Out: {name}'
                                          .format(name=key))
                        try:
                            if url in _url_cache:
                                _url_cache = self._url_cache_handler(url=url,
                                                                     cache=_url_cache)
                        except NameError:
                            self.logger.info('Generating URL Cache: {url}'
                                             .format(url=url))
                            _url_cache = self._url_cache_handler(url=url,
                                                                 cache={url: False})
                        self._checkout(cache_dict=_url_cache, repo_type=repo_type,
                                       url=url,
                                       remote_path=remote_path,
                                       remote_rev=remote_rev,
                                       local_path=local_path)
                    else:
                        self.logger.info('Repository Checkout Disabled')
                        if os.path.exists(local_path):
                            self.logger.info('Local Path Found on File-System: {path}'
                                             .format(path=local_path))
                        else:
                            self.logger.critical('Local Path Missing on File-System: {path}'
                                                 .format(path=local_path))
                            self.logger.critical('\tDesign Might Not Compile...')
                            self.logger.critical('\tConfigure Project to Checkout Location')
                else:
                    self.logger.warning('Processing for "{depend}" Disabled in Settings File: {file_ref}'
                                        .format(depend=key,
                                                file_ref=self.settings_file))

                log.sect_break(self.logger)

        return dependencies

    def _url_cache_handler(self, **kwargs):
        """Caches Passwords for Accessed Controlled URLs.

        To stop the script from requesting passwords for each checkout, if the repository root URL is the
        same, this will cache the password so it only needs to be entered at the console once.

        Args:
            **url (str, optional): Default value: ``None``
            **url_cache_dict (dict, optional): Default value: ``None``

        Returns:
            None

        """
        url = funcs.get_kwarg('url', kwargs, None)
        url_cache_dict = funcs.get_kwarg('cache', kwargs, None)

        if url in url_cache_dict:
            self.logger.debug('URL Already a key in url_cache_dict: {url}'
                              .format(url=url))
        else:
            self.logger.debug('Adding URL as key in url_cache_dict: {url}'
                              .format(url=url))

        # Setup Password Prompt for Use by getpass:
        getpass_prompt = 'Password for {self.repo_username}@{url}:'.format(self=self, url=url)

        # svn logger DEBUG messages contain plain text passwords passed to svn.
        # To prevent the svn logger from writing DEBUG level messages in the log file disable all 'svn'
        # related loggers:
        for name, logr in log.logging.root.manager.loggerDict.iteritems():
            if 'svn' in name:
                logr.disabled = True
                self.logger.debug('Disabled svn logger: {name}:{logger}'
                                  .format(name=name, logger=logr))

        if not url_cache_dict[url]:
            self.logger.debug('No Password Cached for URL: {url}'
                              .format(url=url))
            if not self.dev_flag:
                url_cache_dict[url] = getpass.getpass(prompt=getpass_prompt)
            else:
                self.logger.critical('Running Script in Dev Mode: Password Caching Disabled')
        else:
            self.logger.debug('Password Already Cached for URL: {url}'
                              .format(url=url))

        return url_cache_dict

    def construct_remote_path(self, **kwargs):
        """Constructs the remote path in the externally hosted repository.

        Determines if the URL is ``bitbucket`` from ``urlparse.netloc``
        Uses ``urlparse`` to construct URL, where ``username`` is constructed manually at the front of
        ``urlparse.netloc``

        Uses ``posixpath`` to construct path portion of URL by joining ``urlparse.path``, ``path``
        and ``subpath``.

        Args:
            **url (str): The top-level root URL. See :ref:`settings_subversion`. Default value: ``None``
            **path (str): The path. See :ref:`settings_subversion`.  Default value: ``None``
            **subpath (str): The sub-path. See :ref:`settings_subversion`.  Default value: ``None``
            **bitbucket_username (str, optional): The ``username`` to access ``bitbucket`` repository.
                Default value = ``''``

        Returns:
            (str): Full path of the remote URL.

        """
        url = funcs.get_kwarg('url', kwargs, None)
        path = funcs.get_kwarg('path', kwargs, None)
        subpath = funcs.get_kwarg('subpath', kwargs, None)
        bitbucket_username = funcs.get_kwarg('bitbucket_username', kwargs, '')

        urlunsplit_param = ''
        urlunsplit_query = ''
        urlunsplit_frag = ''

        parsed_url = urlparse.urlsplit(url)

        if 'bitbucket' in parsed_url.netloc:
            self.logger.info('Processing a bitbucket URL: {url}'.format(url=url))

            if bitbucket_username != '':
                username_netloc = bitbucket_username + '@' + parsed_url.netloc
            else:
                username_netloc = parsed_url.netloc
            remote_path = urlparse.urlunparse((parsed_url.scheme,
                                               username_netloc,
                                               parsed_url.path,
                                               urlunsplit_param,
                                               urlunsplit_query,
                                               urlunsplit_frag))
        else:
            self.logger.info('Processing: {url}'.format(url=url))

            remote_path = urlparse.urlunparse((parsed_url.scheme,
                                               parsed_url.netloc,
                                               posixpath.join(parsed_url.path, path, subpath),
                                               urlunsplit_param,
                                               urlunsplit_query,
                                               urlunsplit_frag))

        self.logger.info('Constructed Full Checkout URL: {remote_path}'
                         .format(remote_path=remote_path))

        return remote_path

    def construct_local_path(self, **kwargs):
        """Constructs the local path for the local working-copy.

        Constructed by joining ``root`` and  ``path``.

        Args:
            **root (str): The top-level root. Usually derived from the ``$REPO_ROOT`` environment variable.
                Default value: ``None``
            **path (str): The path, derived from :ref:`settings_subversion`, but with the ``subpath:``
                removed. This allows the switching between ``trunk``, ``branches`` and ``tags`` to be
                managed by the repository client. Default value: ``None``

        Returns:
            (str): Full path of the local working-copy path.

        """
        root = funcs.get_kwarg('root', kwargs, None)
        path = funcs.get_kwarg('path', kwargs, None)

        local_path = os.path.join(root, path)
        self.logger.info('Constructed Full Working Copy Path:  {local_path}'
                         .format(local_path=local_path))

        return local_path

    def _checkout(self, cache_dict, repo_type='subversion', **kwargs):
        """Validates checkout parameters and checks out the source-code from remote location

        Args:
            cache_dict (dict): Default value: ``None``
            repo_type (str, optional): Operating on either a ``'subversion'`` or ``'git'`` repository.
                Default value: ``'subversion'``.

        Keyword Args:
            **url (str): Default value: ``None``.
            **remote_path (str): Default value: ``None``.
            **remote_rev (str): Default value: ``None``.
            **local_path (str): Default value: ``None``.

        Returns:
            (bool): ``False`` if trying to operate on a ``git`` repository.

        """
        url = funcs.get_kwarg('url', kwargs, None)
        remote_path = funcs.get_kwarg('remote_path', kwargs, None)
        remote_rev = funcs.get_kwarg('remote_rev', kwargs, None)
        local_path = funcs.get_kwarg('local_path', kwargs, None)

        wc_exists = False

        if os.path.exists(local_path):
            self.logger.warning('Local Path Already Exists for Checkout Operation: {path}'
                                .format(path=local_path))

            local_repo_obj = self._set_working_copy(local_path=local_path,
                                                    repo_type=repo_type)

            if local_repo_obj and self._check_working_copy(remote_type=repo_type,
                                                           local_repo_obj=local_repo_obj,
                                                           remote_path=remote_path):
                self.logger.warning('Working Copy Location is Already Checked Out. '
                                    'May Require Updating: {path}'
                                    .format(path=local_path))
                wc_exists = True
            else:
                return False

        if not wc_exists:
            remote_repo_obj = self._set_remote(cache_dict, repo_type, **kwargs)
            if remote_repo_obj:
                self.logger.info('Performing Check Out:')
                self.logger.info('\t{remote_path}@{remote_rev} -> {local_path}'
                                 .format(remote_path=remote_path,
                                         remote_rev=remote_rev,
                                         local_path=local_path))
                if repo_type == 'subversion':
                    remote_repo_obj.checkout(local_path, remote_rev)
                elif repo_type == 'git':
                    # \TODO Perform git Clone Here and return True
                    return False
            else:
                self.logger.critical('Problem Performing {repo_type} Checkout:'
                                     .format(repo_type=repo_type.capitalize()))
                self.logger.critical('\t{remote_path}@{remote_rev} -> {local_path}'
                                     .format(remote_path=remote_path,
                                             remote_rev=remote_rev,
                                             local_path=local_path))
                self.logger.critical('Skipping...')
                return False

    def _set_working_copy(self, repo_type='subversion', **kwargs):
        """Connects to an existing local working_copy.

        Args:
            repo_type (str, optional): Operating on either a ``'subversion'`` or ``'git'`` repository.
                Default value: ``'subversion'``.

        Keyword Args:
            **local_path (str): Default value: ``None``.

        Returns:
            (bool): ``False`` if trying to operate on a ``git`` repository.

        """
        local_path = funcs.get_kwarg('local_path', kwargs, None)

        if repo_type == 'subversion':
            import svn.local
            repo_obj = svn.local.LocalClient(local_path)

        elif repo_type == 'git':
            from git import Repo
            repo_obj = False

        return repo_obj

    def _check_working_copy(self, repo_type='subversion', **kwargs):
        """Checks existing local working_copy against expected working-working parameters.

        If a working-copy already exists in the local file-system, check to see if it matches the expected
        remote working-copy.

        Args:
            repo_type (str, optional): Operating on either a ``'subversion'`` or ``'git'`` repository.
                Default value: ``'subversion'``.

        Keyword Args:
            **local_path (str): Default value: ``None``.

        Returns:
            (bool): ``False`` if trying to operate on a ``git`` repository.

        """
        repo_obj = funcs.get_kwarg('local_repo_obj', kwargs, None)
        remote_path = funcs.get_kwarg('remote_path', kwargs, None)

        if repo_type == 'subversion':
            # Fetch the Associated URL from the Working Copy
            try:
                repo_info = repo_obj.info()
                wc_url = repo_info['url']
            except Exception as e:
                self.logger.critical('Failed to Connect with Working Copy')
                self.logger.critical('\t{msg}'
                                     .format(msg=e))
                self.logger.critical('\tSkipping...')
                return False
        elif repo_type == 'git':
            # \TODO Fetch the Associated URL from the Working Copy when using git and return True
            return False

        if wc_url == remote_path:
            self.logger.info('URL Match: Valid Working Copy:')
            self.logger.info('\t{url}'
                             .format(url=remote_path))
            return True
        else:
            self.logger.critical('URL Mismatched: Invalid Working Copy:')
            self.logger.critical('\tExpected: {url}'
                                 .format(url=remote_path))
            self.logger.critical('\tGot:      {url}'
                                 .format(url=wc_url))
            return False

    def _set_remote(self, cache_dict, repo_type='subversion', **kwargs):
        """ Sets the remote repository for performing Checkout/Clone operations.

        Args:
            cache_dict (dict): Default value: ``None``
            repo_type (str, optional): Operating on either a ``'subversion'`` or ``'git'`` repository.
                Default value: ``'subversion'``.

        Keyword Args:
            **url (str): Default value: ``None``.
            **remote_path (str): Default value: ``None``.

        Returns:
            (bool): ``False`` if trying to operate on a ``git`` repository.

        """

        url = funcs.get_kwarg('url', kwargs, None)
        remote_path = funcs.get_kwarg('remote_path', kwargs, None)

        if repo_type == 'subversion':
            import svn.remote
            remote_repo_obj = svn.remote.RemoteClient(remote_path,
                                                      username=self.repo_username,
                                                      password=cache_dict[url])
            try:
                repo_info = remote_repo_obj.info()
                self.logger.info('Successfully Connected to Remote Location: {username}@{url}'
                                 .format(username=self.repo_username, url=remote_path))
                return remote_repo_obj
            except Exception as e:
                self.logger.critical('Failed to Connect to Remote Location: {username}@{url}'
                                     .format(username=self.repo_username, url=remote_path))
                self.logger.critical('\t{msg}'
                                     .format(msg=e))
                self.logger.critical('Skipping...')
                return False

        elif repo_type == 'git':
            # \TODO Add Remote Support for git and return equiv. git remote_obj
            return False

    def get_category_from_path(self, **kwargs):
        """Gets ``category:`` from ``path``.

        The first directory in the path string represents the category.

        Keyword Args:
            **path (str): Default value: ``''``
            **category_mapping (dict, optional): Category mapping (see :ref:`config_categories`).
                Default value: ``dict()``.
            **supported_categories (list of str, optional): List of supported categories from ``config.yml``
                configuration file (see :ref:`config_categories`). Default value: ``list()``.

        Returns:
            (str): the ``category`` extracted from ``path``.

        """
        path = funcs.get_kwarg('path', kwargs, '')
        category_mapping = funcs.get_kwarg('category_mapping', kwargs, dict())
        supported_categories = funcs.get_kwarg('supported_categories', kwargs, list())

        cat = path.split('/')[0]

        for k, v in category_mapping.iteritems():
            if v == cat:
                cat = k

        if cat in supported_categories:
            self.logger.info('Category: {cat}'
                             .format(cat=cat))
            return cat
        else:
            self.logger.error('Could Not Resolve Category from Path')
            self.logger.error('\tPath: {path}'
                              .format(path=path))
            self.logger.error('\tCategory: {cat}'
                              .format(cat=cat))
            self.logger.error('\tSupported Categories: {cats}'
                              .format(cats=supported_categories))
            log.errorexit(self.logger)

    def get_contrib_lib_from_path(self, **kwargs):
        """Gets ``contrib_lib:`` from ``path``.

        Assumes (i know!) that ``contrib_lib`` exists between the ``category`` and ``name``.
        For a valid ``contrib_lib`` to exist the number of elements in ``path`` should be = 3.

        Keyword Args:
            **name (str): The project name being processed. Default value: ``''``
            **path (str): The path of the project on the file-system. Default value: ``''``
            **category_mapping (dict, optional): Category mapping (see :ref:`config_categories`).
                Default value: ``dict()``.

        Returns:
            (str): the ``contrib_lib`` extracted from ``path``.

        """

        name = funcs.get_kwarg('name', kwargs, '')
        path = funcs.get_kwarg('path', kwargs, '')
        category_mapping = funcs.get_kwarg('category_mapping', kwargs, dict())

        path_elements = path.split('/')
        self.logger.debug('Nof Path Elements: {len}'
                          .format(len=len(path_elements)))

        cat = path_elements[0]

        if len(path_elements) == 3:
            for k, v in category_mapping.iteritems():
                if v == cat:
                    cat = k

            contrib_lib = path_elements[1]
            path_name = path_elements[2]

            self.logger.debug('Category : {cat}'
                              .format(cat=cat))
            self.logger.debug('Contrib  : {contrib_lib}'
                              .format(contrib_lib=contrib_lib))
            self.logger.debug('Path Name: {path_name}'
                              .format(path_name=path_name))

            if path_elements[2] == name:
                contrib_lib = path_elements[1]
                self.logger.info('Contributor: {contrib_lib}'
                                 .format(contrib_lib=contrib_lib))
                return contrib_lib

        # If it gets this far raise a warning because no valid contrib_lib was found
        self.logger.warning('No Contributor for: {name}'
                            .format(name=name))
        return None


class ProjectDependency(object):
    """Processes project dependencies.

    Takes a dictionary and converts keys to attributes before parsing configuration to construct all
    attributes required to describe a Dependency Object

    Args:
        repo_root (str): The resolved ``$REPO_ROOT`` system environment variable. Required by:
            :mod:`projectmanager.ProjectDependency.layout_to_dir` and
            :mod:`projectmanager.ProjectDependency.prune_path_list`
        name (str): Name of dependency
        category (str): The dependency's category
        url (str): Root URL to remote repository location for the dependency
        local_path (str): Local path of the *working copy* for the dependency
        remote_path (str): Remote path, from the ``url`` for the dependency
        remote_rev (str): Specific repository revision for the dependency
        required_vhdl_libs (list of str, optional): List of required HDL libraries required by the dependency.
            Default value: ``list()``
        vunit_default (bool, optional): VUnit dependency flag. Default value: ``False``
        top_level (bool, optional): Project Top-level dependency flag. Default value: ``False``

        board (str, optional): Target board for dependency. Default value: ``None``
        board_settings (str, optional): Settings file name for target board for dependency.
            Default value: ``None``
        family (str, optional): Target FPGA Family for HDL dependency. Default value: ``None``
        device (str, optional): Target FPGA Device for HDL dependency. Default value: ``None``

    Keyword Args:
        **repo_config_dict (dict): The layout dictionary which defines the projects layout within the
            repository and working copy on the local file-system.
            Required by :mod:`projectmanager.ProjectDependency.layout_to_dir`
            Default value: ``dict()``
        **lib_append_categories (list of str): Default value: ``list()``
        **bitbucket_username (str, optional): Default value: ``None``

        **tag_replacement_dict (dict): Dictionary of required tag replacement fields required by
            :mod:`projectmanager.ProjectDependency.layout_tag_attr_replace`. This is variable based on
            ``category``
            Default value: ``dict()``
        **retag_layout (bool, optional). Retags the layout list (for 'vendor_ip'. Default value: ``True``

    """
    def __init__(self, repo_root, name, category, url, local_path, remote_path, remote_rev,
                 required_vhdl_libs=list(), vunit_default=False, top_level=False,
                 board_name=None, board_settings=None, family=None, device=None, **kwargs):

        self.logger = log.config_logger(name=__name__, class_name=self.__class__.__name__)
        setattr(self, 'category', category)
        setattr(self, 'top_level', top_level)
        setattr(self, 'required_vhdl_libs', required_vhdl_libs)
        setattr(self, 'vunit_default', vunit_default)
        setattr(self, 'url', url)
        setattr(self, 'local_path', local_path)
        setattr(self, 'remote_path', remote_path)
        setattr(self, 'remote_rev', remote_rev)

        setattr(self, 'family', family)
        setattr(self, 'device', device)

        lib_append_categories = funcs.get_kwarg('lib_append_categories', kwargs, list())
        retag_layout = funcs.get_kwarg('retag_layout', kwargs, True)

        if vunit_default:
            lib = self.get_lib_from_name(name=name,
                                         category=category,
                                         lib_append_categories=lib_append_categories)
        else:
            lib = None

        setattr(self, 'lib', lib)
        setattr(self, 'bitbucket_username', funcs.get_kwarg('bitbucket_username', kwargs, None))

        repo_config_dict = funcs.get_kwarg('repo_config_dict', kwargs, dict())
        self.logger.debug('Tag Replacements:')
        for k, v in funcs.get_kwarg('tag_replacement_dict', kwargs, dict()).items():
            self.logger.debug('\t{k}:{v}'.format(k=k, v=v))
            setattr(self, k, v)

        layout_str = self.category + '_layout'
        self.logger.debug('Using Layout: {layout}'
                          .format(layout=layout_str))

        setattr(self, '_temp_layout_list', list())
        _layout_dict = repo_config_dict[layout_str]
        self._top_dirs = list()
        self.layout_list = list()

        top_refs = self.set_top_refs(category, name, self.tool_version)

        if category == 'boards':
            setattr(self, 'is_board', True)
            if board_name:
                self.logger.info('Dependency is a Board: Using Board Name as Name: {board_name}'
                                 .format(board_name=board_name))
                setattr(self, 'name', board_name)
            else:
                self.logger.critical('Dependency is a Board: But No Board Name Supplied, Using: {name}'
                                     .format(name=name))
                setattr(self, 'name', name)
            if board_settings:
                if board_settings.endswith('.yml'):
                    setattr(self, 'board_settings', board_settings)
                else:
                    setattr(self, 'board_settings', board_settings + '.yml')
            else:
                default_settings_file = 'default_settings.yml'
                self.logger.warning('No Board Settings File Name Supplied. Using: {default_settings_file}'
                                    .format(default_settings_file=default_settings_file))
                setattr(self, 'board_settings', default_settings_file)

        else:
            setattr(self, 'name', name)
            setattr(self, 'is_board', False)
            setattr(self, 'board_settings', None)

        self.layout_to_dir(layout_dict=_layout_dict,
                           repo_root=repo_root,
                           top_refs=top_refs,
                           replace_tags=True)

        for kw in self._top_dirs:
            attr_name = self.top_dir_lookup(dir_name=kw)

            path_list = self.prune_path_list(path_list=self.layout_list,
                                             root_path=repo_root,
                                             keyword=kw)

            if path_list:
                if len(path_list) == 1:
                    self.logger.debug('Created Attribute: {attr} {value}'
                                      .format(attr=attr_name, value=path_list[0]))
                    setattr(self, attr_name, path_list[0])
                else:
                    self.logger.warning('More than One Path Found when Generating {attr}_dir: {path_list}'
                                        .format(attr=kw, path_list=path_list))
                    self.logger.warning('Created Attribute from First Value: {attr} {value}'
                                        .format(attr=attr_name, value=path_list[0]))
                    setattr(self, attr_name, path_list[0])
            else:
                self.logger.debug('Not Creating _dir Attribute...')

        if category == 'vendor_ip' and retag_layout:
            setattr(self, 'layout_dict', _layout_dict)

            retagged_layout_list = self.retag_path(term='vendor_ip',
                                                   tag='<NAME>',
                                                   paths=self.layout_list,
                                                   repo_root=repo_root)

            retagged_layout_list = self.retag_path(term=self.vendor,
                                                   tag='<VENDOR>',
                                                   paths=retagged_layout_list,
                                                   repo_root=repo_root)

            if self.tool_version:
                retagged_layout_list = self.retag_path(term=self.tool_version,
                                                       tag='<TOOL_VERSION>',
                                                       paths=retagged_layout_list,
                                                       repo_root=repo_root)

            if family:
                retagged_layout_list = self.retag_path(term=family,
                                                       tag='<FAMILY>',
                                                       paths=retagged_layout_list,
                                                       repo_root=repo_root)

            if device:
                retagged_layout_list = self.retag_path(term=device,
                                                       tag='<DEVICE>',
                                                       paths=retagged_layout_list,
                                                       repo_root=repo_root)

            setattr(self, 'layout_list', retagged_layout_list)

            for p in self.layout_list:
                self.logger.debug('Rebuilt Vendor IP Layout: {p}'.format(p=p))

        elif category == 'vendor_ip':
            pass

        else:
            pass

    def retag_path(self, **kwargs):
        """Re-tags path(s).

        Keyword Args:
            **term (str): Term to retag.
            **tag (str): Tag value to replace term with.
            **paths (str or list of str): absolute path(s) to retag. This assumes the absolute path is in the
                form: ``$REPO_ROOT/<TERM>/xx/xx/xx/<TERM>`` where the second term will be replaced with
                ``tag``.
            **repo_root (str): The actual path of the system environment variable ``$REPO_ROOT``

        Returns:
            list of str: List of retagged absolute paths. Empty ``list()`` if no repo_root supplied.
        """
        term = funcs.get_kwarg('term', kwargs, None)
        tag = funcs.get_kwarg('tag', kwargs, '<NAME>')
        paths = funcs.get_kwarg('paths', kwargs, list())
        repo_root = funcs.get_kwarg('repo_root', kwargs, None)

        if isinstance(paths, (str, )) and paths != "":
            paths = [paths]

        if repo_root:
            term_root = os.path.join(repo_root, term)
        else:
            return list()

        rebuild_layout_list = list()
        for p in paths:
            try:
                split_path = p.split(term_root)[1][1:]
            except IndexError:
                term_root = repo_root
                split_path = p.split(term_root)[1][1:]

            renamed_path = split_path.replace(term, tag)
            rebuilt_path = os.path.join(term_root, renamed_path)
            rebuild_layout_list.append(rebuilt_path)
            self.logger.debug('Rebuilt Layout: {p}'.format(p=rebuilt_path))

        return rebuild_layout_list

    def get_lib_from_name(self, **kwargs):
        """Determines the ``VHDL`` library name from project name.

        Determines the ``VHDL`` library name from the project name, ignoring if suffix already exists.
        the suffix is only appended if the ``category`` exists in the ``lib_append_categories`` list

        Keyword Args:
            **name (str): The project name being processed. Default value: ``''``
            **category (str): The ``category`` of the project being processed. Default value: ``''``
            **lib_append_categories (list of str, optional): List of categories to append ``lib_suffix``
                from ``config.yml`` configuration file (see :ref:`config_categories`). If the ``category``
                is **not** in this list the suffix will **not** be appended. Default value: ``list()``.
            **lib_suffix (str, optional): The library suffix to append. Default value: ``'_lib'``

        Returns:
            (str): The name of the ``VHDL`` library

        """
        name = funcs.get_kwarg('name', kwargs, '')
        category = funcs.get_kwarg('category', kwargs, '')
        lib_append_categories = funcs.get_kwarg('lib_append_categories', kwargs, list())
        lib_suffix = funcs.get_kwarg('lib_suffix', kwargs, '_lib')
        suffix_len = len(lib_suffix)
        suffix_idx = -suffix_len

        self.logger.debug('Determining Library from Name: {name}'
                          .format(name=name))
        self.logger.debug('Library Suffix: {suffix} [{idx}]'
                          .format(suffix=lib_suffix, idx=suffix_idx))

        if category in lib_append_categories:
            if len(name) > suffix_len:
                if name[suffix_idx:] != lib_suffix:
                    name = name + lib_suffix
            else:
                name = name + lib_suffix

        self.logger.info('Library Name: {name}'
                         .format(name=name))

        return name

    @staticmethod
    def top_dir_lookup(**kwargs):
        """Maps supported top-level directory names to known values for specified usage throughout

        Keyword Args:
            **dir_name (str): Name of directory name to attempt to map.

        Returns:
            str: Mapped name if matched. ``dir_name`` if *not* matched.

        """
        dir_name = funcs.get_kwarg('dir_name', kwargs, '')

        if dir_name in ['constraints', 'constr', 'constrs']:
            name = 'constraints'

        elif dir_name in ['docs', 'doc', 'documents', 'documentation']:
            name = 'docs'

        elif dir_name in ['netlists', 'net', 'nets']:
            name = 'netlists'

        elif dir_name in ['scripts', 'script']:
            name = 'scripts'

        elif dir_name in ['settings', 'setting']:
            name = 'settings'

        elif dir_name in ['simulation', 'sim', 'sims']:
            name = 'simulation'

        elif dir_name in ['src', 'srcs', 'sources']:
            name = 'src'

        else:
            name = dir_name

        return '{attr}_dir'.format(attr=name)

    @staticmethod
    def set_top_refs(category, name, tool_version):
        """

        Args:
            category (str): category to determine the top-level reference to return.
            name (str): returned if ``category`` is *not* ``boards`` or ``vendor_ip``
            tool_version (str): returned if ``category`` *is* ``boards`` or ``vendor_ip``

        Returns:
            list of str

        """
        if category == 'boards':
            return [tool_version]
        elif category == 'vendor_ip':
            return [tool_version]
        else:
            return [name]

    def layout_to_dir(self, **kwargs):
        """Takes a single top-level and creates the directory and file structure as a list.

        This layout structure is expected to be defined in the layout_dict keyword passed to the module.

        Uses top_refs list to look for a reference to indicate the top reference string, which is
        used to populate self._top_dirs, this can then be used to create attributes for top_level reference
        directories.

        Keyword Args:
            **layout_dict (dict): Default value: ``dict()``
            **repo_root (str): Default value: ``None``
            **top_refs (list of str): Default value: ``list()``
            **replace_tags (bool): Default value: ``True``

        Returns:
            None

        """
        layout_dict = funcs.get_kwarg('layout_dict', kwargs, dict())
        repo_root = funcs.get_kwarg('repo_root', kwargs, None)
        top_refs = funcs.get_kwarg('top_refs', kwargs, list())
        replace_tags = funcs.get_kwarg('replace_tags', kwargs, True)

        self.logger.debug('layout_to_dir()replace_tags: {replace_tags}'
                          .format(replace_tags=replace_tags))
        self.logger.debug('layout_to_dir():layout_dict: {layout_dict}'
                          .format(layout_dict=layout_dict))
        self.logger.debug('layout_to_dir():repo_root:   {repo_root}'
                          .format(repo_root=repo_root))

        if isinstance(layout_dict, (dict,)):
            for key, value in layout_dict.items():
                if replace_tags:
                    key = self.layout_tag_attr_replace(tag=key)
                    if key in top_refs:
                        if isinstance(value, (list, dict,)):
                            for i in value:
                                self._top_dirs.append(i.keys()[0])
                self.logger.debug('layout_to_dir():key:{}'.format(key).lower())
                self.logger.debug('1:layout_to_dir({}, {})'.format(value, os.path.join(repo_root, key)))
                if value:
                    self.layout_to_dir(layout_dict=value,
                                       repo_root=os.path.join(repo_root, key),
                                       top_refs=top_refs,
                                       replace_tags=replace_tags)
                else:
                    self.logger.debug(os.path.join(repo_root, key))
                    self.layout_list.append(os.path.join(repo_root, key))

        elif isinstance(layout_dict, (list,)):
            for item in layout_dict:
                if isinstance(item, (dict,)):
                    self.logger.debug('2:layout_to_dir({}, {})'.format(item, repo_root))
                    self.layout_to_dir(layout_dict=item,
                                       repo_root=repo_root,
                                       top_refs=top_refs,
                                       replace_tags=replace_tags)
                else:
                    if replace_tags:
                        item = self.layout_tag_attr_replace(tag=item)
                    self.logger.debug('os.repo_root.join({}, {})'.format(repo_root, item))
                    self.logger.debug(os.path.join(repo_root, item))
                    self.layout_list.append(os.path.join(repo_root, item))

    def layout_tag_attr_replace(self, **kwargs):
        """Replaces ``<TAG>`` with corresponding attribute

        Looks for ``<TAG>`` (enclosed in ``<>``) in tag string passed to the function, and if found
        returns a string with the tag replaced by the value in the ``self.<TAG>`` attribute.

        If the attribute exists but is not populated with a value an "empty"  string ``''`` is returned.
        This allows all <TAG> options in the layout configuration to be optional.
        Although ``self.name`` should always have a value as it is also used to determine filenames
        in the directory structure.

        Keyword Args:
            **tag (str): string to check for sub-strings enclosed in ``<>``.

        Returns:
            (str): An empty string if corresponding attribute for the ``<TAG>`` is **not** found; or the
            corresponding attribute if found; or the original ``<TAG>`` if anything else.

        """
        tag = funcs.get_kwarg('tag', kwargs, None)

        if '<' in tag and '>' in tag:
            attribute_tag = funcs.strip_tag(tag)
            self.logger.debug('Processing {tag}: {attribute_tag}'
                              .format(tag=tag, attribute_tag=attribute_tag))
        else:
            self.logger.debug('Not a Valid Tag: {tag}'
                              .format(tag=tag))
            return tag

        if hasattr(self, attribute_tag):
            if not getattr(self, attribute_tag):
                self.logger.critical('Attribute Not Found: {}'
                                     .format(attribute_tag))
                return ''
            else:
                self.logger.debug('Valid Tag {tag}: {attribute_tag}'
                                  .format(tag=tag, attribute_tag=attribute_tag))

                resolved_attr = getattr(self, attribute_tag)
                self.logger.debug('Resolved Attribute from Tag: {}'
                                  .format(resolved_attr))
                return re.sub('(<[^>]+>)', resolved_attr, tag)
        else:
            self.logger.debug('Attribute Not Found: {}'
                              .format(attribute_tag))
            return tag

    def prune_path(self, **kwargs):
        """Prunes path down towards ``root_path``.

        Takes a path and prunes that path until prune_to is found, if root_path is reached it means that
        prune_to was not found in the path.

        Returns path up to and including prune_to, or False if not found.

        Keyword Args:
            **path (str): Path to prune. Default value: ``None``
            **prune_to (str): Prune down to this path. Default value: ``None``
            **root_path (str): If ``root_path`` is reached the prune fails. Default value: ``None``

        Returns:
            (str): The found pruned path. The `bool:` ``False`` is returned if ``root_path`` is reached
            without finding the prune criteria.

        """
        path = funcs.get_kwarg('path', kwargs, None)
        prune_to = funcs.get_kwarg('prune_to', kwargs, None)
        root_path = funcs.get_kwarg('root_path', kwargs, None)

        while True:
            if os.path.split(path)[1] == prune_to:
                self.logger.debug('Pruned Path: {}'
                                  .format(path))
                return path
            elif os.path.split(path)[0] == root_path:
                self.logger.critical('{prune} Not found in: {path}'
                                     .format(prune=prune_to, path=path))
                return False
            else:
                path = os.path.split(path)[0]

    def prune_path_list(self, **kwargs):
        """Prunes list of paths based on ``keyword`` matching.

        Keyword Args:
            **path_list (list of str): List of paths to prune. Default value: ``None``
            **keyword (str): Keyword which **must** exist in ``path_list`` item for prune.
                Default value: ``''``
            **root_path (str): If ``root_path`` is reached the prune fails. Default value: ``None``

        Returns:
            (list of str): A list of pruned paths.

        """
        path_list = funcs.get_kwarg('path_list', kwargs, None)
        keyword = funcs.get_kwarg('keyword', kwargs, '')
        root_path = funcs.get_kwarg('root_path', kwargs, None)

        keyword_matches = [kw for kw in path_list if keyword in kw]

        pruned_paths = []
        for path in keyword_matches:
            pruned_path = self.prune_path(path=path, prune_to=keyword, root_path=root_path)
            if pruned_path not in pruned_paths:
                self.logger.debug('Adding Path to Pruned Paths: {}'
                                  .format(pruned_path))
                pruned_paths.append(pruned_path)

        return pruned_paths

    def set_as_board(self, **kwargs):

        top_level_dependency = funcs.get_kwarg('top_level_dependency', kwargs, None)
        board_priority_list = funcs.get_kwarg('board_priority_list', kwargs,
                                              ['vendor', 'tool_version', 'family', 'device'])

        board_settings_file = False
        self.logger.info('.' * 80)
        self.logger.info('Additional Board Processing...')
        if self.settings_dir:
            self.logger.debug('Board Settings Path: {settings_dir}'
                              .format(settings_dir=self.settings_dir))

            for root, subpath, files in os.walk(self.settings_dir):
                for f in files:
                    try:
                        if self.board_settings in f:
                            board_settings_file = os.path.join(root, f)
                            self.logger.info('Found Settings File for Board: {f}'
                                             .format(f=board_settings_file))
                            break
                    except AttributeError:
                        if 'default_settings' in os.path.splitext(f):
                            board_settings_file = os.path.join(root, f)
                            self.logger.info('Found Default Settings File for Board: {f}'
                                             .format(f=board_settings_file))
                            break

            if board_settings_file:
                with open(board_settings_file, 'r') as ymlfile:
                    setattr(self, 'board_settings', yaml.load(ymlfile))
                    self.logger.info('Loaded Board Settings from YAML File: {f}'
                                     .format(f=board_settings_file))

                    try:
                        board_tool_version = fpgavendor_iface.resolve_tool_version(tool_version=self.board_settings['tool_version'],
                                                                                   vendor=self.board_settings['vendor'])
                        self.board_settings['tool_version'] = board_tool_version
                    except KeyError:
                        pass

            self.logger.info('Using Settings from Board...')

            for key in board_priority_list:
                if key in self.board_settings:
                    if self.board_settings[key] == getattr(top_level_dependency, key, False):
                        self.logger.debug('[{key}] Project Setting: {proj} Matches Board Setting: {board}.'
                                          .format(key=key,
                                                  proj=getattr(top_level_dependency, key, False),
                                                  board=self.board_settings[key]))
                        setattr(self, key, self.board_settings[key])

                    else:
                        self.logger.warning('[{key}] Project Setting: {proj} Does Not Matches Board Setting: '
                                            '{board}. Using Board Setting.'
                                            .format(key=key,
                                                    proj=getattr(top_level_dependency, key, False),
                                                    board=self.board_settings[key]))

                        setattr(self, key, self.board_settings[key])

            for key in self.board_settings:
                if not hasattr(self, key):
                    self.logger.info('[{key}] Adding Setting from: {board_settings_file}'
                                     .format(key=key, board_settings_file=board_settings_file))
                    setattr(self, key, self.board_settings[key])

            if hasattr(self, 'ip'):
                setattr(self, 'has_vendor_ip', True)
            else:
                setattr(self, 'has_vendor_ip', False)

            if not hasattr(self, 'board_id'):
                setattr(self, 'board_id', 'X"0000_0000"')
            if not hasattr(self, 'board_timestamp_enabled'):
                setattr(self, 'board_timestamp_enabled', False)


class VendorIpDependency(object):
    """Vendor IP is an Vendor IP object containing methods and attributes required for processing ``vendor_ip``

    Keyword Args:
        **repo_root (str): Absolute path to the system environment ``$REPO_ROOT``.
        **master_vendor_ip (obj): A project dependency object for the *master* ``vendor_ip`` dependency for
            the project.
        **vendor (str): FPGA Vendor. Used to determine ``vendor_ip`` locations.
            Valid values: ``'xilinx'`` and ``altera'``. Default value: ``'xilinx'``
        **tool_version (str): FPGA Tool Version. Used to determine ``vendor_ip`` locations.
        **family (str): FPGA Family. Used to determine ``vendor_ip`` locations.
        **device (str): FPGA Device. Used to determine ``vendor_ip`` locations.
        **ip_dict (dict):
        **settings_file (str): Absolute path to settings YAML file, used in logs.
    """
    def __init__(self, **kwargs):
        self.logger = log.config_logger(name=__name__, class_name=self.__class__.__name__)

        setattr(self, 'repo_root', funcs.get_kwarg('repo_root', kwargs, None))
        setattr(self, 'vendor', funcs.get_kwarg('vendor', kwargs, 'xilinx'))
        setattr(self, 'tool_version', funcs.get_kwarg('tool_version', kwargs, None))
        setattr(self, 'family', funcs.get_kwarg('family', kwargs, None))
        setattr(self, 'device', funcs.get_kwarg('device', kwargs, None))
        ip_dict = funcs.get_kwarg('ip_dict', kwargs, dict())
        setattr(self, 'settings_file', funcs.get_kwarg('settings_file', kwargs, ''))
        master_vendor_ip = funcs.get_kwarg('master_vendor_ip', kwargs, None)

        master_layout_list = list()

        if master_vendor_ip:

            master_layout_list = self.resolved_master_tags(paths=master_vendor_ip.layout_list,
                                                           vendor=self.vendor,
                                                           tool_version=self.tool_version,
                                                           family=self.family,
                                                           device=self.device)

            for p in master_layout_list:
                self.logger.info('(Unresolved) Master Vendor IP Path: {p}'.format(p=p))

            resolved_ip = dict()
            for cat, subcats in ip_dict.items():
                if isinstance(subcats, (dict, )):
                    for subcat, v in subcats.items():
                        if isinstance(v, (dict, )):
                            try:
                                if v['enabled']:
                                    resolved_ip[subcat] = {'ipcat': cat,
                                                           'ipsubcat': '',
                                                           'lib': v['library'],
                                                           'wrapper_file': v['wrapper_file']}

                                    self.logger.debug('No Subcategory!: {cat}|{name}'
                                                      .format(cat=cat,
                                                              name=subcat))
                            except KeyError:
                                for n, s in v.items():
                                    try:
                                        if s['enabled']:
                                            resolved_ip[n] = {'ipcat': cat,
                                                              'ipsubcat': subcat,
                                                              'lib': s['library'],
                                                              'wrapper_file': s['wrapper_file']}

                                            self.logger.debug('Subcategory!: {cat}|{subcat}|{name}'
                                                              .format(cat=cat,
                                                                      subcat=subcat,
                                                                      name=n))
                                    except KeyError:
                                        self.logger.critical('Vendor IP Category/Sub-Category too Deep: '
                                                             '{cat}|{subcat}|{name}. Skipping'
                                                             .format(cat=cat,
                                                                     subcat=subcat,
                                                                     name=n))
            for k, v in resolved_ip.items():
                paths = list()

                for p in master_layout_list:
                    resolved_path = p.replace('<NAME>', k)
                    resolved_path = resolved_path.replace('<IPCAT>', v['ipcat'])
                    resolved_path = resolved_path.replace('<IPSUBCAT>', v['ipsubcat'])
                    paths.append(os.path.abspath(resolved_path))

                for p in master_layout_list:
                    if 'common_wrapper_files' in p:
                        try:
                            wrapper_name = v['wrapper_file'].replace('_wrapper', '')
                            resolved_path = p.replace('<NAME>', wrapper_name)
                            resolved_path = resolved_path.replace('<IPCAT>', v['ipcat'])
                            resolved_path = resolved_path.replace('<IPSUBCAT>', v['ipsubcat'])
                            if os.path.abspath(resolved_path) not in paths:
                                paths.append(os.path.abspath(resolved_path))
                        except AttributeError:
                            pass

                self.logger.debug('All Found Paths for {ip}:'
                                  .format(ip=k))
                for path in paths:
                    self.logger.info('(Resolved) IP Search Path: {path}'
                                     .format(path=path))

                for path in paths:
                    for root, subpaths, filenames in os.walk(path):
                        self.logger.debug('Subpaths: {subpaths}'.format(subpaths=subpaths))
                        top_level_paths = [os.path.join(root, sp) for sp in subpaths]
                        for top in top_level_paths:
                            self.logger.debug('\tTop-Level Path: {top}'
                                              .format(top=top))
                            top_dir_str = ProjectDependency.top_dir_lookup(dir_name=os.path.split(top)[1])
                            if top_dir_str in resolved_ip[k]:
                                resolved_ip[k][top_dir_str].append(top)
                            else:
                                resolved_ip[k][top_dir_str] = [top]
                        break

            setattr(self, 'enabled_ip', resolved_ip)

    def resolved_master_tags(self, **kwargs):
        """

        Keyword Args:
            **paths (str, or list of str): Absolute path to resolve tags
            **vendor (str): FPGA Vendor. Used to determine ``vendor_ip`` locations.
                Valid values: ``'xilinx'`` and ``altera'``. Default value: ``'xilinx'``
            **tool_version (str): FPGA Tool Version. Used to determine ``vendor_ip`` locations.
            **family (str): FPGA Family. Used to determine ``vendor_ip`` locations.
            **device (str): FPGA Device. Used to determine ``vendor_ip`` locations.

        Returns:
            list of str: List of absolute paths with tags resolved.
        """

        paths = funcs.get_kwarg('paths', kwargs, None)
        vendor = funcs.get_kwarg('vendor', kwargs, 'xilinx')
        tool_version = funcs.get_kwarg('tool_version', kwargs, None)
        family = funcs.get_kwarg('family', kwargs, None)
        device = funcs.get_kwarg('device', kwargs, None)

        if isinstance(paths, (str, )) and paths != "":
            paths = [paths]

        resolved_paths = list()

        for p in paths:
            untagged_path = p.replace('<VENDOR>', vendor)
            untagged_path = untagged_path.replace('<TOOL_VERSION>', tool_version)
            untagged_path = untagged_path.replace('<FAMILY>', family)
            untagged_path = untagged_path.replace('<DEVICE>', device)
            split_root = os.path.join(untagged_path.split('<NAME>')[0], '<NAME>')
            if split_root not in resolved_paths:
                resolved_paths.append(split_root)

        return resolved_paths


if __name__ == '__main__':
    logger.info("projectmanager {} {}"
                .format(__version__, version.revision))
    log.sect_break(logger)

    project = RepoFlow()

else:
    logger.info(__str__)
