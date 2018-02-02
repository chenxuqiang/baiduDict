# -*- coding: utf-8 -*-

import re
import sys

key = r"chuxiuhong@hit.edu.cn"
re1 = r'@.+?\.'
pattern = re.compile(re1)
items = pattern.findall(key)
for item in items:
    print item
