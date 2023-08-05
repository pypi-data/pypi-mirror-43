#!/usr/bin/python
from RoboteqCommand import RoboteqCommand, RuntimeCommand, RuntimeQuery, ConfigSetting
import CppHeaderParser
import sys
# set sys in order to be able to locate header fileself.
sys.path = ["../"] + sys.path


# TODO move Roboteq Importer to its own module
class RoboteqCommandImporter():
    """Blank base class for all file importer to inherit from
    By default, it imports serialized python data directly
    with eval(). So we can print a dictionary and it will"""
    # We have to give the importer the source of all the commands to be imported
    # This can be a file name or a

    def __init__(self, _importPath):
        self.Path = _importPath

    # gernates command dictionary from printed dictionary value, should be overwriten
    def generateCommandDict(self):
        with open(self.Path, 'r') as Source:
            commandDict = eval(Source.read())
            # TODO Check that code actually evaluates to a dictionary
            # TODO will have to change If I can't build it into a custom datastructure.
            return commandDict

    # This is a class mehtod that you can use to automatically import a source
    # without keeping the importer arround
    @classmethod
    def RoboteqImport(cls, _importPath):
        Importer = cls(_importPath)
        return Importer.generateCommandDict()

    # TODO add methods to merge multiple sources, specify imports from different devices
    # TODO consider mehtods to export dictionaries
    # TODO Dictionaries should eventually be replaced with custom datastructure that are special for Roboteq commands. Should refactor so that all code uses This


class RoboteqCPPImporter(RoboteqCommandImporter):
    """sub class of Roboteq Comand importer for importing from header files from the RoboteQ C++ install_dependencies
    In these headers, commands are given as a series of defines in the form of:
    #define CMDSTR BASE10HEXID
    CMDSTR: the command's roboteq identity string. This is the string you use in microbasic.
    BASE10HEXID: the command's hex id, but represented in decimal."""

    def __init__(self, _importPath):
        super(RoboteqCPPImporter, self).__init__(_importPath)

        try:
            self.cppHeader = CppHeaderParser.CppHeader(self.Path)
        except CppHeaderParser.CppParseError as e:
            print('CppHeaderParser encountered Error:' + e)

    def generateCommandDict(self):

        RoboteqCommandDict = dict()

        for define in self.cppHeader.defines:
            command = define.split(' ')
            if len(command) == 2:
                 # TODO try to optimize this code to perform proper data access for fast operation.
                 # TODO there is definitely a better way to do the string formatting in python
                 # The formatting of the print statement comes from the round about way that values are #defined in the Roboteq CPP install_dependencies
                 # Their identity string is defined as a decimal representation of their HEX valueself.
                 # we need to do all of that conversion here in order to make this work with Roboteq Command Generator.
                 RoboteqCommandDict[command[0]] = RoboteqCommand(command[0][1:], int(command[1]))

        return RoboteqCommandDict
