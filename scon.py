from collections import namedtuple
__version__ = "1.0"
__build__ = "Latest"
__platform__ = "Stable"
class Comment:
	'''Add a comment.'''
	isComment = True
	visComment = __name__
	uuid = object()
class SCONDecodeError(Exception):
	pass
def verify(data,x=0,y=0):
	for i in data:
		if type(data[i]) == dict:
			verify(data[i],y=y+1)
		if i == '':
			raise SCONDecodeError("Extraneous ; found "+str(x) + "," + str(y))
def parse(text):
	__doc__ = '''The parser, Used internally'''
	result = {}
	tree = []
	comments = []
	parsed = result
	listmode = False
	mode = 0
	ldepth = 0
	name = ""
	value = ""
	string = False
	wastring = False
	waslist = False
	cw = ''
	comment = ''
	for i in range(0,len(text)):
		cw += text[i]
		if cw == '=' and string == False:
			mode = 1
			cw = ''
		elif cw == '"':
			if mode == 1:
				if string:
					wastring = True
				string = not string
				cw = ''
		elif cw == '\"':
			if string:
				value += '"'
				cw = ''
		elif cw == ',' and listmode:
			if value.isnumeric() and wastring == False:
				value = int(value)
			elif value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			elif value.lower() == 'null':
				value = None
			if waslist == False:
				parsed.append(value)
			else:
				waslist = False
			value = ''
			cw = ''
			wastring = False
		elif cw == ";":
			if string:
				value += ';'
			else:
				if value.isnumeric():
					value = int(value)
				elif value.lower() == 'true':
					value = True
				elif value.lower() == 'false':
					value = False
				elif value.lower() == 'null':
					value = None
			if mode == 2:
				comments.append(comment)
				comment = ''
				mode = 0
				cw = ''
			elif listmode == False:
				parsed[name] = value
				name = ''
				value = ''
				mode = 0
				cw = ''
				wastring = False
				waslist = False
			else:
				name = ''
				value = ''
				mode = 0
				cw = ''
				listmode = False
				wastring = False
		elif cw == '\n':
			if string:
				value += '\n'
			cw = ''
		elif cw == '\t':
			if string:
				value += '\t'
			cw = ''
		
		elif cw == ' ':
			if string:
				value += ' '
			if mode == 2:
				comment += ' '
			cw = ''
		elif cw == '{' and mode == 0 and string == False:
			tree.append(parsed)
			parsed[name] = {}
			parsed = parsed[name]
			cw = ''
			name = ''
		elif cw == '}' and mode == 0 and string == False:
			parsed = tree[len(tree)-1]
			tree.pop(len(tree)-1)
			value = ''
			cw = ''
		elif cw == '[' and mode == 1 and string == False:
			tree.append(parsed)
			if type(tree[len(tree)-1]) == dict:
				parsed[name] = []
				parsed = parsed[name]
			if type(tree[len(tree)-1]) == list:
				parsed.append([])
				parsed = parsed[len(parsed)-1]
			listmode = True
			ldepth += 1
			cw = ''
			name = ''
		elif cw == ']' and mode == 1 and string == False:
			if value.isnumeric() and wastring == False:
				value = int(value)
			elif value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			elif value.lower() == 'null':
				value = None
			parsed.append(value)
			value = ''

			parsed = tree[len(tree)-1]
			tree.pop(len(tree)-1)
			cw = ''
			wastring = False
			if type(tree[ldepth-1]) == dict:
				value = ''
				name = ''
			waslist = True
			ldepth -= 1
		elif cw == "#":
			mode = 2
			cw = ''
		elif cw.isascii():
			if mode == 0:
				name += cw
			if mode == 1:
				value += cw
			if mode == 2:
				comment += cw
			cw = ''
	f = namedtuple("result",['data','comments'])
	verify(result)
	return f(data=result,comments=comments)
def make(data,ind=0,comments=[]):
	made = ''
	for i in data:
		if 'isComment' in dir(i):
			if i.visComment == __name__:
				made += '\t'*ind+'#'+data[i] + ';\n' 
		elif type(data[i]) == int:
			made += '\t'*ind+i + '=' + str(data[i]) + ';\n'
		elif type(data[i]) == str:
			made += '\t'*ind+i + '="' + data[i] + '";\n'
		elif type(data[i]) == bool:
			made += '\t'*ind+i + '=' + str(data[i]).lower() + ';\n'
		elif data[i] == None:
			made += '\t'*ind+i + '=' + 'null;\n'
		elif type(data[i]) == float:
			made += '\t'*ind+i + '="' + data[i] + '";\n'
		elif type(data[i]) == dict:
			made += '\t'*ind+i+'{\n'+make(data[i],ind+1)+'\t'*ind+'}\n'
		elif type(data[i]) == list:
			made += '\t'*ind+i+'='+data[i].__repr__().replace("'",'"')+';\n'
	return made
def dumps(obj):
	'''Creates a SCON file from a dictionary.  
##### Attribute info:
* obj  
  * type: dict

Returns a SCON string'''
	return make(obj)
def dump(obj,fp):
	'''Creates and writes a SCON file from a dictionary.  
##### Attribute info:
* obj
  * type: dict
* fp
  * type: builtin_function_or_method

Make sure that fp is writable.'''
	if not fp.writable:
		raise PermissionError("Make sure the file object is writeable")
	e = make(obj)
	fp.write(e)
	fp.close()
def loads(obj):
	'''Creates a dictonary from a SCON string.  
##### Attribute info:
* obj
  * type: str

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file.'''
	return parse(obj)
def load(fp):
	'''Creates a dictonary from a SCON file.  
##### Attribute info:
* fp
  * type: builtin_function_or_method

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file. '''
	if not fp.readable:
		raise PermissionError("Make sure the file object is readable")
	return parse(fp.read())	