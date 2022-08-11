import pymongo
from flask import Flask, render_template, request,session
app = Flask(__name__, template_folder="templtes")

connectionString="mongodb://localhost:27017/"
client = pymongo.MongoClient(connectionString)
db = client['Hostel']
mycol1 =db.owner
mycol2 = db.manager
mycol3 = db.residents
mycol4 = db.workers
mycol5 = db.residents_req
mycol6 = db.workers_req
mycol7 = db.sms_List
mycol8 = db.complains
mycol9 = db.Food_list
mycol10 = db.Rooms_list
mycol11 = db.Ordered_food
mycol12 = db.Room_allotment
mycol13 = db.available_rooms

# OWNER fUNCTIONS

def saveDataOwner():      
    ownerinfo = {
        "name": ownerName,
        "email" : ownerEmail,
        "pin":ownerPin
    }
    mycol1.insert_one(ownerinfo)

def changeDataOwner():
    filter = { 'email': email }
    newvalues = { "$set": { 'pin': pin } }
    mycol1.update_one(filter,newvalues)

def DataOwnerchange():
    filter = { 'email': email }
    newvalues = { "$set": { 'pin': password } }
    mycol1.update_one(filter,newvalues)

def verifyemail(email, password):
    global ownerEmail
    global ownerPin
    x = mycol1.find_one({"email":email})
    if(x):
        return True
    return False

def rlength():
    residents=mycol3.find()
    count=0
    for resident in residents:
        count=count+1
    return count

def wlength():
    workers=mycol4.find()
    count=0
    for worker in workers:
        count=count+1
    return count

def flength():
    foods=mycol9.find()
    count=0
    for food in foods:
        count=count+1
    return count

def roomlength():
    rooms=mycol10.find()
    count=0
    for room in rooms:
        count=count+1
    return count

def totalexpenditures():
    pass

def totalsalaries():
    workers=mycol4.find()
    count=0
    for worker in workers:
        s=int(worker.get("salary"))
        count=count+s
    return count

def saveSmsowner():
    message ={
        "msg":sms,
        "by" :"owner"
    }
    mycol7.insert_one(message)

def verifyowner(email, password):
    global ownerEmail
    global ownerPin
    x = mycol1.find_one({"email":email,"pin":password})
    if(x):
        return True
    return False

#MANAGER FUNCTIONS

def saveDataManager():      
    managerinfo = {
        "name": managerName,
        "email" : managerEmail,
        "pin":managerPin
    }
    mycol2.insert_one(managerinfo)

def saveSmsmanager():
    message ={
        "msg":sms,
        "by":"manager"
    }
    mycol7.insert_one(message)

def verifymanager(email, password):
    global managerEmail
    global managerPin
    x = mycol2.find_one({"email":email,"pin":password})
    if(x):
        return True
    return False

def saveData():       
    rinfo = {
        "name": Name,
        "email" : Email,
        "pin":Pin
    }
    mycol3.insert_one(rinfo)
    
def worker_saveData():      
    winfo = {
        "name": Name,
        "job" : job,
        "salary":Salary
    }
    mycol4.insert_one(winfo)

def DataManagerchange():
    filter = { 'email': email }
    newvalues = { "$set": { 'pin': password } }
    mycol2.update_one(filter,newvalues)

def verifyemailmanager(email, password):
    global managerEmail
    global managerPin
    x = mycol2.find_one({"email":email})
    if(x):
        return True
    return False

def saveDataFood():    
    foodinfo = {
        "name": name,
        "quantity" : quantity,
        "price":price
    }
    mycol9.insert_one(foodinfo)

def saveDataRooms():
    roominfo = {
        "typeR": typeR,
        "priceR" : priceR,
        "totalR":totalR,
        "startingR":startingR
    }
    mycol10.insert_one(roominfo)
    
def changeDataManager():
    filter = { 'email': email }
    newvalues = { "$set": { 'pin': pin } }
    mycol2.update_one(filter,newvalues)
    

# RESIDENT FUNCTIONS
def rinfo(email):
    x=mycol3.find_one({"email":email})
    return x

def rrinfo(email):
    x=mycol12.find_one({"email":email})
    return x

