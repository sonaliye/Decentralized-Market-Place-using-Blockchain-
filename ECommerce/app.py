from flask import Flask, render_template, request
import operationsMongo
import userActivities
app = Flask(__name__)

ProdList = []
ActivityList = ['Please Login. No Activity.']
lblMessageValue = 'Execute admin operations below:'
@app.route('/')
def home():
    print('app begin')
    try:
        # opMongObj = operationsMongo.operationsMongo()
        # ProdList = opMongObj.getAllItemList()
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)
    except: 
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)

@app.route('/getMessage', methods=['GET'])
def getMessage():
    try:
        opMongObj = operationsMongo.operationsMongo()
        lastTransaction = opMongObj.getLastTransactionLog()
        if(lastTransaction):
            lblMessageValue = lastTransaction
        return render_template('admin.html', lblMessageValue = lblMessageValue)
    except: 
        print('Error Encountered.')
        return render_template('admin.html', lblMessageValue = lblMessageValue)

@app.route('/getActivityMessage', methods=['GET'])
def getActivityMessage():
    try:
        opMongObj = operationsMongo.operationsMongo()
        activityObj = userActivities.userActivities()
        # Get Last Activity from Activity Monitor for Login Status
        lastActivity = opMongObj.getLastActivityLog()
        status = activityObj.identifyActivity(lastActivity)
        if status["Activity"] == "Login":
            if status["Status"] == "Success":
                ProdList = opMongObj.getAllItemListByID(status["UserID"])
                ActivityList = [lastActivity]
        # Get Last Transaction from Transaction Status
        lastTransaction = opMongObj.getLastTransactionLog()
        if(lastTransaction):
            status2 = activityObj.identifyActivity(lastTransaction)
            if status2["Activity"] == "Buy":
                ProdList = opMongObj.getAllItemListByID(status["UserID"])
                ActivityList.append(lastTransaction)
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)
    except: 
        print('Error Encountered.')
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)

@app.route('/buyItem', methods=['POST', 'GET'])
def buyItem():
    try:
        print('Inside POST')
        itemID = str(request.form['itemID'])
        print(itemID)
        activityObj = userActivities.userActivities()
        activityObj.balanceUpdate(itemID)
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)
    except: 
        print('Error Encountered.')
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)

@app.route('/btnAddUser', methods=['POST'])
def btnAddUser():
    try:
        UserData = request.form.to_dict()
        print(UserData['addUserID'])
        print(UserData['addUsername'])
        print(UserData['addPassword'])
        print(UserData['addBalance'])
        userID = UserData['addUserID']
        userName = UserData['addUsername']
        userPassword = UserData['addPassword']
        userBalance = UserData['addBalance']
        opMongObj = operationsMongo.operationsMongo()
        opMongObj.addUser(userID, userName, userPassword, userBalance)
        return render_template('admin.html', lblMessageValue = lblMessageValue)
    except: 
        print('Error Encountered.')
        return render_template('admin.html',lblMessageValue = lblMessageValue)

@app.route('/btnUpdateUser', methods=['POST'])
def btnUpdateUser():
    try:
        UserData = request.form.to_dict()
        print(UserData['updateUserID'])
        print(UserData['updatePassword'])
        print(UserData['updateNewPassword'])
        userID = UserData['updateUserID']
        userPassword = UserData['updatePassword']
        userNewPassword = UserData['updateNewPassword']
        opMongObj = operationsMongo.operationsMongo()
        opMongObj.modifyUser(userID, userPassword, userNewPassword)
        return render_template('admin.html', lblMessageValue = lblMessageValue)
    except:
        return render_template('admin.html', lblMessageValue = lblMessageValue)

@app.route('/btnDeleteUser', methods=['POST'])
def btnDeleteUser():
    try:
        UserData = request.form.to_dict()
        print(UserData['deleteUserID'])
        print(UserData['deletePassword'])
        userID = UserData['deleteUserID']
        userPassword = UserData['deletePassword']
        opMongObj = operationsMongo.operationsMongo()
        opMongObj.DeleteUser(userID, userPassword)
        return render_template('admin.html', lblMessageValue = lblMessageValue)
    except:
        return render_template('admin.html', lblMessageValue = lblMessageValue)

@app.route('/btnAddItem', methods=['POST'])
def btnAddItem():
    try:
        UserData = request.form.to_dict()
        print(UserData['addItemID'])
        print(UserData['addItemName'])
        print(UserData['addItemDescription'])
        print(UserData['addItemColor'])
        print(UserData['addItemPrice'])
        print(UserData['addItemUserID'])
        itemID = UserData['addItemID']
        itemName = UserData['addItemName']
        itemDescription = UserData['addItemDescription']
        itemColor = UserData['addItemColor']
        itemPrice = UserData['addItemPrice']
        itemUserID = UserData['addItemUserID']
        opMongObj = operationsMongo.operationsMongo()
        opMongObj.addItem(itemID, itemName, itemUserID, itemDescription, itemPrice, itemColor)
        return render_template('admin.html', lblMessageValue = lblMessageValue)
    except:
        return render_template('admin.html', lblMessageValue = lblMessageValue)

@app.route('/btnUpdateItemPrice', methods=['POST'])
def btnUpdateItemPrice():
    try:
        UserData = request.form.to_dict()
        print(UserData['updateItemID'])
        print(UserData['updateItemPrice'])
        itemID = UserData['updateItemID']
        itemPrice = UserData['updateItemPrice']
        opMongObj = operationsMongo.operationsMongo()
        opMongObj.modifyItemPrice(itemID, itemPrice)
        return render_template('admin.html', lblMessageValue = lblMessageValue)
    except:
        return render_template('admin.html', lblMessageValue = lblMessageValue)

@app.route('/btnDeleteItem', methods=['POST'])
def btnDeleteItem():
    try:
        UserData = request.form.to_dict()
        print(UserData['deleteItemID'])
        itemID = UserData['deleteItemID']
        opMongObj = operationsMongo.operationsMongo()
        if opMongObj.DeleteItem(itemID):
            lblMessageValue = 'Item deleted successfully.'
        else:
            lblMessageValue = 'Unable to delete user.'
        return render_template('admin.html', lblMessageValue = lblMessageValue)
    except:
        return render_template('admin.html', lblMessageValue = lblMessageValue)

@app.route('/btnLogin', methods=['POST', 'GET'])
def btnLogin():
    try:
        UserData = request.form.to_dict()
        print(UserData['loginUsername'])
        print(UserData['loginPassword'])
        username = UserData['loginUsername']
        password = UserData['loginPassword']
        opMongObj = operationsMongo.operationsMongo()
        if opMongObj.LoginUser(username, password):
            ActivityLog = str(username) + ' Login Successful.'
        else:
            ActivityLog = 'Login Fail.'
        opMongObj.addActivityLog(ActivityLog)
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)
    except:
        return render_template('home.html', ProdList = ProdList, ActivityList = ActivityList)

@app.route('/admin')
def admin():
    return render_template('admin.html', lblMessageValue = lblMessageValue)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact') 
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port= 5000, debug = True)