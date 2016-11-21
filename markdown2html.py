import re;

#MD = markdown

list_level = 0;
block_tags_list = 0;
# markdown_replacing_rules = 
# {
#   #Blocks: DONE
#   "h1": ["h1", r"^#[^#]+.*$",True],
#   "h2": ["h2", r"^##[^#]+.*$",True],
#   "h3": ["h3", r"^###[^#]+.*$",True],
#   "h4": ["h4", r"^####[^#]+.*$",True],
#   "h5": ["h4", r"^#####[^#]+.*$",True],
#   "h6": ["h4", r"^######[^#]+.*$",True],
#   "h1under1": ["h1", r"^====*$", True],
#   "h1under2": ["h1", r"^----*$", True],

#   "code" : ["code", r"^    ", True],

#   #Inline, bold must go first, image must go first
#   "bold" : ["b", r"\*\*[^*]+?\*\*", True],
#   "boldunder":["b", r"__[^_]+?__",True],
#   "emphasis": ["em", r"\*[^*]+?\*", True],
#   "emphasisunder":["em", r"_[^_]+?_", True],
#   "strikethrough": ["del",r"~~[^~]+?~~", True],

#   "image" : ["img", r"\!\[.*?\]\(.*?\)", True],
#   "link": ["a", r"\[.*?\]\(.*?\)", True],
#   #List
# }

rules_order = [];
#While this line
#First through all the block elements, and get all the division of <p> and others
#Second go through each inline elements
#Replace all the other symbol elements, (simple replace)
#Next line

#Step0
#Convert /r/n to /n and other stuff, tab to space!!!
#Step1
# Line based, search for matching and replace.
#Step2
# If nothing is replace, enclose each line in <p> mode.
# Only two line break break the current mode.
#Step3
# Postprocessings
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

    def _numberOfConsecutiveCharacters(self, origStr, character, startingIndex):
        j = startingIndex
        count = 0
        while j < len(origStr):
            if origStr[j] == character:
                count += 1
            else:
                break
            j += 1
        return count 

class MDRegexTag(MDTag):
    def __init__(self, nameStr, regexStr):
        self.regexObj = re.compile(regexStr, re.DOTALL)
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

class MDMultilineTag(MDTag):
    def __init__(self, nameStr):
        super(MDMultilineTag, self).__init__(nameStr)
    
    def flush(self):
        """none -> str,
        Flush what's currently remained in the MDMultilineTag
        """
        raise Exception('Metho not implemented!')

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

class MDParaTag(MDMultilineTag):
    def __init__(self):
        self.capturingMode = False
        self.capturedStr = ""
        super(MDParaTag,self).__init__("p tag")

    def action(self,origStr):
        if self.capturingMode == False:
            self.capturingMode = True
            self.capturedStr += origStr
            return ("", True, True)
        else:
            if origStr.strip(" ") == '\n':
                returnStr = self.capturedStr
                self._reset()
                return returnStr, True, False
            else:
                self.capturedStr += origStr
                return ("", True, True)
                
    def _reset(self):
        self.capturingMode = False
        self.capturingStr = ""
        
    def flush(self):
        pass

