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

# print (li_f)


li.extend(li_f)
# print (li)

# dict

numbers = {'one' : 1, 'two' : 2, 'three' : 3, 'one' : 8, 'one' : 0}

# invalid_dict = {[1,2,3]: "123"}  # => Yield a TypeError: unhashable type: 'list'
# valid_dict = {(1,2,3):[1,2,3]}   # Values can be of any type, however.
# valid_dict = {(1,2,3):'123'}   # Values can be of any type, however.

# print(numbers.get('one'))
# print(numbers.get('four','hi'))
# print(numbers.get('four', 6))


