class MyError(Exception):
     def __init__(self, value):
       self.value = value
     def __str__(self):
       return repr(self.value)



def add( ):     
    try:
       raise MyError(2*2)
    except MyError as e:
         return 'false', e.value
        
	
var= add()
print var
if var:
   print 'true'