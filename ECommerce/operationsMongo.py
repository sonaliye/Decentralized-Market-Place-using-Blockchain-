import pymongo

class operationsMongo:
    def __init__(self):
        print("Function called")
        
    def addUser(self, UserID, name, password, balance):
        try: 
            myclient = pymongo.MongoClient() 
            emp_rec1 = { 
                "UserID": UserID,
                "Name": name, 
                "Password": password,
                "Balance": balance
            }
            db = myclient["eCommerce"]
            collection = db.Person
            collection.insert_one(emp_rec1)
            print("Add User. Connected successfully!!!") 
            self.addTransactionLog(UserID + " User added.")
            return True
        except:
            print("Could not connect to MongoDB")
            self.addTransactionLog("Unable to add User at this time.")
            return False

    def modifyUser(self, UserID, oldPassword, newPassword):
        try: 
            conn = pymongo.MongoClient() 
            print("Modify User. Connected successfully!!!") 
            db = conn.eCommerce
            collection = db.Person
            myquery = { "UserID": UserID }
            for record in collection.find(myquery):
                if oldPassword==record["Password"]:
                    collection.update_many( {"UserID":UserID}, { "$set":{"Password":newPassword} } ) 
                    self.addTransactionLog("Password updated for User : " + UserID)
                    return True
            return False
        except:   
            print("Could not connect to MongoDB")
            self.addTransactionLog("Unable to update password for User at this time.")
            return False

    def modifyUserBalance(self, UserID, newBalance):
        try: 
            conn = pymongo.MongoClient() 
            print("Modify User. Connected successfully!!!") 
            db = conn.eCommerce
            collection = db.Person
            myquery = { "UserID": UserID }
            for record in collection.find(myquery):
                collection.update_many( {"UserID": UserID}, { "$set":{"Balance":newBalance} } ) 
                self.addTransactionLog("Balance updated to " + newBalance + " for User: " + UserID)
                return True
            return False
        except:   
            print("Could not connect to MongoDB")
            self.addTransactionLog("Unable to update Balance at this time.")
            return False
    
    def getUserBalance(self,UserID):
        try: 
            conn = pymongo.MongoClient() 
            print("Get User Balance. Connected successfully!!!") 
            db = conn.eCommerce
            collection = db.Person
            myquery = { "UserID":UserID}
            balance = ""
            for record in collection.find(myquery):
                balance = record["Balance"]
            if balance != "":
                return balance
            return "0"
        except:
            print("Could not connect to MongoDB")
            return "0"

    def addItem(self, ItemID, ItemName, UserID, Description, Price, Color):
        self.ItemID = ItemID
        self.ItemName = ItemName
        self.UserID = UserID
        self.Description = Description
        self.Price = Price
        self.Color = Color
        try:
            conn = pymongo.MongoClient()
            print("Add Item. Connected successfully!")
            AddedItems_rec1 = {
                "ItemID" : self.ItemID,
                "ItemName" : self.ItemName,
                "UserID" : self.UserID,
                "Description" : self.Description,
                "Price" : self.Price,
                "Color" : self.Color
            }
            db = conn.eCommerce
            collection = db.Items
            collection.insert(AddedItems_rec1)
            self.addTransactionLog("Product: " + ItemID + " successfully added. Owner: " + UserID)
            return True
        except:
            print("Could not connect to MongoDB")
            self.addTransactionLog("Unable to add item at this time.")
            return False

    def modifyItemPrice(self, ItemID, Price):
        try: 
            conn = pymongo.MongoClient() 
            print("Modify Item. Connected successfully!!!") 
            db = conn.eCommerce
            collection = db.Items
            
            result = collection.update_many( {"ItemID":ItemID}, {"$set":{"Price":Price} } )
            self.addTransactionLog("Price updated for Product: " + ItemID + ". New price: " + Price)
            return result
        except:
            self.addTransactionLog("Unable to update Price at this time.")
            print("Could not connect to MongoDB")

    def modifyItemOwner(self, ItemID, UserID):
        try: 
            conn = pymongo.MongoClient() 
            print("Modify Item. Connected successfully!!!") 
            db = conn.eCommerce
            collection = db.Items
            result = collection.update_many( {"ItemID":ItemID}, {"$set":{"UserID":UserID} } )
            return result
        except:   
            print("Could not connect to MongoDB")
    
    def getItem(self, ItemID):
        try: 
            conn = pymongo.MongoClient() 
            print("Get Item Owner. Connected successfully!!!") 
            db = conn.eCommerce
            collection = db.Items
            myquery = { "ItemID":ItemID}
            for record in collection.find(myquery):
                return record
            return False
        except:   
            print("Could not connect to MongoDB")
            return False

    def getAllItemList(self):
        ProdList = []
        try:
            conn = pymongo.MongoClient()
            print("Get All Item-List. Connected successfully!")
            db = conn.eCommerce
            collection = db.Items
            #myquery = {"ItemID" : ItemID}
            for record in collection.find():
                # print ("ItemID:" + str(record["ItemID"]))
                # print("ItemName:" + str(record["ItemName"]))
                # print("UserID:"+ str(record["UserID"]))
                # print("Description:" + str(record["Description"]))
                # print("Price:" + str(record["Price"]))
                # print("Color:" + str(record["Color"]))
                item = {}
                item['ItemID'] = str(record["ItemID"])
                item['ItemName'] = str(record["ItemName"])
                item['Description'] = str(record["Description"])
                item['UserID'] = str(record["UserID"])
                item['Color'] = str(record["Color"])
                item['Price'] = str(record["Price"])
                ProdList.append(item)
        except:
            print("Could not connect to MongoDB")
        return ProdList
        
    def getAllItemListByID(self, UserID):
        ProdList = []
        try:
            conn = pymongo.MongoClient()
            print("Get All Item-List. Connected successfully!")
            db = conn.eCommerce
            collection = db.Items
            #myquery = {"ItemID" : ItemID}
            for record in collection.find():
                if UserID != str(record["UserID"]):
                    # print ("ItemID:" + str(record["ItemID"]))
                    # print("ItemName:" + str(record["ItemName"]))
                    # print("UserID:"+ str(record["UserID"]))
                    # print("Description:" + str(record["Description"]))
                    # print("Price:" + str(record["Price"]))
                    # print("Color:" + str(record["Color"]))
                    item = {}
                    item['ItemID'] = str(record["ItemID"])
                    item['ItemName'] = str(record["ItemName"])
                    item['Description'] = str(record["Description"])
                    item['UserID'] = str(record["UserID"])
                    item['Color'] = str(record["Color"])
                    item['Price'] = str(record["Price"])
                    ProdList.append(item)
        except:
            print("Could not connect to MongoDB")
        return ProdList

    def DeleteUser(self,UserID,password):
        try:
            conn = pymongo.MongoClient()
            print("Delete User. Connected successfully!!!")
            db = conn.eCommerce
            collection = db.Person
            myquery = {"UserID" : UserID}
            for record in collection.find(myquery):
                if record["Password"]==password:
                    collection.delete_one(myquery)
                    self.addTransactionLog("Successfully deleted User: " + UserID + " from Database.")
                    return True
                else:
                    self.addTransactionLog("Unable to delete User at this time.")
                    return False
        except:
            print("Could not connect to MongoDB")
            self.addTransactionLog("Unable to delete User at this time.")
            return False

    def DeleteItem(self, ItemID):
        self.ItemID = ItemID
        try:
            conn = pymongo.MongoClient()
            print("Delete Item. Connected successfully!")
            db = conn.eCommerce
            collection = db.Items
            myquery = {"ItemID" : ItemID}
            record = collection.delete_one(myquery)
            self.addTransactionLog("Successfully deleted Item: " + ItemID + " from Database.")
            return True
        except:
            print("Could not connect to MongoDB")
            self.addTransactionLog("Unable to delete Item at this time.")
            return False

    def LoginUser(self, UserID, password):
        try:
            conn = pymongo.MongoClient()
            print("Login User. Connected successfully!!!")
            db = conn.eCommerce
            collection = db.Person
            myquery = {"UserID" : UserID}
            for record in collection.find(myquery):
                if record["Password"] == password:
                    return True
            return False
        except:
            print("Could not connect to MongoDB")
            return False

    def addActivityLog(self, log):
        try: 
            myclient = pymongo.MongoClient() 
            print("Add Ativity Log. Connected successfully!!!") 
            emp_rec1 = { 
                "Activity": log
            }
            db = myclient["eCommerce"]
            collection = db.ActivityLog
            collection.insert_one(emp_rec1)
            return True
        except:
            print("Could not connect to MongoDB")
            return False

    def getLastActivityLog(self):
        try: 
            myclient = pymongo.MongoClient() 
            print("Get Ativity Log. Connected successfully!!!") 
            db = myclient["eCommerce"]
            collection = db.ActivityLog
            lastActivity = ""
            for record in collection.find():
                lastActivity = record["Activity"]
            return lastActivity
        except:
            print("Could not connect to MongoDB")
            return ""

    def addTransactionLog(self, log):
        try: 
            myclient = pymongo.MongoClient() 
            emp_rec1 = { 
                "Transaction": log
            }
            db = myclient["eCommerce"]
            collection = db.Transactions
            collection.insert_one(emp_rec1)
            print("Add Transaction Log. Connected successfully!!!") 
            return True
        except:
            print("Could not connect to MongoDB")
            return False

    def getLastTransactionLog(self):
        try: 
            myclient = pymongo.MongoClient() 
            print("Get Transaction Log. Connected successfully!!!") 
            db = myclient["eCommerce"]
            collection = db.Transactions
            lastTransaction = ""
            for record in collection.find():
                lastTransaction = record["Transaction"]
            return lastTransaction
        except:
            print("Could not connect to MongoDB")
            return ""

# if __name__ == '__main__':
#     p1 = operationsMongo()
#     # p1.addUser("109","TSmith9","TSmith@1029")
#     p1.modifyUser("109", "abc", "efg")
#     #p1.modifyproduct("201","abc","abc","abc","abc")
#     #p1.getuser("efg")
#     #p1.getitem("202")
#     # p1.getAllItemList()