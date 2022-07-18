# This program was used to solve the problem for table and no table situtaion.
# I found out that when product name begins with compellent it has description and when its Dell then its table

import re

regex='\ADell'

state="Compellent Dell is a good Dell"

result=re.search(regex,state)

if result:
    print("Works")
else:
    print("Doesn't")
