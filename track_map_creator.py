
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

with open("track_map.py","w") as fd:
    create_track(fd)
    create_map(fd)

# import track_map
# track_map.ascii("abc")
l = [294,297,299]
def map_to_str(l = []):
    s = ""
    if len(l) == 0:
        return ""
    else:
        l[len(l) - 1] += 1
    for c in l:
        s += chr(c/3-1)
    print s


map_to_str(l)