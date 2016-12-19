
def create_track(outfile):
    ft = '''def __ascii_%d(s, d=100):\n if d ==0 or len(s) == 0: raise Exception("") \n else: track_map[ord(s[0])](s[1:], d - 1)\n'''
    for i in range(0, 255):
        outfile.write(ft % i)

def create_map(outfile):
    ft = '''track_map = %s'''
    s = str([ "__ascii_%d" % i for i in range(0, 255)])
    s = s.replace('\'', '')
    s += '\n'
    outfile.write(ft % s)
    ft = '''def ascii(s, d=100):\n if d ==0 or len(s) == 0: raise Exception("") \n else: track_map[ord(s[0])](s[1:], d - 1)\n'''
    outfile.write(ft)

# with open("track_map.py","w") as fd:
    # create_track(fd)
    # create_map(fd)

# import track_map
# track_map.ascii("abc")
# l = [345,336,336,351,99,186,99,372,42,33,30,335]
def map_to_str(l = []):
    s = ""
    if len(l) == 0:
        return ""
    else:
        l[len(l) - 1] += 1
    for c in l:
        s += chr(c/3-1)
    print s

import re
def tract_to_list(s = ''):
    return [int(i) for i in re.findall(r'\d+', s)]
l = tract_to_list('''  File "track_map.py", line 372
  File "track_map.py", line 42
  File "track_map.py", line 33
  File "track_map.py", line 345
  File "track_map.py", line 336
  File "track_map.py", line 336
  File "track_map.py", line 351
  File "track_map.py", line 99
  File "track_map.py", line 186
  File "track_map.py", line 99
  File "track_map.py", line 372
  File "track_map.py", line 42
  File "track_map.py", line 33
  File "track_map.py", line 30
  File "track_map.py", line 105
  File "track_map.py", line 255
  File "track_map.py", line 306
  File "track_map.py", line 348
  File "track_map.py", line 351
  File "track_map.py", line 99
  File "track_map.py", line 243
  File "track_map.py", line 294
  File "track_map.py", line 351
  File "track_map.py", line 351
  File "track_map.py", line 306
  File "track_map.py", line 345
  File "track_map.py", line 333
  File "track_map.py", line 99
  File "track_map.py", line 252
  File "track_map.py", line 351
  File "track_map.py", line 345
  File "track_map.py", line 318
  File "track_map.py", line 333
  File "track_map.py", line 312
  File "track_map.py", line 105
  File "track_map.py", line 135
  File "track_map.py", line 42
  File "track_map.py", line 33
  File "track_map.py", line 30
  File "track_map.py", line 138
  File "track_map.py", line 138
  File "track_map.py", line 99
  File "track_map.py", line 372
  File "track_map.py", line 105
  File "track_map.py", line 336
  File "track_map.py", line 297
  File "track_map.py", line 321
  File "track_map.py", line 306
  File "track_map.py", line 300
  File "track_map.py", line 351
  File "track_map.py", line 99
  File "track_map.py", line 360
  File "track_map.py", line 318
  File "track_map.py", line 351
  File "track_map.py", line 315
  File "track_map.py", line 99
  File "track_map.py", line 150
  File "track_map.py", line 99
  File "track_map.py", line 330
  File "track_map.py", line 306
  File "track_map.py", line 330
  File "track_map.py", line 297
  File "track_map.py", line 306
  File "track_map.py", line 345
  File "track_map.py", line 105
  File "track_map.py", line 99
  File "track_map.py", line 186
  File "track_map.py", line 99
  File "track_map.py", line 372
  File "track_map.py", line 105
  File "track_map.py", line 294
  File "track_map.py", line 345
  File "track_map.py", line 345
  File "track_map.py", line 294
  File "track_map.py", line 366
  File "track_map.py", line 99
  File "track_map.py", line 360
  File "track_map.py", line 318
  File "track_map.py", line 351
  File "track_map.py", line 315
  File "track_map.py", line 99
  File "track_map.py", line 150
  File "track_map.py", line 99
  File "track_map.py", line 306
  File "track_map.py", line 327
  File "track_map.py", line 306
  File "track_map.py", line 330
  File "track_map.py", line 306
  File "track_map.py", line 333
  File "track_map.py", line 351
  File "track_map.py", line 105
  File "track_map.py", line 135
  File "track_map.py", line 378
  File "track_map.py", line 135
  File "track_map.py", line 378
  File "track_map.py", line 135
  File "track_map.py", line 42
  File "track_map.py", line 33
  File "track_map.py", line 30
  File "track_map.py", line 371

''')
map_to_str(l)