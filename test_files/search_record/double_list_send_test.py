list_record = [
    ['Lily', 'victory', '2019-12-05 21:08:06'],
    ['Lily', 'defeat', '2019-12-07 13:25:32']
]

# str_record = str(list_record)
# print(str_record)
# print(list(str_record))
# str_record = "&&&".join(list_record)

list_child = []
for item in list_record:
    str_child = "&&".join(item)
    list_child.append(str_child)
str_record = "&&&".join(list_child)
print(str_record)

list_record_2 = []
for ele in str_record.split("&&&"):
    list_record_2.append(ele.split("&&"))

print(list_record_2)