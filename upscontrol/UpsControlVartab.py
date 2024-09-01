# A very simple hierachical data storage

import json
import os
from copy import deepcopy

class VarTabException(Exception):
    pass

class VarTab():
    MAX_RECURSION = 10

    def __init__(self, config_file=None):
        self.__config_file = config_file
        self.__data = {}

    def Load(self, config_file = None, init=None):
        if config_file is None:
            config_file = self.__config_file

        try:
            # Try to load config file
            with open(config_file, "r") as f:
                self.__data = json.load(f)

        except:
            # No config file, so try to init from initial data
            if init is None:
               raise VarTabException("No initial config specified")

            else:
                self.__data = deepcopy(init)
                
    def __create_file_with_mode(self, path, flags, mode):
        print("__create_file_with_mode: %s flags %o mode %o" % (path, flags, mode))
        oldmask = os.umask(0)
        f = os.open(path, flags, mode)
        # If file already exists, set mode to override
        os.chmod(path, mode)
        # Put the mask back
        os.umask(oldmask)
        return f

    def Save(self, config_file = None, mode = 0o600):
        if config_file is None:
            config_file = self.__config_file

        if config_file is None:
            raise VarTabException("No config file specified")

        try:
            with open(config_file, "w", opener=lambda path, flags: self.__create_file_with_mode(path, flags, mode)) as f:
                f.write(json.dumps(self.__data, indent=4, sort_keys=True))
        except Exception as e:
            print("VarTab.Save: %s" % str(e))

    def GetAllValues(self):
        return deepcopy(self.__data)

    def SetAllValues(self, values):
        self.__data = deepcopy(values)

    def __getitem__(self, key=None):
        return self.GetValue(key)

    def __setitem__(self, key, value):
        self.SetValue(key, value)

    def FindValue(self, varname, subvar=None, write=False):
        varvalue = self.__data if subvar is None else subvar

        for piece in varname.split("."):
            # print("FindValue: piece %s varvalue %s" % (piece, varvalue))
            if type(varvalue) is dict:
                if piece in varvalue:
                    varvalue = varvalue[piece]
                elif write:
                    # We are setting values, so create the dictionary entry here
                    varvalue[piece] = {}
                    varvalue = varvalue[piece]
                else:
                    raise VarTabException("Undefined: %s in %s" % (piece, varname))
            elif piece == '':
                raise VarTabException("Ran out of subfields looking for %s" % (varname))
            else:
                raise VarTabException("Trying to get element %s in non-dictionary" % (piece))

        return varvalue

    # Return a value if present, else exception thrown for undefined
    # If no value given, returns entire tree
    def GetValue(self, varname="", subvar=None, evaluate=True, recursion=0):
        if recursion > self.MAX_RECURSION:
            raise VarTabException("recursion overflow looking for %s" % (varname))

        if varname == "":
            return self.__data if subvar is None else subvar

        value = self.FindValue(varname, subvar=subvar)

        if evaluate:
            # Process any macros in the varname
            if type(value) is str:
                working = True
                while working:
                    # Look for start of macro
                    start = value.find("${")
                    if start >= 0:
                        # Look for end of macro
                        end = value.find("}", start + 2)
                        if end >= 0:
                            newvalue = self.GetValue(value[start+2:end], recursion=recursion + 1, evaluate=evaluate)
    
                            # String replacement within the text
                            value = value[:start] + str(newvalue) + value[end+1:]
                        else:
                            working = False
                    else:
                        working = False
    
            if type(value) == str:
                # If $evel{xxx} then evaluate expression to get return value
                start = value.find("$eval{")
                if start >= 0:
                    end = value.find("}", start+6)
                    if end >= 0:
                        value = eval(value[start+6:end])

        return value

    def SetValue(self, varname, value, subvar=None, protect=True):
        try:
            first, last = varname.rsplit('.', maxsplit=1)
            subvar = self.FindValue(first, subvar=subvar, write=True)

        except:
            subvar = self.__data if subvar is None else subvar
            last = varname

        # print("SetValue: protect %s subvar %s" % (protect, subvar))

        if protect and last in subvar and type(subvar[last]) is str and (subvar[last].find("$eval{") >= 0 or subvar[last].find("${") >= 0):
            raise VarTabException("Var %s contains evaluated field and not overriden: %s" % (varname, subvar[last]))

        else:
            subvar[last] = value

