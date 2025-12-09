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
                print(f"Collision at index {index} -> moving to next index")
                index = (index + 1) % self.Table_Size
            
            print(f"The value Placed at index {index}")
            self.Table[index] = (key,value)    
        
    def display(self):
            print("\nCurrent Hash Table is:")
            for i, item in enumerate(self.Table):
                print(f"Index {i}: {item}")        
            
        
        
        
        
ht = hashTable(5)    # 5 is the size of the HashTable
ht.insertion(12, "Ali")     # 12 % 5 = 2
ht.insertion(7, "Sara")     # 7 % 5 = 2 --> Collision
ht.insertion(22, "Hamza")   # 22 % 5 = 2 --> Again Collision 
ht.insertion(4, "Zain")     # 4 % 5 = 4
ht.display()