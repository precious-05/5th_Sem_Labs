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
            while self.Table[index] is not None:
                print(f"Collision at index {index} → moving to next index")
                index = (index + 1) % self.Table_Size
            
            self.Table[index] = (key,value)    
        
        def display(self):
            print("\nCurrent Hash Table:")
            for i, item in enumerate(self.table):
                print(f"Index {i}: {item}")        
            
        
        