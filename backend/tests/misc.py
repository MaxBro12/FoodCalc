from random import randint


test = '1234567890'
u = 'test'

v = randint(1,len(test))

new_test = test[0:v], test[v:]

print(new_test[0] + u + new_test[1])
