li = []

for i in range(9):
    li.append(i + 3)

li2 = li[:]
# print (li == li2)
# print (li is li2)

li2 = li
# print(li2)

# print (li == li2)
# print (li is li2)

li_f = []
for i in li:
    li_f.append(i + 0.1)

print (li_f)


li.extend(li_f)
print (li)