from common import *
# class NonePattern(Exception):
#     def __init__(self, arg):
#         self.__arg = arg
#     def __str__(self):
#         return self.__arg

class SpaceFilter:
    space_set = set([' ','\t','\n', '\r'])
    def __call__(self, s, pos = 0):
        while pos < len(s):
            # if pos + 1 < len(s) and s[pos:pos+2] in self.space_set :
                # pos += 2
            if s[pos] in self.space_set:
                pos += 1
            else:
                break
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

def LuaInvalidFilter(s = ""):
    p  = SpaceFilter()(s)
    p +=CommentFilter().FromLuaStr(s[p:])
    p += SpaceFilter()(s[p:])
    return p


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
    def GetData(self):
        return self.__data

class NumberDelimiter:
    def __FromStr(self, s = ""):
        pos = 0
        is_float = False
        is_number = False
        is_hex = False
        is_scientfic = False
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
                #e
                elif is_scientfic == False and (s[pos] == 'e' or s[pos] == 'E'):
                    is_scientfic = True
                    pos += 1
                    if pos < len(s) and (s[pos] == '-' or s[pos] == '+'):
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
    def add_esc(self,s):
        pos = 0
        __buffer = ""
        while pos < len(s):
            if s[pos] == '\\':
                # if pos + 2 < len(self.__data) and self.__data[pos + 1] == '\\': 
                    # __buffer += self.__data[pos:pos +1]
                    # pos += 2
                # else:
                __buffer += s[pos:pos+2]
                pos += 2
            elif s[pos] == self.__delimiter:
                __buffer += '\\'
                __buffer += s[pos:pos+1]
                pos += 1
            else:
                __buffer += s[pos:pos+1]
                pos += 1
        return __buffer
    def ToPythonStr(self):
        return self.__delimiter+self.__data+self.__delimiter
    def ToLuaStr(self):
        return self.__delimiter+self.__data+self.__delimiter
    def GetData(self):
        
        return self.__data.decode("string_escape")
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
            if s[pos] == '\\':
                pos += 2
            elif s[pos] == end_char:
                    #+1 because of the skipping of the end char --"' or "", for next parser
                    return pos + 1, String(s[1:pos], "\"")        
            else:
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
    def GetData(self):
        return self.__data
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
    def GetData(self):
        return None
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

# class Comment:
#     def __init__(self, s, f = "--%s\n"):
#         self.__data = s
#         self.__lua_format = f
#     def ToPythonStr(self):
#         return "#%s\n" % self.__data
#     def ToLuaStr(self):
#         return self.__lua_format % self.__data

class CommentFilter:
    def __FromStr(self, s = "", b = "", e = ""):
        if s[:len(b)] != b:
            return 0
        pos = s.find(e)
        if pos == -1:
            return 0
        return pos + len(e)#, Comment(s[:pos + len(e)], b+"%s"+e) 
    def FromPythonStr(self, s = ""):
        p = self.__FromStr(s, "#", "\n")
        if p == 0:
            return p
        return p + self.FromLuaStr(s[p:])
    def FromLuaStr(self, s = ""):
        p = self.__FromStr(s, "--[[","]]")
        if p == 0:
            p = self.__FromStr(s, "--", "\n")
            if p == 0:
                return p
        return p + LuaInvalidFilter(s[p:])

        
# class Key:
#     def __init__(self, k):
#         self.__data = k
#     def ToPythonStr(self):
#         if isinstance(self.__data, int):
#             return str(self.__data)
#         elif isinstance(self.__data, int):
#             return '"%s"' % self.__data
#         else:
#             raise NonePattern(str(self.__data))
#     def ToLuaStr(self):
#         if isinstance(self.__data, int):
#             return "[%d]" % self.__data
#         elif isinstance(self.__data, str):
#             return '["%s"]' % self.__data
#         else:
#             raise NonePattern(str(self.__data))

