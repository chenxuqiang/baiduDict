# -*- coding: utf-8 -*-

import sys
import time
i = 0
x = 0
sum = 1000
result = "complete "
bar = "[>        ]"
print len(bar)
barList = list(bar)
print '\r' + bar,
for i in range(0, 1000, 1):
    if x < i / 100:
        x = i / 100
        barList[x] = '='
        if x != 9:
            barList[x + 1] = '>'
        bar = ''.join(barList)
        #print '\r'+ "comlete (%d/%d): " % (i, sum) + bar,
    else:
        print '\r' + "complete (%d/%d): " % (i, sum) + bar,
    i += 1
    time.sleep(0.01)


