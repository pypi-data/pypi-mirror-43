# -*- coding: utf8 -*-
"""

******************
``projectflow.py``
******************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``projectflow.py`` is a module to handle the project aspects of the tool-flow. This module is responsible for
generating source code (if enabled) using ``xml2vhdl``, collating all of the source-code for the project,
and adding all ``HDL`` files to a ``VUnit`` object which can then be used to perform operations relevant
to the current project.

"""
import helpers.customlogging as log
import helpers.arguments as arguments
import helpers.version as my_version
import helpers.funcs as funcs

import projectmanager as projectmanager
import xml2vhdl_iface as xml2xml_iface
import fpgavendor_iface as fpgavendor_iface
import vunit_iface as vunit_iface

import os
import shutil

logger = log.config_logger(name=__name__)
LOGLEVEL = log.LogLevelsConsts

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(0, 2, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class ProjectFlow(projectmanager.RepoFlow):
    """

    """

    def __init__(self, **kwargs):
        super(ProjectFlow, self).__init__()
        log.sect_break(self.logger)
        self.logger.info('Processing Project...')
        log.sect_break(self.logger)

        hdl_file_ext = ['.vhd', '.vhdl', '.v']

        if self.vendor == 'xilinx':
            ip_ext = ['.xci']
            constr_ext = ['.xdc']
        elif self.vendor == 'altera':
            ip_ext = ['.ip', '.qsys', '.qip']
            constr_ext = ['.sdc', '.qsf', '.tcl']

        all_ip_files = list()
        all_ip_wrapper_files = list()
        all_constr_files = list()
        ip_wrapper_files_no_dups = list()
        exclude_hdl_keywords = ['/vhd', '/verilog']
        exclude_hdl_keywords.extend(self.exclude_keywords)

        exclude_ip_keywords = ['/ip']
        exclude_ip_keywords.extend(self.exclude_keywords)

        try:
            setattr(self, 'family_mappings', self.config['fpga'][self.vendor]['family_mappings'])
        except KeyError:
            setattr(self, 'family_mappings', dict())

        if self.xml2vhdl_support:
            self.process_xml2vhdl(dependencies=self.dependencies,
                                  settings_file=self.settings_file,
                                  clean=True)
        else:
            self.logger.info('XML2VHDL Support: Disabled')

        # \todo Check when vendor_ip locations are available for processing XML2VHDL.

        log.sect_break(self.logger)
        self.logger.info('Processing EXCLUDE Terms...')
        self.logger.info('Using Exclude Keywords from: {config_file}'.format(config_file=self.config_file))
        for kw in self.exclude_keywords:
            self.logger.info('\t{kw}'.format(kw=kw))

        supported_vendors = self.config['fpga']['supported_vendors']
        self.exclude_keywords = self.add_vendor_to_exclude_terms(exclude_terms=self.exclude_keywords,
                                                                 vendor=self.vendor,
                                                                 supported_vendors=supported_vendors)

        self.logger.info('Updated Exclude Keywords with Vendors to Exclude:')
        for kw in self.exclude_keywords:
            self.logger.info('\t{kw}'.format(kw=kw))

        vunit_hdl_dict = dict()
        has_board = False

        self.logger.info('Searching for Top-Level in Project...')
        for depend in self.dependencies:
            # self.logger.error('{depend}'.format(depend=dir(depend)))
            if depend.top_level:
                self.logger.info('Found Top-Level: {depend.lib}.{depend.name}'.format(depend=depend))
                setattr(self, 'lib', getattr(depend, 'lib', None))
                setattr(self, 'project_lib', self.lib)
                setattr(self, 'local_path', getattr(depend, 'local_path', None))
                setattr(self, 'simulation_dir', getattr(depend, 'simulation_dir', None))
                top_level_dependency = depend
                break

        self.logger.info('Searching for Board in Project...')
        for depend in self.dependencies:
            if depend.is_board:
                self.logger.info('Found Board: {depend.lib}.{depend.name}'.format(depend=depend))
                if not hasattr(self, 'local_path'):
                    setattr(self, 'lib', getattr(depend, 'lib', None))
                    setattr(self, 'project_lib', self.lib)
                    local_path = os.path.join(getattr(depend, 'local_path', None),
                                              self.vendor,
                                              depend.name,
                                              self.tool_version)
                    setattr(self, 'local_path', local_path)
                    setattr(self, 'simulation_dir', getattr(depend, 'simulation_dir', None))
                    top_level_dependency = depend
                has_board = True
                setattr(self, 'project_top_level', self.top_level)
                board_priority_list = ['vendor', 'tool_version', 'family', 'device',
                                       'name', 'lib', 'top_level', 'board_id', 'board_timestamp_enabled']

                depend.set_as_board(top_level_dependency=top_level_dependency,
                                    board_priority_list=board_priority_list)

                setattr(self, 'is_board', True)
                for key in board_priority_list:
                    setattr(self, key, getattr(depend, key, None))
                break

        if hasattr(self, 'board_id'):
            self.logger.debug('Processing Board ID for Project: {self.board_id}'.format(self=self))
            board_id = self.board_id
            for char in ['X', 'x', '"', '_', 'U', '\\']:
                if char in board_id:
                    board_id = board_id.replace(char, "")
            setattr(self, 'board_id', int(board_id, 16))
            self.logger.info('Processed Board ID: {self.board_id}'.format(self=self))

        for depend in self.dependencies:
            if depend.vunit_default and depend.name != 'vendor_ip':
                self.logger.info('.' * 80)
                self.logger.info('Processing: {depend.lib}.{depend.name}'.format(depend=depend))

                src_files_list = list()

                try:
                    src_files_list = self.get_files(root_path=depend.src_dir,
                                                    file_exts=hdl_file_ext,
                                                    exclude_terms=self.exclude_keywords,
                                                    exclude_filename='EXCLUDE',
                                                    growing_list=src_files_list)
                except AttributeError as e:
                    self.logger.critical('Could Not Process HDL for: {depend.name}'
                                         .format(depend=depend))
                    self.logger.critical('{e}'.format(e=e))

                if src_files_list:
                    vunit_hdl_dict[depend.lib] = src_files_list

                try:
                    all_constr_files = self.get_files(root_path=depend.constraints_dir,
                                                      file_exts=constr_ext,
                                                      exclude_terms=self.exclude_keywords,
                                                      exclude_filename='EXCLUDE',
                                                      growing_list=all_constr_files)
                except AttributeError as e:
                    self.logger.critical('Could Not Process Constraints for: {depend.name}'
                                         .format(depend=depend))
                    self.logger.critical('{e}'.format(e=e))

            if getattr(depend, 'has_vendor_ip', False):
                self._validate_vendor_ip_requirements()
                self.logger.info('Processing IP for: {depend.name}'.format(depend=depend))

                for vend_ip in self.dependencies:
                    if vend_ip.vunit_default and vend_ip.name == 'vendor_ip':
                        self.logger.info('Found Master Vendor IP Dependency...')
                        ip_dependencies = projectmanager.VendorIpDependency(repo_root=self.repo_root,
                                                                            master_vendor_ip=vend_ip,
                                                                            vendor=depend.vendor,
                                                                            tool_version=depend.tool_version,
                                                                            family=depend.family,
                                                                            device=depend.device,
                                                                            ip_dict=depend.ip)

                ip_cnt = 0
                for k, v in ip_dependencies.enabled_ip.items():
                    self.logger.info('-' * 80)
                    self.logger.info('Processing Enabled IP: {k}'.format(k=k))
                    self.logger.info('Searching for Vendor IP Design Files...')
                    generated_ip_exclude_keywords = list()
                    generated_hdl_exclude_keywords = list()

                    if self.vendor == 'altera':
                        generated_ip_path = os.path.join('/ip', k)
                        generated_hdl_exclude_keywords = [generated_ip_path]
                        generated_ip_exclude_keywords = [generated_ip_path]
                        self.logger.info('(Altera) Excluding Generated IP Path: {path}'
                                         .format(path=generated_ip_path))

                        generated_hdl_exclude_keywords.extend(exclude_hdl_keywords)
                        generated_ip_exclude_keywords.extend(exclude_ip_keywords)

                    elif self.vendor == 'xilinx':
                        generated_hdl_exclude_keywords = exclude_hdl_keywords
                        generated_ip_exclude_keywords = exclude_ip_keywords

                    self.logger.debug('Exclude Terms for IP Files: {excl}'
                                      .format(excl=generated_hdl_exclude_keywords))
                    self.logger.debug('Exclude Terms for IP Wrapper Files: {excl}'
                                      .format(excl=generated_ip_exclude_keywords))
                    try:
                        all_ip_files = self.get_files(root_path=v['src_dir'],
                                                      file_exts=ip_ext,
                                                      exclude_terms=generated_hdl_exclude_keywords,
                                                      exclude_filename='EXCLUDE',
                                                      growing_list=all_ip_files)
                    except AttributeError as e:
                        self.logger.critical('Could Not Process IP Files for Vendor IP: {k}'
                                             .format(k=k))
                        self.logger.critical('{e}'.format(e=e))

                    except KeyError as e:
                        self.logger.critical('Could Not Process IP Files for Vendor IP: {k}'
                                             .format(k=k))
                        self.logger.critical('{e}'.format(e=e))

                    self.logger.info('Searching for Vendor IP HDL Wrapper Files...')

                    try:
                        self.logger.debug('Searching for IP Wrapper Files in: {path}'
                                          .format(path=v['src_dir']))
                        all_ip_wrapper_files = self.get_files(root_path=v['src_dir'],
                                                              file_exts=hdl_file_ext,
                                                              exclude_terms=generated_ip_exclude_keywords,
                                                              exclude_filename='EXCLUDE',
                                                              growing_list=all_ip_wrapper_files)
                    except AttributeError as e:
                        self.logger.critical('Could Not Process HDL Wrapper Files for Vendor IP: {k}'
                                             .format(k=k))
                        self.logger.critical('{e}'.format(e=e))

                    except KeyError as e:
                        self.logger.critical('Could Not Process HDL Wrapper Files for Vendor IP: {k}'
                                             .format(k=k))
                        self.logger.critical('{e}'.format(e=e))

                    try:
                        all_constr_files = self.get_files(root_path=v['constraints_dir'],
                                                          file_exts=constr_ext,
                                                          exclude_terms=self.exclude_keywords,
                                                          exclude_filename='EXCLUDE',
                                                          growing_list=all_constr_files)
                    except AttributeError as e:
                        self.logger.critical('Could Not Process Constraints for Vendor IP: {k}'
                                             .format(k=k))
                        self.logger.critical('{e}'.format(e=e))

                    except KeyError as e:
                        self.logger.critical('Could Not Process Constraints for Vendor IP: {k}'
                                             .format(k=k))
                        self.logger.critical('{e}'.format(e=e))

                    ip_cnt += 1
                    self.logger.debug('#' * 80)
                    self.logger.debug('IP Pass: #{ip_cnt}'.format(ip_cnt=ip_cnt))
                    for ip_file in all_ip_files:
                        self.logger.debug('\t{ip_file}'.format(ip_file=ip_file))

                    for wf in all_ip_wrapper_files:
                        self.logger.debug('\t{wf}'.format(wf=wf))

                if all_ip_files:
                    setattr(self, 'has_vendor_ip', True)
                    setattr(self, 'ip_files', all_ip_files)
                else:
                    setattr(self, 'has_vendor_ip', False)
                    setattr(self, 'ip_files', list())

                if all_constr_files:
                    setattr(self, 'constr_files', all_constr_files)
                else:
                    setattr(self, 'constr_files', list())

                for wf in all_ip_wrapper_files:
                    fname = os.path.split(wf)[1]
                    if any(fname in f for f in ip_wrapper_files_no_dups):
                        if 'common_wrapper_files' not in wf:
                            for cwf in ip_wrapper_files_no_dups:
                                if os.path.split(wf)[1] in cwf:
                                    self.logger.info('Two Wrapper Files Found. Prioritising Wrapper File:')
                                    self.logger.info('\tremoving: {cwf}'.format(cwf=cwf))
                                    ip_wrapper_files_no_dups.remove(cwf)
                                    self.logger.info('\tadding:   {wf}'.format(wf=wf))
                                    ip_wrapper_files_no_dups.append(wf)
                    elif wf not in ip_wrapper_files_no_dups:
                        self.logger.info('Single Wrapper File Found:')
                        self.logger.info('\tadding:   {wf}'.format(wf=wf))
                        ip_wrapper_files_no_dups.append(wf)
                    else:
                        self.logger.debug('Duplicate Wrapper File Found:')
                        self.logger.debug('\tskipping: {wf}'.format(wf=wf))

                if ip_wrapper_files_no_dups:
                    vunit_hdl_dict[v['lib']] = ip_wrapper_files_no_dups

        self.logger.debug('Completed VUnit Source Files Additions')
        for k, v in vunit_hdl_dict.items():
            for f in v:
                self.logger.debug('{lib}.{f}'.format(lib=k, f=f))

        self.logger.info('-' * 80)
        self.logger.info('Name:              {self.name}'.format(self=self))
        self.logger.info('Library:           {self.lib}'.format(self=self))
        self.logger.info('Top-Level:         {self.top_level}'.format(self=self))

        setattr(self, 'top_level_files', self.get_top_level_files(vunit_hdl_dict=vunit_hdl_dict,
                                                                  top_level_lib=self.lib,
                                                                  top_level=self.top_level,
                                                                  top_ids=['top_', '_top'],
                                                                  settings_file=self.settings_file))

        if hasattr(self, 'project_top_level'):
            self.logger.info('Project Top-Level: {self.project_top_level}'.format(self=self))
            if isinstance(self.project_top_level, (list, )):
                project_top_name = self.remove_top_id(name=self.project_top_level[0])
            else:
                setattr(self, 'project_top_level', [self.project_top_level])
                project_top_name = self.remove_top_id(name=self.project_top_level[0])
            board_name = self.remove_top_id(name=self.name)
        else:
            setattr(self, 'project_top_level', None)
            top_level_stripped_path = os.path.split(self.top_level_files[0])[1]
            top_level_stripped_ext = os.path.splitext(top_level_stripped_path)[0]
            project_top_name = self.remove_top_id(name=top_level_stripped_ext)
            board_name = None

        project_name_override = self.project_name_override
        setattr(self, 'project_name', self.generate_project_name(top_level_name=project_top_name,
                                                                 project_name_override=project_name_override,
                                                                 board_name=board_name))

        if 'boards' in self.local_path:
            build_path = os.path.join(self.local_path, 'build',
                                      self.project_name)
        else:
            build_path = os.path.join(self.local_path, 'build',
                                      self.vendor, self.tool_version, self.project_name)

        setattr(self, 'build_path', build_path)
        self.logger.info('Build Path: {self.build_path}'
                         .format(self=self))

        self.logger.info('Creating VUnit Object for Current Library: {lib}'
                         .format(lib=self.lib))
        self.logger.debug('msim_64bit: {self.sim_mode}'.format(self=self))
        if self.sim_mode == 64:
            msim_mode = True
        else:
            msim_mode = False

        setattr(self, 'hdl_sim_libs', self.config['simulation'][self.vendor])

        clean_precompiled_libs = False
        for c in ['precompiled_sim']:
            if c in self.clean:
                self.logger.debug('Clean Option Found: "{c}". Cleaning Precompiled Simulation Libraries...'
                                  .format(c=c))
                clean_precompiled_libs = True
                break

        vu = vunit_iface.VUnitProject(simulation_path=self.simulation_dir,
                                      sim_pre_compiled_libs_path=self.sim_pre_compiled_libs_path,
                                      fpga_vendor=self.vendor,
                                      fpga_toolversion=self.tool_version,
                                      sim_version=self.sim_version,
                                      setting_file=self.settings_file,
                                      hdl_lib_file_dict=vunit_hdl_dict,
                                      args=self.args,
                                      clean_precompiled_libs=clean_precompiled_libs,
                                      hdl_sim_libs=self.hdl_sim_libs,
                                      msim_64bit=msim_mode,
                                      use_osvvm=False,
                                      use_verification_components=False,
                                      modelsim_installdir=self.modelsim_installdir,
                                      repo_root=self.repo_root)

        try:
            use_glbl = self.use_glbl
        except AttributeError:
            self.logger.warning("'use_glbl:' Missing in Settings File: {settings}"
                                .format(settings=self.settings_file))
            self.logger.warning("\t'Setting to: 'use_glbl: False'")
            use_glbl = False

        vu.setup_simulation_options(vendor=self.vendor,
                                    glbl=use_glbl,
                                    glbl_lib=self.lib)

        try:
            if self.args.gui:
                sim_init_script = os.path.join(self.simulation_dir,
                                               self.sim_version,
                                               self.sim_init_script)
                if os.path.isfile(sim_init_script):
                    vu.configure_gui(sim_init_script=sim_init_script,
                                     repo_root=self.repo_root)
                else:
                    self.logger.critical('Could Not Find Simulation Init Script: {file}'
                                         .format(file=sim_init_script))

        except AttributeError:
            pass

        if self.vendor == 'xilinx':
            vu.add_vivado_sim_dependencies(vivado_path=self.xilinx_vivado,
                                           glbl=use_glbl,
                                           glbl_lib=self.lib)
            project_name = self.project_name + '.xpr'

        elif self.vendor == 'altera':
            project_name = self.project_name + '.qsf'

        if self.family in self.family_mappings:
            self.logger.debug('Family Mapping Found...')
            family = self.family_mappings[self.family]
            setattr(self, 'family', family)

        else:
            self.logger.debug('Family Mapping Not Found...')

        constraint_files = list()

        proj_hdl_files = list()
        top_level_hdls = [hdl for hdl in vunit_hdl_dict[self.lib] if self.top_level[0] in hdl]
        for top in top_level_hdls:
            top_level_hdl_files = vu.get_compile_order(top_level_file=top,
                                                       top_level_lib=self.lib)
            if self.project_top_level:
                found_proj_top = False
                proj_top_level_hdls = [hdl for hdl in vunit_hdl_dict[self.project_lib]
                                       if self.project_top_level[0] in hdl]
                for src_file in top_level_hdl_files:
                    if proj_top_level_hdls == os.path.abspath(src_file.name):
                        found_proj_top = True
                        break
                if found_proj_top:
                    self.logger.info('Found Project Top-Level Found.')
                    for src_file_obj in top_level_hdl_files:
                        if [src_file_obj.library.name, os.path.abspath(src_file_obj.name)] \
                                not in proj_hdl_files:
                            proj_hdl_files.append([src_file_obj.library.name,
                                                   os.path.abspath(src_file_obj.name)])
                else:
                    for proj_top in proj_top_level_hdls:
                        proj_top_level_hdl_files = vu.get_compile_order(top_level_file=proj_top,
                                                                        top_level_lib=self.project_lib)

                        for src_file_obj in proj_top_level_hdl_files:
                            if [src_file_obj.library.name, os.path.abspath(src_file_obj.name)] \
                                    not in proj_hdl_files:
                                proj_hdl_files.append([src_file_obj.library.name,
                                                       os.path.abspath(src_file_obj.name)])
                        for src_file_obj in top_level_hdl_files:
                            if [src_file_obj.library.name, os.path.abspath(src_file_obj.name)] \
                                    not in proj_hdl_files:
                                proj_hdl_files.append([src_file_obj.library.name,
                                                       os.path.abspath(src_file_obj.name)])

        for src in proj_hdl_files:
            self.logger.debug('{src}'.format(src=src))

        rebuild_project = False
        for c in ['all', 'fpga']:
            if c in self.clean:
                self.logger.debug('Clean Option Found: "{c}". Rebuilding Project'.format(c=c))
                rebuild_project = True
                break

        fpgaproject = fpgavendor_iface.FpgaProject(project_name=project_name,
                                                   build_path=self.build_path,
                                                   top_level_entity=self.top_level,
                                                   family=self.family,
                                                   device=self.device,
                                                   hdl_src_files=proj_hdl_files,
                                                   ip_files=self.ip_files,
                                                   constraint_files=self.constr_files,
                                                   repo_root=self.repo_root,
                                                   rebuild_project=rebuild_project,
                                                   board_id=self.board_id,
                                                   board_timestamp_enabled=self.board_timestamp_enabled)

        if self.has_vendor_ip:
            self.generate_vendor_ip()
            vu.compile_project_ip(project_file=fpgaproject.get_project_file())

        log.sect_break(self.logger)
        self.logger.info('Processed Project')

        if not self.headless and self.open_gui == 'fpga':
            project_file = fpgaproject.get_project_file()
            if self.vendor == 'altera':
                project_file = os.path.splitext(project_file)[0] + '.qpf'
                self.logger.info('Opening Project: {project}'
                                 .format(project=project_file))
                fpgavendor_iface.run_quartus_sh(quartus_bin='quartus',
                                                gui=True,
                                                project_file=project_file)
            elif self.vendor == 'xilinx':
                self.logger.info('Opening Project: {project}'
                                 .format(project=project_file))
                fpgavendor_iface.run_vivado(vivado_bin='vivado',
                                            mode='gui',
                                            tcl_file_name=project_file)

        log.sect_break(self.logger)

    def generate_vendor_ip(self):
        """

        """
        for ip in self.ip_files:
            if self.vendor == 'altera':
                self.logger.info('Generating Vendor IP From File: {ip}'
                                 .format(ip=ip))
                ip_path, ip_file = os.path.split(ip)
                ip_name = os.path.splitext(ip_file)[0]
                output_path = os.path.join(ip_path, ip_name)
                self.logger.info('Generating IP in: {path}'.format(path=output_path))
                self.logger.info('Using FPGA Family: {self.family}'.format(self=self))
                self.logger.info('Using FPGA Device: {self.device}'.format(self=self))

                clean = False
                for c in ['all', 'ip']:
                    if c in self.clean:
                        self.logger.debug('Clean Option Found: "{c}". Cleaning IP'.format(c=c))
                        clean = True
                        break

                if not os.path.exists(output_path) or clean:
                    fpgavendor_iface.run_ip_generate(exe='qsys-generate',
                                                     ip_file=ip,
                                                     output_path=output_path,
                                                     synth=True,
                                                     synth_language='VERILOG',
                                                     family=self.family,
                                                     device=self.device,
                                                     clean=clean)
                    fpgavendor_iface.run_ip_generate(exe='qsys-generate',
                                                     ip_file=ip,
                                                     output_path=output_path,
                                                     synth=False,
                                                     sim_language='VHDL',
                                                     family=self.family,
                                                     device=self.device,
                                                     clean=False)
                else:
                    self.logger.warning('Skipping Generation. Output Path Already Exists: {path}'
                                        .format(path=output_path))
            elif self.vendor == 'xilinx':
                pass

    def get_files(self, **kwargs):
        """

        Keyword Args:
            **root_path (str): Absolute path to path to start searching from. Searching will be recursive.
            **file_exts (list of str): A list of file extensions, including preceding ``.``, to search for.
            **exclude_terms (list of str): A list of strings, which if any are found in the path, will
                result in the path being excluded from the search.
            **exclude_filename (str, optional): If a file matching this name is found in the search path it
                will be read line-by-line to provide additional terms for excluding files from the path
                where the exclude file is found. Default value: ``'EXCLUDE'``
            **growing_list (list of str, optional): A list to append found files to. This allows lists to
                grow. If not provided a new list will be generated. Default value: ``list()``


        Returns:
            list of str: List of absolute paths of files matching search criteria.

        """
        root_path = funcs.get_kwarg('root_path', kwargs, '')
        file_exts = funcs.get_kwarg('file_exts', kwargs, list())
        exclude_terms = funcs.get_kwarg('exclude_terms', kwargs, list())
        exclude_filename = funcs.get_kwarg('exclude_filename', kwargs, 'EXCLUDE')
        growing_list = funcs.get_kwarg('growing_list', kwargs, list())

        found_file_list = self.search_paths_for_files(root_path=root_path,
                                                      file_extensions=file_exts,
                                                      exclude_terms_list=exclude_terms,
                                                      exclude_filename=exclude_filename)

        if found_file_list:
            for f in found_file_list:
                if f not in growing_list:
                    growing_list.append(f)

        return growing_list

    def remove_top_id(self, **kwargs):
        """Removes ``top`` ID from string

        Removes ``_top`` or ``top_`` from name.

        Keyword Args:
            name (str): Name to remove ``top`` ID from.

        Returns:
            str: ``name`` with ``_top`` or ``top_`` removed.

        """
        name = funcs.get_kwarg('name', kwargs, '')

        if name.endswith('_top'):
            top_level_name = name[:-4]
        elif name.startswith('top_'):
            top_level_name = name[4:]
        else:
            top_level_name = name

        return top_level_name

    def _validate_vendor_ip_requirements(self):
        """Checks all attributes to process vendor_ip exist

        Returns:
            bool: ``True`` if successful. Performs a ``sys.exit()`` if unsuccessful.

        """
        try:
            vendor_requirements = True
            if isinstance(self.vendor, (str,)) and self.vendor != "":
                pass
            else:
                vendor_requirements = False
                self.logger.error('Can Not Process Vendor IP. Unsupported Vendor: {self.vendor}'
                                  .format(self=self))
            if isinstance(self.tool_version, (str,)) and self.tool_version != "":
                pass
            else:
                vendor_requirements = False
                self.logger.error('Can Not Process Vendor IP. Unsupported Tool Version: {self.tool_version}'
                                  .format(self=self))
            if isinstance(self.family, (str,)) and self.family != "":
                pass
            else:
                vendor_requirements = False
                self.logger.error('Can Not Process Vendor IP. Unsupported Family: {self.family}'
                                  .format(self=self))
            if isinstance(self.device, (str,)) and self.device != "":
                pass
            else:
                vendor_requirements = False
                self.logger.error('Can Not Process Vendor IP. Unsupported Device: {self.device}'
                                  .format(self=self))

            if not vendor_requirements:
                self.logger.error('Can Not Process Vendor IP. Requirements Not Met.')
                self.logger.error('Update Settings File and Retry: {self.settings_file}'
                                  .format(self=self))
                log.errorexit(self.logger)

        except AttributeError as e:
            self.logger.error('Missing Settings Required to Process Vendor IP')
            self.logger.error('{e}'.format(e=e))
            self.logger.error('Update Settings File and Retry: {self.settings_file}'
                              .format(self=self))
            log.errorexit(self.logger)

        return True

    def search_paths_for_files(self, **kwargs):
        """Recursive search of root path for files matching file extension and exclusion criteria.

        Keyword Args:
            **root_path (str or list of str): The root path(s) to recursively search
            **file_extensions (list of str): A list of file extensions to search. Must include '.' prefix
                to match requirements of ``os.path.splitext()[1]``.
            **exclude_terms_list (list of str): A list of exclude terms. A path containing `any` item in this
                list will be excluded from the search.
            **exclude_filename (str, optional): Any file found in the search paths matching this name will
                be parsed, line-by-line, to add path specific exclusions. Default value: ``'EXCLUDE'``

        Returns:
            list of str: A list of absolute paths of files matching criteria. Empty list if none found.

        """
        root_paths = funcs.get_kwarg('root_path', kwargs, list())
        file_extensions = funcs.get_kwarg('file_extensions', kwargs, list())
        exclude_terms_list = funcs.get_kwarg('exclude_terms_list', kwargs, list())
        exclude_filename = funcs.get_kwarg('exclude_filename', kwargs, 'EXCLUDE')

        if isinstance(root_paths, (str, )) and root_paths != "":
            root_paths = [root_paths]

        search_paths = list()
        exclude_file_list = list()

        found_file_list = list()

        for root_path in root_paths:
            self.logger.info('Searching for {exts} Files in: {path} '.format(exts=file_extensions,
                                                                             path=root_path))
            for root, subdirs, filenames in os.walk(root_path):
                self.logger.debug('Subpaths: {subdirs}'.format(subdirs=subdirs))
                if filenames:
                    if any(kw in root for kw in exclude_terms_list):
                        kw_matches = [kw for kw in exclude_terms_list if kw in root]
                        self.logger.debug("Filtering Path. Keyword Exclusion(s): "
                                          "'{kw}' in Path: {path}"
                                           .format(path=root, kw=kw_matches))
                    else:
                        search_paths.append(root)

            if search_paths:
                self.logger.info('Valid Search Paths:')
                for path in search_paths:
                    self.logger.info('\t{path}'.format(path=path))
            else:
                self.logger.warning('No Search Paths Found while Processing: {path}'
                                    .format(path=root_path))

            for path in search_paths:
                for root, subdirs, filenames in os.walk(path):
                    for f in filenames:
                        if f == exclude_filename:
                            exclude_file = os.path.join(root, f)
                            if exclude_file not in exclude_file_list:
                                exclude_file_list.append(exclude_file)
                                self.logger.info("'{exclude_filename}' File Found: {exclude_file}"
                                                 .format(exclude_filename=exclude_filename,
                                                         exclude_file=exclude_file))
                        else:
                            if os.path.splitext(f)[1] in file_extensions:
                                found_file_list.append(os.path.join(root, f))
                            else:
                                self.logger.debug("Filtering File. Ext Exclusion(s): "
                                                  "'{ext}' Not in {exts} for Filename: {path}"
                                                  .format(ext=os.path.splitext(f)[1],
                                                          exts=file_extensions,
                                                          path=os.path.join(root, f)))
                    break

        if found_file_list:
            self.logger.debug('Unfiltered Files:')
            for f in found_file_list:
                self.logger.debug('\t{f}'.format(f=f))
        else:
            self.logger.debug('No Files Found while Processing:')
            for path in root_paths:
                self.logger.debug('\t{path}:'
                                  .format(path=path))

        exclude_file_keywords = list()
        no_dups_file_list = list()

        if exclude_file_list:
            for f in exclude_file_list:
                self.logger.info("Parsing '{exclude_filename}' File: {exclude_file}"
                                 .format(exclude_filename=exclude_filename,
                                         exclude_file=f))
                with open(f) as fp:
                    for l in fp.read().splitlines():
                        if len(l.split()) == 0:
                            self.logger.debug("\tSkipping Empty Line in '{exclude_filename}' File"
                                              .format(exclude_filename=exclude_filename))
                        else:
                            self.logger.debug("\t'{exclude_filename}' File Term: {exclude_term}"
                                              .format(exclude_filename=exclude_filename,
                                                      exclude_term=l))
                            exclude_file_keywords.append(l)

        if exclude_file_keywords:
            for unfiltered_file in found_file_list:
                if any(kw in unfiltered_file for kw in exclude_file_keywords):
                    kw_matches = [kw for kw in exclude_file_keywords if kw in unfiltered_file]
                    self.logger.warning("Filtering File. '{exclude_filename}' File Keyword Exclusion(s): "
                                        "{kw} in Path: {path}"
                                        .format(exclude_filename=exclude_filename,
                                                path=unfiltered_file,
                                                kw=kw_matches))
                else:
                    if unfiltered_file not in no_dups_file_list:
                        self.logger.debug('Adding File to Filtered List: {filtered_file}'
                                          .format(filtered_file=unfiltered_file))
                        no_dups_file_list.append(unfiltered_file)
        else:
            for unfiltered_file in found_file_list:
                if unfiltered_file not in no_dups_file_list:
                    self.logger.debug('Adding File to Filtered List: {filtered_file}'
                                      .format(filtered_file=unfiltered_file))
                    no_dups_file_list.append(unfiltered_file)

        if no_dups_file_list:
            self.logger.info('Filtered Files:')
            for f in no_dups_file_list:
                self.logger.info('\t{f}'.format(f=f))
            return no_dups_file_list
        else:
            self.logger.warning('No Files Found while Processing:')
            for path in root_paths:
                self.logger.warning('\t{path}'
                                    .format(path=path))
            return list()

    def __repr__(self):
        return "{self.__class__.__name__}(log_to_console={self.log_to_console})".format(self=self)

    def __str__(self):
        return "{} is a {self.__class__.__name__} object".format(__name__, self=self)

    def process_xml2vhdl(self, **kwargs):
        """Processes project to configure and generate VHDL from XML using ``xml2vhdl``

        Keyword Args:
            **dependencies (list of obj): List of dependency objects in the current project.
            **clean (bool, optional): Cleans the output directories prior to generation.
                Default value: ``False``
            **settings_file (str): Full path of settings file used to generate the current project. Used to
                reference in logging.

        Returns:
            None

        """
        dependencies = funcs.get_kwarg('dependencies', kwargs, None)
        clean = funcs.get_kwarg('clean', kwargs, False)
        settings_file = funcs.get_kwarg('settings_file', kwargs, self.settings_file)

        xml2vhdl_lib_status = dict()
        xml2vhdl_required_libs = list()

        pre_generated_terms = ['pre_generated']
        xml_generated_terms = ['vhd', 'generated']
        vhdl_generated_terms = ['generated']

        for depend in dependencies:
            if depend.name == 'xml2vhdl':
                if isinstance(depend.required_vhdl_libs, (list,)):
                    for lib in depend.required_vhdl_libs:
                        xml2vhdl_lib_status[lib] = False
                        xml2vhdl_required_libs.append(lib)
                else:
                    self.logger.critical('Incorrect setting for XML2VHDL in: {settings}'
                                         .format(settings=settings_file))
                    self.logger.critical('\t"required_vhdl_libs:" entry for "xml2vhdl` Must be a List')
                break

        self.logger.debug('Pre-check XML2VHDL Dependency Status(es):')
        for k, v in xml2vhdl_lib_status.items():
            self.logger.debug('{k}: {v}'.format(k=k, v=v))

        for depend in self.dependencies:
            if depend.name in xml2vhdl_required_libs and depend.vunit_default:
                xml2vhdl_lib_status[depend.name] = True

        self.logger.debug('Post-check XML2VHDL Dependency Status(es):')
        for k, v in xml2vhdl_lib_status.items():
            self.logger.debug('{k}: {v}'.format(k=k, v=v))

        for lib in xml2vhdl_required_libs:
            if not xml2vhdl_lib_status[lib]:
                self.logger.error('XML2VHDL Dependencies Missing: {lib}'.format(lib=lib))
                self.logger.error('Check that it is included, enabled and a unit_default in: {settings}'
                                  .format(settings=settings_file))
                log.errorexit(self.logger)

        self.logger.info('XML2VHDL Support: Enabled')
        self.logger.info('Processing VHDL Dependencies for XML2VHDL Generation...')
        xml2vhdl_settings = xml2xml_iface.Xml2Vhdl(xml2vhdl_path=self.xml2vhdl_path)

        for depend in dependencies:
            if depend.vunit_default:
                # todo: The ``not in`` clause should be redundant once boards and vendor_ip support is
                #       added to :mod:`projectmanager`
                try:
                    if depend.name not in ['boards', 'vendor_ip']:
                        xml2vhdl_settings = self.process_xml2vdl_src_code(xml2vhdl_obj=xml2vhdl_settings,
                                                                          dependency=depend,
                                                                          src_root=os.path.join(depend.src_dir,
                                                                                                'xml'),
                                                                          generated_terms=xml_generated_terms,
                                                                          pre_generated_terms=pre_generated_terms,
                                                                          clean=clean)
                        xml2vhdl_settings = self.process_xml2vdl_src_code(xml2vhdl_obj=xml2vhdl_settings,
                                                                          dependency=depend,
                                                                          src_root=os.path.join(depend.src_dir,
                                                                                                'vhdl'),
                                                                          generated_terms=vhdl_generated_terms,
                                                                          pre_generated_terms=pre_generated_terms,
                                                                          clean=clean)
                except AttributeError as e:
                    self.logger.critical('Could Not Process XML2VHDL for: {depend.name}'
                                         .format(depend=depend))
                    self.logger.critical('{e}'.format(e=e))

        xml2vhdl_settings.generate_vhdl(working_dir=self.xml2vhdl_path)

    def get_top_level_files(self, **kwargs):
        """Gets top-level files from a dictionary of library/absolute file paths.

        Keyword Args:
            **vunit_hdl_dict (dict): Dictionary of list of HDL files, grouped by keys representing the
                corresponding VHDL library.
            **top_level_lib (str): Name of top-level library.
            **top_level (list of str, or str, optional): Top-level filenames.
                Does *not* require file extension. Will search for possible top-levels if not included.
                Default value: ``''``
            **top_ids (list of str, optional): List of terms to determine if HDL top-level filename contains a
                top-level entity. Default value: ``['top_', 'top_']``
            **settings_file (str, optional): Path to settings file to reference in logs.
                Default value: ``''``

        Returns:
            list of str: Absolute paths of top-level files, performs a sys.exit if no top-level files found.

        """
        vunit_hdl_dict = funcs.get_kwarg('vunit_hdl_dict', kwargs, dict())
        top_level_lib = funcs.get_kwarg('top_level_lib', kwargs, '')
        top_level = funcs.get_kwarg('top_level', kwargs, '')
        top_ids = funcs.get_kwarg('top_ids', kwargs, ['_top', '_top'])
        settings_file = funcs.get_kwarg('settings_file', kwargs, '')

        self.logger.info('Finding Top-Level File(s) for: {top_level_lib}'
                         .format(top_level_lib=top_level_lib))

        # \todo This resolves issues where wrapper files are added to None key. This should be stopped
        #       from happening before the script gets here.
        for k, v in vunit_hdl_dict.items():
            self.logger.debug('vunit_hdl_dict: {k}: {v}'.format(k=k, v=v))
            if k is None:
                vunit_hdl_dict.pop(None, None)

        top_level_libs = [key for key in vunit_hdl_dict if top_level_lib in key]
        top_level_files = list()

        if not top_level_libs:
            self.logger.critical('No Top-Level Libraries Found.')
        elif isinstance(top_level, (list,)) and top_level:
            self.logger.debug('Top-Level Files Defined in Settings File: {settings}'
                              .format(settings=settings_file))
            for top in top_level:
                self.logger.debug('\t{top}'
                                  .format(top=top))
                for lib in top_level_libs:
                    for f in vunit_hdl_dict[lib]:
                        filename = os.path.split(f)[1]
                        if top in filename:
                            self.logger.info('Top-Level File: {f}'
                                             .format(f=f))
                            top_level_files.append(f)
        elif isinstance(top_level, (str,)) and top_level != "":
            self.logger.debug('Top-Level Files Defined in Settings File: {settings}'
                              .format(settings=settings_file))
            self.logger.debug('\t{top}'.format(top=top_level))
            for lib in top_level_libs:
                for f in vunit_hdl_dict[lib]:
                    filename = os.path.split(f)[1]
                    if top_level in filename:
                        self.logger.info('Top-Level File: {f}'
                                         .format(f=f))
                        top_level_files.append(f)
        else:
            self.logger.warning('No Top-Level File(s) Defined in Settings File: {settings}'
                                .format(settings=settings_file))

            for lib in top_level_libs:
                for f in vunit_hdl_dict[lib]:
                    filename = os.path.split(f)[1]
                    if top_level_lib in filename and any(t in filename for t in top_ids):
                        self.logger.info('Possible Top-Level File: {f}'
                                         .format(f=f))
                        top_level_files.append(f)

        if top_level_libs and top_level_files:
            self.logger.debug('Top-Level Files:')
            for top in top_level_files:
                self.logger.debug('\t{top}'.format(top=top))

            return top_level_files
        else:
            self.logger.error('No Top-Level Files Found.')
            log.errorexit(self.logger)

    def file_type_detect(self, f_list, ext='.xml'):
        """Detects files of type in list using file extension.

        Args:
            f_list (list): List of file names
            ext (str, optional): File extension to detect. *Must* include ``.``. Default value: ``.xml``

        Returns:
             bool: ``True`` if one file in list is detected, otherwise ``False``

        """
        if isinstance(f_list, (list, )):
            for f in f_list:
                if os.path.splitext(f)[-1] == ext:
                    return True

        return False

    def process_xml2vdl_src_code(self, **kwargs):
        """process source code required by ``xml2vhdl`` generation.

        Keyword Args:
            **xml2vhdl_obj (obj): A :mod:`xml2vhdl_iface.Xml2Vhdl` object to operate on. If one isn't supplied
                one will be generated.
            **dependency (obj): A :mod:`projectmanager.ProjectDependency` object for dependency to process
                for valid``xml2vhdl`` source code.
            **src_root (str): Path to source code location to process.
            **generated_terms (list of str): A list of strings which could be folders where generated
                source code is stored.
            **pre_generated_terms (list of str): A list of strings which could be folders where pre_generated
                source code is stored.
            **clean (bool, optional): Cleans the generated locations using ``shutil.rmtree`` to delete the
                directory(ies) and ``os.makedirs`` to recreate the directory(ies). Default value: ``False``.

        Returns:
            obj: a :mod:`projectflow.Xml2Vhdl` object with attributes updated/completed.

        """
        xml2vhdl_obj = funcs.get_kwarg('xml2vhdl_obj', kwargs, xml2xml_iface.Xml2Vhdl())
        depend = funcs.get_kwarg('dependency', kwargs, None)
        src_root = funcs.get_kwarg('src_root', kwargs, None)
        generated_terms = funcs.get_kwarg('generated_terms', kwargs, list())
        pre_generated_terms = funcs.get_kwarg('pre_generated_terms', kwargs, list())
        clean = funcs.get_kwarg('clean', kwargs, False)

        existing_generated_paths = list()

        if os.path.exists(src_root):
            for root, subpaths, filenames in os.walk(src_root):
                if filenames:
                    self.logger.info('{depend.name}: Found Source(s):'
                                     .format(depend=depend))
                    self.logger.info('\tXML2VHDL Root: {path}'.format(path=src_root))
                    if self.file_type_detect(filenames, '.xml'):
                        xml2vhdl_obj.add_to_path(attr='input_folder', add_paths=src_root)
                        self.logger.info('\tFound: {filenames}'.format(filenames=filenames))
                else:
                    self.logger.info('{depend.name}: No Sources Found for XML2VHDL Generation.'
                                     .format(depend=depend))

                if subpaths:
                    self.logger.debug('{depend.name}: subpaths: {subpaths}'
                                      .format(depend=depend, subpaths=subpaths))
                    for path in subpaths:
                        for term in generated_terms:
                            if term in path:
                                existing_generated_paths.append(os.path.join(src_root, path))
                        for term in pre_generated_terms:
                            if term in path:
                                xml2vhdl_obj.add_to_path(attr='path',
                                                              add_paths=os.path.join(src_root,
                                                                                     path))

                            # Remove pre_generated terms from existing_generated_paths
                            existing_generated_paths = [x for x in existing_generated_paths if term not in x]
                break
        else:
            self.logger.info('{depend.name}: No Sources Found for XML2VHDL Generation.'
                             .format(depend=depend))

        if existing_generated_paths:
            self.logger.info('Found the Following Existing Locations for XML2VHDL Generated Source Code:')
            for path in existing_generated_paths:
                self.logger.info('\t{path}'.format(path=path))
                if clean:
                    self.logger.warning('Cleaning Directory: {path}'.format(path=path))
                    shutil.rmtree(path)
                    os.makedirs(path)

        return xml2vhdl_obj

    def add_vendor_to_exclude_terms(self, exclude_terms=None, **kwargs):
        """Add FPGA vendor to exclude terms.

        Adds `other` FPGA vendors to exclude terms list.

        Args:
            exclude_terms (str or list of str, optional): exclude term(s) to append.

        Keyword Args:
            **vendor (str, optional): FPGA vendor. Valid values: from ``supported_vendors``.
                Default value: ``'xilinx'``
            **supported_vendors (list of str): List of supported FPGA vendors.
                Default value: ``list(['xilinx', 'altera'])``
        Returns:
            list of str: List of exclude terms, with all 'other` FPGA vendors, other than ``vendor``
            argument appended.

        """
        default_vendor_list = ['xilinx', 'altera']
        vendor = funcs.get_kwarg('vendor', kwargs, 'xilinx')
        supported_vendors = funcs.get_kwarg('supported_vendors', kwargs, default_vendor_list)

        if not isinstance(supported_vendors, (list, )):
            self.logger.critical("'supported_vendors' Not a List. Using: {default_vendor_list}"
                                 .format(default_vendor_list=default_vendor_list))

        if vendor not in supported_vendors:
            self.logger.critical("'vendor' Not in Supported Vendor List. Using: {default_vendor}"
                                 .format(default_vendor=default_vendor_list[0]))
            vendor = default_vendor_list[0]

        self.logger.debug('Vendor:            {vendor}'
                          .format(vendor=vendor))
        self.logger.debug('Supported Vendors: {supported_vendors}'
                          .format(supported_vendors=supported_vendors))

        excluded_vendors = [term for term in supported_vendors if term != vendor]
        self.logger.debug('Excluded Vendors:  {excluded_vendors}'
                          .format(excluded_vendors=excluded_vendors))

        if isinstance(exclude_terms, (list, )):
            updated_exclude_terms = exclude_terms
            updated_exclude_terms.extend(excluded_vendors)
        elif isinstance(exclude_terms, (str, )) and exclude_terms != "":
            updated_exclude_terms = [exclude_terms]
            updated_exclude_terms.extend(excluded_vendors)
        else:
            updated_exclude_terms = excluded_vendors

        self.logger.debug('Excluded Terms:    {updated_exclude_terms}'
                          .format(updated_exclude_terms=updated_exclude_terms))

        if not updated_exclude_terms:
            return list()
        else:
            return updated_exclude_terms

    def generate_project_name(self, **kwargs):
        """Generates FPGA Vendor ``project_name`` based on top-level entity name, board name and name override

        If the top-level name and the board name match the board name will be used.
        Keyword Args:
            **top_level_name (str): Top-level entity name
            **project_name_override (str, optional): Project name override
            **board_name (str): Board name

        Returns:
            str: project name if successful, ``None`` if unsuccessful.

        """
        top_level_name = funcs.get_kwarg('top_level_name', kwargs, None)
        project_name_override = funcs.get_kwarg('project_name_override', kwargs, None)
        board_name = funcs.get_kwarg('board_name', kwargs, None)

        if isinstance(project_name_override, (str, )) and project_name_override != "":
            self.logger.info('Using Project Name Override Value as Project Name: {project_name}'
                             .format(project_name=project_name_override))
            return project_name_override

        if board_name is None:
            if isinstance(top_level_name, (str, )) and top_level_name != "":
                self.logger.info('Using Top-Level Entity Name as Project Name: {project_name}'
                                 .format(project_name=top_level_name))
                return top_level_name
        elif isinstance(self.board, (str,)) and self.board != "":
            if isinstance(top_level_name, (str,)) and top_level_name != "":
                if board_name == top_level_name:
                    project_name = board_name
                else:
                    project_name = board_name + '_' + top_level_name
                    self.logger.info('Using Board and Top-Level Entity Name as Project Name: {project_name}'
                                     .format(project_name=project_name))
                return project_name

        self.logger.critical('Could Not Determine Project Name.')
        self.logger.critical('\tTop-Level Name       : {top_level_name'
                             .format(top_level_name=top_level_name))
        self.logger.critical('\tProject Name Override: {project_name_override}'
                             .format(project_name_override=project_name_override))
        self.logger.critical('\tBoard Name           : {board_name}'
                             .format(board_name=board_name))
        return None


if __name__ == '__main__':
    logger.info("projectflow {} {}"
                .format(__version__, version.revision))
    log.sect_break(logger)

    project = ProjectFlow()

else:
    logger.info(__str__)
