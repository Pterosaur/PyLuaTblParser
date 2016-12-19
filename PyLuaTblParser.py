import track_map

class NonePattern(Exception):
    def __init__(self, arg):
        self.__arg = arg
    def __str__(self):
        return self.__arg


class SpaceFilter:
    space_set = set([' ','\t','\n', '\r'])
    def __call__(self, s, pos = 0):
        while pos < len(s) and s[pos] in SpaceFilter.space_set:
            pos+=1
        return pos

def __space_filter(func):
    def wrapper(s = ""):
        pos = SpaceFilter()(s)
        p, t = func(s[pos:])
        if p == 0:
            return 0,t
        else:
            return pos + p, t
    wrapper.__name__ = func.__name__
    return wrapper

class Number:
    def __init__(self,data = 0,key = None): 
        self.__data = data
        self.key = key
    def ToPythonStr(self):
        return str(self.__data)
    def ToLuaStr(self):
        return str(self.__data)
    def GetRawData(self):
        return self.__data

class NumberDelimiter:
    def __FromStr(self, s = ""):
        pos = 0
        is_float = False
        is_number = False
        is_hex = False
        while pos < len(s):
            if s[pos].isdigit():
                is_number = True
                pos += 1
            else:
                #sign
                if pos == 0 and (s[pos] == '-' or s[pos] == '+'):
                    pos += 1
                #dot
                elif s[pos] == '.' and is_float == False:
                    is_float = True
                    pos += 1
                else:
                    break
        if is_number == False:
            return 0,None
        if is_float:
            return pos, Number(float(s[:pos]))
        return pos, Number(int(s[:pos]))
    def FromPythonStr(self, s = ""):
        return self.__FromStr(s)
    def FromLuaStr(self, s = ""):
        return self.__FromStr(s)

class String:
    def __init__(self, s= "", d = "\""):
        self.__data = s
        self.__delimiter = d
    def ToPythonStr(self):
        return self.__delimiter+self.__data+self.__delimiter
    def ToLuaStr(self):
        return self.__delimiter+self.__data+self.__delimiter
    def GetRawData(self):
        return self.__data

class StringDelimiter:
    def __FromStr(self, s = ""):
        pos = 0
        if pos >= len(s) or (s[pos] != '"' and s[pos] !="'"):
            return 0,None
        end_char = s[pos] 
        pos+=1
        while pos < len(s):
            if s[pos] == end_char:
                if s[pos - 1] != '\\':
                    #+1 because of the skipping of the end char --"' or "", for next parser
                    return pos + 1, String(s[1:pos], end_char)        
            pos += 1
        return 0,None
    def FromPythonStr(self, s):
        return self.__FromStr(s)
    def FromLuaStr(self, s = ""):
        return self.__FromStr(s)

class Bool:
    def __init__(self, b = False):
        self.__data = b
    def ToPythonStr(self):
        return str(self.__data)
    def ToLuaStr(self):
        return str(self.__data).lower()
    def GetRawData(self):
        return self.__data

class BoolDelimiter:
    __py_true = "True"
    __py_false = "False"
    __lua_true = "true"
    __lua_false = "false"
    def __FromStr(self, s , false_flag, true_flag):
        if s.find(true_flag) == 0:
            return len(true_flag), Bool(True)
        elif s.find(false_flag) == 0:
            return len(false_flag), Bool(False)
        else :
            return 0, None
    def FromPythonStr(self, s = ""):
        return self.__FromStr(s, BoolDelimiter.__py_false, BoolDelimiter.__py_true)
    def FromLuaStr(self, s = ""):
        return self.__FromStr(s, BoolDelimiter.__lua_false, BoolDelimiter.__lua_true)

class Null:
    def ToPythonStr(self):
        return "None"
    def ToLuaStr(self):
        return "nil"
    def GetRawData(self):
        return None

class NullDelimiter:
    def __FromStr(self, s, flag):
        if s.find(flag) == 0:
            return len(flag),Null()
        return 0, None
    def FromPythonStr(self, s = ""):
        return self.__FromStr(s,"None")
    def FromLuaStr(self, s = ""):
        return self.__FromStr(s,"nil")


def Traits(value):
    # if isinstance(value, int) or isinstance(value, float) or isinstance(value, long):
    #     return Number(value)
    # elif isinstance(value, bool):
    #     return Bool(value)
    # elif value == None:
    #     return Null()
    # elif isinstance(value, str):
    #     return String(value)
    # elif isinstance(value, list):
    #     return List(value)
    # elif isinstance(value, dict):
    #     return Dict(value)
    # else:
    #     raise TypeError
    if isinstance(value, str):
        value = '"%s"' % value
    else:
        value = str(value)
    p, value = PythonStrToStruct(value)
    if p != 0:
        return value
    else:
        raise NonePattern(value)

