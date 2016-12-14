class SpaceFilter:
    __space_set = set([' ','\t','\n'])
    def __call__(self, str, pos = 0):
        while SpaceFilter.__space_set.issubset(str[pos]):
            pos+=1
        return pos

def AddPythonPrefix(value):
    key = ""
    if hasattr(value,"key"):
        if isinstance(value.key, int):
            key += str(value.key)
        elif isinstance(value.key, str):
            key += "\"" + value.key + "\""
        key += ":"
    return key + value.ToPythonStr()

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

class NumberDelimiter:
    def __FromStr(self, s = ""):
        s = s.lstrip()
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
    def __init__(self, s= ""):
        self.__data = s
    def ToPythonStr(self):
        return "\""+self.__data+"\""
    def ToLuaStr(self):
        return self.__data

class StringDelimiter:
    def __FromStr(self, s = ""):
        s = s.lstrip()
        pos = 0
        if pos < len(s) or s[pos] != '"' or s[pos] !="'":
            return 0,None
        end_char = s[pos] 
        pos+=1
        while pos < len(s):
            if s[pos] == end_char:
                if s[pos - 1] != '\\':
                    return pos, String(s[:pos])        
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
    def __getitme__(self, key):
        return self.__data[key]

class ListDelimiter:
    def FromPythonStr(self, s = ""):
        s = s.lstrip()
        pos = 0
        l = []
        if s[pos] != '[':
            return 0,None
        pos += 1
        while pos < len(s):
            if s[pos] == ']':
                return pos, l
            if s[pos] == ',':
                pos += 1
            pos = 

        return 0, None

class Dict:
    def __init__(self, d = {}):
        self.__data = d
    def ToPythonStr(self):
        l_buffer = ""
        for key, value in self.__data.items():
            if hasattr(value,"key") is False:
                value.key = key
            l_buffer += AddPythonPrefix(value)
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

def Generator(str,Delimiter):
    def Run(str, Dlimiter):
        result = None
        while True:
            result = Delimiter(str)
            if len(result) == 1:
                if result[0]:
                    continue
                else:
                    return None
            else:
                if result[0]:
                    return result[1]
                else:
                    return None
    return Run


def LuaStrToStruct(s):
    empty = None
    result = None
    number_generator = Generator(s, NumberDelimiter())
    string_generator = Generator(s, StringDelimiter())

                

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

s = List([String("abc"),Number(1),Number(2)])
print s.ToPythonStr()
print s.ToLuaStr()

print float('.123')
print "Success"
