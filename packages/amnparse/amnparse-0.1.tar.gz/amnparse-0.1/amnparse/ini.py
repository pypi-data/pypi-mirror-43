from collections import Mapping
import re

class IniParser(Mapping):
    """Class used to parse and output INI files"""
    def __init__(self, path = None):
        """
        Initializes an instance of the class
        Args:
            path (str): Optional file name to parse upon initializing.  Default: None
        """
        self.path = path
        self._dict = {}
        
        # parse if a path was provided; swallows all errors!
        if (self.path is not None):
            try:
                self.from_file()
            except Exception as e:
                pass
    
    # collections.Mapping    
    def __iter__(self):
        return iter(self._dict)
        
    # collections.Mapping
    def __len__(self):
        return len(self._dict)
        
    def __str__(self):
        """
        Returns the groups as an INI-formatted string
        """
        retval = ''
        
        for k in sorted(self._dict):
            retval = retval + "[{}]\n".format(k)
            
            # python 2/3 switch
            if hasattr(self._dict[k], "iteritems") == True:
                for var, val in self._dict[k].iteritems():
                    retval = retval + "{}={}\n".format(var, val)
            else:
                for var, val in iter(self._dict[k].items()):
                    retval = retval + "{}={}\n".format(var, val)
                
            retval = retval + "\n"
            
        return retval
        
    # more collections.Mapping shit
    # fun fact, this class acts like a dict
    def __getitem__(self, k):
        return self._dict[k]
        
    def __setitem__(self, k, v):
        self._dict[k] = v
        
    def __contains__(self, v):
        return v in self._dict
    # end Mapping methods
        
    def add_group(self, name = 'global', reset = True):
        """
        Adds a named group to the config, overwiting it unless specified
        Args:
            name (str): string that denotes the name of the group.  Default: 'global'
            reset (bool): overwrite flag.  If true, the group is reset if it already exists.  Default: True
        """
        if (reset == True):
            self._dict[name] = {}
            
        if name not in self._dict:
            self._dict[name] = {}
            
        return self._dict[name]
        
    def to_file(self, tpath = None):
        """
        Writes the contents (groups + properties) to the provided file path
        Args:
            tpath (str): file path where the INI is written to.  Default: None
        """
        if (tpath is None):
            tpath = self.path
            
        if (tpath is None):
            pass
            
        fh = file(tpath, "w")
        fh.write(self.__str__())
        fh.close()
        
    def from_file(self, fpath = None):
        if (fpath is None):
            fpath = self.path
        else:
            self.path = fpath
            
        self.read_groups(fpath)

    def from_str(self, string):
        self.read_groups_string(string.split("\n"))
        
    def read_groups(self, fpath):
        if (fpath is None or len(fpath) == 0):
            raise ValueError("No file path specified.")
        
        # get each line of our file
        fh = open(fpath, 'r')
        lines = fh.readlines()
        fh.close()
        
        self.read_groups_string(lines)
        
    def read_groups_string(self, lines):
        self._dict.clear()
        
        active_group = None
        
        for line in lines:
            # ignore comments
            mach = re.search(r'^;', line)
            if mach is not None:
                continue
                
            # strip newlines if we got em
            line = re.sub(r'(\r|\n)', '', line)
            # looking for groups
            mach = re.search(r'^\[(.+?)\]', line)
            
            if (mach is not None):
                active_group = mach.group(1)
                self._dict[mach.group(1)] = {}
            elif (mach is None):
                # not a group but a key=val pair
                mach = re.search(r'^(.+?)=(.*)$', line)
                if (mach is not None):
                    if (active_group is not None):
                        var, val = mach.group(1), mach.group(2)
                        if (val is not None and len(val) > 0):
                            self._dict[active_group][var] = val

def parse_ini_file(path):
    """
    Creates an IniParser instance and parses the provided file
    Args:
        path (str): Path to an INI file to parse
    """
    inst = IniParser()
    # raise all exceptions!
    inst.from_file(path)
    return inst
    
def parse_ini_string(string):
    """
    Creates an IniParser instance and parses the provided text
    Args:
        string (str): text in INI configuration file format
    """
    inst = IniParser()
    inst.from_str(string)
    return inst