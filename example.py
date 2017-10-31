# import the library
from max17043 import max17043

# init a variable
m = max17043()

# read and print the voltage of the battery
print(m.getVCell())

# read and print the capacity of the battery
print(m.getVoc())

# print everything about the battery and the max17043 module
print(m)

# restart the module
m.quickStart()

# close the connection to the module
m.deinit()