class KeyDelimiter:
    def FromPythonStr(self, s = ""):
        pos = SpaceFilter()(s)
        if len(s[pos:]) == 0:
            return 0
        p,v = NumberDelimiter().FromPythonStr(s[pos:])
        if p == 0:
            p,v = StringDelimiter().FromPythonStr(s[pos:])
            if p == 0:
                return 0, None
        pos += p
        pos += SpaceFilter()(s[pos:])
        if s[pos] != ':':
            return 0, None
        pos += 1
        return pos, v.GetRawData()
    def FromLuaStr(self, s = ""):
        pos = SpaceFilter()(s)
        if len(s[pos:]) == 0:
            return 0, None
        if s[pos] == '[':
            pos += 1
            #filtrate space and comment
            pos += LuaInvalidFilter(s[pos:])
            p, v = NumberDelimiter().FromLuaStr(s[pos:])
            if p == 0:
                p, v = StringDelimiter().FromLuaStr(s[pos:]) 
                if p == 0:
                    return 0, None
            pos += p 
            #filtrate space and comment
            pos += LuaInvalidFilter(s[pos:])
            if s[pos] == ']':
                pos += 1
                pos += LuaInvalidFilter(s[pos:])
                if s[pos] == '=':
                    pos += 1
                    return pos, v.GetRawData()
            return 0, None
        if s[pos].isalpha() == False and s[pos] != '_':
            return 0, None
        key_buffer = ""
        while s[pos].isalpha() or s[pos].isdigit() or s[pos] == '_':
            key_buffer += s[pos]
            pos += 1
            if pos >= len(s):
                return 0, None
        #filtrate space and comment
        pos += LuaInvalidFilter(s[pos:])
        if s[pos] != '=':
            return 0, None
        return pos+1,key_buffer

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
        value = '"%s"' % value.encode("string_escape")
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
            l_buffer += s.ToLuaStr() + ',\n'
        return "{%s}" % l_buffer
    def GetRawData(self):
        l = []
        for i in self.__data:
            l.append(i.GetRawData())
        return l
    def GetData(self):
        l = []
        for i in self.__data:
            l.append(i.GetData())
        return l
    def __getitme__(self, key):
        return self.__data[key].GetData()
    def __setitem__(self, key, value):
        self.__data[key] = Traits(value)

class ListDelimiter:
    def __FromStr(self, s , begin_char, end_char, delimiter_char, generator, comment_point):
        pos = 0
        l = []
        if pos < len(s) and s[pos] != begin_char:
            return 0,None
        pos += 1
        delimiter_emerge = True
        pos +=comment_point(s[pos:])
        while pos < len(s):
            pos += SpaceFilter()(s[pos:])
            if s[pos] == end_char: 
                #+1 because of the skipping of end char --"]", for next parser
                return pos + 1, List(l)
            elif s[pos] == delimiter_char :
                if delimiter_emerge == True:
                    break
                delimiter_emerge = True
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
        pos +=comment_point(s[pos:])
        return 0, None

    def FromPythonStr(self, s = ""):
        return self.__FromStr(s, '[',']',',',PythonStrToStruct, CommentFilter().FromPythonStr)

    def FromLuaStr(self, s = ""):
        try:
            return self.__FromStr(s, '{','}',',',LuaStrToStruct,CommentFilter().FromLuaStr)
        except NonePattern:
            return 0, None

def AddPythonPrefix(key, value):
    buffer = ""
    if isinstance(key, int) or isinstance(key, long):
        buffer += str(key)
    elif isinstance(key, str):
        buffer += "\"" + key + "\""
    else:
        raise NonePattern(str(key) + "=" +value)
    buffer += ":"
    return buffer + value.ToPythonStr()

def AddLuaPrefix(key, value):
    if isinstance(key, str):
        return ('["%s"]' % key) + "=" + value.ToLuaStr() + "\n"
    elif isinstance(key, int):
        return ('[%d]' % key )+ "=" + value.ToLuaStr() + "\n"
    else:
        raise NonePattern(str(key) + "=" +value)

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
            # if isinstance(k, str):
                # k = k.decode("string_escape")
            d[k] = v.GetRawData()
        return d
    def GetData(self):
        d = {}
        for k, v in self.__data.items():
            if isinstance(k, str):
                k = k.decode("string_escape")
            d[k] = v.GetData()
        return d
        
    def __getitem__(self, key):
        return self.__data[key].GetData()
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
            pos += SpaceFilter()(s[pos:])
            if s[pos] == "}":
                return pos + 1, Dict(d)
            elif s[pos] == ',' :
                if delimiter_emerge == True:
                    break
                delimiter_emerge = True
                pos += 1
            else:
                if delimiter_emerge == False:
                    break
                delimiter_emerge = False
                #get key
                # p, k = PythonStrToStruct(s[pos:])
                p, k = KeyDelimiter().FromPythonStr(s[pos:])
                if p == 0:
                    break
                else:
                    pos += p
                    # while pos < len(s) and s[pos] != ':':
                        # pos += 1
                    # if pos >= len(s):
                        # break
                    # pos += 1
                    #get value
                    p, v = PythonStrToStruct(s[pos:])
                    if p == 0:
                        break
                    pos += p
                    d[k] = v
        return 0,None
    def FromLuaStr(self, s = ""):
        pos = 0
        index = 1
        delimiter_emerge = True
        d = {}
        if pos < len(s) and s[pos] != "{":
            return 0, None
        pos += 1
        while pos < len(s):
            # pos += SpaceFilter()(s[pos:])
            pos += LuaInvalidFilter(s[pos:])
            if s[pos] == "}":
                return pos + 1, Dict(d)
            elif s[pos] == ',':
                if delimiter_emerge == True:
                    break
                delimiter_emerge = True
                pos += 1
            else:
                if delimiter_emerge == False:
                    break
                delimiter_emerge = False
                try:
                    p,v = LuaStrToStruct(s[pos:])
                    pos += p
                    if isinstance(v, Null):
                        index += 1
                        continue
                    d[index] = v
                    index += 1
                except NonePattern:
                    #get key
                    #filtrate the space
                    # pos += SpaceFilter()(s[pos:])
                    # if pos == len(s):
                    #     break
                    # #filtrate the Comment
                    # p,v = CommentDelimiter().FromLuaStr(s[pos:])
                    # if p != 0:
                    #     pos += p
                    # p = SpaceFilter()(s[pos:])
                    # if p!= 0:
                    #     pos +=p
                    # #right flag
                    # if pos > len(s) or s[pos].isalpha() == False:
                    #     break
                    # key_buffer = "" 
                    # while s[pos] != '=' and s[pos] not in SpaceFilter.space_set:
                    #     key_buffer += s[pos] 
                    #     pos += 1
                    #     if pos == len(s):
                    #         return 0, None
                    # pos += SpaceFilter()(s[pos:])
                    # if pos == len(s):
                    #     break
                    # if s[pos] != '=':
                    #     break
                    # pos += 1
                    p, k = KeyDelimiter().FromLuaStr(s[pos:])
                    if p == 0:
                        break
                    pos += p
                    p, v = LuaStrToStruct(s[pos:])
                    if p == 0:
                        break
                    else:
                        pos += p
                        if isinstance(v, Null) == False:
                            d[k] = v
        return 0, None

