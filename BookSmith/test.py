s = {"Atharva" : {1, 2, 3, 4, }, "Joshi" : {5, 2, 4, 6, }}

for key, values in s.items():
	print(key)
	print(values)
	for p in values:
		print(p, end=" ")
	print()


print("Hello")
p = {1, 2, 3, 4, }
for i in p:
	print(i)


st = {1}
print("Is empty? : ", bool(st))

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(lst[:9])