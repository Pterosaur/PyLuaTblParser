
from PyLuaTblParser import *

parser = PyLuaTblParser()

parser.load('''abc{
    array = {65,23,5,},
    dict = {
        mixed = {
              
              43,54.33,false,9,string = "value",
            },
            null = nil,
            array = {3,6,4,},
            string = "value",
    },
}''')
print parser.dumpDict()
# print parser.dumpLuaTable("table_test.lua")
# # print PythonStrToStruct('''{
# #      "array": [65, 23, 5],
# #      "dict": {
# #           "mixed": {
# #                1: 43,
# #                2: 54.33,
# #                3: False,
# #                4: 9,
# #                "string": "value"
# #           },
# #           "null" : None,
# #           "array": [3, 6,4],
# #           "string": "value"
# #      }
# # }
# # ''')[1].ToLuaStr()
# parser.loadLuaTable("table_test.lua")

# print parser["array"]
# parser["array"] = {"test_set_item":True}
# print parser.dump()
# parser.update({"test_update":[1,2]})
# print parser.dump()