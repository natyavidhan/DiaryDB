import random
import string
import cryptocode
import json

name = input("Your Name: ")

res = ''.join(random.choices(string.ascii_letters+string.digits,k=30)) 
print("Key :"+ str(res))  

file = json.load(open('keys.json'))
file[name]=cryptocode.encrypt(res, res)
json.dump(file, open('keys.json', 'w'), indent=4)

#nGePpFhrNROLZdzwxOTKadtSX3nPSg SG2
#uCZDJJhnjrMs5iAzWuwY0Z7EWWNxHP SG