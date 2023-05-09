
rec = {}
rec['one'] = "This is one"
rec[2] = "This is two"

print(rec['one'])

rec['one'] = 'This is new one'

pr = {'name': 'john','code':6734, 'dept': 'sales'}

print (rec['one']) 

print (rec[2]) 
print (pr) 

print (pr.keys()) 

print (pr.values() )

pr.sort(key = lambda x:x['name'])
print (pr)



seq = [0, 1, 2, 3, 5, 8, 13]
filtered = filter(lambda x: x % 2 != 0, seq)
print(list(filtered))


