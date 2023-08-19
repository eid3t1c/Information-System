
from pymongo import MongoClient
from flask import Flask,request,jsonify,Response,redirect
import json
import datetime
import os 
from hashlib import sha256


MONGODB_HOSTNAME = os.environ.get("MONGODB_HOSTNAME","mongo")


client = MongoClient("mongodb://{0}:27017/".format(MONGODB_HOSTNAME))

db = client['DigitalNotes']

Users = db['Users']
Notes = db['Notes']
Admins = db['Admins']

app = Flask(__name__)
Time = datetime.datetime.now()


global default_admin
default_admin = True
global id 
global flag
flag =0


def insertAdmin(data):
    db['Admins'].insert_one(data)
    return True 

def insert(data):
    db['Notes'].insert_one({"title": data['title'],"text" : data['text'],"keys" : data['keys'],"time" : Time,"id" : id})
    return True 


@app.route('/register',methods = ['POST'])
def register():
    data = None
    global id
    id = 0
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['email','username','name','password']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500)
    us1 = Users.find_one({"email":data['email']})
    us2 = Users.find_one({"username":data['username']})
    if us1 == None and us2 == None:
            id = sha256(str(data['email']).encode()+os.urandom(20)).hexdigest()
            User = {"email": data['email'], "username": data['username'],  "name":data['name'],  "password":data['password'],"id":id}
            Users.insert_one(User)
            return Response(data['name']+" was added to the MongoDB",status=200,mimetype='application/json')
    else:
        return Response("There is already a user with these inputs",status=200,mimetype='application/json')

@app.route('/login',methods = ['POST'])
def login():
    data = None
    global id
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    global flag
    Fields = ['email','username','password']
    if flag == 1 or flag == 2:
        return Response("You are already logged in",status = 200,mimetype="application/json")
    else:
        for i in Fields:
            if not i in data:
                return Response(i+ ' field is missing', status=500)
            us1 = Users.find_one({"email":data['email'],"username" : data['username'],"password" : data['password']}) 
            ad1 = Admins.find_one({"email":data['email'],"username" : data['username'],"password" : data['password']})
            if us1 != None:
                id = us1["id"]
                flag = 1
                return Response("Access granted for user",status = 200,mimetype="application/json")
            elif ad1 != None:
                id = ad1["id"]
                flag = 2
                return Response("Access granted for admin",status = 200,mimetype="application/json")
            else:
                return Response("Either Email,Username or Password is wrong",status = 500,mimetype='application/json')

@app.route('/createNote',methods =['POST'])
def createNote():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['title','text','keys']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500)
    if flag == 1:
        if Notes.find_one({"title" : data['title'],"id" : id}):
            return Response("Note with that title already exist",status = 500,mimetype='application/json')
        else:
            if insert(data):
                return Response('Note with title: '+data['title']+' Successfully inserted ', status=200,mimetype='application/json')
            else:
                return Response('Internal error', status=500,mimetype='application/json') 
    else:
        if flag == 2:
            return Response("You are not a User")
        else:
            return Response("You have to login first",status=500,mimetype="application/json")

@app.route('/search',methods = ['GET'])
def search():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['title']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500)
    if flag  == 1:
        if "title" in data:
            answer = Notes.find_one({'title' : data["title"],"id" : id})
            if answer != None:
                answer = {"title" : answer['title'],"text" : answer['text'],"keys" : answer['keys'],"time" : answer["time"]}
                return jsonify(answer)
            else:
                return Response("There is no such title in Notes Collection",status = 500,mimetype = 'application/json')
        else:
            return Response("Internal Error",status =500,mimetype = 'application/json')
    else:
        if flag == 2:
            return Response("You are not a User")
        else:
            return Response("You have to login first",status=500,mimetype="application/json")

@app.route('/searchKeys',methods = ['GET'])
def searchKey():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['keys']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500)
    if flag == 1:
        if "keys" in data:
            counter = Notes.find({"keys" : data["keys"], "id" : id})
            if counter != None:
                answer = []
                for key in counter:
                    key = {"title" : key["title"],"text" : key["text"],"keys" : key["keys"],"time" : key["time"]}
                    answer.append(key)
                fAnswer = sorted(answer,key = lambda a:a['time'])
                if answer == []:
                    return Response("No such keys in Notes collection",status = 500,mimetype = "application/json")
                else:
                    return jsonify(fAnswer), 200
    else:
        if flag == 2:
            return Response("You are not a User")
        else:
            return Response("You have to login first",status=500,mimetype="application/json")
        

@app.route('/update',methods = ['POST'])
def update():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad  json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['title','title2','text','keys']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500)
    if flag == 1:
        if "title" in data:
            answer = Notes.find_one({"title" : data['title'],"id" : id})
            if answer == None:
                return Response("There is no such title in Notes collection",status=500,mimetype='application/json')

            try:
                answer = Notes.update_one({"title":data['title'],"id" : id}, 
                    {"$set":
                    {
                        "title":data['title2'], 
                        "text" :data['text'], 
                        "keys" :data['keys']

                    }
                    })
                answer = Notes.find_one({"title" : data['title2'], "id" : id})    
                answer = {'title':answer['title'], 'text':answer['text'], 'keys':answer['keys'] }
                return jsonify(answer), 200
            except Exception as e:
                return Response({'Note could not be updated'},status=500,mimetype='application/json')
    else:
        if flag == 2:
            return Response("You are not a User")
        else:
            return Response("You have to login first",status=500,mimetype="application/json")
    
    
    