def create_object():
    MyEmail=session["Remail"]
    MyObject=rinfo(MyEmail)
    return MyObject

def create_object2():
    MyEmail=session["Remail"]
    MyObject=rrinfo(MyEmail)
    return MyObject

def return_email():
    return email

def verify(email, password):
    global MyName
    global MyObject
    x = mycol3.find_one({"email":email,"pin":password})
    if(x):
        MyObject=x
        return True
    return False

def totalPrice(food,quantity):
    y = mycol9.find_one({"name":food})
    quantity1=int(quantity)
    price1=int(y.get("price"))
    total1=quantity1 * (price1)
    return total1

def updatefoodList(quant):
    filter = { "name": food }
    x=mycol9.find_one(filter)
    y=int(x.get("quantity"))
    z=int(quant)
    newvalues = { "$set": { 'quantity': y-z } }
    mycol9.update_one(filter,newvalues)


def saveDataorderedFood():      
    order = {
        "email": email,
        "item":[orderf]
    }
    mycol11.insert_one(order)

@app.route("/")
def Page():
    return render_template("mainLoginPage.html")

# Owner Pages

@app.route("/loginowner")
def login1():
    return render_template("Owner/loginOwner.html")

@app.route("/ownerhome")
def owner():
    return render_template("Owner/owner.html",residents=rlength(),workers=wlength(), totalsalary=totalsalaries())

@app.route("/createAccountManager")
def AccountManager():
    return render_template("Owner/registerManager.html")

@app.route("/sendMessage")
def sendMessageManager():
    global ownerEmail
    return render_template("Owner/sendMessageToManager.html")

@app.route("/recieveMessage")
def recieveMessageManager():
    sms_List=mycol7.find()
    return render_template("Owner/recieveMessageOwner.html",smsList=sms_List)

@app.route("/residentsDetail")
def ResidentsDetail():
    id_list = mycol3.find()
    return render_template("Owner/residentDetail.html",My_List=id_list)

@app.route("/workersDetail")
def Workers():
    worker_List = mycol4.find()
    return render_template("Owner/workersDetail.html",MyList=worker_List)

@app.route("/room")
def MyownerRooms():
    room_List=mycol10.find()
    return render_template("Owner/roomsDetail.html",myList=room_List)

@app.route("/sendMessageByOwner", methods=['POST', 'GET'])
def smsSend():
    global ownerEmail
    global sms
    if request.method == "POST":
        sms = request.form['sms']
        saveSmsowner()
    return render_template("Owner/sendMessageToManager.html")
    
@app.route("/owner", methods=['POST', 'GET'])
def ownerVerfiy():
    password = request.form['pin']
    global MyEmail
    MyEmail = request.form['myemail']
    if verifyowner(MyEmail, password):
        count1=rlength()
        count2=wlength()
        return render_template("Owner/owner.html",residents=rlength(),workers=wlength(), totalsalary=totalsalaries())
    else:
        return render_template("Owner/loginOwner.html")

@app.route("/profileowner")
def profile1():
    data=mycol1.find()
    return render_template("Owner/profileOwner.html",MyList=data)

@app.route("/profilemanagerOwner")
def profile23():
    global name
    global email
    global pin
    data=mycol2.find()
    return render_template("Owner/profileManager.html", MyList=data)#,email=managerEmail, name=managerName, pin=managerPin)


@app.route("/signupmanager", methods=['POST', 'GET'])
def managerForm():
    global managerName
    global managerEmail
    global managerPin
    managerName = request.form['name1']+" "+request.form['name2']
    managerEmail = request.form['email']
    managerPin = request.form['password']
    saveDataManager()
    return render_template("Owner/owner.html",residents=rlength(),workers=wlength(), totalincome=totalexpenditures(), totalsalary=totalsalaries())

    
@app.route("/registerMyOwner")
def register():
    return render_template("Owner/registerOwner.html")

@app.route("/myregisterOwner", methods=['POST', 'GET'])
def createAcoount23():
    global ownerEmail
    global ownerName
    global ownerPin
    name = request.form['name1']+" "+request.form['name2']
    email = request.form['email']
    pin = request.form['password']
    ownerName=name
    ownerEmail=email
    ownerPin=pin
    saveDataOwner()
    return render_template("Owner/loginOwner.html")

