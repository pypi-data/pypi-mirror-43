# -*- coding: utf8 -*-
"""

**************
``docflow.py``
**************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``docflow.py`` is a module provided to setup and manage the auto-documentation generation using ``doxygen``
and ``sphinx``. Project specific values are extracted from the corresponding ``settings.yml`` YAML file
and the projects structure is determined from the ``config.yml`` YAML file, each passed to the module via
:mod:`arguments` (see :ref:`arguments`).

Todo:
    * Consider Moving ``doxygen`` and ``sphinx`` template values to ``config.yml`` YAML file for improved
      flexibility.
    * Determine the name to assign to: ``breathe_project_name``.

"""
import helpers.customlogging as log
import helpers.version as my_version
import projectmanager as project

import helpers.funcs as funcs
import os
import shutil
import subprocess
import datetime
import yaml
import lxml.html

logger = log.config_logger(name=__name__)
LOGLEVEL = log.LogLevelsConsts

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(0, 2, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class ProjectDoc(project.RepoFlow):
    """An object describing the configuration and settings for the projects documentation generation.

    Inherits: project.RepoFlow (obj): Inherited RepoFlow object. See :obj:`projectmanager.RepoFlow`.

    Keyword Args:
        **include_dependencies (bool, optional): Process and include project dependencies in the
            generated documentation. Default value: ``False``

    """
    def __init__(self, **kwargs):
        include_dependencies = funcs.get_kwarg('include_dependencies', kwargs, False)
        super(ProjectDoc, self).__init__()

        doxyfiles = list()
        breathe_projects = list()
        self.logger.debug('Configuration:')
        self.logger.debug('\t{self.doxygen_installdir}'
                          .format(self=self))
        self.logger.debug('\t{self.doxypypy_script}'
                          .format(self=self))
        self.logger.debug('\t{self.doxy_template}'
                          .format(self=self))
        self.logger.debug('\t{self.doxy_extra_style_sheets}'
                          .format(self=self))
        self.logger.debug('\t{self.dot_path}'
                          .format(self=self))
        self.logger.debug('\t{self.sphinx_conf_template}'
                          .format(self=self))
        self.logger.debug('\t{self.sphinx_make_template}'
                          .format(self=self))

        try:
            doxy_mainpage_dict = self.doxy_mainpage
        except (AttributeError, KeyError) as e:
            doxy_mainpage_dict = dict()

        try:
            release_uri = self.release_uri
        except (AttributeError, KeyError) as e:
            release_uri = False

        try:
            issue_uri = self.issue_uri
        except (AttributeError, KeyError) as e:
            issue_uri = False

        try:
            releases_document_name = self.releases_document_name
        except (AttributeError, KeyError) as e:
            releases_document_name = False

        try:
            header = self.header
        except AttributeError:
            header = '_static/esdg_header.rst'

        for depend in self.dependencies:
            if depend.top_level:
                self.source_code_publication_msg(name=depend.name,
                                                 restricted_flag=self.restricted_src)
                self.logger.info('Processing Documentation for Top-Level: {name}'.format(name=depend.name))
                doxy_source_path, doxy_build_path = self.set_doxy_paths(doc_root=depend.docs_dir,
                                                                        doxy_version=self.doxy_version,
                                                                        clean=self.doc_clean)
                logo_file = self.set_logo(doc_root=depend.docs_dir,
                                          logo_path=self.logo_path,
                                          logo_name=self.logo_name)

                image_path = self.set_image_path(doc_root=depend.docs_dir,
                                                 image_path=self.image_path)

                source_path = self.set_source_path(doc_root=depend.docs_dir,
                                                   source_path=self.source_path)

                if self.language == 'python':
                    breathe_project = ''
                    src_code_path = os.path.join(depend.scripts_dir, 'python')

                else:
                    src_code_path = depend.src_dir
                    doxy_input_paths = [depend.src_dir, depend.scripts_dir]

                    doxyfile, breathe_project = self.generate_doxyfile(repo_root=self.repo_root,
                                                                       name=depend.name,
                                                                       doxy_input_paths=doxy_input_paths,
                                                                       doxy_source_path=doxy_source_path,
                                                                       doxy_build_path=doxy_build_path,
                                                                       doxy_template=self.doxy_template,
                                                                       doxy_extra_style_sheets=self.doxy_extra_style_sheets,
                                                                       project_logo=logo_file,
                                                                       restricted_src=self.restricted_src,
                                                                       project_title=self.project_title,
                                                                       project_version=self.project_version,
                                                                       doxy_image_path=image_path,
                                                                       project_language=self.language,
                                                                       doxypypy_script=self.doxypypy_script,
                                                                       dot_path=self.dot_path)

                    self.logger.info('Running Doxygen for: {doxy}'.format(doxy=doxyfile))
                    self.run_doxygen(doxyfile=doxyfile)

                doxygen_generated_html_path = os.path.join(doxy_build_path, 'generated', 'html')
                if os.path.exists(doxygen_generated_html_path):
                    self.logger.info('Found Doxygen Generated HTML: {path}'
                                     .format(path=doxygen_generated_html_path))
                    doxy_mainpage_name = self.generate_doxymainpage(doxy_mainpage_dict=doxy_mainpage_dict,
                                                                    doxy_source_path=doxy_source_path,
                                                                    generated_html_path=doxygen_generated_html_path)

                    doxyfile, breathe_project = self.generate_doxyfile(repo_root=self.repo_root,
                                                                       name=depend.name,
                                                                       doxy_input_paths=doxy_input_paths,
                                                                       doxy_source_path=doxy_source_path,
                                                                       doxy_build_path=doxy_build_path,
                                                                       doxy_mainpage_name=doxy_mainpage_name,
                                                                       doxy_template=self.doxy_template,
                                                                       doxy_extra_style_sheets=self.doxy_extra_style_sheets,
                                                                       project_logo=logo_file,
                                                                       restricted_src=self.restricted_src,
                                                                       project_title=self.project_title,
                                                                       project_version=self.project_version,
                                                                       doxy_image_path=image_path,
                                                                       project_language=self.language,
                                                                       doxypypy_script=self.doxypypy_script,
                                                                       dot_path=self.dot_path)

                    self.logger.info('Running Doxygen for: {doxy}'.format(doxy=doxyfile))
                    self.run_doxygen(doxyfile=doxyfile)
                else:
                    self.logger.info('Could Not Find Doxygen Generated HTML: {path}'
                                     .format(path=doxygen_generated_html_path))
                    doxygen_generated_html_path = None

                sphinx_source_path, sphinx_build_path, \
                    sphinx_static_path = self.set_sphinx_paths(doc_root=depend.docs_dir,
                                                               sphinx_version=self.sphinx_version,
                                                               sphinx_static='_static',
                                                               clean=self.doc_clean)

                self.preprocess_sphinxconf(breathe_project=breathe_project,
                                           src_code_path=src_code_path,
                                           sphinx_source_path=sphinx_source_path,
                                           sphinx_build_path=sphinx_build_path,
                                           restricted_src=self.restricted_src,
                                           project_title=self.project_title,
                                           project_version=self.project_version,
                                           project_author=self.project_author,
                                           project_org=self.project_org,
                                           release_uri=release_uri,
                                           issue_uri=issue_uri,
                                           releases_document_name=releases_document_name,
                                           style_sheets=self.doxy_extra_style_sheets,
                                           image_path=image_path,
                                           source_path=source_path,
                                           static_path=sphinx_static_path,
                                           project_logo=logo_file,
                                           toc_depth=4,
                                           sphinx_conf_template=self.sphinx_conf_template,
                                           sphinx_make_template=self.sphinx_make_template,
                                           doxygen_html_path=doxygen_generated_html_path,
                                           project_language=self.language,
                                           header=header)

                self.run_sphinx(source_path=sphinx_source_path,
                                build_path=sphinx_build_path,
                                builder='html',
                                use_make=False)

            elif include_dependencies:
                depend_settings = self.load_settings_from_yaml(settings_root=depend.settings_dir)

                try:
                    doxy_mainpage_dict = depend_settings.doxy_mainpage
                except (AttributeError, KeyError) as e:
                    doxy_mainpage_dict = dict()

                self.source_code_publication_msg(name=depend.name,
                                                 restricted_flag=depend_settings.restricted_src)
                self.logger.info('Processing Documentation for Dependency: {name}'.format(name=depend.name))
                self.set_doxy_paths(doc_root=depend.docs_dir,
                                    doxy_version=self.doxy_version,
                                    clean=depend_settings.doc_clean)

                self.set_logo(doc_root=depend_settings.docs_dir,
                              logo_path=depend_settings.logo_path,
                              logo_name=depend_settings.logo_name)

                image_path = self.set_image_path(doc_root=depend.docs_dir,
                                                 image_path=depend_settings.image_path)

                source_path = self.set_source_path(doc_root=depend.docs_dir,
                                                   source_path=depend_settings.source_path)

                doxy_input_paths = [depend.src_dir, depend.scripts_dir]

                doxyfile, breathe_project = self.generate_doxyfile(repo_root=self.repo_root,
                                                                   name=depend.name,
                                                                   doxy_input_paths=doxy_input_paths,
                                                                   doxy_source_path=doxy_source_path,
                                                                   doxy_build_path=doxy_build_path,
                                                                   doxy_template=self.doxy_template,
                                                                   doxy_extra_style_sheets=self.doxy_extra_style_sheets,
                                                                   project_logo=logo_file,
                                                                   source_path=source_path,
                                                                   restricted_src=depend_settings.restricted_src,
                                                                   project_title=depend_settings.project_title,
                                                                   project_version=depend_settings.project_version,
                                                                   doxy_image_path=image_path,
                                                                   project_language=depend_settings.language,
                                                                   doxypypy_script=self.doxypypy_script,
                                                                   dot_path=self.dot_path)

                self.logger.info('Running Doxygen for: {doxy}'.format(doxy=doxyfile))
                self.run_doxygen(doxyfile=doxyfile)

                doxygen_generated_html_path = os.path.join(doxy_build_path, 'generated', 'html')
                if os.path.exists(doxygen_generated_html_path):
                    self.logger.info('Found Doxygen Generated HTML: {path}'
                                     .format(path=doxygen_generated_html_path))

                    doxy_mainpage_name = self.generate_doxymainpage(doxy_mainpage_dict=doxy_mainpage_dict,
                                                                    doxy_source_path=doxy_source_path,
                                                                    generated_html_path=doxygen_generated_html_path)

                    doxyfile, breathe_project = self.generate_doxyfile(repo_root=self.repo_root,
                                                                       name=depend.name,
                                                                       doxy_input_paths=doxy_input_paths,
                                                                       doxy_source_path=doxy_source_path,
                                                                       doxy_build_path=doxy_build_path,
                                                                       doxy_mainpage_name=doxy_mainpage_name,
                                                                       doxy_template=self.doxy_template,
                                                                       doxy_extra_style_sheets=self.doxy_extra_style_sheets,
                                                                       project_logo=logo_file,
                                                                       restricted_src=self.restricted_src,
                                                                       project_title=self.project_title,
                                                                       project_version=self.project_version,
                                                                       doxy_image_path=image_path,
                                                                       project_language=self.language,
                                                                       doxypypy_script=self.doxypypy_script,
                                                                       dot_path=self.dot_path)

                    self.logger.info('Running Doxygen for: {doxy}'.format(doxy=doxyfile))
                    self.run_doxygen(doxyfile=doxyfile)
                else:
                    self.logger.info('Could Not Find Doxygen Generated HTML: {path}'
                                     .format(path=doxygen_generated_html_path))
                    doxygen_generated_html_path = None

                sphinx_source_path, sphinx_build_path, \
                    sphinx_static_path = self.set_sphinx_paths(doc_root=depend.docs_dir,
                                                               sphinx_version=self.sphinx_version,
                                                               sphinx_static='_static',
                                                               clean=self.doc_clean)

                self.preprocess_sphinxconf(breathe_project=breathe_project,
                                           src_code_path=depend.src_dir,
                                           sphinx_source_path=sphinx_source_path,
                                           sphinx_build_path=sphinx_build_path,
                                           restricted_src=self.restricted_src,
                                           project_title=self.project_title,
                                           project_version=self.project_version,
                                           project_author=self.project_author,
                                           project_org=self.project_org,
                                           release_uri=release_uri,
                                           issue_uri=issue_uri,
                                           releases_document_name=releases_document_name,
                                           style_sheets=self.doxy_extra_style_sheets,
                                           image_path=image_path,
                                           source_path=source_path,
                                           static_path=sphinx_static_path,
                                           project_logo=logo_file,
                                           toc_depth=4,
                                           sphinx_conf_template=self.sphinx_conf_template,
                                           sphinx_make_template=self.sphinx_make_template,
                                           doxygen_html_path=doxygen_generated_html_path,
                                           project_language=self.language,
                                           header=header)

                self.run_sphinx(source_path=sphinx_source_path,
                                build_path=sphinx_build_path,
                                builder='html',
                                use_make=False)

    def __repr__(self):
        return "{self.__class__.__name__}(log_to_console={self.log_to_console})".format(self=self)

    def __str__(self):
        return "{} is a {self.__class__.__name__} object".format(__name__, self=self)

    def source_code_publication_msg(self, **kwargs):
        """ Sends a Critical Warning to the Console if Source Code Will be Published in the Documentation

        Keyword Args:
            **name (str, optional): Name of project which is publishing source code in the
                generated documentation. Default value: ``''``
            **restricted_flag(bool, optional): Flag to determine if source-code is being published in the
                generated documentation. Default value: ``True``

        Returns:
            None

        """
        name = funcs.get_kwarg('name', kwargs, '')
        restricted_flag = funcs.get_kwarg('restricted_flag', kwargs, True)

        if not restricted_flag:
            self.logger.critical('Publishing Source Code in Documentation for: {name}'
                                 .format(name=name))
        else:
            self.logger.info('Source Code NOT Published in Documentation for: {name}'
                             .format(name=name))

    def load_settings_from_yaml(self, **kwargs):
        """Loads a ``settings.yml`` YAML file and returns the 'documentation' key.

        Keyword Args:
            **settings_root (str, optional): Path to the project's root ``settings`` directory.
                Default value: ``''``
            **settings_filename (str, optional): Name of settings file to use.
                Default value: ``default_settings.yml``

        Returns:
            None

        """
        settings_root = funcs.get_kwarg('settings_root', kwargs, '')
        settings_filename = funcs.get_kwarg('settings_filename', kwargs, 'default_settings.yml')

        settings_filename = os.path.join(settings_root, settings_filename)
        if os.path.isfile(settings_filename):
            with open(settings_filename, 'r') as ymlfile:
                settings = yaml.load(ymlfile)
                self.logger.info('Loading Settings from: {settings}'
                                 .format(settings=settings_filename))
        else:
            self.logger.error('Can Not Load Default Settings File: {filename}'
                              .format(filename=settings_filename))
            log.errorexit(self.logger)
        try:
            return settings['documentation']
        except KeyError:
            self.logger.error("Can Not Load 'documentation' Settings from File: {filename}"
                              .format(filename=settings_filename))
            log.errorexit(self.logger)

    def set_logo(self, **kwargs):
        """Sets the full-path to the logo to use in generated documentation.

        Keyword Args:
            **doc_root (str, optional): Path to projects root ``docs`` directory.
                Default value: ``''``
            **logo_path (str, optional): Relative Path, from ``doc_root``, to the project's logo directory.
                Default value: ``''``
            **logo_name (str, optional): Name of logo file to use.
                Default value: ``''``

        Returns:
            str: the full-path to the logo if found on file-system.

            or:
                bool: ``False`` if not found.

        """
        doc_root = funcs.get_kwarg('doc_root', kwargs, '')
        logo_path = funcs.get_kwarg('logo_path', kwargs, '')
        logo_name = funcs.get_kwarg('logo_name', kwargs, '')

        logo = os.path.abspath(os.path.join(doc_root, logo_path, logo_name))
        if os.path.isfile(logo):
            self.logger.info('Using Logo: {logo}'
                             .format(logo=logo))
            return logo
        else:
            self.logger.warning('Logo Missing From File-System: {logo}'
                                .format(logo=logo))
            return False

    def set_image_path(self, **kwargs):
        """Sets the full-path to the images directory to use in generated documentation.

        Keyword Args:
            **doc_root (str, optional): Path to projects root ``docs`` directory.
                Default value: ``''``
            **image_path (str, optional): Relative Path, from ``doc_root``, to the project's image directory.
                Default value: ``''``

        Returns:
            str: the full-path to the images directory if found on file-system.

            or:
                bool: ``False`` if not found.

        """
        doc_root = funcs.get_kwarg('doc_root', kwargs, '')
        image_path = funcs.get_kwarg('image_path', kwargs, '')
        image_path = os.path.abspath(os.path.join(doc_root, image_path))

        if os.path.exists(image_path):
            self.logger.info('Using Image Path: {path}'
                             .format(path=image_path))
            return image_path
        else:
            self.logger.warning('Image Path Missing From File-System: {path}'
                                .format(path=image_path))
            return False

    def set_source_path(self, **kwargs):
        """Sets the full-path to the source directory to use in generated documentation.

        Keyword Args:
            **doc_root (str, optional): Path to projects root ``docs`` directory.
                Default value: ``''``
            **source_path (str, optional): Relative Path, from ``doc_root``, to the project's
                source_path directory. Default value: ``''``

        Returns:
            str: the full-path to the source directory if found on file-system

            or:
                bool: ``False`` if not found.

        """
        doc_root = funcs.get_kwarg('doc_root', kwargs, '')
        source_path = funcs.get_kwarg('source_path', kwargs, '')
        source_path = os.path.abspath(os.path.join(doc_root, source_path))

        if os.path.exists(source_path):
            self.logger.info('Using Source Path: {path}'
                             .format(path=source_path))
            return source_path
        else:
            self.logger.warning('Source Path Missing From File-System: {path}'
                                .format(path=source_path))
            return False

    def set_doxy_paths(self, **kwargs):
        """Sets the ``doxygen`` source and build paths.

        .. note::

           The keyword argument ``doxy_version`` should be available on the host system and this value must be
           included in the :ref:`config_documentation` :ref:`doxygen_config` :ref:`doxygen_supported_tools`
           within the configuration file (see :ref:`configuration`).

        Keyword Args:
            **doc_root (str, optional): Path to projects root ``docs`` directory.
                Default value: ``''``
            **doxy_version (str, optional): version number of ``doxygen`` - determines the build path.
                Default value: ``''``
            **clean (bool, optional): if set to ``True``, removes all existing files from the build directory.
                Default value: ``False``

        Returns:
            tuple: tuple containing:
                * str: Full path of ``doxygen`` source location.
                * str: Full path of ``doxygen`` build location.

        """
        doc_root = funcs.get_kwarg('doc_root', kwargs, '')
        doxy_version = funcs.get_kwarg('doxy_version', kwargs, '')
        clean = funcs.get_kwarg('clean', kwargs, False)

        doxy_source = os.path.join(doc_root, 'doxygen', 'source')
        if not os.path.exists(doxy_source):
            os.makedirs(doxy_source)
            self.logger.info('Creating Doxygen Source Path: {path}'
                             .format(path=doxy_source))
        else:
            self.logger.warning('Doxygen Source Path Exists: {path}'
                                .format(path=doxy_source))

        doxy_build = os.path.join(doc_root, 'doxygen', doxy_version, 'build')
        if not os.path.exists(doxy_build):
            os.makedirs(doxy_build)
            self.logger.info('Creating Doxygen Build Path: {path}'
                             .format(path=doxy_build))
        elif clean:
            self.logger.info('Cleaning Doxygen Build Path: {path}'.
                             format(path=doxy_build))
            shutil.rmtree(doxy_build)
            os.makedirs(doxy_build)
        else:
            self.logger.warning('Doxygen Build Path Exists: {path}'
                                .format(path=doxy_build))

        return doxy_source, doxy_build

    def set_sphinx_paths(self, **kwargs):
        """Sets the ``sphinx`` source, build and static paths.

        .. note::

           The keyword argument ``sphinx_version`` should be available on the host system and this value must
           be included in the :ref:`config_documentation` :ref:`sphinx_config` :ref:`sphinx_supported_tools`
           within the configuration file (see :ref:`configuration`).

        Keyword Args:
            **doc_root (str, optional): Path to projects root ``docs`` directory.
                Default value: ``''``
            **sphinx_version (str, optional): version number of ``sphinx`` to use - determines the build path.
                Default value: ``''``
            **sphinx_static (str, optional): ``sphinx`` static directory name. Where existing source files
                are copied to in order to be included in the generated documentation.
                Default value: ``'_static'``
            **clean (bool, optional): if set to ``True``, removes all existing files from the build directory.
                Default value: ``False``

        Returns:
            tuple: tuple containing:
                * str: Full path of ``sphinx`` source location.
                * str: Full path of ``sphinx`` build location.
                * str: Full path of ``sphinx`` static location.

        """
        doc_root = funcs.get_kwarg('doc_root', kwargs, '')
        sphinx_version = funcs.get_kwarg('sphinx_version', kwargs, '')
        sphinx_static = funcs.get_kwarg('sphinx_static', kwargs, '_static')
        clean = funcs.get_kwarg('clean', kwargs, False)

        sphinx_source = os.path.join(doc_root, 'sphinx', 'source')
        if not os.path.exists(sphinx_source):
            os.makedirs(sphinx_source)
            self.logger.info('Creating Sphinx Source Path: {path}'
                             .format(path=sphinx_source))
        else:
            self.logger.info('Sphinx Source Path Exists: {path}'
                             .format(path=sphinx_source))

        sphinx_static_path = os.path.join(sphinx_source, sphinx_static)
        if not os.path.exists(sphinx_static_path):
            os.makedirs(sphinx_static_path)
            self.logger.info('Creating Sphinx Static Path: {path}'
                             .format(path=sphinx_static_path))
        elif clean:
            self.logger.info('Cleaning Sphinx Static Path: {path}'
                             .format(path=sphinx_static_path))
            shutil.rmtree(sphinx_static_path)
            os.makedirs(sphinx_static_path)
        else:
            self.logger.warning('Sphinx Static Path Exists: {path}'
                                .format(path=sphinx_static_path))

        sphinx_build = os.path.join(doc_root, 'sphinx', sphinx_version, 'build')
        if not os.path.exists(sphinx_build):
            os.makedirs(sphinx_build)
            self.logger.info('Creating Sphinx Build Path: {path}'
                             .format(path=sphinx_build))
        elif clean:
            self.logger.info('Cleaning Sphinx Build Path: {path}'
                             .format(path=sphinx_build))
            shutil.rmtree(sphinx_build)
            os.makedirs(sphinx_build)
        else:
            self.logger.warning('Sphinx Build Path Exists: {path}'
                                .format(path=sphinx_build))

        return sphinx_source, sphinx_build, sphinx_static_path

    def generate_doxymainpage(self, **kwargs):
        """Generates the ``doxygen`` Main Page to act as link between ``doxygen`` and ``sphinx`` documentation

        Parses ``generated_html_path`` looking for HTML files where the filename ends with ``htmlpagefilter``
        and added the file to the generated mainpage, along with the pages title extracted from the HTML page.

        Keyword Args:
            **doxy_mainpage_dict (dict, optional): Dictionary of mainpage settings defining the structure and
                configuration of the mainpage to generate. Default value: ``dict()``
            **doxy_source_path (str, optional): Full path to the ``doxygen`` source path.
                Default value: ``None``
            **generated_html_path (str, optional): Full path to the generated ``doxygen`` generated HTML.
                Default value: ``None``
            **doxy_mainpage_title (str, optional): Tile of the generated mainpage which is referenced in
                the generated documentation.
                Default value: ``'Doxygen Index``
            **htmlpagefilter (str, optional): The suffix of the HTML pages to add to the generated mainpage
                (excluding the file extension).
                Default value: ``'page``

        Returns:
            str: Name of the generated main page

        """
        doxy_mainpage_dict = funcs.get_kwarg('doxy_mainpage_dict', kwargs, dict())
        doxy_source_path = funcs.get_kwarg('doxy_source_path', kwargs, None)
        generated_html_path = funcs.get_kwarg('generated_html_path', kwargs, None)
        doxy_mainpage_title = funcs.get_kwarg('doxy_mainpage_title', kwargs, 'Doxygen Index')
        htmlpagefilter = funcs.get_kwarg('htmlpagefilter', kwargs, 'page')

        try:
            doxy_mainpage_name = doxy_mainpage_dict['mainpage_name']
            self.logger.info('Doxygen Main Page Name: {name}'
                                 .format(name=doxy_mainpage_name))
        except KeyError:
            doxy_mainpage_name = 'README.md'
            self.logger.critical('Doxygen Main Page Name Not Defined defaulting to: {name}'
                                 .format(name=doxy_mainpage_name))

        doxy_mainpage_links_name = os.path.splitext(doxy_mainpage_name)[0].lower() + '_links.md'

        try:
            doxy_autostruct = doxy_mainpage_dict['autostruct']
        except KeyError:
            doxy_autostruct = list()
            self.logger.info('No Additional Content Will Added to Doxygen Main Page when Generating: {name}'
                             .format(name=doxy_mainpage_name))

        try:
            doxy_autogen_pagelinks = doxy_mainpage_dict['autogen_pagelinks']
            if doxy_autogen_pagelinks:
                self.logger.info('Doxygen Main Page Links Will Auto-Generate into: {name}'
                                 .format(name=doxy_mainpage_links_name))
                if doxy_mainpage_links_name not in doxy_autostruct:
                    doxy_autostruct.append(doxy_mainpage_links_name)

                mainpage_links_contents = list()
                htmlfiles = list()
                for dirpath, dirnames, filenames in os.walk(generated_html_path):
                    htmlfiles.extend(filenames)
                    break

                filteredhtmlfiles = [f for f in htmlfiles if os.path.splitext(f)[0].endswith(htmlpagefilter)]
                for pagelink in filteredhtmlfiles:
                    page = lxml.html.parse(os.path.join(generated_html_path, pagelink))
                    title = page.find(".//title").text
                    mainpage_links_contents.append('* \subpage {pagelink} "{title}"'
                                                   .format(pagelink=os.path.splitext(pagelink)[0],
                                                           title=title))

                doxy_mainpage_links_name_path = os.path.join(doxy_source_path, doxy_mainpage_links_name)
                self.logger.info('Generating: {f}'.format(f=doxy_mainpage_links_name_path))
                funcs.writefile_as_list(full_path=doxy_mainpage_links_name_path,
                                        contents=mainpage_links_contents)

        except KeyError:
            doxy_autogen_pagelinks = False
            self.logger.critical('Doxygen Main Page Auto Generate Page Links Not Defined defaulting to: {bool}'
                                 .format(bool=doxy_autogen_pagelinks))

        doxy_mainpage_contents = list()
        doxy_mainpage_contents.append('@mainpage {title}'.format(title=doxy_mainpage_title))
        doxy_mainpage_contents.append('')

        if doxy_autostruct:
            for item in doxy_autostruct:
                item_path = os.path.abspath(os.path.join(doxy_source_path, item))
                if os.path.isfile(item_path):
                    self.logger.info('\tProcessing: {path}'.format(path=item_path))
                    with open(item_path) as mdfile:
                        doxy_mainpage_contents.extend(mdfile.read().splitlines())
                    doxy_mainpage_contents.append('- - -')
                else:
                    self.logger.warning('\tSkipping:   {path}'.format(path=item_path))

        doxy_md_path = os.path.abspath(os.path.join(doxy_source_path, doxy_mainpage_name))
        self.logger.info('Generating: {f}'.format(f=doxy_md_path))
        funcs.writefile_as_list(full_path=doxy_md_path, contents=doxy_mainpage_contents)

        return doxy_mainpage_name

    def generate_doxyfile(self, **kwargs):
        """Generate the ``doxygen`` ``.doxyfile`` from project derived values and template.

        .. warning::

           ``EXAMPLE_PATH`` is set with fixed locations and should be modified to be defined in project
           ``settings.yml`` YAML file.

        Keyword Args:
            **repo_root (str, optional): Full resolved path defined by ``$REPO_ROOT``
                Default value: ``''``
            **name (str, optional): The name of the ``.doxyfile`` to generate.
                Default value: ``''``
            **doxy_input_paths (list of str, optional): List of paths to include as input sources for
                the generation of documentation. Default value: ``list()``
            **doxy_source_path (str, optional): Path to ``doxygen`` source directory which includes
                common documentation files (``*.md``) to include in generated documentation.
                Default value: ``''``
            **doxy_build_path (str, optional): Full path where to build documentation. Default value: ``''``
            **doxy_mainpage_name (str, optional): Name of the mainpage to use as ``index.html`` in
                generated HTML documentation. Default value: ``'README.md'``
            **doxy_template (str, optional): Full path of template file to use for generic ``.doxyfile``
                configuration options. Default value: ``''``
            **doxy_extra_style_sheets (str, optional): Extra CSS style sheets used in the generation of
                HTML pages. Default value: ``''``
            **image_path (str, optional): Full path of images to include in generated documentation.
                Default value: ``False``
            **restricted_src (bool, optional): If set ``True`` stops source code from being published in the
                generated documentation. Default value: ``True``
            **project_title (str, optional): The project title used in the generated documentation.
                Default value: ``''``
            **project_version (str, optional): The project version number, in the form: ``YYYY.NN``
                used in the generated documentation. Default value: ``''``
            **project_logo (bool, optional): Full path to the logo to use in the generated documentation.
                Default value: ``False``
            **project_language (str, optional): The language of the project being generated, used to optimise
                the output of the generated documentation. Default value: ``''``
            **doxypypy_script (str, optional): Full path of ``doxypypy.py`` for parsing ``python`` code in
                ``doxygen``. ``sphinx`` is preferred over this option. Default value: ``''``
            **dot_path (str, optional): Full path to ``dot`` for using ``graphviz`` to generate
                diagrams in generated documentation. Default value: ``''``
        Returns:
            tuple: tuple containing:
                * str: Full path of the generated ``doxyfile``
                * str: Full path of the generated ``xml`` to be used by ``breathe`` to bridge ``doxygen`` and
                  ``sphinx`` generated documentation.

            or:
                int: ``-1`` on failure.

        """
        repo_root = funcs.get_kwarg('repo_root', kwargs, '')
        name = funcs.get_kwarg('name', kwargs, '')
        doxy_input_paths = funcs.get_kwarg('doxy_input_paths', kwargs, list())
        doxy_source_path = funcs.get_kwarg('doxy_source_path', kwargs, '')
        doxy_build_path = funcs.get_kwarg('doxy_build_path', kwargs, '')
        doxy_mainpage_name = funcs.get_kwarg('doxy_mainpage_name', kwargs, 'README.md')
        doxy_template = funcs.get_kwarg('doxy_template', kwargs, '')
        doxy_extra_style_sheets = funcs.get_kwarg('doxy_extra_style_sheets', kwargs, '')
        image_path = funcs.get_kwarg('doxy_image_path', kwargs, False)
        restricted_src = funcs.get_kwarg('restricted_src', kwargs, True)
        project_title = funcs.get_kwarg('project_title', kwargs, '')
        project_version = funcs.get_kwarg('project_version', kwargs, '')
        project_logo = funcs.get_kwarg('project_logo', kwargs, False)
        project_language = funcs.get_kwarg('project_language', kwargs, '')
        doxypypy_script = funcs.get_kwarg('doxypypy_script', kwargs, '')
        dot_path = funcs.get_kwarg('dot_path', kwargs, '')

        if os.path.isfile(doxy_template):
            with open(doxy_template) as doxyfile:
                doxy_template_contents = doxyfile.read()
        else:
            self.logger.critical('Template {template} Does Not Exist on File System'
                                 .format(template=doxy_template))
            return -1

        doxy_settings_header_start = "# Automatically Generated Settings (DO NOT MODIFY)"
        doxy_sectbreak = "#" * 80
        doxy_project_name = "PROJECT_NAME = "
        doxy_project_number = "PROJECT_NUMBER = "
        doxy_project_logo = "PROJECT_LOGO = "
        doxy_project_output_dir = "OUTPUT_DIRECTORY = "
        doxy_strip_from_path = "STRIP_FROM_PATH = "
        doxy_warn_logfile = "WARN_LOGFILE = "
        doxy_md_path = os.path.abspath(os.path.join(doxy_source_path, doxy_mainpage_name))
        if os.path.isfile(doxy_md_path):
            self.logger.info('Using Doxygen MainPage File: {path}'
                             .format(path=doxy_md_path))
            doxy_input = "INPUT = {mainpage} ".format(mainpage=doxy_md_path)
            doxy_use_mdfile_as_mainpage = "USE_MDFILE_AS_MAINPAGE = {mainpage}".format(mainpage=doxy_md_path)
        else:
            self.logger.warning('Cannot Find Doxygen MainPage File: {path}'
                                .format(path=doxy_md_path))
            doxy_input = "INPUT = "
            doxy_use_mdfile_as_mainpage = ""

        doxy_input_list = list()
        doxy_example_path = "EXAMPLE_PATH = "
        doxy_image_path = "IMAGE_PATH = "
        doxy_have_dot = "HAVE_DOT = "
        doxy_dot_path = "DOT_PATH = "
        doxy_html_extra_stylesheet = "HTML_EXTRA_STYLESHEET = "
        doxy_verbatim_headers = "VERBATIM_HEADERS = "
        doxy_source_browser = "SOURCE_BROWSER = "
        doxy_settings_header_end = "# The following Settings are Copied from Template File:"
        doxy_template_location = "# {template}".format(template=doxy_template)

        doxy_input_filter = "INPUT_FILTER = "
        # Language Dependent Settings:
        doxy_opt_output_vhdl = "OPTIMIZE_OUTPUT_VHDL = "
        doxy_opt_output_java = "OPTIMIZE_OUTPUT_JAVA = "
        doxy_filter_patterns = "FILTER_PATTERNS = "

        # Restrict Source Code in Documentation:
        if restricted_src:
            doxy_verbatim_headers += "NO"
            doxy_source_browser += "NO"
        else:
            doxy_verbatim_headers += "YES"
            doxy_source_browser += "YES"

        doxy_project_name = doxy_project_name + '"' + str(project_title) + '"'
        doxy_project_number = doxy_project_number + '"' + str(project_version) + '"'

        # Project Logo
        if project_logo:
            doxy_project_logo = doxy_project_logo + project_logo
        else:
            self.logger.warning('PROJECT_LOGO Not Set')

        # Image Path
        if image_path:
            doxy_image_path += image_path
        else:
            logger.warning('IMAGE_PATH Not Set')

        # and create log and generated folders:
        log_path = os.path.join(doxy_build_path, 'log', 'log.txt')
        output_dir = os.path.join(doxy_build_path, 'generated')
        breathe_project = os.path.join(output_dir, 'xml')
        doxy_project_output_dir = doxy_project_output_dir + output_dir
        doxy_warn_logfile = doxy_warn_logfile + log_path

        for path in doxy_input_paths:
            doxy_input_list.append(path)

        # Strip from Path
        doxy_strip_from_path = doxy_strip_from_path + repo_root

        # Input Paths:
        if project_language == 'python':
            doxy_opt_output_java += "YES"
            doxy_opt_output_vhdl += "NO"
            doxy_filter_patterns = (doxy_filter_patterns + "*.py="
                                    + doxypypy_script)
            doxy_input_list = self._parse_input_list(paths_list=doxy_input_paths,
                                                     term='python')
        elif project_language == 'vhdl':
            doxy_opt_output_java += "NO"
            doxy_opt_output_vhdl += "YES"
            doxy_input_list = self._parse_input_list(paths_list=doxy_input_paths,
                                                     term='vhdl')

        doxy_example_list = self._parse_input_list(paths_list=doxy_input_paths,
                                                   term='html')
        doxy_input_string = ''
        for inc_path in doxy_input_list:
            # Don't Add Examples to Source Code Input List...
            if inc_path not in doxy_example_list:
                doxy_input_string = doxy_input_string + inc_path + ' '
        doxy_input += doxy_input_string

        # Example Path:
        doxy_example_string = ''
        for inc_path in doxy_example_list:
            doxy_example_string = doxy_example_string + inc_path + ' '
        doxy_example_path += doxy_example_string

        # DOT Handling
        doxy_have_dot += "YES"
        doxy_dot_path += dot_path

        # Get Extra Stylesheet(s)
        if isinstance(doxy_extra_style_sheets, (list,)):
            extra_stylesheet = ''
            for style in doxy_extra_style_sheets:
                extra_stylesheet = extra_stylesheet + style + ' '
        else:
            extra_stylesheet = doxy_extra_style_sheets

        doxy_html_extra_stylesheet += extra_stylesheet

        settings_doxyfile = [doxy_sectbreak,
                             doxy_settings_header_start,
                             doxy_sectbreak,
                             doxy_project_name,
                             doxy_project_number,
                             doxy_project_logo,
                             doxy_image_path,
                             doxy_strip_from_path,
                             doxy_input,
                             doxy_example_path,
                             doxy_project_output_dir,
                             doxy_warn_logfile,
                             doxy_html_extra_stylesheet,
                             doxy_have_dot, doxy_dot_path,
                             doxy_opt_output_vhdl,
                             doxy_opt_output_java,
                             doxy_filter_patterns,
                             doxy_input_filter,
                             doxy_verbatim_headers,
                             doxy_source_browser,
                             doxy_use_mdfile_as_mainpage,
                             doxy_sectbreak,
                             doxy_settings_header_end,
                             doxy_template_location,
                             doxy_sectbreak]

        for line in doxy_template_contents.split('\n'):
            settings_doxyfile.append(line)

        doxyfile = os.path.join(doxy_source_path, name + '.doxyfile')
        self.logger.info('Generating: {f}'.format(f=doxyfile))
        funcs.writefile_as_list(full_path=doxyfile, contents=settings_doxyfile)

        return doxyfile, breathe_project

    def _parse_input_list(self, **kwargs):

        paths_list = funcs.get_kwarg('paths_list', kwargs, list())
        term = funcs.get_kwarg('term', kwargs, '')

        parsed_list = list()

        for p in paths_list:
            for root, subdirs, files in os.walk(p):
                for subdir in subdirs:
                    if term in root or term in subdir:
                        parsed_list.append(os.path.join(root, subdir))

        for p in parsed_list:
            self.logger.debug('Found: {path}'
                              .format(path=p))

        return parsed_list

    def run_doxygen(self, **kwargs):
        """``doxygen`` runner

            Keyword Args:
                **doxyfile (str, optional): The full path of ``doxygen`` ``.doxyfile`` used to generate
                    documentation. Default value: ``''``
                **doxy_bin (str, optional): The name of the bin to use to execute ``doxygen``
                    Default value: ``'doxygen'``

            Returns:
                None
            """
        doxyfile = funcs.get_kwarg('doxyfile', kwargs, '')
        doxy_bin = funcs.get_kwarg('doxy_bin', kwargs, 'doxygen')
        subprocess.call([doxy_bin, doxyfile])

    def run_sphinx(self, **kwargs):
        """``sphinx`` runner

        Keyword Args:
            **sphinx_source_path (str, optional): The path of ``sphinx`` source to generate documentation.
                Default value: ``''``
            **sphinx_build_path (str, optional): The path where ``sphinx`` will generate the documentation.
                Default value: ``''``
            **builder (str, optional): builder to invoke.
                Valid values: ``html``. Default value: ``html``
            **use_make (bool ,optional): Use the `Makefile` to generate documentation instead of executing
                directly. Default value: ``False``

        Returns:
            int: ``0`` on Success

        """
        source_path = funcs.get_kwarg('source_path', kwargs, '')
        build_path = funcs.get_kwarg('build_path', kwargs, '')
        builder = funcs.get_kwarg('builder', kwargs, 'html')
        use_make = funcs.get_kwarg('use_make', kwargs, False)

        supported_builders = ['html', 'latex']
        if builder not in supported_builders:
            self.logger.warning('Unsupported Sphinx Builder: {builder}'
                                .format(builder=builder))
            builder = supported_builders[0]
            self.logger.warning('\t Defaulting to: {builder}'
                                .format(builder=builder))

        if use_make:
            self.logger.info('Using Makefile to Build Documentation from Sphinx')
            from_dir = os.getcwd()
            makepath = os.path.abspath(os.path.join(source_path, '..'))
            os.chdir(makepath)
            subprocess.call(['make', builder])
            os.chdir(from_dir)
            return 0

        else:
            subprocess.call(['sphinx-build', '-b', builder, source_path, build_path])
            return 0

    def preprocess_sphinxconf(self, **kwargs):
        """Preprocessing for the ``sphinx`` ``conf.py`` File based on the current settings

        Checks locations of directories and files exist and copies relevant files to documentation source
        directory prior to generating the configuration file.

        Keyword Args:
            **source_path (str, optional): Documentation source path.
                Default value: ``''``

            **src_code_path (str, optional): Top-level path of source code to add to
                ``sphinx`` documentation. This path will searched recursively, directories name: ``template``
                will be added to a list to be used to add template files to the configuration.
                Default value: ``''``
            **sphinx_source_path (str, optional): The path of ``sphinx`` source code to add in the generated
                documentation. Default value: ``''``
            **sphinx_build_path (str, optional): The path where ``sphinx`` will generate the documentation.
                Default value: ``''``
            **project_name (str, optional): The project name. Default value: ``''``
            **project_version (str, optional): The projects documentation version. Default value: ``''``
            **project_release (str, optional): The project release. Default value: ``''``
            **project_author (str, optional): The project documentation's author. Default value: ``''``
            **project_org (str, optional): The project's organisation. Default value: ``''``
            **project_logo (str, optional): The name of the project logo to use in the project's documentation.
                Default value: ``False``
            **release_uri (str, optional): The URL for releases to determine the release version.
                Default value: ``False``
            **issue_uri (str, optional): The URL for releases to determine the issue reference.
                Default value: ``False``
            **releases_document_name (str or list of str, optional): The name of the Changelog used by
                ``releases``. Default value: ``False``
            **style_sheets (str, optional): Additional Style-Sheets to use when generating HTML
                documentation. Default value: ``False``
            **breathe_project (str, optional): Breathe project to use when bridging doxygen generated
                documentation with sphinx. Default value: ``False``
            **toc_depth (int, optional): The depth of the toctree used in the generated documentation.
                Default value: ``4``
            **image_path (str, optional): Path to directory of images to add to the generated
                ``sphinx`` documentation. Files in this directory will be copied to the ``static_path`` used
                by ``sphinx``. Default value: ``False``
            **source_path (str, optional): Path to directory of source files to add to the generated
                ``sphinx`` documentation. Files in this directory will be copied to the ``static_path`` used
                by ``sphinx``. Default value: ``False``
            **static_path (str, optional): Path to directory where source files will be copied for the
                generation of ``sphinx`` documentation. Default value: ``'_static'``
            **doxygen_html_path (str, optional): Path where ``doxygen`` has generated HTML documentation
                prior to generating the ``sphinx`` documentation. These pages will be copied to a 'html'
                directory in the ``sphinx`` ``static_path`` for inclusion in the generated ``sphinx``
                documentation. Default value: ``None'``
            **sphinx_conf_template (str, optional): Relative Path, from ``docflow.py``, to the ``sphinx``
                configuration file template to append to the generated configuration file.
                Default value: ``''``
            **sphinx_make_template (str, optional): Relative Path, from ``docflow.py``, to the ``sphinx``
                ``Makefile`` file template to append to the generated configuration file.
                Default value: ``''``
            **language (str, optional): Language to determine if module index is included.
                Included if set to: ``python``. Excluded if set to anything else. Default value: ``python``
            **header (str, optional): Header file to reference at the top of the generated file.
                Default value: ``_static/esdg_header.rst``

        Returns:
            None
        """
        src_code_path = funcs.get_kwarg('src_code_path', kwargs, '')
        sphinx_source_path = funcs.get_kwarg('sphinx_source_path', kwargs, '')
        sphinx_build_path = funcs.get_kwarg('sphinx_build_path', kwargs, '')
        project_title = funcs.get_kwarg('project_title', kwargs, '')
        project_version = funcs.get_kwarg('project_version', kwargs, '')
        project_author = funcs.get_kwarg('project_author', kwargs, '')
        project_org = funcs.get_kwarg('project_org', kwargs, '')
        project_logo = funcs.get_kwarg('project_logo', kwargs, False)
        release_uri = funcs.get_kwarg('release_uri', kwargs, False)
        issue_uri = funcs.get_kwarg('issue_uri', kwargs, False)
        releases_document_name = funcs.get_kwarg('releases_document_name', kwargs, False)
        style_sheets = funcs.get_kwarg('style_sheets', kwargs, False)
        breathe_project = funcs.get_kwarg('breathe_project', kwargs, '')
        toc_depth = funcs.get_kwarg('toc_depth', kwargs, 4)
        image_path = funcs.get_kwarg('image_path', kwargs, False)
        source_path = funcs.get_kwarg('source_path', kwargs, False)
        static_path = funcs.get_kwarg('static_path', kwargs, os.path.join(sphinx_source_path, '_static'))
        doxygen_html_path = funcs.get_kwarg('doxygen_html_path', kwargs, None)
        sphinx_conf_template = funcs.get_kwarg('sphinx_conf_template', kwargs, '')
        sphinx_make_template = funcs.get_kwarg('sphinx_make_template', kwargs, '')
        project_language = funcs.get_kwarg('project_language', kwargs, 'python')
        header = funcs.get_kwarg('header', kwargs, '_static/esdg_header.rst')

        src_code_path_list = list()
        if os.path.exists(src_code_path):
            self.logger.debug('Source Path Found: {path}'.format(path=src_code_path))
            for root, subpaths, filenames in os.walk(src_code_path):
                if subpaths:
                    for subpath in subpaths:
                        if 'template' in subpath or 'template' in root:
                            self.logger.debug('Skipping template... {path}'
                                              .format(path=os.path.relpath(os.path.join(root, subpath),
                                                                           sphinx_source_path)))
                        else:
                            path_to_add = os.path.relpath(os.path.join(root, subpath), sphinx_source_path)
                            src_code_path_list.append(path_to_add)
            self.logger.info('Found the Following Source Paths (Relative to Sphinx Source Path):')
            for path in src_code_path_list:
                self.logger.info('\t{path}'
                                 .format(path=path))
        else:
            self.logger.critical('Source Path Not Found: {path}'.format(path=src_code_path))

        if image_path:
            self.logger.info('Copying Images to Static Path: {path}'.format(path=static_path))
            funcs.copy_files_from_dir(image_path, static_path)

        if source_path:
            self.logger.info('Copying Sources to Static Path: {path}'.format(path=static_path))
            funcs.copy_files_from_dir(source_path, static_path)

        if project_logo:
            self.logger.info('Copying Logo: {project_logo}'.format(project_logo=project_logo))
            self.logger.info('\tto Static Path: {path}'.format(path=static_path))
            shutil.copy2(project_logo, static_path)

        if style_sheets:
            abs_css_static_path = os.path.abspath(os.path.join(static_path, 'css'))
            css_static_path = os.path.join('_static', 'css')
            if not os.path.exists(abs_css_static_path):
                self.logger.info('Creating Style Sheet Directory: {path}'
                                 .format(path=abs_css_static_path))
                os.makedirs(abs_css_static_path)
            else:
                self.logger.info('Using Existing Style Sheet Directory: {path}'
                                 .format(path=abs_css_static_path))
            css_paths = list()
            if isinstance(style_sheets, (list,)):
                for f in style_sheets:
                    self.logger.info('Copying Style Sheet: {f}'.format(f=f))
                    self.logger.info('\tto Static Path: {path}'.format(path=abs_css_static_path))
                    css_name = os.path.split(f)[1]
                    shutil.copy2(f, os.path.join(abs_css_static_path, css_name))
                    css_paths.append(os.path.join(css_static_path, css_name))
            else:
                self.logger.info('Copying Style Sheet: {style_sheets}'.format(style_sheets=style_sheets))
                self.logger.info('\tto Static Path: {path}'.format(path=abs_css_static_path))
                css_name = os.path.split(style_sheets)[1]
                shutil.copy2(style_sheets, os.path.join(abs_css_static_path, css_name))
                css_paths.append(os.path.join(css_static_path, css_name))

            for css in css_paths:
                self.logger.debug('CSS: {css}'
                                  .format(css=css))

        if not os.path.exists(breathe_project) and self.language != 'python':
            self.logger.critical('Breathe Project Missing: {breathe_project}'
                                 .format(breathe_project=breathe_project))
            self.logger.critical('\tCheck Doxygen Project Generated Successfully...')
            breathe_project = ''

        make_template_contents = funcs.readfile_as_list(full_path=sphinx_make_template)

        try:
            if os.path.exists(doxygen_html_path):
                self.logger.info('Adding Doxygen Generated HTML Files to Sphinx...')
                abs_html_static_path = os.path.abspath(os.path.join(static_path, 'html'))
                html_static_path = os.path.join('_static', 'html')
                if os.path.exists(abs_html_static_path):
                    shutil.rmtree(abs_html_static_path)
                self.logger.info('Copying Doxygen Generated HTML Files to Sphinx...')
                shutil.copytree(doxygen_html_path, abs_html_static_path)
            else:
                self.logger.info('Not Adding Doxygen Generated HTML Files')
        except TypeError:
            pass

        self.generate_sphinx_index_file(source_code_path=src_code_path,
                                        source_path=sphinx_source_path,
                                        src_code_path_list=src_code_path_list,
                                        max_depth=toc_depth,
                                        language=project_language,
                                        header=header)

        self.process_sphinx_conf_file(source_path=sphinx_source_path,
                                      src_code_path_list=src_code_path_list,
                                      project_name=project_title,
                                      project_version=project_version,
                                      project_release='',
                                      style_sheets=css_paths,
                                      project_org=project_org,
                                      project_author=project_author,
                                      project_logo=project_logo,
                                      release_uri=release_uri,
                                      issue_uri=issue_uri,
                                      releases_document_name=releases_document_name,
                                      toc_depth=toc_depth,
                                      static_path=static_path,
                                      breathe_project=breathe_project,
                                      template_file=sphinx_conf_template)

        self.process_sphinx_makefile(build_path=sphinx_build_path,
                                     make_template=make_template_contents)

    def process_sphinx_conf_file(self, **kwargs):
        """Generates ``sphinx`` ``conf.py`` File based on the current settings

        Completes options from passed values and completes the remaining file by copying the contents from
        a template file.

        Keyword Args:
            **source_path (str, optional): Documentation source path.
                Default value: ``''``
            **src_code_path_list (list of str, optional): List of source code paths to parse to add to
                ``sphinx`` documentation. Default value: ``list()``
            **conf_name (str, optional): The name of ``sphinx`` configuration file to generate.
                Default value: ``conf.py``
            **project_name (str, optional): The project name. Default value: ``''``
            **project_version (str, optional): The projects documentation version. Default value: ``''``
            **project_release (str, optional): The project release. Default value: ``''``
            **project_author (str, optional): The project documentation's author. Default value: ``''``
            **project_org (str, optional): The project's organisation. Default value: ``''``
            **project_logo (str, optional): The name of the project logo to use in the project's documentation.
                Default value: ``False``
            **release_uri (str, optional): The URL for releases to determine the release version.
                Default value: ``False``
            **issue_uri (str, optional): The URL for releases to determine the issue reference.
                Default value: ``False``
            **releases_document_name (str or list of str, optional): The name of the Changelog used by
                ``releases``. Default value: ``False``
            **style_sheets (str, optional): Additional Style-Sheets to use when generating HTML
                documentation. Default value: ``False``
            **template_file (str, optional): The name of sphinx configuration template file.
                file extension. Default value: ``''``
            **breathe_project (str, optional): Breathe project to use when bridging doxygen generated
                documentation with sphinx. Default value: ``False``
            **toc_depth (int, optional): The depth of the toctree used in the generated documentation.
                Default value: ``4``
            **indent_size (int, optional): Number of spaces in indent. Default value: ``4``

        Returns:
            None

        """
        source_path = funcs.get_kwarg('source_path', kwargs, '')
        src_code_path_list = funcs.get_kwarg('src_code_path_list', kwargs, list())
        conf_name = funcs.get_kwarg('conf_name', kwargs, 'conf.py')
        project_name = funcs.get_kwarg('project_name', kwargs, '')
        project_version = funcs.get_kwarg('project_version', kwargs, '')
        project_release = funcs.get_kwarg('project_release', kwargs, '')
        project_author = funcs.get_kwarg('project_author', kwargs, '')
        project_org = funcs.get_kwarg('project_org', kwargs, '')
        project_logo = funcs.get_kwarg('project_logo', kwargs, False)
        release_uri = funcs.get_kwarg('release_uri', kwargs, False)
        issue_uri = funcs.get_kwarg('issue_uri', kwargs, False)
        releases_document_name = funcs.get_kwarg('releases_document_name', kwargs, False)
        style_sheets = funcs.get_kwarg('style_sheets', kwargs, False)
        template_file = funcs.get_kwarg('template_file', kwargs, '')
        breathe_project = funcs.get_kwarg('breathe_project', kwargs, False)
        toc_depth = funcs.get_kwarg('toc_depth', kwargs, 4)
        static_path = funcs.get_kwarg('static_path', kwargs, '_static')
        indent_size = funcs.get_kwarg('indent_size', kwargs, 4)

        indent = '{indent}'.format(indent=' ' * indent_size)

        now = datetime.datetime.now()
        year = now.year

        breathe_project_name = 'mybreatheproject'

        conf_contents = list()
        conf_contents.append("# -*- coding: utf-8 -*-")
        conf_contents.append("#" * 80)
        conf_contents.append("# Automatically Generated Settings (DO NOT MODIFY)")
        conf_contents.append("#" * 80)

        conf_contents.append("import os")
        conf_contents.append("import sys")
        conf_contents.append("")

        for path in src_code_path_list:
            conf_contents.append("sys.path.append(os.path.abspath('{path}'))".format(path=path))
        conf_contents.append("")

        conf_contents.append("project = u'{project_name}'".format(project_name=project_name))
        conf_contents.append("copyright = u'{year}, {org}'".format(year=year, org=project_org))
        conf_contents.append("author = u'{author}'".format(author=project_author))
        conf_contents.append("version = u'{project_version}'".format(project_version=project_version))
        conf_contents.append("release = u'{project_release}'".format(project_release=project_release))
        conf_contents.append("master_doc = 'index'")
        conf_contents.append("htmlhelp_basename = '{project_name}'"
                             .format(project_name=project_name.replace(' ', '') + 'doc'))
        conf_contents.append("latex_documents = [")
        conf_contents.append("{indent}(master_doc, '{project_name_replaced}.tex', u'{project_name} Documentation',"
                             .format(indent=indent, project_name_replaced=project_name.replace(' ', ''), project_name=project_name))
        conf_contents.append("{indent} u'{author}', 'manual'),".format(indent=indent, author=project_author))
        conf_contents.append("]")
        conf_contents.append("man_pages = [")
        conf_contents.append("{indent}(master_doc, '{project_name_lower}', u'{project_name} Documentation',"
                             .format(indent=indent, project_name_lower=project_name.lower(), project_name=project_name))
        conf_contents.append("{indent} [author], 1)".format(indent=indent))
        conf_contents.append("]")
        conf_contents.append("texinfo_documents = [")
        conf_contents.append("{indent}(master_doc, '{project_name}', u'{project_name} Documentation',"
                             .format(indent=indent, project_name=project_name))
        conf_contents.append("{indent} author, '{project_name}', '',"
                             .format(indent=indent, project_name=project_name))
        conf_contents.append("{indent} 'Miscellaneous'),".format(indent=indent))
        conf_contents.append("]")
        conf_contents.append("html_theme_options = {")
        conf_contents.append("{indent}'logo_only': False,".format(indent=indent))
        conf_contents.append("{indent}'navigation_depth': {toc_depth},"
                             .format(indent=indent, toc_depth=toc_depth)),
        conf_contents.append("{indent}'collapse_navigation': False,".format(indent=indent))
        conf_contents.append("}")

        if project_logo:
            logo_file = os.path.split(project_logo)[1]
            logo_path = os.path.join(static_path, logo_file)
            if logo_path.startswith(source_path):
                rel_logo_path = logo_path[len(source_path)+1:]
                self.logger.debug('Converted Logo Path to Relative Path: {path}'.format(path=rel_logo_path))
                conf_contents.append("html_logo = '{logo}'".format(logo=rel_logo_path))
            else:
                self.logger.debug('Using Absolute Logo Path: {path}'.format(path=logo_path))
                conf_contents.append("html_logo = '{logo}'".format(logo=logo_path))

        if static_path.startswith(source_path):
            rel_static_path = static_path[len(source_path)+1:]
            self.logger.debug('Converted Static Path to Relative Path: {path}'.format(path=rel_static_path))
            conf_contents.append("html_static_path = ['{static_path}']".format(static_path=rel_static_path))
        else:
            self.logger.debug('Using Absolute Static Path: {path}'.format(path=static_path))
            conf_contents.append("html_static_path = ['{static_path}']".format(static_path=static_path))

        if breathe_project:
            conf_contents.append("breathe_projects = {{'{project}': '{xml_path}'}}"
                                 .format(project=breathe_project_name,
                                         xml_path=breathe_project))
            conf_contents.append("breathe_default_project = '{project}'"
                                 .format(project=breathe_project_name))

        if style_sheets:
            conf_contents.append("html_context = {")
            conf_contents.append("{indent}'css_files': {css_files},"
                                 .format(indent=indent, css_files=style_sheets))
            conf_contents.append("}")

        conf_contents.append("")
        conf_contents.append("releases_unstable_prehistory = True")
        if release_uri:
            if release_uri.endswith('/'):
                release_uri = release_uri + "%s"
            else:
                release_uri = release_uri + "/%s"
            self.logger.info('Using Releases URL: {release_uri}'
                             .format(release_uri=release_uri))
            conf_contents.append("releases_release_uri = '{release_uri}'"
                                 .format(release_uri=release_uri))

        if issue_uri:
            if issue_uri.endswith('/'):
                issue_uri = issue_uri + "%s"
            else:
                issue_uri = issue_uri + "/%s"
            self.logger.info('Using Issue URL: {issue_uri}'
                             .format(issue_uri=issue_uri))
            self.logger.critical('Releases Issue Not Implemented Yet...: {issue_uri}'
                                 .format(issue_uri=issue_uri))
            # conf_contents.append("releases_issue_uri = '{issue_uri}'".format(issue_uri=issue_uri))

        if releases_document_name:
            conf_contents.append("releases_document_name = '{releases_document_name}'"
                                 .format(releases_document_name=releases_document_name))
        conf_contents.append("")
        conf_contents.append("#" * 80)
        conf_contents.append("# The following Settings are Copied from Template File:")
        conf_contents.append("# {template}".format(template=template_file))
        conf_contents.append("#" * 80)

        conf_template_contents = funcs.readfile_as_list(full_path=template_file)
        for line in conf_template_contents:
            conf_contents.append(line)

        conf_file = os.path.join(source_path, conf_name)
        self.logger.info('Generating: {f}'.format(f=conf_file))
        funcs.writefile_as_list(full_path=conf_file, contents=conf_contents)

    def generate_sphinx_modules(self, ** kwargs):
        """Generates ``sphinx`` reStructuredText Module File

        Searches for ``.py`` files in locations found in ``src_code_path_list``, then passes that list to:
        :func:`docflow.ProjectDoc.generate_automodule`

        Keyword Args:
            **source_code_path (str, optional): Top-Level Path of Source-Code Location.
                Default value: ``''``
            **source_path (str, optional): Documentation source path where the ``<filename>.rst`` should be
                generated. Default value: ``''``
            **filename (str, optional): The name of module file to generate. Default value: ``modules.rst``
            **src_code_path_list (list of str, optional): List of source code paths to parse to add to
                Sphinx documentation. Default value: ``list()``
            **indent_size (int, optional): Number of spaces in indent. Default value: ``3``
            **header (str, optional): Header file to reference at the top of the generated file.
                Default value: ``_static/esdg_header.rst``

        Returns:
            None

        """
        source_code_path = funcs.get_kwarg('source_code_path', kwargs, '')
        source_path = funcs.get_kwarg('source_path', kwargs, '')
        filename = funcs.get_kwarg('filename', kwargs, 'modules.rst')
        src_code_path_list = funcs.get_kwarg('src_code_path_list', kwargs, list())
        indent_size = funcs.get_kwarg('indent_size', kwargs, 3)
        header = funcs.get_kwarg('header', kwargs, '_static/esdg_header.rst')

        fullpath = os.path.join(source_path, filename)
        module_contents = list()
        name = os.path.splitext(filename)[0]
        module_contents.append(".. include:: {header}".format(header=header))
        module_contents.append("")

        module_contents.append(".. _{name}:".format(name=name))
        module_contents.append("")
        title = self.generate_index_heading(heading_text=name.capitalize(),
                                            heading_char='#')

        for line in title:
            module_contents.append(line)
        module_contents.append("")

        if src_code_path_list:
            module_list = list()
            self.logger.info('Parsing Source Code Paths for AutoModule...')
            for path in src_code_path_list:
                automodule_exclude = ['egg-info',
                                      os.path.normpath('/build'),
                                      os.path.normpath('/dist'),
                                      os.path.normpath('/lib')]
                if not any(x in path for x in automodule_exclude):
                    abs_path = os.path.abspath(os.path.join(source_code_path, path))
                    for root, subpaths, filenames in os.walk(abs_path):
                        for f in filenames:
                            if os.path.splitext(f)[1] in ['.py']:
                                if f not in ['__init__.py', ]:  # 'funcs.py']:
                                    module_list.append(os.path.splitext(f)[0])
                        break

            for module in sorted(module_list):
                self.logger.info('\t{module}'
                                 .format(module=module))
                automodule = self.generate_automodule(module=module, indent_size=indent_size)
                for line in automodule:
                    module_contents.append(line)

        self.logger.info('Generating Sphinx Modules File: {f}'
                         .format(f=fullpath))
        funcs.writefile_as_list(full_path=fullpath, contents=module_contents)

    def generate_sphinx_index_file(self, **kwargs):
        """Generates ``sphinx`` reStructuredText Index File

        Searches for ``.rst`` and ``.md`` files in the ``source_path`` and adds them to the generated
        index file.

        If a file matching the ``index_name`` is found it is **not** added to the generated index file.

        If a html directory is found, using the ``/html/`` string, it is added **once** to the generated index
        file.

        Keyword Args:
            **source_code_path (str, optional): Top-Level Path of Source-Code Location.
                Default value: ``''``
            **source_path (str, optional): Documentation source path to parse for valid files to add to index.
                Default value: ``''``
            **static_path (str, optional): The name of the ``sphinx`` Static Path. Default value: ``_static``
            **index_name (str, optional): The name of the index file to generate.
                Default value: ``index.rst``
            **readme_name (str, optional): The name of a valid README file. Could have ``.rst`` or ``.md``
                file extension. Default value: ``README``
            **src_code_path_list (list of str, optional): List of source code paths to parse to add to
                Sphinx documentation. These paths are relative to ``source_path``.
                Default value: ``list()``
            **max_depth (int, optional): The maximum depth of the toctree. Default value: ``2``
            **indent_size (int, optional): Number of spaces in indent. Default value: ``3``
            **language (str, optional): Language to determine if module index is included.
                Included if set to: ``python``. Excluded if set to anything else. Default value: ``python``
            **header (str, optional): Common header file to use in generated documentation.
                Default value: ``'_static/esdg_header.rst'``
        Returns:
            None

        """
        source_code_path = funcs.get_kwarg('source_code_path', kwargs, '')
        source_path = funcs.get_kwarg('source_path', kwargs, '')
        static_path = funcs.get_kwarg('static_path', kwargs, '_static')
        index_name = funcs.get_kwarg('index_name', kwargs, 'index.rst')
        readme_name = funcs.get_kwarg('index_name', kwargs, 'README')
        src_code_path_list = funcs.get_kwarg('src_code_path_list', kwargs, list())
        max_depth = funcs.get_kwarg('max_depth', kwargs, 2)
        indent_size = funcs.get_kwarg('indent_size', kwargs, 3)
        language = funcs.get_kwarg('language', kwargs, 'python')
        header = funcs.get_kwarg('header', kwargs, '_static/esdg_header.rst')
        index_contents = list()

        resolved_src_code_path_list = list()
        for path in src_code_path_list:
            resolved_src_code_path_list.append(os.path.abspath(os.path.join(source_path, path)))

        for path in resolved_src_code_path_list:
            self.logger.debug('Resolved Path: {path}'.format(path=path))

        if language == 'python':
            self.generate_sphinx_modules(source_code_path=source_code_path,
                                         source_path=source_path,
                                         filename='modules.rst',
                                         src_code_path_list=resolved_src_code_path_list,
                                         indent_size=indent_size,
                                         header=header)

        doc_srcs = list()
        self.logger.info('Parsing Sphinx Documentation from: {path}'
                         .format(path=source_path))
        for ext in ['.rst', '.md']:
            self.logger.info('Searching for Documentation Sources with {ext} Extension'
                             .format(ext=ext))
            for root, subdirs, filenames in os.walk(source_path):
                for f in filenames:
                    if ext in f:
                        doc_srcs.append(os.path.join(root, f))

        include_ref = False
        filtered_srcs = list()
        static_html_flag = False
        html_id = '/html/'
        for f in doc_srcs:
            if f.startswith(source_path):
                path = os.path.splitext(f[len(source_path) + 1:])[0]
                if readme_name in path:
                    include_ref = (f[len(source_path) + 1:])
                    self.logger.info('Found README file: {readme}'
                                     .format(readme=include_ref))

                if html_id in path:
                    if not static_html_flag:
                        static_html_flag = True
                        self.logger.info('Found "{html_id}" in {static_path}: {path}'
                                         .format(html_id=html_id, static_path=static_path, path=path))
                else:
                    filtered_srcs.append(path)

        for f in filtered_srcs:
            if os.path.splitext(index_name)[0] in f:
                self.logger.info('Skipping Reference to Self: {index}'
                                 .format(index=index_name))
                filtered_srcs.remove(f)
            elif static_path in f:
                self.logger.info('Skipping Reference to {static_path} for: {f}'
                                 .format(static_path=static_path, f=f))
                filtered_srcs.remove(f)
            else:
                self.logger.debug('Found Documentation Source File: {f}'
                                  .format(f=f))

        if include_ref:
            include = self.generate_include(include_ref=include_ref,
                                            indent_size=indent_size)
            for line in include:
                index_contents.append(line)

        toctree = self.generate_toctree(max_depth=max_depth,
                                        indent_size=indent_size,
                                        srcs=filtered_srcs,
                                        reference_static_html=static_html_flag)

        for line in toctree:
            index_contents.append(line)

        indices_and_tables = self.generate_indices_and_tables(indent_size=indent_size,
                                                              language=language)

        for line in indices_and_tables:
            index_contents.append(line)

        indexfile = os.path.join(source_path, index_name)
        self.logger.info('Generating: {f}'.format(f=indexfile))
        funcs.writefile_as_list(full_path=indexfile, contents=index_contents)

    def generate_include(self, **kwargs):
        """Generates ``sphinx`` reStructuredText include directive

        Generates the include directive, in the form:

        .. code-block:: rest

           .. include:: <include_ref>


        Keyword Args:
            **include_ref (str, optional): The name of the reference to include. Default value: ``''``
            **indent_size (int, optional): Number of spaces in indent. Default value: ``3``

        Returns:
            list of str: A line-by-line list of the complete ``sphinx`` reStructuredText include directive

        """
        include_ref = funcs.get_kwarg('include_ref', kwargs, '')
        indent_size = funcs.get_kwarg('indent_size', kwargs, 3)
        indent = '{indent}'.format(indent=' ' * indent_size)
        include = list()

        include.append('.. include:: {include_ref}'.format(include_ref=include_ref))
        include.append('')

        return include

    def generate_automodule(self, **kwargs):
        """Generates ``sphinx`` reStructuredText auto-module directive

        Generates the auto-module directive, in the form:

        .. code-block:: rest

           .. automodule:: module
              :members:


        Keyword Args:
            **module (str, optional): The name of the module to auto-module. Default value: ``False``
            **indent_size (int, optional): Number of spaces in indent. Default value: ``3``

        Returns:
            list of str: A line-by-line list of the complete ``sphinx`` reStructuredText
            auto-module directive

        """
        module = funcs.get_kwarg('module', kwargs, False)
        indent_size = funcs.get_kwarg('indent_size', kwargs, 3)
        indent = '{indent}'.format(indent=' ' * indent_size)
        automodule = list()

        if module:
            automodule.append('.. automodule:: {module}'.format(module=module))
            automodule.append('{indent}:members:'.format(indent=indent))
            automodule.append('')

        return automodule

    def generate_toctree(self, **kwargs):
        """Generates ``sphinx`` reStructuredText Table-of-Contents Tree

        Generates the TOC Tree, in the form:

        .. code-block:: rest

           ===================
           Index:
           ===================

           ..toctree::
             :maxdepth: 2

             srcs[0]
             srcs[1]
             srcs[n]
             Doxygen Index <_static/html/index.html#://>

        Keyword Args:
            **max_depth (int, optional): The maximum depth of the toctree. Default value: ``2``
            **indent_size (int, optional): Number of spaces in indent. Default value: ``3``
            **srcs (list of str, optional): List of srcs to include in the toctree. Default value: ``list()``
            **reference_static_html (bool, optional): Allows the addition of a link to page external to
                ``sphinx``. Default value: ``False``
            **static_index_text (str, optional): The human readable string for the ``reference_static_html``
                link. Default value: ``Doxygen Index``
            **static_index_link (str, optional): The location of the ``reference_static_html`` link, relative
                to the ``sphinx`` top-level source path. Default value: ``_static/html/index.html``

        Returns:
            list of str: A line-by-line list of the complete ``sphinx`` reStructuredText Table-of-Contents
            Tree

        """
        max_depth = funcs.get_kwarg('max_depth', kwargs, 2)
        indent_size = funcs.get_kwarg('indent_size', kwargs, 3)
        srcs = funcs.get_kwarg('srcs', kwargs, list())
        reference_static_html = funcs.get_kwarg('reference_static_html', kwargs, False)
        static_index_text = funcs.get_kwarg('static_index_text', kwargs, 'Doxygen Index')
        static_index_link = funcs.get_kwarg('static_index_link', kwargs, '_static/html/index.html')

        indent = '{indent}'.format(indent=' ' * indent_size)
        toctree = list()

        title = self.generate_index_heading(heading_text='Index:',
                                            heading_char='=')
        for line in title:
            toctree.append(line)

        toctree.append('.. toctree::')
        toctree.append('{indent}:maxdepth: {depth}'.format(indent=indent, depth=max_depth))
        toctree.append('')

        for src in sorted(srcs):
            toctree.append('{indent}{src}'.format(indent=indent, src=src))

        if reference_static_html:
            self.logger.info('Adding Link to Sphinx Index TOC for Doxygen Generated HTML')
            # Adding #:// due to: https://stackoverflow.com/questions/27979803/external-relative-link-in-sphinx-toctree-directive
            toctree.append('{indent}{static_index_text} <{static_index_link}#://>'
                           .format(indent=indent,
                                   static_index_text=static_index_text,
                                   static_index_link=static_index_link))
            toctree.append('{indent}'.format(indent=indent))
        else:
            toctree.append('{indent}'.format(indent=indent))

        return toctree

    def generate_indices_and_tables(self, **kwargs):
        """Generates ``sphinx`` reStructuredText Indices and Tables List

        Generates the TOC Tree, in the form:

        .. code-block:: rest

           ===================
           Indices and Tables:
           ===================

           * :ref:`genindex`
           * :ref:`modindex`
           * :ref:`search`


        Keyword Args:
            **indent_size (int, optional): Number of spaces in indent. Default value: ``3``
            **language (str, optional): Language to determine if module index is included.
                Included if set to: ``python``. Excluded if set to anything else. Default value: ``python``

        Returns:
            list of str: A line-by-line list of the complete ``sphinx`` reStructuredText Indices and Tables

        """
        indent_size = funcs.get_kwarg('indent_size', kwargs, 3)
        language = funcs.get_kwarg('language', kwargs, 'python')
        indent = '{indent}'.format(indent=' ' * indent_size)
        indices = self.generate_index_heading(heading_text='Indices and Tables:',
                                              heading_char='=')

        indices.append('* :ref:`genindex`')
        if language == 'python':
            indices.append('* :ref:`modindex`')
        indices.append('* :ref:`search`')
        indices.append('')

        return indices

    def generate_index_heading(self, **kwargs):
        """Generates reStructuredText headings matching ``sphinx`` recommended formatting.

        see: `<http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_

        Keyword Args:
            **heading_text (str, optional): The heading string. Default value: ``False``
            **heading_char (str, optional): A single character representing the reStructuredText
                heading level.  Default value: ``#``

                Valid values: ``#``, ``*``, ``=``, ``-``, ``^``, ``"``

        Returns:
            list of str: A line-by-line list of the complete reStructuredText heading

        """
        heading_text = funcs.get_kwarg('heading_text', kwargs, False)
        heading_char = funcs.get_kwarg('heading_char', kwargs, '#')
        heading_len = len(heading_text)

        heading_list = list()

        if heading_text and heading_len > 0:
            if heading_char in ['#', '*']:
                heading_list.append(heading_char * heading_len)
                heading_list.append(heading_text)
                heading_list.append(heading_char * heading_len)
                heading_list.append('')
            elif heading_char in ['=', '-', '^', '"']:
                heading_list.append(heading_text)
                heading_list.append(heading_char * heading_len)
                heading_list.append('')
            else:
                self.logger.critical('Unsupported Heading Char: {char}'.format(char=heading_char))
                return ''
        else:
            return ''
        
        return heading_list

    def process_sphinx_makefile(self, **kwargs):
        """Processes a ``sphinx`` ``Makefile`` from a supplied template.

        Keyword Args:
            **build_path (str, optional): absolute path of the ``sphinx`` build location.
                Default value: ``''``
            **make_file_template (list of str): line-by-line list of ``Makefile`` template contents.
                Default value: ``''``
            **makefile (str, optional): name of the makefile. Default value: ``Makefile``

        Returns:
            None

        """
        build_path = funcs.get_kwarg('build_path', kwargs, '')
        make_template = funcs.get_kwarg('make_template', kwargs, '')
        makefile = funcs.get_kwarg('makefile', kwargs, 'Makefile')
        make_path = os.path.split(build_path)[0]

        makefile = os.path.join(make_path, makefile)
        self.logger.info('Generating: {f}'.format(f=makefile))

        if os.path.isfile(makefile):
            self.logger.warning('Overwriting: {f}'
                                .format(f=makefile))
        else:
            self.logger.info('Writing: {f}'
                             .format(f=makefile))

        with open(makefile, 'w') as f:
            for line in make_template:
                f.write('{line}\n'.format(line=line))


if __name__ == '__main__':
    logger.info("docflow {} {}"
                .format(__version__, version.revision))
    log.sect_break(logger)

    project = ProjectDoc(include_dependencies=False)

else:
    logger.info(__str__)
