# -*- coding: UTF-8 -*-
import random

s = []
while(len(s) < 10):
    x = random.randint(1,50)
    if x not in s:
        s.append(x)
i = 0
for num in s:
    i += 1;
    if (num <= 25):
        print(str(i) + ": ham" + str(num))
    else:
        print(str(i) + ": spam" + str(num - 25))