@app.route("/forgotpinowner")
def Pin():
    return render_template("Owner/forgotpinowner.html")

@app.route("/changepasswordowner")
def loadchangepagepassword():
    global ownerEmail
    return render_template("Owner/changeownerpin.html")

@app.route("/changePinMyOwner", methods=['POST', 'GET'])
def changeownerMypin():
    global ownerEmail
    global email
    global pin
    email = request.form['owneremail']
    pin = request.form['ownerpin']
    if(verifyemail(email, pin)):
        changeDataOwner()
        return render_template("Owner/owner.html",residents=rlength(),workers=wlength(), totalincome=totalexpenditures(), totalsalary=totalsalaries())
    else:
        return render_template("Owner/changeownerpin.html")

@app.route("/frogotPinOwner", methods=['POST', 'GET'])
def changeMyOwnerPassword():
    global email
    global password
    email = request.form['myemail']
    password = request.form['pin']
    if verifyemail(email, password):
        DataOwnerchange()
        return render_template("Owner/loginOwner.html",residents=rlength(),workers=wlength(), totalincome=totalexpenditures(), totalsalary=totalsalaries())
    else:
        return render_template("Owner/forgotpinowner.html")

# Manager Pages


@app.route("/profilemanager")
def profile2():
    global name
    global email
    global pin
    data=mycol2.find()
    return render_template("Manager/profileManager.html",MyList = data)#, email=managerEmail, name=managerName, pin=managerPin)


@app.route("/loginmanager")
def login2():
    return render_template("Manager/loginManager.html")

@app.route("/managerhome")
def manager():
    return render_template("Manager/manager.html",totalresidents=rlength(),totalworkers=wlength())#, totalincome=totalexpenditures(), totalsalary=totalsalaries())#, variable=managerEmail,totalresidents=len(id_list))


@app.route("/sendMessageManager")
def sendMessageOwner():
    return render_template("Manager/sendMessageToOwner.html")#, variable=managerEmail)


@app.route("/recieveMessageManager")
def recieveMessageMYManager():
    sms_List=mycol7.find()
    return render_template("Manager/recieveMessageManager.html",smsList=sms_List)#, variable=managerEmail, smsList=sms_List)

@app.route("/sendMessageByManager", methods=['POST', 'GET'])
def smsSendManger():
    global managerEmail
    global sms
    if request.method == "POST":
        sms = request.form['sms']
        saveSmsmanager()
    return render_template("Manager/sendMessageToManager.html")#, variable=managerEmail)


@app.route("/createAccountresident")
def Account():
    return render_template("Manager/registerResident.html")



@app.route("/registerResident", methods=['POST', 'GET'])
def createAcoount():
    global Email
    global Name
    global Pin
    Name = request.form['name1']+" "+request.form['name2']
    Email = request.form['email']
    Pin = request.form['password']
    saveData()
    return render_template("Manager/manager.html")#, totalincome=totalexpenditures(), totalsalary=totalsalaries())#, variable=managerEmail,totalresidents=len(id_list))


@app.route("/addWorker")
def Woker():
    return render_template("Manager/WorkerAdd.html")


@app.route("/addFood")
def Food():
    return render_template("Manager/foodAdd.html")


@app.route("/residents")
def ResidentDetail():
    id_list = mycol3.find()
    return render_template("Manager/residentDetail.html",My_List=id_list)#, variable=managerEmail, My_List=id_list)

@app.route("/deleteResident",methods=['POST','GET'])
def delete1():
    return render_template("Manager/residentDetail.html")#, variable=managerEmail, My_List=id_list)

@app.route("/workers")
def Worker():
    worker_List = mycol4.find()
    return render_template("Manager/workersDetail.html",MyList=worker_List)#, variable=managerEmail)

@app.route("/deleteWorker",methods=['POST','GET'])
def delete2():
    if request.method=="POST":
        index=request.form['myindex']
        index=int(index)-1
      
    return render_template("Manager/workersDetail.html")#, variable=managerEmail)

@app.route("/Rooms")
def MyRoom():
    global room_List
    room_List=mycol10.find()
    return render_template("Manager/roomsDetail.html",myList=room_List)#, variable=managerEmail, myList=room_List)