class MDListTag(MDRegexTag, MDMultilineTag):
    """
    r" *[0-9]+\. .*"
    """
    def __init__(self):
        self._reset()
        super(MDListTag,self).__init__("list tag", r"^ *(?P<symbol>([0-9]+?\.)|-) (?P<content>.*?)")

    def action(self,origStr):
        if self.capturingMode == False:
            matchObj = self.regexObj.match(origStr)
            if matchObj is None:
                return ("",False,False)
            else:
                newString = matchObj.group("content")
                symbols = self._symbolToHtmlTag(matchObj.group("symbol"))
                self._pushStackToIndentLevel(self._numberOfStartingSpace(origStr),newString, symbols)
                self.capturingMode = True
                return ("",True,True)
        else:
            matchObj = self.regexObj.match(origStr)
            newIndent = self._numberOfStartingSpace(origStr)
            if matchObj is None and not self.escaping:
                if origStr.lstrip(' ') == '\n': #an empty line
                    self.escaping = True
                    self.capturedStrStack[-1][-1] += '\n'
                    return ("", True, True)
                else:
                     self.capturedStrStack[-1][-1] += origStr.lstrip()
                     return ("", True, True)
            elif matchObj is None and self.escaping:
                if origStr.lstrip(' ') == '\n': #an empty line
                    self.escaping = True
                    self.capturedStrStack[-1][-1] += '\n'
                    return ("", True, True)
                else:
                    self._rewindStackToIndentLevel(-1)
                    return_str = self.returnStr
                    self._reset()
                    return (return_str, False, False)
            else:
                self.escaping = False
                newString = matchObj.group("content")
                symbols = self._symbolToHtmlTag(matchObj.group("symbol"))
                
                if newIndent < self.indentStack[-1][0]:
                    if self._insertCurrentOrRewind(newIndent):
                        self._rewindStackToIndentLevel(newIndent)
                        self._insertOnCurrentStack(newString)
                    else:
                        self._insertOnCurrentStack(newString)
                elif newIndent == self.indentStack[-1][0]:
                    self._insertOnCurrentStack(newString)
                else:
                    self._pushStackToIndentLevel(newIndent, newString, symbols)
                return ("", True, True)


    #Private method
    def _symbolToHtmlTag(self,symbol):
        if symbol == "-":
            return "<ul>" , "</ul>"
        else:
            return "<ol>" , "</ol>"

    def _reset(self):
        self.escaping = False
        self.capturingMode = False
        self.indentStack = []
        self.capturedStrStack = []
        self.returnStr = ''

    def _insertCurrentOrRewind(self,newIndent):
        i = len(self.indentStack) - 1
        while i >= 0 and newIndent < self.indentStack[i][0]:
            i -= 1
        if self.indentStack[i][0] == newIndent:
            return True #Rewind
        else:
            return False #insert on current
            
    def _numberOfStartingSpace(self, origStr):
        return self._numberOfConsecutiveCharacters(origStr," ",0)

    def _pushStackToIndentLevel(self, newIndent, newString, newSymbols):
        self.capturedStrStack.append([newString])
        self.indentStack.append((newIndent, newSymbols[0], newSymbols[1]))
    
    def _insertOnCurrentStack(self, new_str):
        self.capturedStrStack[-1].append(new_str)

    def _rewindStackToIndentLevel(self, newIndent):
        i = len(self.indentStack) - 1
        #rewind stack, check which level is current stack
        while i >= 0:
            if newIndent < self.indentStack[-1][0]:
                currentCapturedStrStack = self.capturedStrStack[-1]
                del self.capturedStrStack[-1]
                self._process(currentCapturedStrStack)
                del self.indentStack[-1]
            else:
                break
            i -= 1

    def _process(self, origStrList):
        returnStr = self.indentStack[-1][1]
        for each in origStrList:
            if not (each.startswith("<ol>") or each.startswith("<ul>")):
                returnStr += r"<li>" + each + r"</li>"
            else:
                returnStr += each
        returnStr += self.indentStack[-1][2]
        if len(self.capturedStrStack) == 0:
            self.returnStr = returnStr
        else:
            self.capturedStrStack[-1].append(returnStr)
        
class MDHRTag(MDRegexTag):
    def __init__(self):
        super(MDHRTag, self).__init__("horizontal rule tag", "^ *((\*\*\*\**)|(____*)|(----*))$")
    
    def action(self, origStr):
        if self.regexObj.match(origStr):
            return ("<hr>\n", True, False)
        else:
            return ("", False ,False)

