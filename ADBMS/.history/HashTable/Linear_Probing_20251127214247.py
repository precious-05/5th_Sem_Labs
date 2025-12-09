# Understanding the Hash Table using the Open Addressing (Linear Probing)
class hashTable:
    def __init__(self,Table_Size):
        self.Table_Size=Table_Size
        self.Table = [None]*Table_Size   #------------  This will create [None, None, None, None, None]   
        
        def hash(self,key):
            return key % self.Table_Size   #-----------  Formula:   Key % Array_Size
        
        
        def insertion(self, key, value):
            index = self.hash(key)
            
            print(f"\nInserting key={key}, value ='{value}'")
            print(f"Initial hashed index is = {index}")
            
            
            #------------ Insertion Using Linearr probing 
            
            
        
        