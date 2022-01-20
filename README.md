# SCONlite
#### **S**emicolon **C**ut **O**bject **N**otation
A better way to dictonary 
## Build Info
Version: 1.0 (Limited)  
Build: Latest (Jan 20 2022 @ 6:21 PM EST)  
Platform: Stable
## Release Notes
Inital Release
***
## Description:
SCON (Pronounced: scone) is a versatile way for formmatting data and is loosely based on JSON, and can be used across multiple platforms.
## How to Use:
\**Examples can be found in the examples directory of the repo*
### Supported Types:
- `str`
- `int`
- `bool`
- `list`
- `dict`
- `NoneType`
### Comments
***
#### Comment()
Put this as a key in the dictonary and the value will become a comment.

Writing SCON
---
#### dump(obj,fp)
Creates and writes a SCON file from a dictionary.  
##### Attribute info:
* obj
  * type: dict
* fp
  * type: builtin_function_or_method

Make sure that fp is writable.
***
#### dumps(obj)
Creates a SCON file from a dictionary.  
##### Attribute info:
* obj
  * type: dict

Returns a SCON string

Reading SCON
---
#### load(fp)
Creates a dictonary from a SCON file.  
##### Attribute info:
* fp
  * type: builtin_function_or_method

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file.  
***
#### loads(obj)
Creates a dictonary from a SCON string.  
##### Attribute info:
* obj
  * type: str

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file. 
# What does a SCON file look like?
```python
string="This is a string";
int=0;
true_bool=true;
false_bool=false;
nothing=null;
list=[0,1,2,3,4,5,6,7,8,9];
sub_dictionary0{
	sub_value="I am a sub";
}
#Every line ends with semicolons execept for dictionaries. this comment will continue until you put a semicolon;
```
# You have reached the end of the documentation!
Happy database creation!
# Coming Soon
- Micropython port
***
Check out other builds such as `experimental` or `developer`
©2022 Github73840134