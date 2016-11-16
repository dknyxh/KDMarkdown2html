import re;

#MD = markdown

list_level = 0;
block_tags_list = 0;
# markdown_replacing_rules = 
# {
# 	#Blocks: DONE
# 	"h1": ["h1", r"^#[^#]+.*$",True],
# 	"h2": ["h2", r"^##[^#]+.*$",True],
# 	"h3": ["h3", r"^###[^#]+.*$",True],
# 	"h4": ["h4", r"^####[^#]+.*$",True],
# 	"h5": ["h4", r"^#####[^#]+.*$",True],
# 	"h6": ["h4", r"^######[^#]+.*$",True],
# 	"h1under1": ["h1", r"^====*$", True],
# 	"h1under2": ["h1", r"^----*$", True],

# 	"code" : ["code", r"^    ", True],

# 	#Inline, bold must go first, image must go first
# 	"bold" : ["b", r"\*\*[^*]+?\*\*", True],
# 	"boldunder":["b", r"__[^_]+?__",True],
# 	"emphasis": ["em", r"\*[^*]+?\*", True],
# 	"emphasisunder":["em", r"_[^_]+?_", True],
# 	"strikethrough": ["del",r"~~[^~]+?~~", True],

# 	"image" : ["img", r"\!\[.*?\]\(.*?\)", True],
# 	"link": ["a", r"\[.*?\]\(.*?\)", True],
# 	#List
# }

rules_order = [];
#While this line
#First through all the block elements, and get all the division of <p> and others
#Second go through each inline elements
#Replace all the other symbol elements, (simple replace)
#Next line

#Step0
#Convert /r/n to /n and other stuff
#Step1
# Line based, search for matching and replace.
#Step2
# If nothing is replace, enclose each line in <p> mode.
# Only two line break break the current mode.
#Step3
# ?
#Step4
# Profit!


class MDTag(object):
	def __init__(self,nameStr):
		self.nameStr = nameStr
	def action(self, origStr):
		""" str -> str, ismatch(bool), ismutiline
		Take a string and do manipulation to the string

		Return a string after the modification.
		bool, if the bool is true, caller shouldn't call others
		another bool, if the bool is true, the caller should continue call
		the method on the next string.
		"""
		raise Exception('Method not implemented!')

	def flush(self):
		pass

class MDRegexTag(MDTag):
	def __init__(self, nameStr, regexStr):
		self.regexObj = re.compile(regexStr)
		super(MDRegexTag, self).__init__(nameStr)

	def action(self, origStr):
		""" str -> str, ismatch(bool), ismutiline
		Take a string and do manipulation to the string

		Return a string after the modification.
		bool, if the bool is true, caller shouldn't call others
		another bool, if the bool is true, the caller should continue call
		the method on the next string.
		"""
		raise Exception('Method not implemented!')


#block level
class MDHeaderTag(MDRegexTag):
	def __init__(self):
		rawString = ""
		for i in range(6):
			if (i!=0):
				rawString += r"|"
			rawString += r"(^"+'#'*(i+1)+r"[^#\n]+.*$)"
		super(MDHeaderTag, self).__init__("header tag", rawString)


	def action(self, origStr):
		matchObj = self.regexObj.match(origStr)
		if matchObj is None:
			return ("", False ,False)
		else:
			return (self.process(matchObj), True , False)

	def process(self,matchObj):
		""" matchObj -> str
		Take a matchObj and do manipulation to the string
		Return a string after the modification
		"""
		count = 0
		newString = matchObj.group(0)
		for ch in newString:
			if ch == "#":
				count+=1
			else:
				break
		newString = newString.strip("#")
		newString = "<h{}>{}</h{}>".format(str(count), newString, str(count))
		return newString

class MDParaTag(MDTag):
	def __init__(self):
		self.capturingMode = False
		self.capturingStr = ""
		super(MDParaTag,self).__init__("p tag")

	def action(self,origStr):
		if self.capturingMode == False:
			if origStr.strip() != '\n':
				pass
		else:
			pass

