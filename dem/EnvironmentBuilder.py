import os, shutil
import textwrap

import subprocess

import sys
import virtualenv


class EnvironmentBuilder(object):
    @staticmethod
    def build(project, config):
        project_dir = os.path.join(os.getcwd(), '.devenv', project)
        if os.path.exists(project_dir):
            return

        print('[dem] building environment')
        deps_dir = os.path.join(project_dir, 'dependencies')
        downloads_dir = os.path.join(project_dir, 'downloads')

        os.makedirs(project_dir)

        virtualenv.create_environment(project_dir)

        EnvironmentBuilder._install_dem_into_virtual_environment(project_dir, config)

        os.makedirs(deps_dir)
        os.makedirs(downloads_dir)

    @staticmethod
    def _install_dem_into_virtual_environment(project_dir, config):
        if sys.platform == 'win32':
            bin = 'Scripts'
            exe = 'pip.exe'
        else:
            bin = 'bin'
            exe = 'pip'

        cmd = [os.path.join(project_dir, bin, exe)]
        if config.has_http_proxy():
            cmd.extend(['--proxy', config.http_proxy()])
        cmd.extend(['install', 'dem'])
        print(cmd)
        subprocess.call(cmd)

