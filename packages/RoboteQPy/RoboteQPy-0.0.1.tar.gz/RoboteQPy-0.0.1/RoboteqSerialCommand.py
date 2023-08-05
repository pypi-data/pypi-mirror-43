#TODO Figure out some way to unit test thing thing

import RoboteqCommand
import serial
import io

#General purpose commander on a StringIO object.
#Can use this class to mock behavior of RoboteQ command classes in Unittests
class RoboteqSerialCommander(RoboteqCommand.RoboteqCommander):


    @classmethod
    def connectOverRS232(cls, _TokenList,*SerialArgs):
        """Function decorator to create serial object on the fly using provided settings"""
        ser = serial.Serial(*SerialArgs, timeout = .01)  #specify default timeout of 1 sec using timeout keyord arg
        sio = sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
        Serialcommander1 = cls(_TokenList, sio)
        return Serialcommander1


    #TODO Iplement exception raising if there is no response from Roboteq Device, or if somehting else goes wrong with the serial connection.
    def _SubmitOutput(self, commandString):
        """Function to return command string to Roboteq Device
        Should be redefined in inherited classes to interface over any port
        Aruments: commandString - string commander should send to RoboteQ Device
        Returns: Will retrun a string that is the response from the Roboteq Device"""
        #Submits to user supplied outputStream
        #may want to save this functionality for derived classes
        outputString = commandString + '_'
        print(outputString)
        self.outputStream.write(outputString)    #Roboteq Devices accept the underscore charcter as a command terminator
        self.outputStream.flush()
        #TODO there has got to be a better way of doing this than 2 readlines
        self.outputStream.readline()
        controllerResponse = self.outputStream.readline()
        return controllerResponse