class MDListTag(MDRegexTag):
	pass


#Need to happen before <p>
class MDCodeTag(MDTag):
	def __init__(self):
		self.capturingMode = False
		self.capturedStr = ""
		super(MDCodeTag, self).__init__("code tag")

	#Private method
	def _numberOfStartingSpace(self, origStr):
		count = 0;
		for ch in origStr:
			if ch == ' ':
				count+=1
			else:
				break
		return count

	def action(self, origStr):
		if self.capturingMode == False:
			numberOfWhiteSpace = self._numberOfStartingSpace(origStr)
			if numberOfWhiteSpace >= 4 and origStr[numberOfWhiteSpace]!='\n':
				self.capturingMode = True
				self.capturedStr += origStr[numberOfWhiteSpace:]
				return ("", True, True)
			else:
				return (origStr, False, False)
		else:
			numberOfWhiteSpace = self._numberOfStartingSpace(origStr)
			if numberOfWhiteSpace >= 4:
				self.capturedStr += origStr[4:]
				return ("",True,True)
			elif numberOfWhiteSpace < 4 and origStr[numberOfWhiteSpace] == '\n':
				self.capturedStr += origStr[numberOfWhiteSpace:]
				return ("",True,True)
			else:
				self.capturingMode = False
				return_str = self.process(self.capturedStr)
				self.capturedStr = ""
				return (return_str,False,False)

	def flush(self):
		pass


	def process(self,capturedStr):
		return '<div><pre><code class="language-none">' + capturedStr + "</code></pre></div>\n"



#Inline
class MDBoldTag(MDRegexTag):
	def __init__(self):
		super(MDBoldTag,self).__init__("bold tag", r"\*\*[^*]+?\*\*")

	def action(self,origStr):
		matchObj = self.regexObj.match(origStr)
		if matchObj:
			pass
		else:
			return ("", False, False)

class MDEmphasisTag(MDRegexTag):
	def __init__(self):
		super(MDEmphasisTag,self).__init__("emphasis tag", r"\*[^*]+?\*")

	def action(self,origStr):
		pass

class MDStrikeThroughTag(MDRegexTag):
	def __init__(self):
		super(MDStrikeThroughTag,self).__init__("strike through tag", r"~~[^~]+?~~")

	def action(self,origStr):
		pass

class MDImgTag(MDRegexTag):
	pass

class MDLinkTag(MDRegexTag):
	pass


#Parser
class MDParser:
	def __init__():
		self.orderList = [];
	"""
	Private:
		Convert the one linw to MDTag
	"""
	def _convertLineToMDTag(line):
		pass

	def parse(mdstring):
		pass
		return self.orderList

	def render():
		pass
		return html

class MDBlockParser:
	pass

class MDInlineParser:
	pass
# Test:
h = MDHeaderTag();
print h.action("######hahsdf###")

# b = MDBoldTag();
# print b.action("sDAFSd")

c = MDCodeTag();
test_code = """
     This is in code

###sdfasf###########################
    dsfsdaf
   
    safaf
      dsfs
sdfsdfa
    sdfaf
   sdsdf
    dsfasdf
    sdfad
    sfdaf
    
"""
return_str = ""
control = None
for line in test_code.splitlines(True):
	print("%%%%%%" + line)
	if (control == None):
		print("Control none")
		new_str,match,capture = c.action(line)
		print("$$Add str:" + new_str)
		return_str += new_str
		if match:
			print("match!Should not do others")
		else:
			print("Not match!Should do others")
		if capture:
			control = c
			print("capture!")
		else:
			control = None
			print("not capture!")
	else:
		print("Control is c")
		new_str,match,capture = c.action(line)
		return_str += new_str
		print("$$Add str:" + new_str)
		if match:
			print("continue match!Should not do others")
		else:
			print("Not match!Out")
		if capture:
			control = c
			print("continue capture!")
		else:
			control = None
			print("not capture!Out")
if control:
	new_str,match,capture = c.action("   dsf\n")
	return_str += new_str
print(return_str)