class DelimiterAdaptor:
    def __init__(self, s, delimiter):
        self.__arg = s
        self.__delimiter = delimiter
    def __call__(self):
        return self.__delimiter(self.__arg)
    def GetArg(self):
        return self.__arg
    def SetArgOffset(self,offset):
        if offset < len(self.__arg):
            self.__arg = self.__arg[offset:]
        else:
            self.__arg = self.__arg[len(self.__arg) - 1:]

import track_map

def Generator(*ds):
    for d in ds:
        pos, struct = d()
        if pos != 0:
            return pos, struct
    global case
    raise NonePattern(ds[0].GetArg())
    # global source_input
    # track_map.ascii(source_input+ "\n--------------\n" +ds[0].GetArg(), 10000)
    # track_map.ascii(ds[0].GetArg(), 10000)

def escape_transform(s):
    escape_map = {
        "\'":r"\'",
        "\"":r"\"",
        "\\":r"\\",
        "\a":r"\a",
        "\b":r"\b",
        "\f":r"\f",
        "\n":r"\n",
        "\t":r"\t",
        "\r":r"\r",
        "\v":r"\v",
    }
    __buff = ""
    for c in s:
        if c in escape_map:
            __buff += escape_map[c]
        else:
            __buff += c
    return __buff

def PythonListToStruct(d = []):
    result = []
    for i in d:
        if isinstance(i, bool):
            result.append(Bool(i))
        elif isinstance(i, str):
            result.append(String(escape_transform(i)))
            # result.append(String(i))
        elif i == None:
            result.append(Null())
        elif isinstance(i, int) or isinstance(i, float):
            result.append(Number(i))
        elif isinstance(i, list):
            result.append(PythonListToStruct(i))
        elif isinstance(i, dict):
            result.append(PythonDictToStruct(i))
    return List(result)
            
def PythonDictToStruct(d = {}):
    result = {}
    for k, v in d.items():
        if isinstance(k, int) or isinstance(k, str):
            if isinstance(k, str):
                # k = k.encode("string_escape").encode("ascii").replace('"','\\"')
                k = escape_transform(k)
            if isinstance(v, bool):
                result[k] = Bool(v)
            elif isinstance(v, str):
                # result[k] = String(v.encode("string_escape").replace('"','\\"'))
                result[k] = String(escape_transform(v))
            elif isinstance(v, int) or isinstance(v, float):
                result[k] = Number(v)
            elif isinstance(v, list):
                result[k] = PythonListToStruct(v)
            elif isinstance(v, dict):
                result[k] = PythonDictToStruct(v)
    return Dict(result)
        
            

@__space_filter
def PythonStrToStruct(s):
    p = CommentFilter().FromPythonStr(s)
    p += SpaceFilter()(s[p:])
    s = s[p:]
    number_generator = DelimiterAdaptor(s, NumberDelimiter().FromPythonStr)
    string_generator = DelimiterAdaptor(s, StringDelimiter().FromPythonStr)
    bool_generator   = DelimiterAdaptor(s, BoolDelimiter().FromPythonStr)
    null_generator   = DelimiterAdaptor(s, NullDelimiter().FromPythonStr)
    # comment_generator= DelimiterAdaptor(s, CommentDelimiter().FromPythonStr)
    list_generator   = DelimiterAdaptor(s, ListDelimiter().FromPythonStr)
    dict_generator   = DelimiterAdaptor(s, DictDelimiter().FromPythonStr)
    return Generator(
        number_generator,
        string_generator, 
        bool_generator,
        null_generator,
        # comment_generator,
        list_generator,
        dict_generator
     )

