import functools
import ast

class SpaceFilter:
    __space_set = set([' ','\t','\n', '\r'])
    def __call__(self, str, pos = 0):
        while str[pos] in SpaceFilter.__space_set:
            pos+=1
        return pos

def __space_filter(func):
    # @functools.wraps(func)
    def wrapper(s = ""):
        pos = SpaceFilter()(s)
        p, t = func(s[pos:])
        if p == 0:
            return 0,t
        else:
            return pos + p, t
    return wrapper
        

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

def AddLuaPrefix(value):
    key = ""
    if hasattr(value, "key") and isinstance(value.key, str):
        key += "=" + value.key
    return key + value.ToLuaStr()

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
        while pos < len(s):
            if False == s[pos].isdigit():
                if pos == 0 and s[pos] == '-':
                    pos += 1
                    continue
                if s[pos] == '.' and is_float == False:
                    is_float = True
                    pos += 1
                    continue
                break
            pos += 1
        if pos == 0:
            return 0,None
        if is_float:
            return pos, Number(float(s[:pos]))
        return pos, Number(long(s[:pos]))

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
        return self.__data
    def __getitme__(self, key):
        return self.__data[key]

class ListDelimiter:
    def FromPythonStr(self, s = ""):
        pos = 0
        l = []
        if s[pos] != '[':
            return 0,None
        pos += 1
        while pos < len(s):
            if s[pos] == ']':
                #+1 because of the skipping of end char --"]", for next parser
                return pos + 1, List(l)
            if s[pos] == ',' or s[pos] ==' ':
                pos += 1
            else:
                p, t= PythonStrToStruct(s[pos:])
                if p == 0:
                    break
                pos += p
                l.append(t)
        return 0, None

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
            if hasattr(value,"key") is False:
                value.key = key
            l_buffer += AddLuaPrefix(value)
        return "{%s}" % l_buffer
    def __getitme__(self, key):
        return self.__data[key]

class DictDelimiter:
    def FromPythonStr(self, s = ""):
        pos = 0
        d = {}
        if s[pos] != "{":
            return 0,None
        pos += 1
        while pos < len(s):
            if s[pos] == "}":
                return pos + 1, Dict(d)
            if s[pos] == ',' or s[pos] == ' ':
                pos += 1
            else:
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

            
            

def DelimiterAdaptor(s, Delimiter):
    def Delimit():
         return Delimiter(s)
    return Delimit

def Generator(*ds):
    for d in ds:
        pos, struct = d()
        if pos != 0:
            return pos, struct
    raise "NonePattern"

@__space_filter
def PythonStrToStruct(s):
    number_generator = DelimiterAdaptor(s, NumberDelimiter().FromPythonStr)
    string_generator = DelimiterAdaptor(s, StringDelimiter().FromPythonStr)
    list_generator   = DelimiterAdaptor(s, ListDelimiter().FromPythonStr)
    dict_generator   = DelimiterAdaptor(s, DictDelimiter().FromPythonStr)
    return Generator(number_generator, string_generator, list_generator,dict_generator)

# def LuaStrToStruct(s):
#     empty = None
#     result = None
#     number_generator = Generator(s, NumberDelimiter())
#     string_generator = Generator(s, StringDelimiter())

class PyLuaTblParser:
    '''load(self, s) '''
    def __init__(self):
        self.__m_dict = {}

    def load(self, s):
        pass

    def dump(self):
        pass

    def loadLuaTable(self, f):
        pass

    def dumpLuaTable(self, f):
        pass

    def loadDict(self, d):
        pass

    def dumpDict(self):
        pass

# s = Dict(ast.literal_eval("{1:2}"))
# print s.ToPythonStr()
# print s.ToLuaStr()

print PythonStrToStruct('''{
     "array": [65, 23, 5],
     "dict": {
          "mixed": {
               1: 43,
               2: 54.33,
               3: false,
               4: 9
               "string": "value"
          },
          "array": [3, 6, 4],
          "string": "value"
     }
}
 ''')[1].ToPythonStr()

print "Success"