@app.route("/deleteRoom",methods=['POST','GET'])
def delete3():
    if request.method=="POST":
        index=request.form['myindex']
        index=int(index)-1
        #room_List.pop(index)
    return render_template("Manager/roomsDetail.html")#, variable=managerEmail, myList=room_List)

@app.route("/foods")
def MyFoods():
    food_List=mycol9.find()
    return render_template("Manager/foodDetail.html", MyList=food_List)#, variable=managerEmail, MyList=food_List)

@app.route("/deleteFood",methods=['POST','GET'])
def delete4():
    if request.method=="POST":
        index=request.form['myindex']
        index=int(index)-1
        #food_List.pop(index)
        #saveDataFood()
    return render_template("Manager/foodDetail.html")#, variable=managerEmail, MyList=food_List)

@app.route("/complains")
def Mycomplains():
    complains=mycol8.find()
    return render_template("Manager/recievedComplains.html",listcomplains=complains)#, variable=managerEmail, listcomplains=complains)


@app.route("/addworker", methods=['POST', 'GET'])
def Workersadd():
    global managerEmail
    global job
    global Name
    global Salary
    Name = request.form['name1']+" "+request.form['name2']
    job = request.form['job']
    Salary =request.form['salary']
    worker_saveData()
    return render_template("Manager/manager.html")#, variable=managerEmail,totalresidents=len(id_list))

@app.route("/manager", methods=['POST', 'GET'])
def managerVerfiy():
    password = request.form['pin']
    global MyEmail
    MyEmail = request.form['myemail']
    if verifymanager(MyEmail, password):
        return render_template("Manager/manager.html",totalresidents=rlength(),totalworkers=wlength(),totalfoods=flength(),types=roomlength())#, variable=managerEmail,totalresidents=len(id_list)),
    else:
        return render_template("Manager/loginManager.html")

@app.route("/addFastFood", methods=['POST', 'GET'])
def fastFood():
    global name
    global quantity
    global price
    name = request.form['name1']+" "+request.form['name2']
    quantity = request.form['quantity']
    price = request.form['price']
    saveDataFood()
    return render_template("Manager/foodDetail.html")#, variable=managerEmail, MyList=food_List)

@app.route("/changepasswordmanager")
def loadchangepagepasswordmanager():
    global managerEmail
    return render_template("Manager/changemanagerpin.html")#, variable=managerEmail)


@app.route("/forgotmanagerpin")
def managerforgotpin():
    return render_template("Manager/forgotpinmanager.html")


@app.route("/changePinMyManager", methods=['POST', 'GET'])
def changemanagerMypin():
    global managerEmail
    global email
    global pin
    email = request.form['manageremail']
    pin = request.form['managerpin']
    if(verifyemailmanager(email, pin)):
        changeDataManager()
        return render_template("Manager/manager.html")#, variable=managerEmail,totalresidents=len(id_list))
    else:
        return render_template("Manager/changemanagerpin.html")#, variable=managerEmail)

@app.route("/frogotPinManager", methods=['POST', 'GET'])
def changeMyManagerPassword():
    email = request.form['myemail']
    password = request.form['pin']
    if verifyemailmanager(email, password):
        DataManagerchange()
        return render_template("Manager/loginManager.html")
    else:
        return render_template("Manager/forgotpinmanager.html")

@app.route("/requestsResidents")
def requests1():
    request_residence=mycol5.find()
    return render_template("Manager/requestResidence.html", MyList=request_residence)

@app.route("/deleteResidentapply",methods=['POST','GET'])
def delete11():
    if request.method=="POST":
        index=request.form['myindex']
        index=int(index)-1
        
    return render_template("Manager/requestResidence.html")

@app.route("/requestsJobs")
def requests2():
    request_jobs=mycol6.find()
    return render_template("Manager/requestsJobs.html", MyList=request_jobs)
    
@app.route("/deleteJob",methods=['POST','GET'])
def delete22():
    if request.method=="POST":
        index=request.form['myindex']
        index=int(index)-1
       
    return render_template("Manager/requestsJobs.html")#, variable=managerEmail)

@app.route("/changinRoom")
def ChangeRoom():
    return render_template("Manager/Rooms.html")#, variable=managerEmail)


