import sconlite
res = sconlite.loads(open('test.sco','r').read())
print(res.data,res.comments)