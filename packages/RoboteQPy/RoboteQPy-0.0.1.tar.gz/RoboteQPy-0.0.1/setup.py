#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'RoboteQPy',
        version = '0.0.1',
        description = 'Module for interfacing Python with RoboteQ Products',
        long_description = 'A library that connects to RoboteQ products over USB, or RS232 serial. Once connected, you can send controller commands to the RoboteQ device.\n                 Further development will focus on helpful funcitons that aid application development as well components that aid in robotics integration.      \n              ',
        author = 'Gabriel Isko',
        author_email = 'gabe.isko@gmail.com',
        license = 'MIT',
        url = 'https://www.roboteq.com',
        scripts = [],
        packages = [],
        namespace_packages = [],
        py_modules = [
            'RoboPy',
            'RoboteqCPPimporter',
            'RoboteqCommand',
            'RoboteqSerialCommand'
        ],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