@app.route("/addanewmyRoom", methods=['POST', 'GET'])
def NewRoom():
    global typeR
    global priceR
    global totalR
    global startingR
    room_List=mycol10.find()
    if request.method == "POST":
        typeR = request.form['typeR']
        priceR = request.form['priceR']
        totalR = request.form['totalR']
        startingR = request.form['startingR']
        saveDataRooms()
    return render_template("Manager/roomsDetail.html",myList=room_List)#, variable=managerEmail, myList=room_List)

# Login Resident

@app.route("/login")
def residentLogin():
    return render_template("Resident/loginResident.html")

@app.route("/profileresident")
def profile3():
    global name
    global email
    global pin
    MyObject=create_object()
    MyEmail=MyObject.get("email")
    MyName=MyObject.get("name")
    MyPin=MyObject.get("pin")
    return render_template("Resident/profileResident.html",email=MyEmail, name=MyName, pin=MyPin)


@app.route("/resident")
def resident():
    global MyObject
    MyEmail=session["Remail"]
    x=create_object2()
    y=x.get("typeR")
    z=x.get("Rno")
    sum="150"
    return render_template("Resident/resident.html",typeR=y,Rno=z,expen=sum, variable=MyEmail)


@app.route("/getRoom")
def allotmet():
    MyEmail=session["Remail"]
    room_List=mycol10.find()
    available=mycol13.find()
    return render_template("Resident/allotmentofRoom.html", roomlist=room_List,variable=MyEmail, noR=available)


@app.route("/orderfood")
def FastFood():
    global food_List
    MyEmail=session["Remail"]
    food_List=mycol9.find()
    return render_template("Resident/orderFood.html", foodList=food_List,variable=MyEmail)


@app.route("/orderfooddetail")
def FastFoodDetail():
    global MyEmail
    MyEmail=session["Remail"]
    x = mycol11.find_one({"email":MyEmail})
    if(x):
        item=x.get("item")
        y = mycol9.find({})
        return render_template("Resident/orderedfoods.html",MyList=item,MyDict=y, variable=MyEmail)
    else:
        return render_template("Resident/orderedfoods.html", variable=MyEmail)


@app.route("/foodDetail")
def FoodDetail():
    MyEmail=session["Remail"]
    food_List=mycol9.find()
    return render_template("Resident/foodDetails.html", MyList=food_List, variable=MyEmail)


@app.route("/sendComplains")
def complainssend():
    MyEmail=session["Remail"]
    return render_template("Resident/sendComplains.html", variable=MyEmail)


@app.route("/sendComplain", methods=['POST', 'GET'])
def compalinsend():
    global MyName
    global complain
    if request.method == "POST":
        complain = request.form['sms']+","
        saveComplains()
    return render_template("Resident/sendComplains.html", variable=MyEmail)

def saveComplains():
    MyEmail=session["Remail"]
    message ={
        "complain":complain,
        "by":MyEmail
    }
    mycol8.insert_one(message)




@app.route("/success", methods=['POST', 'GET'])
def loginVerfiy():
    global MyEmail
    global MyPin
    MyPin = request.form['pin']    
    MyEmail = request.form['myemail']
    session["Remail"]=MyEmail
    MyObject=create_object2()
    
    if verify(MyEmail, MyPin):
        x=mycol12.find_one({"email":MyEmail})
        if(x):   
            y=x.get("typeR")
            z=x.get("Rno")
            sum="150"
            return render_template("Resident/resident.html", variable=MyEmail,typeR=y,Rno=z,expen=sum)
        else:
            return render_template("Resident/resident.html", variable=MyEmail)
    else:
        return render_template("Resident/loginResident.html")


@app.route("/forgotpinresident")
def changepin():
    return render_template("Resident/changeresidentpin.html", variable=MyEmail)


@app.route("/changepinresident")
def residentpin():
    return render_template("Resident/forgot-pin-resident.html")


