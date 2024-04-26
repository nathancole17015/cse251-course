# Include cse 251 common Python files
from cse251 import *
import threading
print('hello world')

# variables 

t1 = 1
t2 = dict()
t2["mykey"] = 123456
print(t2)

t3 = [1,2,3,4,5]
print(t3)



# functions 
def do_something_useful(param1 = 0,param2 = 0,param3=0):
    print("Before",param1,param2,param3)
    time.sleep(3) # could be input/output
    print("After",param1,param2,param3)


# do_something_useful(param3=45)
# do_something_useful(1,2,3)

t4 = threading.Thread(target= do_something_useful, args=(4,))
t5 = threading.Thread(target= do_something_useful, args=(5,))
t4.start()
t5.start()
t4.join()
t5.join()
# data structures 

