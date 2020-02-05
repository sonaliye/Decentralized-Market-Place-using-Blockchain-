import operationsMongo

class userActivities:
    def __init__(self):
        print("Function called")

    def identifyActivity(self, log):
        try:
            words = log.split()
            self.UserID = words[0]
            words.reverse()
            self.Status = "Fail"
            self.Activity = words[1]

            if words[0]=="Successful.":
                self.Status = "Success"

            singleActivity = {
                "UserID": self.UserID,
                "Activity": self.Activity,
                "Status": self.Status
            }
            print(singleActivity)
            return singleActivity
        except:
            print('Error encountered.')
            return {}

    def balanceUpdate(self, itemID):
        try:
            balance = "0"
            transactionLog = ""
            opMongObj = operationsMongo.operationsMongo()
            lastActivity = opMongObj.getLastActivityLog()
            status = self.identifyActivity(lastActivity)
            item = opMongObj.getItem(itemID)
            print(item["Price"])

            if status["Activity"] == "Login":
                if status["Status"] == "Success":
                    balance = opMongObj.getUserBalance(status["UserID"])

            if int(balance)==0 or int(balance)<int(item["Price"]):
                transactionLog = status["UserID"] +  " : Not Enough Balance. ItemID: " + itemID + ". Buy Failed."
            else:
                newUserBalance = int(balance)-int(item["Price"])
                balance = opMongObj.getUserBalance(item["UserID"])
                oldUserBalance = int(balance)+int(item["Price"])
                opMongObj.modifyItemOwner(itemID, status["UserID"])
                opMongObj.modifyUserBalance(status["UserID"],str(newUserBalance))
                opMongObj.modifyUserBalance(item["UserID"],str(oldUserBalance))
                transactionLog = status["UserID"] + " : New Balance: " + str(newUserBalance) + " ItemID: " + itemID + " Buy Successful."
            print('Updating transaction in Transactions table.')
            opMongObj.addTransactionLog(transactionLog)
            return True
        except:
            print('Unable to update Balances. No transaction done.')
            return False

# if __name__ == '__main__':
#     obj = userActivities()
#     obj.identifyActivity("sonali Login Successful.")