class List:
    def __init__(self, l = []):
        self.__data = l
    def ToPythonStr(self):
        l_buffer = ""
        for item in self.__data:
            l_buffer += item.ToPythonStr() + ','
        if len(l_buffer) == 0:
            return "[]"
        return "[%s]" % l_buffer[0: len(l_buffer) - 1]
    def ToLuaStr(self):
        l_buffer = ""
        for s in self.__data:
            l_buffer += s.ToLuaStr() + ','
        return "{%s}" % l_buffer
    def GetRawData(self):
        l = []
        for i in self.__data:
            l.append(i.GetRawData())
        return l
    def __getitme__(self, key):
        return self.__data[key].GetRawData()
    def __setitem__(self, key, value):
        self.__data[key] = Traits(value)

class ListDelimiter:
    def __FromStr(self, s , begin_char, end_char, delimiter_char, generator):
        pos = 0
        l = []
        if s[pos] != begin_char:
            return 0,None
        pos += 1
        delimiter_emerge = True
        while pos < len(s):

            if s[pos] == end_char: 
                #+1 because of the skipping of end char --"]", for next parser
                return pos + 1, List(l)
            elif s[pos] == delimiter_char :
                if delimiter_emerge == True:
                    break
                delimiter_emerge = True
                pos += 1
            elif s[pos] in SpaceFilter.space_set:
                pos += 1
            else:
                if delimiter_emerge == False:
                    break
                delimiter_emerge = False
                p, t= generator(s[pos:])
                if p == 0:
                    break
                pos += p
                l.append(t)
        return 0, None

    def FromPythonStr(self, s = ""):
        return self.__FromStr(s, '[',']',',',PythonStrToStruct)

    def FromLuaStr(self, s = ""):
        try:
            return self.__FromStr(s, '{','}',',',LuaStrToStruct)
        except NonePattern:
            return 0, None

def AddPythonPrefix(key, value):
    buffer = ""
    if isinstance(key, int) or isinstance(key, long):
        buffer += str(key)
    elif isinstance(key, str):
        buffer += "\"" + key + "\""
    else:
        raise "KeyError"
    buffer += ":"
    return buffer + value.ToPythonStr()

def AddLuaPrefix(key, value):
    # key = str(key)
    # if isinstance(value.key, str):
    if isinstance(key, str):
        return str(key) + "=" + value.ToLuaStr()
    else:
        return value.ToLuaStr()

class Dict:
    def __init__(self, d = {}):
        self.__data = d
    def ToPythonStr(self):
        l_buffer = ""
        for key, value in self.__data.items():
            l_buffer += AddPythonPrefix(key, value) + ","
        return "{%s}" % l_buffer[0: len(l_buffer) - 1]
    def ToLuaStr(self):
        l_buffer = ""       
        for key,value in self.__data.items():
            l_buffer += AddLuaPrefix(key,value) + ","
        return "{%s}" % l_buffer
    def GetRawData(self):
        d = {}
        for k, v in self.__data.items():
            d[k] = v.GetRawData()
        return d
    def __getitem__(self, key):
        return self.__data[key].GetRawData()
    def __setitem__(self, key, value):
        self.__data[key] = Traits(value)
    def update(self, new):
        for k, v in new.items():
            self.__data[k] = Traits(v)