@__space_filter
def LuaStrToStruct(s):
    p = CommentFilter().FromLuaStr(s)
    p += SpaceFilter()(s[p:])
    s = s[p:]
    number_generator = DelimiterAdaptor(s, NumberDelimiter().FromLuaStr)
    string_generator = DelimiterAdaptor(s, StringDelimiter().FromLuaStr)
    bool_generator   = DelimiterAdaptor(s, BoolDelimiter().FromLuaStr)
    null_generator   = DelimiterAdaptor(s, NullDelimiter().FromLuaStr)
    # comment_generator= DelimiterAdaptor(s, CommentDelimiter().FromLuaStr)
    list_generator   = DelimiterAdaptor(s, ListDelimiter().FromLuaStr)
    dict_generator   = DelimiterAdaptor(s, DictDelimiter().FromLuaStr)
    pos, v = Generator(
        number_generator, 
        string_generator, 
        bool_generator,
        null_generator, 
        # comment_generator,
        list_generator, 
        dict_generator)
    return pos + p, v

class VersionControl:
    def __init__(self):
        self.__data = None
        self.__version_id = 0
    
    def GetConstData(self):
        return self.__data
    def GetData(self):
        self.__version_id += 1
        return self.__data
    def GetVersionId(self):
        return self.__version_id
    
    def SetData(self, data, vid = -1):
        self.__data = data
        if id != -1:
            self.__version_id = vid
        else:
            self.__version_id += 1
    

class PyLuaTblParser:
    '''load(self, s) '''
    def __init__(self):
        self.__data = None
        self.__stable = VersionControl()
        self.__mutable = VersionControl()

    def load(self, s = ""):
        # try:
            # self.__data = LuaStrToStruct(s)[1]
        # except NonePattern:
            # track_map.ascii(s[996:], 100000)
        try:
            data = LuaStrToStruct(s)[1]
        except NonePattern:
            track_map.ascii(s[996:], 100000)
        self.__stable.SetData(data, max(self.__stable.GetVersionId(), self.__mutable.GetVersionId()) + 1)
        
# 
    def dump(self):
        # if self.__data == None:
            # return ""
        # else:
            # return self.__data.ToLuaStr()
        data = self.__get_stable_data_()
        if data == None:
            return ""
        else:
            return data.ToLuaStr()

    def loadLuaTable(self, f):
        with open(f,"r") as in_file:
            s = in_file.read()
            # track_map.ascii(s, 100000)
            self.load(s)

    def dumpLuaTable(self, f):
        with open(f,"w") as out_file:
            # if self.__data != None:
            if self.__get_stable_data_() != None:
                out_file.write(self.dump())

    def loadDict(self, d):
        # self.__data = PythonStrToStruct(str(d).decode("string_escape"))[1]
        # self.__data = PythonDictToStruct(d)
        data = PythonDictToStruct(d)
        self.__stable.SetData(data, max(self.__stable.GetVersionId(), self.__mutable.GetVersionId()) + 1)

    def dumpDict(self):
        # if self.__data == None:
            # return {}
        # else:
            # d = self.__data.GetData()
            # return d
        data = self.__stable.GetConstData()
        if data == None:
            return None
        else:
            return data.GetData()
            # result = {}
            # for k, v in d:
                # if isinstance(k, str):
                    # k = k.decode("string_escape")
                # if isinstance(v, str):
                    # v = v.decode("string_escape")
                # result[k] = v
    
    def __get_mutalbe_data_(self):
        if self.__mutable.GetVersionId() < self.__stable.GetVersionId():
            vid = self.__stable.GetVersionId()
            data = self.dumpDict()
            self.__mutable.SetData(data, vid)
        return self.__mutable.GetData()
        
    def __get_stable_data_(self):
        if self.__mutable.GetVersionId() > self.__stable.GetVersionId():
            vid = self.__mutable.GetVersionId()
            data = self.__mutable.GetConstData()
            self.loadDict(data)
            # self.__stable.SetData(data, vid)
        return self.__stable.GetConstData()
                    
    def __getitem__(self, key):
        data = self.__get_mutalbe_data_()
        if data == None:
            raise KeyError(key)
        return data[key]
        # return self.__data[key]
    def __setitem__(self, key, value):
        # self.__data[key] = value
        # self.update({key:value})
        self.__get_mutalbe_data_()[key] = value
    def update(self, new):
        self.__get_mutalbe_data_().update(new)