@app.route('/delete',methods = ['DELETE'])
def delete():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['title']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500)
    if flag == 1:
        if "title" in data:
            delete = Notes.find_one({"title":data['title'],"id" : id})
        else:
            return Response("There is no such title in Notes collection",status=500,mimetype='application/json')
        if delete != None:
            delete = Notes.delete_one({"title":data['title'],"id" : id})
            return Response("Title: "+data['title']+" Was found and deleted",status=500,mimetype='application/json')
        else:
            return Response("No such title in Notes",status=500,mimetype='application/json')
    else:
        if flag == 2:
            return Response("You are not a User")
        else:
            return Response("You have to login first",status=500,mimetype="application/json")


@app.route('/NotesByDate',methods = ['GET'])
def NoteByDate():
    data = None
    global id
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['choice']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500)
    if flag == 1:
        if data['choice'] == "Descending":
            notes = Notes.find({"id" : id})
            if notes == None:
                return Response("Couldnt find Notes",status = 500,mimetype = "application/json")
            array = []
            for date in notes:
                date = {"title" : date["title"],"text" : date["text"],"keys" : date["keys"],"time" : date["time"]}
                array.append(date)
            fAnswer = sorted(array,key = lambda b:b["time"],reverse=True)
            return jsonify(fAnswer), 200
        elif data['choice'] == "Ascending":
            notes = Notes.find({"id" : id})
            if notes == None:
                return Response("Couldnt find Notes",status = 500,mimetype = "application/json")
            array = []
            for date in notes:
                date = {"title" : date["title"],"text" : date["text"],"keys" : date["keys"],"time" : date["time"]}
                array.append(date)
            fAnswer = sorted(array,key = lambda b:b["time"],reverse=False)
            return jsonify(fAnswer), 200
        else:
            return Response("Please enter Anseding or Desending",status = 500,mimetype = "application/json")
    else:
        if flag == 2:
            return Response("You are not a User")
        else:
            return Response("You have to login first",status=500,mimetype="application/json")

@app.route('/deleteAcc',methods = ['DELETE'])
def deleteAcc():
    global flag
    if flag == 1:
            Users.delete_one({'id': id})
            Notes.delete_many({'id': id})
            flag = 0
            return Response('the person and its notes with that mail was removed', status=200,mimetype='application/json')
    else:
        if flag == 2:
            return Response("You are not a User")
        else:
            return Response("You have to login first",status=500,mimetype="application/json")
        

@app.route('/InsertAdmin',methods=['POST'])
def InsertAdmin():
    data = None
    global flag
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['username','email','password']
    if flag == 2:
        for i in Fields:
            if not i in data:
                return Response(i+ ' field is missing', status=500)
        ad1 = Admins.find_one({"username" : data['username'],"email" : data['email']})
        if  ad1 == None:
                id = sha256(str(data['email']).encode()+os.urandom(20)).hexdigest()
                admin = {"username" : data['username'],"email" : data['email'],"password" : data['password'],"id" : id}
                Admins.insert_one(admin)
                return Response("Admin with name: "+data['username']+" Successfully inserted",status = 200,mimetype='application/json')
        else:
            return Response("There is already an admin with these credentials",status = 500,mimetype = 'application/json')
    else:
        if flag == 1:
            return Response("You are not an admin")
        else:
            return Response("You have to log in first")


@app.route('/deleteUser',methods = ['DELETE'])
def deleteUser():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['username']
    for i in Fields:
        if not i in data:
            return Response(i+ ' field is missing', status=500,mimetype='application/json')
    global flag
    if flag == 2: 
            delete = Users.find_one({"username" : data['username']})
            if delete != None:
                Users.delete_one({"username" : data['username']})
                Notes.delete_many({'id' : delete['id']})
                return Response("User's account deleted",status = 200,mimetype='application/json')
            else:
                return Response("There is no such username",status= 500,mimetype='application/json')
    else:
        if flag == 1:
            return Response("You are not an admin")
        else:
            return Response("You have to log in first")

@app.route('/deleteAdmin',methods = ['DELETE'])
def deleteAdmin():
    data = None
    global flag
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("Bad Request",status=500,mimetype='application/json')
    Fields = ['username']
    if flag == 2:
        delete = Admins.find_one({"username" : data['username']})
        if delete != None:
            Admins.delete_one({"username" : data['username']})
            return Response("Admin's account deleted",status = 200,mimetype='application/json')
        else:
            return Response("There is no such username",status= 500,mimetype='application/json')
    else:
        if flag == 1:
            return Response("You are not an admin")
        else:
            return Response("You have to log in first")

@app.route('/signout',methods = ['GET'])
def signout():
    global flag
    if flag == 1 or flag == 2:
        flag = 0 
        return Response("signed out",status=200,mimetype='application/json')
    else:
        return Response("You are not logged in",status=200,mimetype='application/json')
    
@app.route('/getAdmins',methods = ['GET'])
def getAdmins():
    if flag == 2:
        documents = Admins.find({})
        ad = []
        for document in documents:
            ad_temp = {"username" : document['username'],"email" : document['email'],"password" : document['password']}
            ad.append(ad_temp)

        return jsonify(ad), 200
    else:
        if flag == 1:
            return Response("You are not an admin")
        else:
            return Response("You have to log in first")


@app.route('/getUsers',methods = ['GET'])
def getUsers():
    if flag == 2:
        documents = Users.find({})
        us = []
        for document in documents:
            us_temp = {"username" : document['username'],"email" : document['email'],"password" : document['password']}
            us.append(us_temp)

        return jsonify(us) , 200
    else:
        if flag == 1:
            return Response("You are not an admin")
        else:
            return Response("You have to log in first")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
