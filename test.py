#!/usr/bin/python
from markdown2html import *


# Test:
# h = MDHeaderTag();
# print h.action("######hahsdf###")

# b = MDBoldTag();
# print b.action("sDAFSd")

c = MDCodeTag();
# test_code = """
#      This is in code

# ###sdfasf###########################
#     dsfsdaf
     
#     safaf
#       dsfs
# sdfsdfa
#     sdfaf
#    sdsdf
#     dsfasdf
#     sdfad
#     sfdaf
        
# """
# return_str = ""
# control = None
# for line in test_code.splitlines(True):
#   print("%%%%%%" + line)
#   if (control == None):
#       print("Control none")
#       new_str,match,capture = c.action(line)
#       print("$$Add str:" + new_str)
#       return_str += new_str
#       if match:
#           print("match!Should not do others")
#       else:
#           print("Not match!Should do others")
#       if capture:
#           control = c
#           print("capture!")
#       else:
#           control = None
#           print("not capture!")
#   else:
#       print("Control is c")
#       new_str,match,capture = c.action(line)
#       return_str += new_str
#       print("$$Add str:" + new_str)
#       if match:
#           print("continue match!Should not do others")
#       else:
#           print("Not match!Out")
#       if capture:
#           control = c
#           print("continue capture!")
#       else:
#           control = None
#           print("not capture!Out")
# if control:
#   new_str,match,capture = c.action("   dsf\n")
#   return_str += new_str
# print(return_str)

# inline = MDInlineCode()
# inline.action("""
# ``ds`af``
# ``saf``
# `
# `sdf ` `
# `` ` ``
# ``` `` ```
# `d```
# ```sdaf`` sdasdf``` sdfa`saf``sdvsvzx`` `` sdaf`1sv`svzxc``
#     """)


#inline = MDInlineCode()
#inline.action("""`d```
# ``""")
#listTag = MDListTag()
#test_code = """
#1. sddfavxczvz
#2. safdsa
# 3. sdfafsadf
# 4. fsddfasdf
# sdfsdafas
#         sdfsadfsaf
# - sdfasf
#                - sdfafdas
#        - fdsadfa
#- sdfadfa
#                 - fsdafdfsaf
#        - fdsafafas
#fsdfadfafadf
#3. sdfsafdaf
#                5. dsafasdfa
#        4. ssdfdafaf
#3. sdfasdfaf
#                         8. sfdasdfda
#        3. sdasdfasf
#
#- sdafdasfd
# - fsdafaf
#         - dasfasf
#
#fsdfsaf
#
#- sdfasdfa
# - dsafa
# 1. sdafdsaf
#                 - fdsafa
# - dsafaf
#- sdfadf
#- fsdfaf
#
#sdfsafda
#"""
#return_str = ""
#control = None
#for line in test_code.splitlines(True):
#    print("%%%%%%" + line.strip('\n'))
#    if (control == None):
#            print("Control none")
#            new_str,match,capture = listTag.action(line)
#            print("$$Add str:" + new_str)
#            return_str += new_str
#            if match:
#                    print("match!Should not do others")
#            else:
#                    print("Not match!Should do others")
#            if capture:
#                    control = listTag
#                    print("capture!")
#            else:
#                    control = None
#                    print("not capture!")
#    else:
#            print("Control is c")
#            new_str,match,capture = listTag.action(line)
#            return_str += new_str
#            print("$$Add str:" + new_str)
#            if match:
#                    print("continue match!Should not do others")
#            else:
#                    print("Not match!Out")
#            if capture:
#                    control = listTag
#                    print("continue capture!")
#            else:
#                    control = None
#                    print("not capture!Out")
#if control:
#    new_str,match,capture = listTag.action("   \nsdadfasfd\n")
#    return_str += new_str
#print(return_str)
#

