import sconlite
res = sconlite.load(open('test.sco','r'))
print(res.data,res.comments)