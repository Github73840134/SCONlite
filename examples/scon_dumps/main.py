import sconlite
data = {'string':'apple',
	   'integer':0,
	   'truebool':True,
	   'falsebool':False,
	   'none':None,
	   sconlite.Comment():'A comment to top it off'}
final = sconlite.dumps(data)
file = open('demo.sco','w+')
file.write(final)
file.close()