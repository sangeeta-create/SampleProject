#!/usr/bin/env python
# coding: utf-8

# In[1]:


def maxSalary(salRange):
    salRange = salRange.replace(",","").replace(" .","")
    if len(salRange.split('-')) == 2: 
        maxSal = salRange.split('-')[1]
        if maxSal.find('(') == -1:
            1
        else:
            maxSal = maxSal[0:maxSal.find('(')]
    else:
        maxSal = salRange.split('-')[0]
#     print(salRange)
    return int(maxSal)
#     print(sals[1])

