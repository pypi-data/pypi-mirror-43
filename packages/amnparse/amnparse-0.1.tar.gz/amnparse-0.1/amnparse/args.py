import shlex

class ArgsParser(object):
    """Class that brings getopt-like functionality to Python"""
    def __init__(self, fmt):
        self.fmt = fmt
        self.longest = max(fmt, key=len)

    @classmethod
    def from_str(self, string):
        return shlex.split(string)
        
    def __contains__(self, serch):
        return serch in self.fmt
        
    def parse(self, args, block = None):
        skip_next = False
        
        for idx, arg in enumerate(args):
            if skip_next == True:
                skip_next = False
                continue
                
            if len(arg) > 1 and arg[0] == '-' and arg[1] != '-':
                for flag in list(arg):
                    for fmtspec, val in self.fmt.iteritems():
                        if fmtspec != "-{}".format(flag):
                            continue
                        
                        param = None
                        
                        if val[0] == True:
                            param = args[idx + 1]
                            skip_next = True
                            
                        if block is not None:
                            block(fmtspec, idx, param)
            else:
                if block is not None:
                    block(None, idx, arg)
                    
    def usage(self):
        txt = ["\nOPTIONS:\n"]
        
        for entry in sorted(self.fmt):
            fmtspec, val = entry, self.fmt[entry]
            
            if val[0] == True:
                opt = " <opt>  "
            else:
                opt = "        "
                
            txt.append("   {}{}{}".format(fmtspec.ljust(len(self.longest)), opt, val[1]))
        
        txt.append("")
        return "\n".join(txt)
        
    def arg_required(self, opt):
        if opt in self.fmt:
            return self.fmt[opt][0]