from io import StringIO
from enum import Enum


# TODO consider changing name of this away from the command since it generates confusing conflict with runtime command
class RoboteqCommand:
    """Class to use as generic class for a roboteq command"""
    __slots__ = ('Identity', 'HexID', 'Name', 'Function', 'Aliases')

    def __init__(self, _Identity, _HexID, _Name='', _Function='', _Aliases=None):
        # TODO consider making Requied underlying values immutable after they are initialized, or at least private
        """Constructor: A Roboteq Command
        Required Values:
            Identity: Unique Identity String
            HexID: Underlying Hex value for Command
            Type: Command type, either a runtime command, a runtimequery, or a configuration command

        Optional Arguments:
            Name: Verbose name of Command
            Function: Name of argument to use as function name
            Aliases: Other working aliases that command can be called by in MicroBasic"""
        _Aliases = _Aliases or []
        if isinstance(_Identity, str):
            self.Identity = _Identity
        else:
            raise TypeError("Alias must be a String")
            # TODO check that Alias is all CppHeaderParser
            # TODO add support for multiple aliases
        if isinstance(_HexID, int) and _HexID < 255:
            self.HexID = _HexID
        else:
            raise TypeError("HexID must be a positive number 255 or below")

        self.Name = _Name  # TODO consider manipulating __name__ from these
        self.Function = _Function

    # have to override eq in order to check if commands are equivalent
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__slots__ == other.__slots__
        return False

    def __iter__(self):
        return iter(self.__slots__)

    def items(self):
        for attribute in self.__slots__:
            yield attribute, getattr(self, attribute)


class RuntimeCommand(RoboteqCommand):
    pass


class RuntimeQuery(RoboteqCommand):
    pass


class ConfigSetting(RoboteqCommand):
    pass


class RoboteqCommandLibrary(dict):
    """This structure is going to have to hold a set of RoboteQ commands that can be accessed using their identity stringself.
    Each command must have a unitque identity string. Should also only allow 1 type in each dictionary"""
    pass

# Genreates Roboteqcommands for commanders to use
# acts as base class for Roboteq commanders that actually interact with Roboteq Devices


class RoboteqCommander:
    """This is the core Roboteq Command class, with a generic RoboteqCommander Being an instantiation set up to use basic StringIO

    The intention of this class is to have 3 main stages of commanding:
    1) Construction: Command is constructed with constructOutput(), which creates the actual contents of the CommandDictionary
    2) Formatting: Command is formatted based on the platform and protocol that it is being used on
    3) Submission: Command is submitted to the controllerself.


    This Class is structured like this in order to allow subclasses to be created to work with different platforms and be able to modify each step of the process for outputting to a controllerself.

    By default this class outputs a command string, currently. """

    def __init__(self, _TokenList, _outputStream):
        self.TokenList = _TokenList
        self.outputStream = _outputStream

    def _ConstructOutput(self, CommandType, token, *args):
        """Generates input to Format output as a tuple of """
        output = ''

        output = self.TokenList[token].Identity
        return (CommandType, output, *args)

    def _FormatOutput(self, _args):
        """Generates data chunk that gets sent as an argument to SubmitOutput"""
        CommandType, tokenString, *args = _args
        CommandOutput = [tokenString]
        CommandOutput.extend(str(v) for v in args)
        return CommandType + ' '.join(CommandOutput)


    def _SubmitOutput(self, commandString):
        self.outputStream.write(commandString + "\n")
        controllerResponse = self.outputStream.readline()
        return controllerResponse

    def Command(self, CommandType, token, *args):
        """Accesor method for calling the full Construct->Format->Submit stack"""
        try:
            return self._SubmitOutput(self._FormatOutput(self._ConstructOutput(CommandType, token, *args)))
        except KeyError as err:
            #TODO make this go into a log isntead
            print('Key {0} not found in commander libary!'.format(err))

    # command to call runtime commands
    def setCommand(self, token, *args):
        return self.Command('!', token, *args)

    # command to call runtime queries
    def getValue(self, token, *args):
        return self.Command('?', token, *args)

    # command to set configuration settings
    def setConfig(self, token, *args):
        return self.Command('^',  token, *args)

    # function to get configuration settings
    def getConfig(self, token, *args):
        submitToken = self.TokenList[token].Identity
        return self.Command('~',  token, *args)