class MDQuoteTag(MDRegexTag, MDMultilineTag):
    def __init__(self):
        self._reset()
        super(MDQuoteTag, self).__init__("quote tag", r"^(> ?)+(?P<content>.*?)")
        
    def action(self,origStr):
        if self.capturingMode == False:
            matchObj = self.regexObj.match(origStr)
            if matchObj is None:
                return ("",False,False)
            else:
                newString = matchObj.group("content")
                self._pushStackToIndentLevel(self._numberOfStartingBackquote(origStr), newString)
                self.capturingMode = True
                return ("",True,True)
        else:
            matchObj = self.regexObj.match(origStr)
            newIndent = self._numberOfStartingBackquote(origStr)
            if matchObj is None and not self.escaping:
                if origStr.lstrip(' ') == '\n': #an empty line
                    self.escaping = True
                    self.capturedStrStack[-1][-1] += '\n'
                    return ("", True, True)
                else:
                     self.capturedStrStack[-1][-1] += origStr.lstrip()
                     return ("", True, True)
            elif matchObj is None and self.escaping:
                if origStr.lstrip(' ') == '\n': #an empty line
                    self.escaping = True
                    self.capturedStrStack[-1][-1] += '\n'
                    return ("", True, True)
                else:
                    self._rewindStackToIndentLevel(-1)
                    return_str = self.returnStr
                    self._reset()
                    return (return_str, False, False)
            else:
                self.escaping = False
                newString = matchObj.group("content")
                if newIndent < self.indentStack[-1]:
                    if newString == '\n': #empty
                        self.escapingLevel = True
                    else:
                        if self.escapingLevel == True:
                            self._rewindStackToIndentLevel(newIndent)
                            self._insertOnCurrentStack(newString)
                            self.escapingLevel = False
                        else:
                            self._insertOnCurrentStack(newString)
                            self.escapingLevel = False
                elif newIndent == self.indentStack[-1]:
                    self._insertOnCurrentStack(newString)
                else:
                    self._pushStackToIndentLevel(newIndent, newString)
                return ("", True, True)

            
    #Private method
    def _reset(self):
        self.escaping = False
        self.escapingLevel = False
        self.capturingMode = False
        self.indentStack = []
        self.capturedStrStack = []
        self.returnStr = ''
        
    def _numberOfStartingBackquote(self, origStr):
        i = 0
        count = 0
        while i < len(origStr):
            if origStr[i] == '>' or ' ':
                if origStr[i] == '>':
                    count += 1
            else:
                break
            i += 1
        return count
    
    
    def _insertCurrentOrRewind(self,newIndent):
        i = len(self.indentStack) - 1
        while i >= 0 and newIndent < self.indentStack[i]:
            i -= 1
        if self.indentStack[i] == newIndent:
            return True #Rewind
        else:
            return False #insert on current
            
    def _numberOfStartingSpace(self, origStr):
        return self._numberOfConsecutiveCharacters(origStr," ",0)

    def _pushStackToIndentLevel(self, newIndent, newString):
        inbetween = 0
        if len(self.indentStack) > 0:
            inbetween = newIndent - self.indentStack[-1] - 1
            for i in range(inbetween):
                self.capturedStrStack.append([''])
                self.indentStack.append(self.indentStack[-1] + inbetween + 1)
        self.capturedStrStack.append([newString])
        self.indentStack.append(newIndent)
    
    def _insertOnCurrentStack(self, new_str):
        self.capturedStrStack[-1].append(new_str)
        
    def _rewindStackToIndentLevel(self, newIndent):
        i = len(self.indentStack) - 1
        #rewind stack, check which level is current stack
        while i >= 0:
            if newIndent < self.indentStack[-1]:
                currentCapturedStrStack = self.capturedStrStack[-1]
                del self.capturedStrStack[-1]
                self._process(currentCapturedStrStack)
                del self.indentStack[-1]
            else:
                break
            i -= 1

    def _process(self, origStrList):
        returnStr = "<blockquote>"
        for each in origStrList:
            returnStr += each
        returnStr += "</blockquote>"
        if len(self.capturedStrStack) == 0:
            self.returnStr = returnStr
        else:
            self.capturedStrStack[-1].append(returnStr)

class MDCodeBlockTag(MDRegexTag, MDMultilineTag):
    def __init__(self):
        self.captureingMode = False
        self.capturedString = ""
        self.language = ""
        super(MDCodeBlockTag, r" *```(?P<language>.*)")
    
    def action(self,origStr):
        if self.capturedMode == False:
            matchObj = self.regexObj.match(origStr)
            if matchObj is None:
                return ("", False, False)
            else:
                self.captureingMode = True
                self.language = matchObj.group("language").strip()
                return ("", True, True)
        else:
            matchObj = self.regexObj.match(origStr)
            if matchObj is None:
                self.capturedString += origStr
                return ("", True, True)
            else:
                self.captureingMode = False
                returnStr = self._process()
                self._reset()
                return (returnStr, True, False)
                
    def _process(self):
        if self.language:
            return '<div><pre><code class="language-{}">{}</code></pre></div>'.format(self.language,self.capturedString)
        else:
            return '<div><pre><code class="language-none">{}</code></pre></div>'.format(self.capturedString)
        
                    
    def _reset(self):
        self.capturedString = ""
        self.captureingMode = False
        self.language = ""