@app.route("/changePinMyResident", methods=['POST', 'GET'])
def changeResidentMypin():
    MyEmail=session["Remail"]
    x=create_object2()
    y=x.get("typeR")
    z=x.get("Rno")
    sum="150"
    email = request.form['residentemail']
    password = request.form['residentpin']
    if(verifyemailResident(email, password)):
        changeDataResident(email,password)
        return render_template("Resident/resident.html", variable=MyEmail,typeR=y,Rno=z,expen=sum)
    else:
        return render_template("Resident/changeresidentpin.html", variable=managerEmail)


@app.route("/frogotPinResident", methods=['POST', 'GET'])
def changeMyResidentPassword():
    email = request.form['myemail']
    password = request.form['pin']
    if verifyemailResident(email, password):
        changeDataResident()
        return render_template("Resident/loginResident.html")
    else:
        return render_template("Resident/forgot-pin-resident.html")

def changeDataResident(email,password):
    filter = { 'email': email }
    newvalues = { "$set": { 'pin': password } }
    mycol3.update_one(filter,newvalues)

def verifyemailResident(email, password):
    x = mycol3.find_one({"email":email,"pin":password})
    if(x):
        return True
    return False


@app.route("/getnewRoom", methods=['POST', 'GET'])
def Myroom():
    global roomno
    global roomtype
    global email
    global password
    MyEmail = session["Remail"]

    sum="150"
    email = request.form['myemail']
    password = request.form['pin']
    roomtype = request.form['room']
    roomno = request.form['room_no.']
    if verify(email, password):
        saveDataResidentroom()
        x = create_object2()
        y = x.get("typeR")
        z = x.get("Rno")
        return render_template("Resident/resident.html", variable=MyEmail,typeR=y,Rno=z,expen=sum)
    else:
        return render_template("Resident/allotmentofRoom.html", variable=MyEmail, roomlist=room_List)

def saveDataResidentroom():
    roominfo = {
        "email":email,
        "Rno":roomno,
        "typeR": roomtype
    }

    rno=int(roomno)
    myquery = {"Rno": rno}
    mycol12.insert_one(roominfo)
    mycol13.delete_one(myquery)

@app.route("/orderfoodnow", methods=['POST', 'GET'])
def ordermyfood():
    global email
    global food
    global quantity
    global orderf
    email = request.form['oemail']
    password = request.form['pin']
    food = request.form['food']
    quantity = request.form['quantity']
    total = totalPrice(food,quantity)
    orderf={"food":food,"quantity":quantity,"total":total}
    if verify(email, password):
        global MyObject
        updatefoodList(quantity)
        x=mycol11.find_one({"email":email})
        if(x):
            y=x.get("item")
            y.append(orderf)
            filter = { 'email': email }
            newvalues = { "$set": { 'item': y } }
            mycol11.update_one(filter,newvalues)

        else:
            saveDataorderedFood()
        return render_template("Resident/orderFood.html")#, variable=MyEmail)#, foodList=MyObject.myOrderedFoods)
    else:
        return render_template("Resident/orderFood.html", variable=MyEmail, foodList=food_List)
    


@app.route("/peoplehome")
def people():
    return render_template("people.html")


@app.route("/applyresidence")
def peopleApply1():
    return render_template("ResidenceApply.html")


@app.route("/applyjob")
def peopleApply2():
    return render_template("ApplyJob.html")

@app.route("/applyResidence",methods=['POST','GET'])
def apply1():
    if request.method=="POST":
        global Email
        global Name
        global Pin
        Name=request.form['name1']+" "+request.form['name2']
        Email = request.form['email']
        Pin = request.form['pin']
        saveDataRequestsResidents()
        return render_template("people.html")
    return render_template("ResidenceApply.html")

def saveDataRequestsResidents():
    rinfo = {
        "name": Name,
        "email" : Email,
        "pin":Pin
    }
    mycol5.insert_one(rinfo)

@app.route("/applyJob",methods=['POST','GET'])
def apply2():
    global job
    global Name
    global Email
    if request.method=="POST":
        Name=request.form['name1']+" "+request.form['name2']
        Email = request.form['email']
        job=request.form['job']
        saveDataRequestsWorker()
        return render_template("people.html")
    return render_template("ApplyJob.html")

def saveDataRequestsWorker():       ##***********************************
    winfo = {
        "name": Name,
        "job" : job,
        "email":Email
    }
    mycol6.insert_one(winfo)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
