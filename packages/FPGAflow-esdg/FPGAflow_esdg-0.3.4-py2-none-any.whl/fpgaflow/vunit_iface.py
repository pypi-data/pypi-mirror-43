# -*- coding: utf8 -*-
"""

******************
``vunit_iface.py``
******************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE

``vunit_iface.py`` is a module to handle interfacing and utilising external ``VUnit`` module.

See `VUnit Documentation <https://vunit.github.io/documentation.html>`_.

"""
import helpers.customlogging as log
import helpers.arguments as arguments
import helpers.version as my_version
import helpers.funcs as funcs
import fpgavendor_iface as fpgavendor_iface

import os
import collections
from vunit import VUnit
from vunit.simulator_factory import SIMULATOR_FACTORY

logger = log.config_logger(name=__name__)
LOGLEVEL = log.LogLevelsConsts

rev = filter(str.isdigit, "$Rev$")  # Do Not Modify this Line
version = my_version.Version(0, 2, 0, svn_rev=rev, disable_svn_logging=True)
__version__ = version.get_version()
__str__ = my_version.about(__name__, __version__, version.revision)


class VUnitProject(object):
    """VUnit Project is a VUnit object used to configure and execute simulation test-cases.

    Keyword Args:
        **simulation_path (str): Absolute simulation root path for the VUnit project.
        **sim_pre_compiled_libs (str): Absolute path to the location for precompiled simulation libraries.
        **fpga_vendor (str): FPGA Vendor. Used to determine build and precompiled library locations.
            Valid values: ``'xilinx'`` and ``altera'``. Default value: ``'xilinx'``
        **fpga_toolversion (str): FPGA Tool Version. Used to determine build and precompiled library
            locations.
        **sim_version (str): Simulation Version. Used to determine build and precompiled library locations.
        **hdl_lib_file_dict (dict, optional): A dictionary containing library keys and absolute paths to
            files for each library. Default value: ``dict()``
        **args (obj, optional): ``argparse`` object containing arguments passed to script. If one is not
            supplied it will be generated here.
        **use_osvvm (bool, optional): Use OSVVM Components. Default value ``False``
        **use_verification_components (bool, optional): Use ``VUnit`` Verification Components.
            Default value ``False``
        **settings_file (str): Absolute path to settings YAML file, used in logs.
        **clean_precompiled_libs (bool, optional): If ``True`` clean precompiled standard simulation
            libraries for the current project. Default value: ``False``
        **msim_64bit (bool, optional): If ``False`` uses -32bit flag to execute Modelsim.
        **hdl_sim_libs (dict): Dictionary of Vendor Standard HDL Libraries to add to VUnit.
        **modelsim_installdir (str, optional): Absolute path to the Modelsim install directory.
                Used when compiling ``altera`` standard libraries.
        **repo_root (str): Absolute path to the resolved system environment variable ``$REPO_ROOT``.

    Attributes:
        vu (obj): The VUnit object.

    """
    def __init__(self, **kwargs):
        self.logger = log.config_logger(name=__name__, class_name=self.__class__.__name__)
        simulation_path = funcs.get_kwarg('simulation_path', kwargs, '')
        sim_pre_compiled_libs_path = funcs.get_kwarg('sim_pre_compiled_libs_path', kwargs, '')
        clean_precompiled_libs = funcs.get_kwarg('clean_precompiled_libs', kwargs, False)
        fpga_vendor = funcs.get_kwarg('fpga_vendor', kwargs, 'xilinx')
        fpga_toolversion = funcs.get_kwarg('fpga_toolversion', kwargs, '')
        sim_version = funcs.get_kwarg('sim_version', kwargs, '')
        settings_file = funcs.get_kwarg('settings_file', kwargs, '')
        msim_64bit = funcs.get_kwarg('msim_64bit', kwargs, False)
        hdl_sim_libs = funcs.get_kwarg('hdl_sim_libs', kwargs, dict())
        modelsim_installdir = funcs.get_kwarg('modelsim_installdir', kwargs, '')
        setattr(self, 'repo_root', funcs.get_kwarg('repo_root', kwargs, None))
        setattr(self, 'fpga_vendor', fpga_vendor)
        setattr(self, 'fpga_toolversion', fpga_toolversion)

        self.logger.debug('Simulation Output Path: {simulation_path}'
                          .format(simulation_path=simulation_path))
        self.logger.debug('Simulation Precompiled Library Path: {sim_pre_compiled_libs_path}'
                          .format(sim_pre_compiled_libs_path=sim_pre_compiled_libs_path))
        self.logger.debug('FPGA Vendor: {self.fpga_vendor}'
                          .format(self=self))
        self.logger.debug('FPGA Tool Version: {self.fpga_toolversion}'
                          .format(self=self))
        self.logger.debug('Simulation Tool Version: {sim_version}'
                          .format(sim_version=sim_version))

        setattr(self, 'sim_pre_compiled_libs_path', os.path.join(sim_pre_compiled_libs_path,
                                                                 self.fpga_vendor,
                                                                 self.fpga_toolversion,
                                                                 sim_version))

        setattr(self, 'simulation_path', os.path.join(simulation_path,
                                                      sim_version))

        self.logger.info('[VUnit] Simulation Path: {self.simulation_path}'
                         .format(self=self))

        self.logger.info('[VUnit] Precompiled Libraries Path: {self.sim_pre_compiled_libs_path}'
                         .format(self=self))

        hdl_lib_file_dict = funcs.get_kwarg('hdl_lib_file_dict', kwargs, dict())
        args = funcs.get_kwarg('args', kwargs, arguments.Arguments())

        use_osvvm = funcs.get_kwarg('use_osvvm', kwargs, False)
        use_verification_components = funcs.get_kwarg('use_verification_components', kwargs, False)

        vunit_output_path = os.path.join(self.simulation_path,
                                         getattr(args, 'output_path', 'vunit_output'))

        vunit_xml_report = os.path.join(vunit_output_path,
                                        getattr(args, 'xunit_xml', 'xunit_report.xml'))

        self.logger.info('[VUnit] Output Path: {path}'
                         .format(path=vunit_output_path))
        self.logger.info('[VUnit] XML Report: {path}'
                         .format(path=vunit_xml_report))

        setattr(args, 'output_path', vunit_output_path)
        setattr(args, 'xunit_xml', vunit_xml_report)

        self.vu = VUnit.from_args(args=args)
        if use_osvvm:
            self.logger.info('[VUnit] Enabling OSVVM')
            self.vu.add_osvvm()
        if use_verification_components:
            self.logger.info('[VUnit] Using VUnit Verification Components')
            self.vu.add_verification_components()

        self.add_hdl_files(hdl_lib_file_dict=hdl_lib_file_dict)

        self.compile_standard_libraries(sim_pre_compiled_libs=self.sim_pre_compiled_libs_path,
                                        standard_lib_subpath='standard',
                                        fpga_vendor=self.fpga_vendor,
                                        settings_file=settings_file,
                                        clean=clean_precompiled_libs,
                                        msim_64bit=msim_64bit,
                                        hdl_sim_libs=hdl_sim_libs,
                                        modelsim_installdir=modelsim_installdir)

    def get_compile_order(self, **kwargs):

        top_level_file = funcs.get_kwarg('top_level_file', kwargs, '')
        top_level_lib = funcs.get_kwarg('top_level_lib', kwargs, '')

        if os.path.isfile(top_level_file):
            source_file_obj = self.vu.get_source_file(top_level_file, top_level_lib)
            ordered_source_files = self.vu.get_compile_order([source_file_obj])
            return ordered_source_files
        else:
            return None

    def add_hdl_files(self, **kwargs):
        """Adds HDL Files to corresponding library.

        Keyword Args:
            **hdl_lib_file_dict (dict): A dictionary containing library keys and absolute paths to
                files for each library.

        Returns:
            None

        """
        hdl_lib_file_dict = funcs.get_kwarg('hdl_lib_file_dict', kwargs, dict())

        if isinstance(hdl_lib_file_dict, (dict, )):
            self.logger.info('[VUnit] Adding Files to Corresponding Library:')
            for k, v in hdl_lib_file_dict.items():
                lib = self.vu.add_library(k)
                for f in v:
                    self.logger.info('[VUnit]\t{lib}.{file}'.format(lib=k, file=f))
                    lib.add_source_file(f, no_parse=False)

    def setup_simulation_options(self, **kwargs):
        """Sets up the compile and sim options.

        Keyword Args:
            **vendor (str, optional): Name of the FPGA vendor to determine options to set. Sets
                generic options if not supplied.
            **glbl (bool, optional): Include glbl dependency. Default value: ``False``
            **glbl_lib (str, optional): Library to add glbl to. Default value: ``'xil_defaultlib'``

        Returns:
            None

        """
        vendor = funcs.get_kwarg('vendor', kwargs, False)
        glbl = funcs.get_kwarg('glbl', kwargs, False)
        glbl_lib = funcs.get_kwarg('glbl_lib', kwargs, 'xil_defaultlib')

        logger.info('[VUnit] Setting Modelsim Compilation and Simulation Flags...')

        self.vu.set_sim_option("disable_ieee_warnings", True, allow_empty=True)

        if vendor == 'xilinx':
            self.vu.set_compile_option("modelsim.vlog_flags",
                                       ["-O0", "+define+den1024Mb", "+define+SIM_SPEED_UP"])
            if glbl and isinstance(glbl_lib, (str, )) and glbl_lib != '':
                glbl_flag = glbl_lib + ".glbl"
                self.vu.set_sim_option("modelsim.vsim_flags",
                                       ["-t ps", "-coverage", "-voptargs=+acc", glbl_flag], allow_empty=True)
            else:
                self.vu.set_sim_option("modelsim.vsim_flags",
                                       ["-t ps", "-coverage", "-voptargs=+acc"], allow_empty=True)

        elif vendor == 'altera':
            self.vu.set_compile_option("modelsim.vlog_flags",
                                       ["+define+den1024Mb"])

            self.vu.set_sim_option("modelsim.vsim_flags",
                                   ["-t ps", "+nowarnTFMPC", "-voptargs=+acc"], allow_empty=True)

            # self.vu.set_sim_option("modelsim.vsim_flags",
            #                        ["-t ps -pli", "+nowarnTFMPC", "-voptargs=+acc"], allow_empty=True)
        else:
            self.vu.set_compile_option("modelsim.vlog_flags",
                                       ["-O0", "+define+den1024Mb", "+define+SIM_SPEED_UP"])

            self.vu.set_sim_option("modelsim.vsim_flags",
                                   ["-t ps", "-coverage", "-voptargs=+acc"], allow_empty=True)

        logger.info('[VUnit] Done Setting Modelsim Compilation and Simulation Flags')

    def configure_gui(self, **kwargs):
        """Pre-processing of additional simulation init file to use when GUI mode is enabled.

        Keyword Args:
            **sim_init_script (str): Absolute path to initialisation file for GUI mode.
            **repo_root (str): Replacement str for $REPO_ROOT.

        Returns:
            None

        """
        sim_init_script = funcs.get_kwarg('sim_init_script', kwargs, False)
        repo_root = funcs.get_kwarg('repo_root', kwargs, False)

        if sim_init_script and sim_init_script != "":
            self.logger.info('[VUnit] Pre-processing GUI Init Script: {file}'
                             .format(file=sim_init_script))

            resolved_gui_init_script = self.resolve_gui_init_script(sim_init_script=sim_init_script,
                                                                    repo_root=repo_root)

        if resolved_gui_init_script:
            logger.info('[VUnit] Adding Simulation GUI Initialisation Script to Simulation: {file}'
                        .format(file=resolved_gui_init_script))
            self.vu.set_sim_option("modelsim.init_file.gui", resolved_gui_init_script, allow_empty=True)

    def resolve_gui_init_script(self, **kwargs):
        """Parses Simulation GUI Initialisation Script

        There appears to be an issue with Modelsim directly using $env(REPO_ROOT) in scripts
        passed from ``VUnit`` to Modelsim, so this workaround creates a file with ``REPO_ROOT`` resolved
        and uses the created resolved file instead:

        Keyword Args:
            **sim_init_script (str): Absolute path to initialisation file to resolve.
            **repo_root (str): Replacement str for $REPO_ROOT.

        Returns:
            str:

        """
        sim_init_script = funcs.get_kwarg('sim_init_script', kwargs, False)
        repo_root = funcs.get_kwarg('repo_root', kwargs, False)

        if sim_init_script and sim_init_script != "":
            try:
                with open(sim_init_script) as f:
                    init_cmds = f.readlines()
                init_cmds = [x.strip() for x in init_cmds]
                resolved_init_cmds = list()
                self.logger.info('[VUnit] Resolving $REPO_ROOT in Simulation Initialisation File: {file}'
                                 .format(file=sim_init_script))

                for cmd in init_cmds:
                    resolved_cmd = cmd.replace('$env(REPO_ROOT)', repo_root)
                    resolved_init_cmds.append(resolved_cmd)
                    self.logger.debug('\t{} --> {}'
                                      .format(cmd, resolved_cmd))

                sim_init_temp_file = os.path.splitext(sim_init_script)
                sim_init_temp_file = sim_init_temp_file[0] + '_resolved' + sim_init_temp_file[1]
                logger.info('[VUnit] Writing Resolved Simulation Initialisation File: {file}'
                            .format(file=sim_init_temp_file))

                with open(sim_init_temp_file, 'w') as f:
                    for cmd in resolved_init_cmds:
                        f.write('{line}\n'
                                .format(line=cmd))

                return sim_init_temp_file

            except TypeError:
                self.logger.critical('[VUnit] Could Not Open Simulation Init File: {file}'
                                     .format(file=sim_init_script))
                return False

        else:
            return False

    def compile_standard_libraries(self, **kwargs):
        """Compiles Standard Simulation Libraries

        This method is derived from :
        `VUnit supplied example <https://github.com/VUnit/vunit/blob/master/examples/vhdl/vivado/vivado_util.py>`_

        Keyword Args:
            **sim_pre_compiled_libs (str, optional): Absolute path to the location for precompiled simulation
                libraries. Default value: ``self.sim_pre_compiled_libs_path``
            **standard_lib_subpath (str, optional): Name of standard library subpath.
                Default value: ``'standard'``
            **fpga_vendor (str): FPGA Vendor. Valid values: ``'xilinx'`` or ``'altera'``.
            **settings_file (str): Absolute path to settings YAML file, used in logs.
            **clean (bool, optional): If ``True`` cleans the standard library path.
                Default value: ``False``
            **msim_64bit (bool, optional): If ``False`` uses -32bit flag to execute Modelsim.
                Default value: ``False``
            **hdl_sim_libs (dict): Dictionary of Vendor Standard HDL Libraries to add to VUnit.
            **modelsim_installdir (str, optional): Absolute path to the Modelsim install directory.
                Used when compiling ``altera`` standard libraries.

        Returns:
            bool: ``True`` when successful, ``False`` when unsuccessful.

        """
        sim_pre_compiled_libs_path = funcs.get_kwarg('sim_pre_compiled_libs_path', kwargs,
                                                     self.sim_pre_compiled_libs_path)
        standard_lib_subpath = funcs.get_kwarg('standard_lib_subpath', kwargs, 'standard')
        fpga_vendor = funcs.get_kwarg('fpga_vendor', kwargs, 'xilinx')
        settings_file = funcs.get_kwarg('settings_file', kwargs, '')
        clean = funcs.get_kwarg('clean', kwargs, False)
        msim_64bit = funcs.get_kwarg('verilog_sim_libs', kwargs, False)
        hdl_sim_libs = funcs.get_kwarg('hdl_sim_libs', kwargs, dict())
        modelsim_installdir = funcs.get_kwarg('modelsim_installdir', kwargs, '')

        standard_library_path = os.path.join(sim_pre_compiled_libs_path, standard_lib_subpath)
        self.logger.info('[VUnit] Standard Library Compilation Path: {path}'
                         .format(path=standard_library_path))

        if not os.path.exists(standard_library_path):
            self.logger.warning('[VUnit] Missing Output Path for Standard Libraries: {path}'
                                .format(path=standard_library_path))
            self.logger.warning('\tCreating Directory for Standard Libraries...')
            os.makedirs(standard_library_path)
            logger.warning('\tCreated Directory for Standard Libraries: {path}'
                           .format(path=standard_library_path))
        else:
            logger.info('[VUnit] Using Output Path for Standard Libraries: {path}'
                        .format(path=standard_library_path))

        done_token = os.path.join(standard_library_path, 'all_done.txt')

        if os.path.isfile(done_token):
            if not clean:
                self.logger.info('[VUnit] Standard Libraries Already Compiled...')
                self.logger.info("[VUnit] To Recompile Standard Libraries Use Argument: "
                                 "'--clean precompiled_sim'")

                self.add_standard_libraries(standard_library_path=standard_library_path,
                                            hdl_sim_libs=hdl_sim_libs)

                return True

            else:
                self.logger.warning('[VUnit] Cleaning Precompiled Simulation Libraries: {path}'
                                    .format(path=standard_library_path))
                funcs.clean_path(path=standard_library_path)
                self.logger.info('[VUnit] Cleaned Precompiled Simulation Libraries: {path}'
                                 .format(path=standard_library_path))

        tcl_args = list()
        self.logger.info('[VUnit] Precompiling Standard Libraries into: {path}'
                         .format(path=standard_library_path))

        try:
            simulator_class = SIMULATOR_FACTORY.select_simulator()
            simname = simulator_class.name
            if fpga_vendor == 'xilinx':
                if simname == "rivierapro":
                    simname = "riviera"
            tcl_args.append(simname)
            tcl_args.append(simulator_class.find_prefix().replace("\\", "/"))
            tcl_args.append(standard_library_path)

            if msim_64bit:
                tcl_args.append('True')
            else:
                tcl_args.append('False')

        except AttributeError:
            self.logger.critical('[VUnit] Simulator Class Error. Standard Libraries Not Compiled Correctly.')
            return False

        if fpga_vendor == 'xilinx':
            self.logger.info('[VUnit] Running Vivado to Compile Standard HDL Libraries...')
            fpgavendor_iface.run_vivado(vivado_bin='vivado',
                                        mode="batch",
                                        tcl_file_name=os.path.join(os.path.dirname(__file__),
                                                                   'tcl',
                                                                   'compile_standard_libs.tcl'),
                                        tcl_args=tcl_args)

        elif fpga_vendor == 'altera':
            self.logger.info('[VUnit] Running Quartus ro Compile Standard HDL Libraries...')
            fpgavendor_iface.run_quartus_sh(quartus_bin='quartus_sh',
                                            script_mode=False,
                                            tool=simname,
                                            language='verilog',
                                            modelsim_path=modelsim_installdir,
                                            output_path=standard_library_path)

            fpgavendor_iface.run_quartus_sh(quartus_bin='quartus_sh',
                                            script_mode=False,
                                            tool=simname,
                                            language='vhdl',
                                            modelsim_path=modelsim_installdir,
                                            output_path=standard_library_path)

        self.logger.info('Successfully Compiled Standard Libraries')
        with open(done_token, "w") as fptr:
            fptr.write("done")

        self.add_standard_libraries(standard_library_path=standard_library_path,
                                    hdl_sim_libs=hdl_sim_libs)

        return True

    def add_standard_libraries(self, **kwargs):
        """Adds Standard Simulation Libraries to VUnit

        This method is derived from :
        `VUnit supplied example <https://github.com/VUnit/vunit/blob/master/examples/vhdl/vivado/vivado_util.py>`_

        Keyword Args:
            **vunit_obj (obj, optional): A VUnit object. Default value: ``self.vu``
            **standard_library_path (str, optional): Absolute path to the location for precompiled simulation
                libraries. Default value: ``self.sim_pre_compiled_libs_path``
            **hdl_sim_libs (dict): Dictionary of Vendor Standard HDL Libraries to add to VUnit.

        Returns:
            bool: ``True`` when successful, ``False`` when unsuccessful.

        """
        vunit_obj = funcs.get_kwarg('vunit_obj', kwargs, self.vu)
        standard_library_path = funcs.get_kwarg('standard_library_path', kwargs, list())
        hdl_sim_libs = funcs.get_kwarg('hdl_sim_libs', kwargs, dict())

        self.logger.info('[VUnit] Adding Compiled Standard VHDL and Verilog Libraries to VUnit...')
        for k, v in hdl_sim_libs.items():
            self.logger.debug('{key}: {value}'.format(key=k, value=v))
            if 'verilog' in k:
                path = os.path.join(standard_library_path, 'verilog_libs')
            elif 'vhdl' in k:
                path = os.path.join(standard_library_path, 'vhdl_libs')
            else:
                path = standard_library_path
            try:
                if isinstance(v, (list, )):
                    for lib in v:
                        if os.path.exists(os.path.join(path, lib)):
                            self.logger.info('\t{lib}:{path}'
                                             .format(lib=lib, path=os.path.join(path, lib)))
                            vunit_obj.add_external_library(lib, os.path.join(path, lib))
                        elif os.path.exists(os.path.join(standard_library_path, lib)):
                            self.logger.info('\t{lib}:{path}'
                                             .format(lib=lib, path=os.path.join(standard_library_path, lib)))
                            vunit_obj.add_external_library(lib, os.path.join(standard_library_path, lib))
                        else:
                            self.logger.critical('Can Not Find Precompiled Standard Library: [{lib}]'
                                                 .format(lib=lib))
                            self.logger.critical('\tTried: {path}'
                                                 .format(path=os.path.join(path, lib)))
                            self.logger.critical('\tTried: {path}'
                                                 .format(path=os.path.join(standard_library_path, lib)))
            except ValueError:
                self.logger.warning('[VUnit] Skipping. Library Already Exists in VUnit Object: {lib}'
                                    .format(lib=lib))

    def compile_project_ip(self, **kwargs):
        """Compiles FPGA Project Specific IP Simulation Libraries

        Keyword Args:
            **project_file (str): Absolute path to project file to parse.
            **simulation_path (str, optional): Absolute path to the location for simulation path
                Default value: ``self.simulation_path``
            **project_ip_subpath (str, optional): Name of project_ip libraries subpath.
                Default value: ``'project_ip'``
            **msim_setup_script (str, optional): Filename of ``.tcl`` to compile Vendor IP simulation files
                in Modelsim. Default value: ``'mentor/msim_setup.tcl'``
            **top_level_lib (str, optional): Top-level library to add  Vendor IP simulation file to
                in Modelsim, if ``False`` the library name will match the filename, as configured in the
                generated ``.qip`` file. Default value: ``False``

        Returns:
            None

        """
        project_file = funcs.get_kwarg('project_file', kwargs, None)
        simulation_path = funcs.get_kwarg('simulation_path', kwargs, self.simulation_path)
        project_ip_subpath = funcs.get_kwarg('project_ip_subpath', kwargs, 'project_ip')
        msim_setup_script = funcs.get_kwarg('msim_setup_script', kwargs, 'mentor/msim_setup.tcl')
        top_level_lib = funcs.get_kwarg('top_level_lib', kwargs, False)

        if not project_file:
            self.logger.critical('[VUnit] No Project File Supplied. Vendor IP Simulation Files Not Processed')
            return None
        else:
            self.logger.info('[VUnit] Parsing {project_file} for Vendor IP Simulation'
                             .format(project_file=project_file))

        project_ip_path = os.path.join(simulation_path,
                                       project_ip_subpath,
                                       self.fpga_vendor,
                                       self.fpga_toolversion)

        compile_order_file = os.path.join(project_ip_path, "compile_order.txt")

        self.logger.info('[VUnit] Compiling Project Vendor IP...')
        self.logger.info('[VUnit] Project IP Compilation Path: {path}'
                         .format(path=project_ip_path))

        if not os.path.exists(project_ip_path):
            self.logger.info('[VUnit] Creating Path: {path}'.format(path=project_ip_path))
            os.makedirs(project_ip_path)

        if self.fpga_vendor == 'xilinx':
            pass
        elif self.fpga_vendor == 'altera':
            self.logger.info('[VUnit] Generating Quartus Project Compile Order into: {f}'
                             .format(f=compile_order_file))
            self.logger.info('[VUnit] Setting Up IP Simulation from Quartus Project File...')
            fpgavendor_iface.run_ip_setup_simulation(exe='ip-setup-simulation',
                                                     project_file=project_file,
                                                     output_path=project_ip_path)

            msim_script = os.path.join(project_ip_path, msim_setup_script)
            if os.path.isfile(msim_script):
                self.logger.info('[VUnit] Mentor Modelsim Setup Script Generated Successfully.')

            else:
                self.logger.critical('[VUnit] Failed to Find Setup Script: {msim_script}'
                                     .format(msim_script=msim_script))
                return None

            line_filter = [self.repo_root]
            lib_filter = "-work "
            compile_order_list = list()
            self.logger.info('[VUnit] Post-Processing Mentor Modelsim Setup Script: {msim_script}'
                             .format(msim_script=msim_script))

            # The following line is a workaround to prevent the top-level hdl file being added to
            # to the simulation compile order file. This file should be present in the simulation as
            # the hdl file connected to the design being simulated.
            last_lib = "lvcom$USER_DEFINED_VHDL_COMPILE_OPTIONS$USER_DEFINED_COMPILE_OPTIONS"

            with open(msim_script, "r") as f:
                for line in f.readlines():
                    for filt in line_filter:
                        if filt in line:
                            src_file = line.split('"')[1::2]
                            lib = line[line.find(lib_filter) + len(lib_filter):-1].replace(" ", "")
                            if last_lib in lib:
                                src_file = [lib.split(last_lib)[1].replace('"', '')]
                                self.logger.info('[VUnit] Top-Level IP HDL File Reached: {src_file}'
                                                 .format(src_file=src_file[0]))
                                if top_level_lib and top_level_lib != "":
                                    lib = top_level_lib
                                else:
                                    lib = os.path.splitext(os.path.split(src_file[0])[1])[0]

                            compile_item = '{lib},{f}'.format(lib=lib, f=src_file[0])
                            self.logger.debug(compile_item)
                            compile_order_list.append(compile_item)

            self.logger.info('[VUnit] Extracted Compile Order from: {msim_script}'
                             .format(msim_script=msim_script))

            self.logger.info('[VUnit] Writing Compile Order File: {f}'
                             .format(f=compile_order_file))

            with open(compile_order_file, "w") as f:
                for line in compile_order_list:
                    f.write(line + '\n')

        self.logger.info('[VUnit] Parsing: {f}'
                         .format(f=compile_order_file))

        compile_order, libraries, include_dirs = self.read_compile_order(filename=compile_order_file)
        self.logger.debug('[VUnit] Compile Order:')
        for co in compile_order:
            self.logger.debug('\t{co}'.format(co=co))

        self.logger.info('[VUnit] Adding Vendor IP Simulation Libraries to VUnit...')
        for lib in libraries:
            if "$" in lib:
                self.logger.critical('[VUnit] Problem Parsing MSIM Result Not Adding Library: {lib}'
                                     .format(lib=lib))
            else:
                self.logger.info('\t{lib}'
                                 .format(lib=lib))
                self.vu.add_library(lib, vhdl_standard="93", allow_duplicate=True)

        previous_source = None
        self.logger.info('[VUnit] Adding Vendor IP Simulation Source Files to VUnit...')
        for lib, fname in compile_order:
            if "$" in lib:
                self.logger.critical('[VUnit] Problem Parsing MSIM Result Not Adding: {lib}.{f}'
                                     .format(lib=lib, f=fname))
            else:
                self.logger.info('\t{lib}.{f}'
                                 .format(lib=lib, f=fname))
                is_verilog = fname.endswith(".v") or fname.endswith(".vp") or fname.endswith(".sv")
                source_file = self.vu.library(lib).add_source_file(fname,
                                                                   no_parse=True,
                                                                   include_dirs=include_dirs
                                                                   if is_verilog else None)

                source_file.add_compile_option("rivierapro.vcom_flags", ["-dbg"])
                source_file.add_compile_option("rivierapro.vlog_flags", ["-dbg"])
                if previous_source is not None:
                    source_file.add_dependency_on(previous_source)
                previous_source = source_file

    def read_compile_order(self, **kwargs):
        """Read the vendor_ip simulation compile order file and filter out duplicate files

        Keyword Args:
            **filename (str): Absolute path to compile order filename to process.

        Returns:
            tuple containing: list of str, set, list of str

        """
        filename = funcs.get_kwarg('filename', kwargs, None)
        compile_order = list()
        unique = set()
        include_dirs = set()
        libraries = set()
        self.logger.info('[VUnit] Processing Compilation Order File: {f}'
                         .format(f=filename))

        with open(filename, "r") as ifile:

            for line in ifile.readlines():
                lib, fname = line.strip().split(",")
                libraries.add(lib)
                # Remove duplicates here
                key = (lib, os.path.basename(fname))
                if key in unique:
                    continue
                unique.add(key)

                if self.is_verilog_header(fname):
                    include_dirs.add(os.path.dirname(fname))
                else:
                    compile_order.append((lib, fname))

        return compile_order, libraries, list(include_dirs)

    @staticmethod
    def is_verilog_header(filename):
        """Checks if filename indicates the file is a verilog header file.

        Args:
            filename (str): Filename to check if it matches the criteria of a verilog header file.

        Returns:
            bool: ``True`` if a verilog header file, otherwise ``False``

        """
        return filename.endswith(".vh") or filename.endswith("_support.v") or filename.endswith("_defines.v")

    def add_vivado_sim_dependencies(self, **kwargs):
        """Add Vivado simulation dependencies to VUnit object

        Keyword Args:
            **vivado_path (str): Absolute path to Vivado.
            **src_paths (list of str, optional): List of absolute paths to search for dependencies relative
                to ``vivado_path``.
                Default value: ``['data/verilog/src']``
            **src_files (list of str, optional): List of source file dependencies.
                Default value: ``['glbl.v']``
            **glbl (bool, optional): Include glbl dependency. Default value: ``False``
            **glbl_lib (str, optional): Library to add glbl to. Default value: ``'xil_defaultlib'``
            **vunit_obj (obj, optional): VUnit object. Default value: ``self.vu``

        Returns:
            bool: ``True`` if successful, ``False`` if unsuccessful

        """
        vivado_path = funcs.get_kwarg('vivado_path', kwargs, False)
        src_paths = funcs.get_kwarg('src_paths', kwargs, ['data/verilog/src'])
        src_files = funcs.get_kwarg('src_paths', kwargs, ['glbl.v'])
        glbl = funcs.get_kwarg('glbl', kwargs, False)
        glbl_lib = funcs.get_kwarg('glbl_lib', kwargs, 'xil_defaultlib')
        vunit_obj = funcs.get_kwarg('vunit_obj', kwargs, self.vu)

        glbl_flag = False

        if isinstance(vivado_path, (str, )) and vivado_path != "":
            self.logger.debug('[VUnit] Vivado Path: {path}'.format(path=vivado_path))
        else:
            self.logger.critical('[VUnit] Incorrect Vivado Path: {path}'.format(path=vivado_path))
            return False

        if glbl:
            for sp in src_paths:
                path = os.path.abspath(os.path.join(vivado_path, sp))
                if os.path.exists(path):
                    for f in src_files:
                        if os.path.isfile(os.path.join(path, f)):
                            full_path = os.path.join(path, f)
                            self.logger.info('[VUnit] Found glbl Source File: {path}'
                                             .format(path=full_path))
                            self.logger.info('[VUnit] Adding glbl Support to: {lib}'
                                             .format(lib=glbl_lib))
                            lib = vunit_obj.library(glbl_lib)
                            lib.add_source_file(full_path, no_parse=False)
                            glbl_flag = True
                            break
        else:
            glbl_flag = True

        if glbl_flag:
            return True
        else:
            return False


if __name__ == '__main__':
    pass
else:
    logger.info(__str__)