#Need to happen before <p>
class MDCodeTag(MDMultilineTag):
    def __init__(self):
        self.capturingMode = False
        self.capturedStr = ""
        super(MDCodeTag, self).__init__("code tag")

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

    #Private method
    def _numberOfStartingSpace(self, origStr):
        return self._numberOfConsecutiveCharacters(origStr," ",0)

#Inline
class MDBoldTag(MDRegexTag):
    def __init__(self):
        super(MDBoldTag,self).__init__("bold tag", r"(\*\*(?P<content1>[^*]+?)\*\*)|(__(?P<content2>[^_]+?)__)")

    def _replaceBold(self, matchObj):
        if matchObj.group("content1"):
            return "<b>" + matchObj.group("content1") + "</b>"
        elif matchObj.group("content2"):
            return "<b>" + matchObj.group("content2") + "</b>"
        else:
            return ""
        
    def action(self,origStr):
        returnStr = self.regexObj.sub(self._replaceBold, origStr)
        return returnStr,False,False
    

class MDEmphasisTag(MDRegexTag):
    def __init__(self):
        super(MDEmphasisTag,self).__init__("emphasis tag", r"(\*(?P<content1>[^*]+?)\*)|(_(?P<content2>[^_]+?)_)")

    def _replaceEmphasis(self, matchObj):
        if matchObj.group("content1"):
            return "<em>" + matchObj.group("content1") + "</em>"
        elif matchObj.group("content2"):
            return "<em>" + matchObj.group("content2") + "</em>"
        else:
            return ""
            
    def action(self,origStr):
        returnStr = self.regexObj.sub(self._replaceEmphasis, origStr)
        return returnStr,False,False

class MDStrikeThroughTag(MDRegexTag):
    def __init__(self):
        super(MDStrikeThroughTag,self).__init__("strike through tag", r"~~(?P<content>[^~]+?)~~")

    def _replaceStrikeThrough(self, matchObj):
        return "<del>" + matchObj.group("content") + "</del>"

    def action(self,origStr):
        returnStr = self.regexObj.sub(self._replaceStrikeThrough, origStr)
        return returnStr,False,False
        
class MDImgTag(MDRegexTag):
    def __init__(self):
        super(MDImgTag,self).__init__("img tag",r"\!\[(?P<name>.*?)\]\((?P<src>.*?)\)")

    def _replaceImg(self, matchObj):
        return '<img src="{}" alt="{}">'.format( matchObj.group("src"), matchObj.group("name"))

    def action(self,origStr):
        returnStr = self,regexObj.sub(self._replaceImg, origStr)
        return returnStr, False, False


class MDLinkTag(MDRegexTag):
    def __init__(self):
        super(MDLinkTag,self).__init__("link tag",r"\[(?P<name>.*?)\]\((?P<src>.*?)\)")
        
    def _replaceLink(self, matchObj):
        return '<a href="{}">{}</a>'.format( matchObj.group("src"),matchObj.group("name"))
        
    def action(self,origStr):
        returnStr = self,regexObj.sub(self._replaceLink, origStr)
        return returnStr, False, False
        

