# -*- coding: utf8 -*-
"""

***********************
``fpgavendor_iface.py``
***********************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``fpgavendor_iface.py`` is a module to handle the generation of FPGA projects and interfacing with
:mod:`vunit_iface`, to include the compilation of FPGA vendor simulation modules based on tool version and
FPGA device family.

"""
import helpers.customlogging as log
import helpers.version as my_version
import helpers.funcs as funcs

import os
import shutil
import time
import datetime
from subprocess import check_call, CalledProcessError

logger = log.config_logger(name=__name__)
LOGLEVEL = log.LogLevelsConsts

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(0, 1, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class FpgaProject(object):
    """

    """
    def __init__(self, **kwargs):
        self.logger = log.config_logger(name=__name__, class_name=self.__class__.__name__)
        self.logger.info('*' * 80)
        self.logger.info('** Generating FPGA Project...')
        self.logger.info('*' * 80)
        setattr(self, 'repo_root', funcs.get_kwarg('repo_root', kwargs, ''))
        build_path = funcs.get_kwarg('build_path', kwargs, None)
        rebuild_project = funcs.get_kwarg('rebuild_project', kwargs, True)
        setattr(self, 'board_id', funcs.get_kwarg('board_id', kwargs, 0))
        setattr(self, 'board_timestamp_enabled', funcs.get_kwarg('board_timestamp_enabled', kwargs, False))
        setattr(self, 'tcl_repo_root', '$env(REPO_ROOT)')

        if not build_path:
            self.logger.error('No Build Path Supplied. Can Not Create {self.__class__.__name__}'
                              .format(self=self))
            log.errorexit(self.logger)

        project_name = funcs.get_kwarg('project_name', kwargs, 'project')

        generation_script_name = funcs.get_kwarg('generation_script_name', kwargs, 'project_gen.tcl')
        generation_script_ext = '.tcl'

        project_extension = os.path.splitext(project_name)[1]

        if not generation_script_name.endswith(generation_script_ext):
            generation_script_name = generation_script_name + generation_script_ext

        project_file = os.path.join(build_path, project_name)
        setattr(self, 'project_file', project_file)

        self.logger.info('Project Name:       {project_name}'
                         .format(project_name=project_name))
        self.logger.info('Project Build Path: {build_path}'
                         .format(build_path=build_path))

        family = funcs.get_kwarg('family', kwargs, None)
        device = funcs.get_kwarg('device', kwargs, None)

        top_level_entity = funcs.get_kwarg('top_level_entity', kwargs, '')
        if isinstance(top_level_entity, (list, )):
            top_level_entity = top_level_entity[0]

        self.logger.info('Top-Level Entity:   {top_level_entity}'
                         .format(top_level_entity=top_level_entity))

        hdl_src_files = funcs.get_kwarg('hdl_src_files', kwargs, list())
        ip_files = funcs.get_kwarg('ip_files', kwargs, list())
        constraint_files = funcs.get_kwarg('constraint_files', kwargs, list())

        if project_extension in ['.xpr']:
            vendor = 'xilinx'
            generate_script = self.create_vivado_project(project_name=project_name,
                                                         build_path=build_path,
                                                         top_level_entity=top_level_entity,
                                                         hdl_files=hdl_src_files,
                                                         ip_files=ip_files,
                                                         constraint_files=constraint_files,
                                                         family=family,
                                                         device=device)
        elif project_extension in ['.qpf', '.qsf']:
            vendor = 'altera'
            generate_script = self.create_quartus_project(project_name=project_name,
                                                          build_path=build_path,
                                                          top_level_entity=top_level_entity,
                                                          hdl_files=hdl_src_files,
                                                          ip_files=ip_files,
                                                          constraint_files=constraint_files,
                                                          family=family,
                                                          device=device)

        else:
            self.logger.error('Can Not Determine Vendor from Project File Extension: {file}'
                              .format(file=project_name))
            log.errorexit(self.logger)

        if generate_script:
            generation_script_file_path = build_path
            self.logger.info('Project Build Path: {path}'
                             .format(path=generation_script_file_path))

            if not os.path.exists(generation_script_file_path):
                self.logger.warning('Project Build Path Not Found. Creating: {path}'
                                    .format(path=generation_script_file_path))
                os.makedirs(generation_script_file_path)

            elif rebuild_project:
                self.logger.info('Backing Up Existing Project Build Path: {path}'
                                 .format(path=generation_script_file_path))
                self.backup_project(project_path=generation_script_file_path)

            else:
                self.logger.critical('Project Build Path Exists and Custom Changes Will be Overwritten '
                                     'Without Being Backed Up: {path}'
                                     .format(path=generation_script_file_path))
                self.logger.critical("\tTo Prevent This Warning Use Argument: '--clean fpga' "
                                     "or '--clean all'")
                funcs.clean_path(path=generation_script_file_path)

            self.logger.info('Creating Project Generation Script: {script}'
                             .format(script=generation_script_file_path))

            logger.info('Writing Project Generation Script File: {script}'
                        .format(script=generation_script_file_path))

            fp_generation_script = os.path.join(generation_script_file_path,
                                                generation_script_name)

            with open(fp_generation_script, 'w') as script_fp:
                for line in generate_script:
                    script_fp.write(line + '\n')

            if vendor == 'xilinx':
                run_vivado(vivado_bin='vivado',
                           mode='tcl',
                           tcl_file=generation_script_file_path)

            elif vendor == 'altera':
                saved_path = os.getcwd()
                os.chdir(generation_script_file_path)
                run_quartus_sh(tcl_file_name=fp_generation_script,
                               script_mode=True)
                os.chdir(saved_path)

        self.logger.info('** Finished Generating FPGA Project')
        self.logger.info('*' * 80)

    def get_project_file(self):
        """Gets the absolute path of the project file.

        Returns:
            str: Absolute path of project file. ``None`` if not found.

        """
        return getattr(self, 'project_file', None)

    def add_ip(self, **kwargs):
        """

        Keyword Args:
            **vunit_obj (obj): A :mod:`vunit_iface.VunitProject` object. Default value: ``self.vu``
            **project_file (str): Absolute path to project file.
            **rebuild_project (bool, optional): If ``True`` rebuild existing project.
                Default value: ``False``

        Returns:
            None

        """
        vunit_obj = funcs.get_kwarg('vunit_obj', kwargs, self.vu)
        project_file = funcs.get_kwarg('project_file', kwargs, False)
        rebuild_project = funcs.get_kwarg('rebuild_project', kwargs, False)

        if project_file and project_file != "":
            project_dir = os.path.split(project_file)[0]
            project_extension = os.path.splitext(project_file)[1]

            if os.path.exists(project_dir):
                self.logger.info('Found Project Directory: {project_dir}'
                                 .format(project_dir=project_dir))
                if rebuild_project:
                    self.backup_project_file(project_dir=project_dir)
                else:
                    self.logger.warning('Overwriting Project: {file}'
                                        .format(file=project_file))
            else:
                self.logger.info('Creating Project Directory: {project_dir}'
                                 .format(project_dir=project_dir))
                os.makedirs(project_dir)
        else:
            self.logger.error('Incorrect Project File Supplied: {file}'
                              .format(file=project_file))
            log.errorexit(self.logger)

        self.logger.info('Processing Project File for Simulation: {project_file}'
                         .format(project_file=project_file))

    def backup_project(self, **kwargs):
        """Backup project using timestamp.

        Appends time stamp to the project directory in the form: ``_%Y%m%d%H%M%S`` and uses
        ``shutil.copytree()`` to backup the project. Then cleans the original directory (using
        ``shutil.rmtree()`` and remaking the location using: ``os.makedirs()``)

        Keyword Args:
            **project_path (str): Absolute path to project root.

        Returns:
            None

        """
        project_path = funcs.get_kwarg('project_path', kwargs, False)
        self.logger.info('Backing Up Existing Project:')

        timestamp = time.time()
        backup_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('_%Y%m%d%H%M%S')
        backup_project_path = project_path + backup_timestamp
        self.logger.info('\tfrom: {project_path}'
                         .format(project_path=project_path))
        self.logger.info('\tto  : {project_path}'
                         .format(project_path=backup_project_path))

        shutil.copytree(project_path, backup_project_path)
        logger.info('Backed Up Project Directory and all its Contents to: {project_path}'
                    .format(project_path=backup_project_path))

        self.logger.info('Cleaning Existing Project: {project_path}'
                         .format(project_path=project_path))
        funcs.clean_path(path=project_path)

        self.logger.info('Cleaned Project: {project_path}'
                         .format(project_path=project_path))

    def create_vivado_project(self, **kwargs):
        """Creates a ``vivado`` project using supplied settings.


        Keyword Args:
            **project_name (str, optional): Name of project file to generate.
                Default value: ``'project'``
            **build_path (str): Absolute path to build location for generated project
            **target_language (str, optional): Target default language for the generated project.
                Default value: ``'VHDL'``
            **top_level_entity (str): Top-level HDL entity name.
            **hdl_files_dict (dict): Dictionary of HDL libraries (keys) and list of absolute HDL files.
            **ip_files (list of str): List of absolute paths fof IP files to add to project.
            **constraint_files (list of str): List of absolute paths of constraints to add to project.

        Returns:
            None

        """
        project_name, project_ext = os.path.splitext(funcs.get_kwarg('project_name', kwargs, 'project'))
        build_path = funcs.get_kwarg('build_path', kwargs, '').replace(self.repo_root, self.tcl_repo_root)
        family = funcs.get_kwarg('family', kwargs, None)
        device = funcs.get_kwarg('device', kwargs, None)
        target_language = funcs.get_kwarg('target_language', kwargs, 'VHDL')
        top_level_entity = funcs.get_kwarg('top_level_entity', kwargs, '')
        hdl_files = funcs.get_kwarg('hdl_files', kwargs, dict())
        ip_files = funcs.get_kwarg('ip_files', kwargs, list())
        constraint_files = funcs.get_kwarg('constraint_files', kwargs, list())

        self.logger.info('Generating Vivado Project...')
        self.logger.info('Project Name: {name}'.format(name=project_name))
        self.logger.info('FPGA Family: {family}'
                         .format(family=family))
        self.logger.info('FPGA Device: {device}'
                         .format(device=device))

        project_file = os.path.join(build_path, (project_name + project_ext))
        tcl_cmds_list = list(['#' * 80, '## Auto-Generated Script File, Do Not Modify', '#' * 80])
        tcl_cmds_list.append('create_project {project} -force -part {device}'
                             .format(project=project_file, device=device))
        tcl_cmds_list.append('set_property part {device} [current_project]'
                             .format(device=device))
        tcl_cmds_list.append('set_property target_language {target_language} [current_project]'
                             .format(target_language=target_language))
        tcl_cmds_list.append('set_property XPM_LIBRARIES {XPM_CDC XPM_FIFO XPM_MEMORY} [current_project]')

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding Script Based Parameters:')
        tcl_cmds_list.append('#' * 80)

        tcl_cmds_list.append('set_property generic g_board_id={self.board_id} [current_project]'
                             .format(self=self))

        if self.board_timestamp_enabled:
            timestamp = generate_timestamp()
            self.logger.info('Generated Timestamp: {timestamp}'
                             .format(timestamp=generate_timestamp()))
            tcl_cmds_list.append('set_property generic g_board_timestamp={timestamp} [current_project]'
                                 .format(timestamp=timestamp))

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding HDL Source File(s):')
        tcl_cmds_list.append('#' * 80)

        for src_file_obj in hdl_files:
            hdl_file = src_file_obj[1].replace(self.repo_root, self.tcl_repo_root)
            tcl_cmds_list.append('add_files -norecurse "{hdl_file}"'
                                 .format(hdl_file=hdl_file))
            tcl_cmds_list.append('set_property library {lib} [get_files {hdl_file}]'
                                 .format(lib=src_file_obj[0], hdl_file=hdl_file))

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding IP Source File(s):')
        tcl_cmds_list.append('#' * 80)

        for ip in ip_files:
            ext = os.path.splitext(ip)[-1].lower()
            if ext == '.xci':
                tcl_cmds_list.append('add_files -norecurse "{ip}"'
                                     .format(ip=ip.replace(self.repo_root, self.tcl_repo_root)))
            else:
                self.logger.critical('Unsupported IP File Type ({ext}): {ip}'
                                     .format(ext=ext, ip=ip))

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding Constraints File(s):')
        tcl_cmds_list.append('#' * 80)

        for constr in constraint_files:
            ext = os.path.splitext(constr)[-1].lower()
            if ext == '.xdc':
                tcl_cmds_list.append('add_files -fileset constrs_1 -norecurse "{constr}"'
                                     .format(constr=constr.replace(self.repo_root, self.tcl_repo_root)))
            else:
                self.logger.critical('Unsupported Constraint File Type ({ext}): {constr}'
                                     .format(ext=ext, constr=constr))

        # \todo Add Pre/Post Scripts Here.
        #   tcl_cmds_list.append('set_property STEPS.SYNTH_DESIGN.TCL.PRE "{pre_synth}" [get_runs synth_1]'
        #                        .format(pre_synth=pre_synth))
        #   tcl_cmds_list.append('set_property STEPS.SYNTH_DESIGN.TCL.POST "{post_synth}" [get_runs synth_1]'
        #                        .format(post_synth=post_synth))
        #   tcl_cmds_list.append('set_property STEPS.OPT_DESIGN.TCL.PRE "{pre_opt}" get_runs impl_1]'
        #                        .format(pre_opt=pre_opt))
        #   tcl_cmds_list.append('set_property STEPS.OPT_DESIGN.TCL.POST "{post_opt}" get_runs impl_1]'
        #                        .format(post_opt=post_opt))

        tcl_cmds_list.append('quit')

        self.logger.info('#' * 80)
        logger.info('Project Generation Script:')
        for line in tcl_cmds_list:
            self.logger.info(line)

        self.logger.info('#' * 80)

        return tcl_cmds_list

    def create_quartus_project(self, **kwargs):
        """Creates a ``quartus`` project using supplied settings.

        Copy constraints from ``.qsf`` file line-by-line directly, ignoring blank and commented lines,
        into project file replacing any instance of ``$REPO_PATH`` with ``$env(REPO_ROOT)``.
        Leaves the original constraints file untouched, which should have the same effect as
        having sourced the constraints file.

        Keyword Args:
            **project_name (str, optional): Name of project file to generate.
                Default value: ``'project'``
            **build_path (str): Absolute path to build location for generated project
            **target_language (str, optional): Target default language for the generated project.
                Default value: ``'VHDL_2008'``
            **top_level_entity (str): Top-level HDL entity name.
            **hdl_files_dict (dict): Dictionary of HDL libraries (keys) and list of absolute HDL files.
            **ip_files (list of str): List of absolute paths fof IP files to add to project.
            **constraint_files (list of str): List of absolute paths of constraints to add to project.

        Returns:
            None

        """

        project_name = os.path.splitext(funcs.get_kwarg('project_name', kwargs, 'project'))[0]
        build_path = funcs.get_kwarg('build_path', kwargs, '').replace(self.repo_root, self.tcl_repo_root)
        family = funcs.get_kwarg('family', kwargs, None)
        device = funcs.get_kwarg('device', kwargs, None)
        target_language = funcs.get_kwarg('target_language', kwargs, 'VHDL_2008')
        top_level_entity = funcs.get_kwarg('top_level_entity', kwargs, '')
        hdl_files = funcs.get_kwarg('hdl_files', kwargs, dict())
        ip_files = funcs.get_kwarg('ip_files', kwargs, list())
        constraint_files = funcs.get_kwarg('constraint_files', kwargs, list())

        self.logger.info('Generating Quartus Project...')
        self.logger.info('Project Name: {name}'.format(name=project_name))
        self.logger.info('FPGA Family: {family}'
                         .format(family=family))
        self.logger.info('FPGA Device: {device}'
                         .format(device=device))

        tcl_cmds_list = list(['#' * 80, '## Auto-Generated Project File, Do Not Modify', '#' * 80])
        tcl_cmds_list.append('package require ::quartus::project')
        tcl_cmds_list.append('project_new -family "{family}" -part {device} {project_name}'
                             .format(family=family,
                                     device=device,
                                     project_name=project_name))

        tcl_cmds_list.append('set_global_assignment -name PROJECT_OUTPUT_DIRECTORY {output_path}'
                             .format(output_path=os.path.join(build_path, 'output')))
        tcl_cmds_list.append('set_global_assignment -name VHDL_INPUT_VERSION {vhdl_version}'
                             .format(vhdl_version=target_language))

        tcl_cmds_list.append('set_global_assignment -name TOP_LEVEL_ENTITY {top_level}'
                             .format(top_level=top_level_entity.replace("'", "")))

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding Script Based Parameters:')
        tcl_cmds_list.append('#' * 80)

        tcl_cmds_list.append('set_parameter -name g_board_id {self.board_id}'
                             .format(self=self))

        if self.board_timestamp_enabled:
            timestamp = generate_timestamp()
            self.logger.info('Generated Timestamp: {timestamp}'
                             .format(timestamp=generate_timestamp()))
            tcl_cmds_list.append('set_parameter -name g_board_timestamp {timestamp}'
                                 .format(timestamp=timestamp))

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding HDL Source File(s):')
        tcl_cmds_list.append('#' * 80)
        for src_file_obj in hdl_files:
            tcl_cmds_list.append('set_global_assignment -name VHDL_FILE {hdl_file} -library {lib}'
                                 .format(hdl_file=src_file_obj[1].replace(self.repo_root, self.tcl_repo_root),
                                         lib=src_file_obj[0]))

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding IP Source File(s):')
        tcl_cmds_list.append('#' * 80)

        for ip in ip_files:
            ext = os.path.splitext(ip)[-1].lower()
            if ext == '.qsys':
                tcl_cmds_list.append('set_global_assignment -name QSYS_FILE {ip}'
                                     .format(ip=ip.replace(self.repo_root, self.tcl_repo_root)))
            elif ext == '.ip':
                tcl_cmds_list.append('set_global_assignment -name IP_FILE {ip}'
                                     .format(ip=ip.replace(self.repo_root, self.tcl_repo_root)))
            elif ext == '.qip':
                tcl_cmds_list.append('set_global_assignment -name QIP_FILE {ip}'
                                     .format(ip=ip.replace(self.repo_root, self.tcl_repo_root)))
            else:
                self.logger.critical('Unsupported IP File Type ({ext}): {ip}'
                                     .format(ext=ext, ip=ip))

        tcl_cmds_list.append('#' * 80)
        tcl_cmds_list.append('## Adding Constraints File(s):')
        tcl_cmds_list.append('#' * 80)

        for constr in constraint_files:
            ext = os.path.splitext(constr)[-1].lower()
            if ext == '.qsf':
                with open(constr) as f:
                    for line in f:
                        if line.strip():
                            for r in [self.repo_root, '$REPO_ROOT']:
                                modified_line = line.rstrip().replace(r, self.tcl_repo_root)

                            if modified_line.startswith('##'):
                                self.logger.debug('{old} -> {new}'
                                                  .format(old=line, new=modified_line))
                                tcl_cmds_list.append(modified_line)
                            elif not modified_line.startswith('#'):
                                self.logger.debug('{old} -> {new}'
                                                  .format(old=line, new=modified_line))
                                tcl_cmds_list.append(modified_line)

            elif ext == '.sdc':
                tcl_cmds_list.append('set_global_assignment -name SDC_FILE {constr}'
                                     .format(constr=constr.replace(self.repo_root, self.tcl_repo_root)))
            elif ext == '.tcl':
                tcl_cmds_list.append('set_global_assignment -name TCL_SCRIPT_FILE {constr}'
                                     .format(constr=constr.replace(self.repo_root, self.tcl_repo_root)))
            else:
                self.logger.critical('Unsupported Constraint File Type ({ext}): {constr}'
                                     .format(ext=ext, constr=constr))

        # \todo Add Pre/Post Scripts Here.
        tcl_cmds_list.append('export_assignments')

        self.logger.info('#' * 80)
        logger.info('Project Generation Script:')
        for line in tcl_cmds_list:
            self.logger.info(line)

        self.logger.info('#' * 80)

        return tcl_cmds_list


def generate_timestamp():
    """Generates a Unix 32 Bit Time Stamp from the systems time as an integer value.

    Returns:
        str: Timestamp as an integer for conversion to a VHDL `unsigned` ``std_logic_vector(31 downto 0)``.

    """
    return int(time.time())


def resolve_tool_version(**kwargs):
    """Resolves the tool_version based on vendor

    Keyword Args:
        tool_version (str): Version of tool to resolve.
        vendor (str, optional): Vendor name. Valid values: ``'altera'``, ``'xilinx'``. Default ``'xilinx'``

    Returns:
        str: The resolved ``tool_version`` when successful, otherwise ``False``

    """
    vendor = funcs.get_kwarg('vendor', kwargs, 'xilinx')
    tool_version = funcs.get_kwarg('tool_version', kwargs, None)

    if tool_version:
        if vendor == 'altera':
            return 'quartus_{version}_{release}'.format(version=os.path.split(tool_version)[0],
                                                        release=os.path.split(tool_version)[1])
        else:
            return 'vivado_{release}'.format(release=tool_version)
    else:
        return False


def run_vivado(**kwargs):
    """Runs ``vivado`` in specified mode.

    When running in ``'gui'`` mode, the tcl_file keyword argument is the project file to open.

    .. note::

       The ``shell=True`` in ``check_call`` is important in windows where ``vivado`` is just a bat file.

    Keyword Args:
        **vivado_bin (str, optional): Name of executable to run vivado. Default value: ``'vivado'``
        **mode (str, optional): Name of the mode to run. Valid values: ``'batch'``, ``'tcl'`` or ``'gui'``.
            Default value: ``'batch'``
        **tcl_file_name (str): Absolute path to the ``tcl`` script used by ``vivado`` when running in
            ``'tcl'`` mode, and the project file to open when running in ``'gui'`` mode.
        **tcl_args (str, optional): Additional positional arguments needed to execute ``tcl_file_name``
            Default value: ``None``

    Returns:
        None

    """
    vivado_bin = funcs.get_kwarg('vivado_bin', kwargs, 'vivado')
    mode = funcs.get_kwarg('mode', kwargs, 'batch')
    tcl_file_name = funcs.get_kwarg('tcl_file_name', kwargs, None)
    tcl_args = funcs.get_kwarg('tcl_args', kwargs, None)

    cmd = "{vivado_bin} -nojournal -nolog -notrace".format(vivado_bin=vivado_bin)
    cmd += " -mode {mode} ".format(mode=mode)
    if mode == 'gui':
        cmd += " {tcl_file}".format(tcl_file=os.path.abspath(tcl_file_name))
    else:
        cmd += " -source {tcl_file}".format(tcl_file=os.path.abspath(tcl_file_name))

        if tcl_args is not None:
            cmd += " -tclargs " + " ".join([str(val) for val in tcl_args])

    logger.info('Executing: {cmd}'.format(cmd=cmd))
    check_call(cmd, shell=True)


def run_quartus_sh(**kwargs):
    """Runs ``quartus_sh`` to execute compilation for standard HDL simulation libraries.

    Keyword Args:
        **quartus_bin (str, optional): Name of executable to run quartus. Default value: ``'quartus_sh'``
        **script_mode (bool, optional): Run ``quartus_sh`` in script mode.
            Default value: ``False``
        **
        **tool (str): Name of the tool to run. Should be derived from:
            ``simulator_class = SIMULATOR_FACTORY.select_simulator()``
            ``simname = simulator_class.name``
        **language (str, optional): Valid options: ``'verilog'`` or ``'vhdl'``. Default value: ``'vhdl'``
        **modelsim_path (str): Absolute path to the version of Modelsim to use to compile standard HDL
            libraries.
        **output_path (str): Absolute path where to compile standard HDL libraries.
        **tcl_file_name (str): Absolute path to the ``tcl`` script used by ``vivado``
        **tcl_args (str, optional): Additional positional arguments needed to execute ``tcl_file_name``
            Default value: ``None``
        **gui (bool, optional): Runs Quartus in GUI Mode. Default value: ``False``
        **project_file (str): Absolute path to project file.

    Returns:
        None

    """
    quartus_bin = funcs.get_kwarg('quartus_bin', kwargs, "quartus_sh")
    script_mode = funcs.get_kwarg('script_mode', kwargs, False)
    gui = funcs.get_kwarg('gui', kwargs, False)
    tool = funcs.get_kwarg('tool', kwargs, "quartus")
    language = funcs.get_kwarg('language', kwargs, "vhdl")
    modelsim_path = funcs.get_kwarg('modelsim_path', kwargs, None)
    output_path = funcs.get_kwarg('output_path', kwargs, None)
    tcl_file_name = funcs.get_kwarg('tcl_file_name', kwargs, None)
    tcl_args = funcs.get_kwarg('tcl_args', kwargs, None)
    project_file = funcs.get_kwarg('project_file', kwargs, None)

    if gui:
        cmd = "{quartus_bin}".format(quartus_bin=quartus_bin)
        if project_file:
            cmd += " {project_file}".format(project_file=project_file)

    elif not script_mode:
        cmd = "{quartus_bin} --simlib_comp".format(quartus_bin=quartus_bin)
        cmd += " -tool {tool}".format(tool=tool)
        cmd += " -language {language}".format(language=language)
        cmd += " -tool_path {modelsim_path}".format(modelsim_path=modelsim_path)
        cmd += " -directory {output_path}".format(output_path=output_path)
        cmd += " -family all"
        cmd += " -rtl_only"
    else:
        logger.info('Running {quartus_bin} in Script Mode...'
                    .format(quartus_bin=quartus_bin))
        cmd = "{quartus_bin} -t {tcl_file_name} -v".format(quartus_bin=quartus_bin,
                                                           tcl_file_name=tcl_file_name)

        if tcl_args is not None:
            cmd += " -tclargs " + " ".join([str(val) for val in tcl_args])

    logger.info('Executing: {cmd}'.format(cmd=cmd))
    check_call(cmd, shell=True)


def run_ip_setup_simulation(**kwargs):
    """Executes the Quartus ``run-ip-setup-simulation``

    Executes the ``run-ip-setup-simulation`` to gather simulation setup commands for all Vendor IP libraries
    used in current design.

    Keyword Args:
        **exe (str, optional): Executable to run. Default value: ``'ip-setup-simulation'``
        **project_file (str): Absolute path to project file to process.
        **output_path (str): Absolute path where output files are generated.

    Returns:
        None

    """

    exe = funcs.get_kwarg('exe', kwargs, "ip-setup-simulation")
    project_file = funcs.get_kwarg('project_file', kwargs, None)
    output_path = funcs.get_kwarg('output_path', kwargs, None)

    if not project_file:
        logger.critical('No Project File Supplied. Vendor IP Simulation Files Not Processed')
        return None

    if not output_path:
        logger.critical('No Output Path Supplied. Vendor IP Simulation Files Not Processed')
        return None

    if os.path.isfile(project_file):
        cmd = "{exe}".format(exe=exe)
        cmd += " --quartus-project={project_file}".format(project_file=project_file)
        cmd += " --output-directory={output_path}".format(output_path=output_path)

        logger.info('Executing: {cmd}'.format(cmd=cmd))
        try:
            check_call(cmd, shell=True)
        except CalledProcessError:
            logger.critical('Failed to Generate Simulation Files for Vendor IP (see Report Above): '
                            '{project_file}'
                            .format(project_file=project_file))
    else:
        logger.critical('Can Not Find Project File: {project_file}'
                        .format(project_file=project_file))


def run_ip_generate(**kwargs):
    """Executes the Quartus ``qsys-generate``

    Executes the ``qsys-generate`` to generate Quartus IP.

    Keyword Args:
        **exe (str, optional): Executable to run. Default value: ``'qsys-generate'``
        **ip_file (str): Absolute path to IP file to generate.
        **output_path (str): Absolute path where output files are generated.
        **synth (bool, optional): generate for synthesis if ``True`` otherwise generate for simulation.
            Default value: ``True``
        **synth_language (str, optional): HDL language used to generate synthesis files.
            Valid values: ``'VHDL'`` or ``'VERILOG'``. Default value: ``'VERILOG'``
        **sim_language (str, optional): HDL language used to generate simulation files.
            Valid values: ``'VHDL'`` or ``'VERILOG'``. Default value: ``'VHDL'``
        **family (str, optional): FPGA Family. Default value: ``False``
        **device (str, optional): FPGA Device. Default value: ``False``
        **clean (bool, optional): Cleans IP Path Prior to Generating IP. Default value: ``False``

    Returns:
        None

    """
    exe = funcs.get_kwarg('exe', kwargs, "qsys-generate")
    ip_file = funcs.get_kwarg('ip_file', kwargs, None)
    synth = funcs.get_kwarg('synth', kwargs, True)
    synth_language = funcs.get_kwarg('synth_language', kwargs, 'VERILOG')
    sim_language = funcs.get_kwarg('sim_language', kwargs, 'VHDL')
    family = funcs.get_kwarg('family', kwargs, False)
    device = funcs.get_kwarg('device', kwargs, False)
    output_path = funcs.get_kwarg('output_path', kwargs, None)
    clean = funcs.get_kwarg('clean', kwargs, False)

    if not ip_file:
        logger.critical('No IP File Supplied. Vendor IP Simulation Files Not Generated')
        return None

    if not output_path:
        logger.critical('No Output Path Supplied. Vendor IP Not Generated')
        return None

    if clean:
        logger.info('Cleaning IP Output Path: {output_path}'.format(output_path=output_path))
        funcs.clean_path(path=output_path)

    if os.path.isfile(ip_file):
        cmd = "{exe}".format(exe=exe)
        cmd += " {ip_file}".format(ip_file=ip_file)
        if synth:
            cmd += " --synthesis={synth_language}".format(synth_language=synth_language)
        else:
            cmd += " --simulation={sim_language}".format(sim_language=sim_language)
            cmd += " --allow-mixed-language-simulation"
        cmd += " --output-directory={output_path}".format(output_path=output_path)
        if family:
            cmd += ' --family="{family}"'.format(family=family)
        if device:
            cmd += ' --part="{device}"'.format(device=device)

        logger.info('Executing: {cmd}'.format(cmd=cmd))
        try:
            check_call(cmd, shell=True)
        except CalledProcessError:
            logger.critical('Vendor IP Not Generated (see Report Above): {ip_file}'
                            .format(ip_file=ip_file))
    else:
        logger.critical('Can Not Find Vendor IP File: {ip_file}'
                        .format(ip_file=ip_file))


if __name__ == '__main__':
    pass
else:
    logger.info(__str__)

