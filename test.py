
from PyLuaTblParser import *

parser = PyLuaTblParser()
# parser.loadDict(
# {'root': {
#     96: [[], 1, 2, None],
#     1: 'Test Pattern String',
#     2: {'object with 1 member': ['array with 1 element']},
#     99: -42,
#     4: True,
#     5: False,
#     6: None,
#     97: [[], []],
#     8: 0.5,
#     9: 3.141592653589793e+64,
#     10: 3.141592653589793,
#     7: {
#         'comment': '// /* <!-- --',
#         'false': False,
#         'backslash': '\\\\',
#         'one': 1,
#         'quotes': '" (0x0022) %22 0x22 034 "',
#         'zero': 0,
#         'alpha': 'abcdefghijklmnopqrstuvwyz',
#         'array': [None, None],
#         'special': "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
#         'compact': [
#             1,
#             2,
#             3,
#             4,
#             5,
#             6,
#             7,
#             ],
#         'space': ' ',
#         'hex': '0x01230x45670x89AB0xCDEF0xabcd0xef4A',
#         'controls': '\\b\\f\\n\\r\\t',
#         '\\\\"\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?': 'A key can be any string',
#         'slash': '/ & \\\\',
#         'real': -9876.54321,
#         'digit': '0123456789',
#         'E': 1.23456789e+34,
#         'nil': None,
#         'quote': '\\"',
#         'object': [],
#         'address': '50 St. James Street',
#         'integer': 1234567890,
#         'true': True,
#         'luatext': '{\\"object with 1 member\\" = {\\"array with 1 element\\"}}',
#         'e': 1.23456789e-13,
#         'url': 'http://www.JSON.org/',
#         '# -- -- --> */': ' ',
#         ' s p a c e d ': [
#             1,
#             2,
#             3,
#             4,
#             5,
#             6,
#             7,
#             ],
#         'ALPHA': 'ABCDEFGHIJKLMNOPQRSTUVWYZ',
#         },
#     12: 'rosebud',
#     98: [[]],
#     11: 1066,
#     3: [],
#     94: {1: {'1': 1, '2': 2}, 2: {1: 1, '2': 2}, '3': 3},
#     95: [1, 2, {'1': 1}],
#     }}
# )
# print parser.dumpDict()
# print "\n\n"
parser.load(r'''

{root = {
  "Test Pattern String",
  -- {"object with 1 member" = {"array with 1 element",},},
  {["object with 1 member"] = {"array with 1 element",},},
  {},
  [99] = -42,
  [98] = {{}},
  [97] = {{},{}},
  [96] = {{}, 1, 2, nil},
  [95] = {1, 2, {["1"] = 1}},
  [94] = { {["1"]=1, ["2"]=2}, {1, ["2"]=2}, ["3"] = 3 },
  true,
  false,
  nil,
  {
    ["integer"]= 1234567890,
    real=-9876.543210,
    e= 0.123456789e-12,
    E= 1.234567890E+34,
    zero = 0,
    one = 1,
    space = " ",
    quote = "\"",
    backslash = "\\",
    controls = "\b\f\n\r\t",
    slash = "/ & \\",
    alpha= "abcdefghijklmnopqrstuvwyz",
    ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWYZ",
    digit = "0123456789",
    special = "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
    hex = "0x01230x45670x89AB0xCDEF0xabcd0xef4A",
    ["true"] = true,
    ["false"] = false,
    ["nil"] = nil,
    array = {nil, nil,},
    object = {  },
    address = "50 St. James Street",
    url = "http://www.JSON.org/",
    comment = "// /* <!-- --",
    ["# -- -- --> */"] = " ",
    [" s p a c e d " ] = {1,2 , 3

    ,

    4 , 5        ,          6           ,7        },
    --[[[][][]  Test multi-line comments
    compact = {1,2,3,4,5,6,7},
    - -[luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
    quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
    ["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"]
    = "A key can be any string"]]
    --         ]]
    compact = {1,2,3,4,5,6,7},
    luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
    quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
    ["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"]
    = "A key can be any string"
  },
  0.5 ,31415926535897932384626433832795028841971693993751058209749445923.
  ,
  3.1415926535897932384626433832795028841971693993751058209749445923
  ,

  1066


  ,"rosebud"

}}


''')
d = parser.dumpDict()
print d
parser.loadDict(d)
parser["root"][96] = "Hello World"
parser.update({"root":1})
# parser["root"][4] = "Hello World"
parser.dumpLuaTable("output2.lua")
# print "------------------"
parser.loadLuaTable("output2.lua")
sd2 = parser.dumpDict()

print "--------------------------"
print sd2
# print "-------------"
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