class MDInlineCode(MDTag):
    def __init__(self):
        super(MDInlineCode,self).__init__("inline code tag")

    def action(self,origStr):
        i = 0
        tickList = []
        tickPairs = []
        while i <len(origStr):
            if origStr[i] == "`":
                tickcount = self._numberOfConsecutiveTicks(origStr,i)
                tickList.append([i,tickcount])
                i+= tickcount
            else:
                i+=1
        j = 0
        while j < len(tickList):
            deduction = 0
            found = False
            jchange = 0
            while found == False and tickList[j][1] - deduction > 0:
                curPosition = tickList[j][0] + deduction
                curTickCount = tickList[j][1] - deduction
                k = j + 1
                while k < len(tickList):
                    if curTickCount <= tickList[k][1]:
                        if (curTickCount < tickList[k][1]):
                            tickList.insert(k+1,[tickList[k][0]+curTickCount, tickList[k][1]-curTickCount])
                        tickList[k][1] = curTickCount
                        tickPairs.append(((curPosition,curTickCount),tickList[k]))
                        found = True
                        inbetween = 0
                        while inbetween < k-j+1:
                            del tickList[j]
                            inbetween += 1
                        jchange = -1    
                        break
                    k += 1
                deduction +=1
            j+= (1 + jchange)
            
        returnStr = ''
        nextStartIndex = 0
        for each in tickPairs:
            leftIndex = each[0][0] + each[0][1]
            rightIndex = each[1][0]
            curEndIndex = each[0][0]
            returnStr += origStr[nextStartIndex:curEndIndex] + "<code>" + origStr[leftIndex:rightIndex] +"</code>"
            nextStartIndex = each[1][0] + each[1][1]
        returnStr += [nextStartIndex:]
        return returnStr
    

    def _numberOfConsecutiveTicks(self, origStr, startingIndex):
        return self._numberOfConsecutiveCharacters(origStr,"`",startingIndex)


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
    def __init__(self):
        self.listOfTags = [MDCodeTag(),MDHeaderTag(),MDParaTag(),MDListTag(),\
        MDHRTag(),MDQuoteTag(),MDCodeBlockTag()]
 
    def parse(self, origText):
        curControl = None
        returnStr = ''
        for line in origText.splitlines(True):
            if curControl == None:
                newStr, control = self._lookForMatch(line)
                returnStr += newStr
                curControl = control
                continue
            else:
                oldcontrol = curControl
                newStr, isMatch, isContinues = curControl.action(line)
                returnStr += newStr
                if isContinuous and isMatch:
                    pass
                elif not isContinuous and isMatch:
                    curControl = None
                elif not isContinuous and not isMatch:
                    newStr, control = self._lookForMatch(line,oldcontrol)
                    returnStr += newStr
                    curControl = control
                else:
                    raise("Can't have isContinuous true while isMatch false")
        if curControl:
            returnStr += curControl.flush()
        return returnStr
            
    def _lookForMatch(self, line ,exceptTag = None):
        returnStr = ''
        control = None
        for each in self.listOfTags:
            if each != exceptTag:
                newStr, isMatch, isContinuous = each.action(line)
                returnStr += newStr
                if isContinuous and isMatch:
                    control = each
                    break
                elif not isContinuous and isMatch:
                    control = None
                    break
                elif not isContinuous and not isMatch:
                    continue
                else:
                    raise("Can't have isContinuous true while isMatch false")
        return returnStr, control
                

class MDInlineParser:
    def __init__(self):
        pass



quoteTag = MDQuoteTag()

test_code = """
> sdfasf
> > 
> > >sdsfafas
> > >
> > >fsdaf
> > >
> > > >dsfas
>
> > sdaf
> 
> 
sdfadfsa
> sdfasfa
> sd
> 
> sdf
> sdfs
> 
> 
> sdfsaf
> 
> fsdaf

sd
"""
#return_str = ""
#control = None
#for line in test_code.splitlines(True):
#    print("%%%%%%" + line.strip('\n'))
#    if (control == None):
#            print("Control none")
#            new_str,match,capture = quoteTag.action(line)
#            print("$$Add str:" + new_str)
#            return_str += new_str
#            if match:
#                    print("match!Should not do others")
#            else:
#                    print("Not match!Should do others")
#            if capture:
#                    control = quoteTag
#                    print("capture!")
#            else:
#                    control = None
#                    print("not capture!")
#    else:
#            print("Control is c")
#            new_str,match,capture = quoteTag.action(line)
#            return_str += new_str
#            print("$$Add str:" + new_str)
#            if match:
#                    print("continue match!Should not do others")
#            else:
#                    print("Not match!Out")
#            if capture:
#                    control = quoteTag
#                    print("continue capture!")
#            else:
#                    control = None
#                    print("not capture!Out")
#if control:
#    new_str,match,capture = quoteTag.action("   \nsdadfasfd\n")
#    return_str += new_str
#print(return_str)

b = MDBoldTag()
boldString = b.action("""
__sdsdafa__
_ sdasdf _
 __ sadf __
__ ssdf
asdf __

sdfasf__ sadf__
sadfas__sdafa
**
""")
print(boldString[0])