class DictDelimiter:
    def FromPythonStr(self, s = ""):
        pos = 0
        d = {}
        if s[pos] != "{":
            return 0,None
        pos += 1
        delimiter_emerge = True
        while pos < len(s):
            if s[pos] == "}":
                return pos + 1, Dict(d)
            elif s[pos] == ',' :
                if delimiter_emerge == True:
                    break
                delimiter_emerge = True
                pos += 1
            elif s[pos] in SpaceFilter.space_set:
                pos += 1
            else:
                if delimiter_emerge == False:
                    break
                delimiter_emerge = False
                #get key
                p, k = PythonStrToStruct(s[pos:])
                if p == 0:
                    break
                else:
                    pos += p
                    while pos < len(s) and s[pos] != ':':
                        pos += 1
                    if pos >= len(s):
                        break
                    pos += 1
                    #get value
                    p, v = PythonStrToStruct(s[pos:])
                    if p == 0:
                        break
                    pos += p
                    d[k.GetRawData()] = v
        return 0,None
    def FromLuaStr(self, s = ""):
        pos = 0
        index = 1
        delimiter_emerge = True
        d = {}
        if s[pos] != "{":
            return 0, None
        pos += 1
        while pos < len(s):
            if s[pos] == "}":
                return pos + 1, Dict(d)
            elif s[pos] == ',':
                if delimiter_emerge == True:
                    break
                delimiter_emerge = True
                pos += 1
            elif s[pos] in SpaceFilter.space_set:
                pos += 1
            else:
                if delimiter_emerge == False:
                    break
                delimiter_emerge = False
                try:
                    p,v = LuaStrToStruct(s[pos:])
                    pos += p
                    d[index] = v
                    index += 1
                except NonePattern:
                    #get key
                    #filtrate the space
                    pos += SpaceFilter()(s[pos:])
                    if pos == len(s):
                        break
                    if s[pos].isalpha() == False:
                        break
                    key_buffer = "" 
                    while s[pos] != '=' and s[pos] not in SpaceFilter.space_set:
                        key_buffer += s[pos] 
                        pos += 1
                        if pos == len(s):
                            return 0, None
                    pos += SpaceFilter()(s[pos:])
                    if pos == len(s):
                        break
                    if s[pos] != '=':
                        break
                    pos += 1
                    p, v = LuaStrToStruct(s[pos:])
                    if p == 0:
                        break
                    else:
                        pos += p
                        d[key_buffer] = v
        return 0, None

class DelimiterAdaptor:
    def __init__(self, s, delimiter):
        self.__arg = s
        self.__delimiter = delimiter
    def __call__(self):
        return self.__delimiter(self.__arg)
    def GetArg(self):
        return self.__arg

def Generator(*ds):
    for d in ds:
        pos, struct = d()
        if pos != 0:
            return pos, struct
    # raise NonePattern(ds[0].GetArg())
    track_map.ascii(ds[0].GetArg())

@__space_filter
def PythonStrToStruct(s):
    number_generator = DelimiterAdaptor(s, NumberDelimiter().FromPythonStr)
    string_generator = DelimiterAdaptor(s, StringDelimiter().FromPythonStr)
    bool_generator   = DelimiterAdaptor(s, BoolDelimiter().FromPythonStr)
    null_generator   = DelimiterAdaptor(s, NullDelimiter().FromPythonStr)
    list_generator   = DelimiterAdaptor(s, ListDelimiter().FromPythonStr)
    dict_generator   = DelimiterAdaptor(s, DictDelimiter().FromPythonStr)
    return Generator(number_generator, string_generator, bool_generator, null_generator, list_generator,dict_generator)

@__space_filter
def LuaStrToStruct(s):
    number_generator = DelimiterAdaptor(s, NumberDelimiter().FromLuaStr)
    string_generator = DelimiterAdaptor(s, StringDelimiter().FromLuaStr)
    bool_generator   = DelimiterAdaptor(s, BoolDelimiter().FromLuaStr)
    null_generator   = DelimiterAdaptor(s, NullDelimiter().FromLuaStr)
    list_generator   = DelimiterAdaptor(s, ListDelimiter().FromLuaStr)
    dict_generator   = DelimiterAdaptor(s, DictDelimiter().FromLuaStr)
    return Generator(number_generator, string_generator, bool_generator,null_generator, list_generator, dict_generator)


# def LuaStrToStruct(s):
#     empty = None
#     result = None
#     number_generator = Generator(s, NumberDelimiter())
#     string_generator = Generator(s, StringDelimiter())

class PyLuaTblParser:
    '''load(self, s) '''
    def __init__(self):
        self.__data = None

    def load(self, s):
        self.__data = LuaStrToStruct(s)[1]

    def dump(self):
        if self.__data == None:
            return ""
        else:
            return self.__data.ToLuaStr()

    def loadLuaTable(self, f):
        with open(f,"r") as in_file:
            s = in_file.read()
            self.load(s)

    def dumpLuaTable(self, f):
        with open(f,"w") as out_file:
            if self.__data != None:
                out_file.write(self.dump())

    def loadDict(self, d):
        self.__data = PythonStrToStruct(str(d))[1]

    def dumpDict(self):
        if self.__data == None:
            return ""
        else:
            return self.__data.GetRawData()
    def __getitem__(self, key):
        return self.__data[key]
    def __setitem__(self, key, value):
        self.__data[key] = value
    def update(self, new):
        self.__data.update(new)
