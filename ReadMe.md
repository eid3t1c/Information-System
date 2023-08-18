## Simple Information System Documentation

This is a simple Information System that consists of Users and Admins.

## Used in this project

- Docker
- Python 3
- Flask
- Pymongo
- Image of MongoDB


## Running the Web Service

1. Run the following command to start the containers:
   ```cmd sudo docker-compose up -d ```
   This will create two containers: one for MongoDB and another for the web service.
   That's it! You've successfully set up the Information System and its dependencies.

## LocalHost

client = MongoClient('mongodb://localhost:27017/')

## Collections Of The DataBase

1. db = client['DigitalNotes']

2. Users = db['Users']

3. Notes = db['Notes']

4. Admins = db['Admins']


## <p align="center">Registration</p>

**Endpoint:** /register
**Method:**   Post

To successfully register a new user, you need to provide the following JSON data fields:

1. **Email:**    The email address of the user.
2. **Username:** The desired username for the user's account.
3. **Name:**     The full name of the user.
4. **Password:** The password for the user's account.

If any of these fields are missing, the system will generate an appropriate error message indicating which field is missing.

## User Registration Process

1. The web service checks if all required fields are provided and not empty.
2. If all fields are provided, the service searches through the users collection to determine if the given credentials (email or username) already exist in the database.
   ```python
	us1 = Users.find_one({"email":data['email']})
	us2 = Users.find_one({"username":data['username']}) ```
3. In cases where the provided credentials are not locatable within the database, a distinct identifier is generated through the process of hashing the user's email along with a concatenation of 20 randomly generated bytes. Subsequently, a novel JSON entity encompassing the user's pertinent details is meticulously crafted and subsequently preserved within the designated Users collection.
   ```python
	User = {"email": data['email'], "username": data['username'],  "name":data['name'],  "password":data['password']}
        Users.insert_one(User) ```
4. Upon successful registration, a confirmation message is returned.
	```python
	return Response(data['name']+" was added to the MongoDB",status=200,mimetype='application/json')```
5. Upon unsuccesful registration, an error message is returned.
   	```python
	return Response("There is already a user with these inputs",status=200,mimetype='application/json')```


### POSTMAN: 
```json
{
  "email": "pallis@gmail.com",
  "username": "eid3t1c",
  "name": "alex",
  "password": "s3cr3t"
}
```
### CURL:
```bash
curl -X POST http://127.0.0.1:5000/register -H 'Content-Type:application/json' -d '{ "email" : "pallis@gmail.com" , "username" : "eid3t1c", "name" : "alex","password" : "s3cr3t"}'
```
## result:
**alex was added to the MongoDB**
		   
## <p align="center">Login</p>

**Endpoint:** /login
**Method:**   Post

To successfully login, you need to provide the following JSON data fields:

1. **Email:**    The email address of the user.
2. **Username:** The desired username for the user's account.
3. **Password:** The password for the user's account.

If any of these fields are missing, the system will generate an appropriate error message indicating which field is missing.

## User Login Process

1. The web service checks if all required fields are provided and not empty.
2. If all fields are provided, the service searches through the users collection to determine if the given credentials (email,username,password) already exist in the database.
   ```python
	us1 = Users.find_one({"email":data['email'],"username" : data['username'],"password" : data['password']}) 
        ad1 = Admins.find_one({"email":data['email'],"username" : data['username'],"password" : data['password']}) ```
3. If the credentials are  found in the database, the proper privilidges are given depending if the credentials were found in the user's collection or the admin's collection.
   ```python
	if us1 != None:
                id = us1["id"]
                flag = 1
                return Response("Access granted for user",status = 200,mimetype="application/json")
            elif ad1 != None:
                id = ad1["id"]
                flag = 2
                return Response("Access granted for admin",status = 200,mimetype="application/json")
4. Upon successful Login, a confirmation message is returned.
	```python
	return Response("Access granted for admin",status = 200,mimetype="application/json")
	return Response("Access granted for user",status = 200,mimetype="application/json")```
5. Upon unsuccesful Login, an error message is returned.
   	```python
	return Response("Either Email,Username or Password is wrong",status = 500,mimetype='application/json')```
    
## User Authentication and Role Management System

The system employs a `flag` variable to manage user authentication and access levels. By default, `flag` is set to 0, allowing access to the "register" and "login" services.

### User Role

- When `flag` is set to 1, it indicates that a user is successfully authenticated and logged in.
- Users with a `flag` value of 1 gain access to features reserved for authenticated users.

### Admin Role

- If `flag` is changed to 2, it signals the authentication of an admin.
- Admins, identified by a `flag` value of 2, enjoy elevated privileges and access to admin-specific functionalities.

### POSTMAN: 
```json
{
  "email": "pallis@gmail.com",
  "username": "eid3t1c",
  "password": "s3cr3t"
}
```
### CURL:
```bash
curl -X POST http://127.0.0.1:5000/login -H 'Content-Type:application/json' -d '{ "email" : "pallis@gmail.com" , "username" : "eid3t1c","password" : "s3cr3t"}'
```
## Result:
**Access granted for user**
		
							
## <p align="center">Create Notes</p>

**Endpoint:** /createNote
**Method:**   Post

To successfully create a note, you need to provide the following JSON data fields:

1. **Title:** The title of your note.
2. **text:**  The text that will be included to your note.
3. **keys:**  Keywords that are included to the note's text.
4. **email:** The email address of the user (it is required for the delete service).

If any of these fields are missing, the system will generate an appropriate error message indicating which field is missing.

## Create Note process

1. The web service checks if all required fields are provided and not empty.
2. When all required fields are provided, the service will generate a new note using the provided information. Each note is associated with the id of the user who created it. This ensures that there are no issues related to name or text collisions with other users.
   ```python
	db['Notes'].insert_one({"title": data['title'],"text" : data['text'],"keys" : data['keys'],"time" : Time,data['id] : id})
    	return True  ```
3.  Upon successful note creation, a confirmation message is returned.
	```python
	return Response('Note with title: '+data['title']+' Successfully inserted ', status=200,mimetype='application/json')```
4. Upon unsuccesful note creation, an error message is returned.
   	```python
	return Response('Internal error', status=500,mimetype='application/json') ```

### POSTMAN: 
```json
{
  "title" : "Capture The Flag",
  "text" : "Solve MDFlag from Cryptohack.org , category: Hash Functions",
  "keys" : ["Solve","MDFlag","Hash"],
  "email" : "pallis@gmail.com"
}
```
### CURL:
```bash
curl -X POST http://127.0.0.1:5000/createNote -H 'Content-Type:application/json' -d '{ "title" : "Capture The Flag","text" : "Solver MDFlag from Cryptohack.org , category: Hash Functions","keys" : ["Solve","MDFlag","Hash"],"email" : "pallis@gmail.com"}'
```
## Result: 
**Note with title: Capture The Flag Successfully inserted**
		   
 
## <p align="center">Search Note</p>

**Endpoint:** /search
**Method:**   Get

To successfully search a note, you need to provide the following JSON data fields:

1. **Title:** The title of your note.

If Title is missing, the system will generate an appropriate error message.

## Search Note process

1. The web service checks if title is provided and not empty.
2. If title is provided, the service searches through the Notes collection to determine if the title exist in the database.
   ```python
	answer = Notes.find_one({'title' : data["title"]}) ```
3. If a note with the given title is found in the Notes's collection , a json object with the fields of that note is returned.
   ```python
	answer = {"title" : answer['title'],"text" : answer['text'],"keys" : answer['keys'],"time" : answer["time"]}
        return jsonify(answer)```
4. Upon unsuccesful seaech note, an error message is returned.
   	```python
	return Response("There is no such title in Notes Collection",status =500,mimetype = 'application/json')```


### POSTMAN: 
```json
{
  "title" : "Capture The Flag"
}
```
### CURL:
```bash
curl -X GET http://127.0.0.1:5000/search -H 'Content-Type:application/json' -d '{"title" : "Capture The Flag"}'
```
## Result:
```json
{
    "keys": [
        
        "Solve",
        
        "MDFlag",
        
        "Hash"
    ],
    
    "text": "Solver MDFlag from Cryptohack.org , category: Hash Functions",
    
    "time": "Fri, 01 Jul 2022 00:33:58 GMT",
    
    "title": "Capture The Flag"
}
```

## <p align="center">Search by Keys</p>

**Endpoint:** /searchKeys
**Method:**   Get

To successfully search a note by keys, you need to provide the following JSON data fields:

1. **keys:**  Keywords that are included to the note's text.

If keys field is missing, the system will generate an appropriate error message.

## Search by keys process

1. The web service checks if keys field is provided and not empty.
2. If keys field is provided, the service searches through the Notes collection to determine if the keys exist in the database.
   ```python
	counter = Notes.find({"keys" : data["keys"]}) ```
3. For every json object found with the given keys, a new json object is created with the same fields and inserted in an array.
   ```python
	counter = Notes.find({"keys" : data["keys"]})
            if counter != None:
                answer = []
                for key in counter:
                    key = {"title" : key["title"],"text" : key["text"],"keys" : key["keys"],"time" : key["time"]}
                    answer.append(key)```
4. After every note with the given keys has been inserted, the array is sorted by time of creation.
   ```python
	sorted(answer,key = lambda a:a['time'])```
5. The array is returned as a json object.
  ```python return jsonify(fAnswer), 200```
6. Upon unsuccesful seaech by keys, an error message is returned.
   	```python
	return Response("No such keys in Notes collection",status = 500,mimetype = "application/json")```


### POSTMAN: 
```json
{
  "keys" : "Hash"
}
```
### CURL:
```bash
curl -X GET http://127.0.0.1:5000/searchKeys -H 'Content-Type:application/json' -d '{"keys" : "Hash"}'
```
## Result:
```json
[  {
    "keys": [
        
        "Solve",
        
        "MDFlag",
        
        "Hash"
    ],
    
    "text": "Solver MDFlag from Cryptohack.org , category: Hash Functions",
    
    "time": "Fri, 01 Jul 2022 00:33:58 GMT",
    
    "title": "Capture The Flag"
},
    
    {
       
        "keys": [
            
            "Hash",
            
            "solved"
        ],
        
        "text": "MDFLAG solved -> bruteforce hash length extension, one of my favourite attacks",
        
        "time": "Fri, 01 Jul 2022 02:35:07 GMT",
        
        "title": "CTF Update"
    }
]
```

## <p align="center">Update</p>

**Endpoint:** /update
**Method:**   Post

To successfully create a note, you need to provide the following JSON data fields:

1. **Title:** The current title of your note.
2. **Title2:** The new title of your note.
3. **text:**  The new text that will be included to your note.
4. **keys:**  Keywords that are included to the note's text.

If any of these fields are missing, the system will generate an appropriate error message indicating which field is missing.

## Update process

1. The web service checks if all required fields are provided and not empty.
2. If all fields are provided, the service searches through the Notes collection to determine if the title given exist in the database.
   ```python
	answer = Notes.find_one({"title" : data['title']})```
3. If the Note is found in the database, the current title, text and keys are replaced with the fields that were given.
   ```python
	Notes.update_one({"title":data['title']}, 
                
                {"$set":
               
                {
                    "title":data['title2'], 
                    
                    "text" :data['text'], 
                    
                    "keys" :data['keys']

                }
                
                })
    ```
4. The service then search for the updated version of the note in the Notes collection and returns it as a json object.
	```python
	answer = Notes.find_one({"title" : data['title2']})   
 	answer = {'title':answer['title'], 'text':answer['text'], 'keys':answer['keys'] }
	return  jsonify(answer), 200```
5. Upon unsuccesful Update, an error message is returned.
   	```python
	return Response({'Note could not be updated'},status=500,mimetype='application/json')```

### POSTMAN: 
```json
{
"title": "Capture The Flag",
"title2":"Capture The Flag New CTF",
"text" : "Solve Vote For Pedro, Category : RSA",
"keys" :["Solve","Vote For Pedro","RSA"] 
}
```
### CURL:
```bash
curl -X POST http://127.0.0.1:5000/update -H 'Content-Type:application/json' -d '{"title": "Capture The Flag","title2":"Capture The Flag New CTF","text" : "Solve Vote For Pedro, Category : RSA","keys" :["Solve","Vote For Pedro","RSA"] }'
```
## Result:
```json
{
    "keys": [
        
        "Solve",
        
        "Vote For Pedro",
        
        "RSA"
    ],
    
    "text": "Solve Vote For Pedro, Category : RSA",
    
    "title": "Capture The Flag New CTF"
}
```

## <p align="center">Delete Note</p>

**Endpoint:** /delete
**Method:**   DELETE

To successfully delete a note, you need to provide the following JSON data fields:

1. **Title:** The title of your note.

If Title is missing, the system will generate an appropriate error message.

## Search Note process

1. The web service checks if title is provided and not empty.
2. If title is provided, the service searches through the Notes collection to determine if the title exist in the database.
   ```python
	Notes.find_one({"title":data['title']}) ```
3. If the note with the given title is found in the Notes's collection , the json object is deleted permanently from the Notes collection.
   ```python
	 delete = Notes.delete_one({"title":data['title']})```
4. Upon succes, a confirmation message is returned.
	```python return Response("Title: "+data['title']+" Was found and deleted",status=500,mimetype='application/json')```
5. Upon unsuccesful seaech note, an error message is returned.
   	```python 
	return Response("No such title in Notes",status=500,mimetype='application/json')```
### POSTMAN: 
```json
{
"title": "Capture The Flag"
}
```
### CURL:
```bash
curl -X DELETE http://127.0.0.1:5000/delete -H 'Content-Type:application/json' -d '{"title": "Capture The Flag"}'
```
## Result:
**Title: Capture The Flag Was found and deleted**

## <p align="center">Notes By Date</p>
											

**Endpoint:** /NotesByDate
**Method:**   GET

To successfully retrieve all notes sorted by date, you need to provide the following JSON data fields:
 ```pythonreturn Response("Please enter Anseding or Desending",status = 500,mimetype = "application/json") ```
1. **Choice:** ['Ascending','Descending'] choose on what order should the notes be displayed.

If Choice is missing or has other value, the system will generate an appropriate error message.

## Notes by date process

1. The web service checks if choice is provided and not empty.
2. If choice is provided, the service searches through the Notes collection to recover all notes with the user's id.
   ```python
	notes = Notes.find({}) ```
3. For every note a new json object is created and appended to an array.
   ```python
	for date in notes:
   		date = {"title" : date["title"],"text" : date["text"],"keys" : date["keys"],"time" : date["time"]}
   		array.append(date)```
4. The array is sorted depending of the choice field.
	```fAnswer = sorted(array,key = lambda b:b["time"],reverse=True) <- Descending```
5. Upon success, an array as a json object is returned
   ```python  return jsonify(fAnswer), 200 ```
6. Upon unsuccesful seaech note, an error message is returned.
   	```python 
	return Response("Couldnt find Notes",status = 500,mimetype = "application/json")```

### POSTMAN: 
```json {"choice" : "Ascending"}```
### CURL:
```bash
curl -X GET http://127.0.0.1:5000/NotesByDate -H 'Content-Type:application/json' -d '{"choice" : "Ascending"}'
```
## Result:
```json
[
  {
    "keys": [
      "Solve",
      "Vote For Pedro",
      "RSA"
    ],
    "text": "Solve Vote For Pedro, Category : RSA",
    "time": "Thu, 17 Aug 2023 16:21:02 GMT",
    "title": "Capture The Flag New CTF"
  },
  {
    "keys": [
      "Solve",
      "ctf",
      "crypto"
    ],
    "text": "Solve more crypto ctfs",
    "time": "Fri, 18 Aug 2023 15:33:22 GMT",
    "title": "Improve"
  },
  {
    "keys": [
      "contests",
      "ctf",
      "HTB"
    ],
    "text": "Participate in the HTB contests",
    "time": "Fri, 18 Aug 2023 15:33:22 GMT",
    "title": "ctf contests"
  }
]
```
								
											
## <p align="center">Delete Account</p>
											

**Endpoint:** /deleteAcc
**Method:**   Delete

No json data required.

## Delete Account process

1. Checks if the person is logged in and has user privileges.
2. Delete the user from the User's collection based on his id.
   ```python
	Users.delete_one({'id': id}) ```
3. Deletes all Notes created by the user based on his id.
   ```python
	Notes.delete_many({'id': id})```
4. Sets flag = 0 as if nobody is logged in.
   ```python
	flag = 0 ```
5.  Upon success, a confirmation message is returned.
   ```python return Response('the person and its notes with that mail was removed', status=200,mimetype='application/json') ```

### POSTMAN: 
 Just make a request to the endpoint.
### CURL:
```bash
curl -X DELETE http://127.0.0.1:5000/deleteAcc -H 'Content-Type:application/json'
```
## Result:
**the person and its notes with that mail was removed**

## <p align="center">Insert Admin</p>
											

**Endpoint:** /InsertAdmin
**Method:**   POST

To successfully Insert an admin, you need to provide the following JSON data fields:
 ```pythonreturn Response("Please enter Anseding or Desending",status = 500,mimetype = "application/json") ```
1. **Email:**    The email address of the Admin.
2. **Username:** The desired username for the admin's account.
3. **Password:**     The desired password.

If any of the fields are missing, the system will generate an appropriate error message.

## Insert Admin process

1. The web service checks if the required fields are provided and not empty.
2. If the required fields are provided, the service searches through the Admins collection to determine if any other admin with the given credentials exist in the database.
   ```python
	ad1 = Admins.find_one({"username" : data['username'],"email" : data['email']}) ```
3. If not, a unique id is created and crafted along with the other fields to a JSON object which is then added to the Admins collection.
   ```python
	id = sha256(str(data['email']).encode()+os.urandom(20)).hexdigest()
   	admin = {"username" : data['username'],"email" : data['email'],"password" : data['password'],"id" : id}
   	Admins.insert_one(admin)
   	```
4. Upon succes, a confirmation message is returned.
	```return Response("Admin with name: "+data['name']+" Successfully inserted",status = 200,mimetype='application/json')```
5. Upon failure, an error message is returned.
   	```python 
	return Response("There is already an admin with these credentials",status = 500,mimetype = 'application/json')```
 
Upon registering in the system, an initial default admin account is automatically generated if no other admin accounts exist within the Admins collection. The default admin account comes with the following pre-set credentials:

Username: admin
Password: s3cr3t
Email: ad@gmail.com
ID: [Unique Identifier]

This default admin can be used to create a new admin account.
Then it is advised to delete the default admin.

### POSTMAN: 
```json {"username" : "eid3t1c", "password" : "p4ssw0rd", "email" : "new_admin"}```
### CURL:
```bash
curl -X POST http://127.0.0.1:5000/InsertAdmin -H 'Content-Type:application/json' -d '{"username" : "eid3t1c", "password" : "p4ssw0rd", "email" : "new_admin"}'
```
##RESULT:
**result:Admin with name: eid3t1c Successfully inserted**
 	
## <p align="center">Delete User</p>
											

**Endpoint:** /deleteUser
**Method:**   DELETE

To successfully Delete a User, you need to provide the following JSON data fields:

1. **Username:** The desired username for the admin's account.


If username field is missing, the system will generate an appropriate error message.

## Delete User process

1. The web service checks if the username field is provided and not empty.
2. If provided, the service searches through the Users collection to determine if any user with the given username exist in the database.
   ```python
	delete = Users.find_one({"username" : data['username']}) ```
3. If there is, he is deleted from the Users collection along with his notes deleted with his id.
   ```python
   	if delete != None:
		Users.delete_one({"username" : data['username']})
		Notes.delete_many({'id' : delete['id']})
   	```
4. Upon succes, a confirmation message is returned.
	```return Response("User's account deleted",status = 200,mimetype='application/json')```
5. Upon failure, an error message is returned.
   	```python 
	return Response("There is no such username",status= 500,mimetype='application/json')```

### POSTMAN: 
```json {"username" : "eid3t1c"}```
### CURL:
```bash
curl -X DELETE http://127.0.0.1:5000/deleteUser -H 'Content-Type:application/json' -d '{"username" : "eid3t1c"}'
```
##RESULT:
**User's account deleted**

## <p align="center">Delete Admin</p>
											

**Endpoint:** /deleteAdmin
**Method:**   DELETE

To successfully Delete a User, you need to provide the following JSON data fields:

1. **Username:** The desired username for the admin's account.


If username field is missing, the system will generate an appropriate error message.

## Delete User process

1. The web service checks if the username field is provided and not empty.
2. If provided, the service searches through the Admins collection to determine if any Admin with the given username exist in the database.
   ```python
	delete = Users.find_one({"username" : data['username']}) ```
3. If there is, he is deleted from the Admins collection.
   ```python
   	if delete != None:
            Admins.delete_one({"username" : data['username']})
   	```
4. Upon succes, a confirmation message is returned.
	```return Response("Admin's account deleted",status = 200,mimetype='application/json')```
5. Upon failure, an error message is returned.
   	```python 
	return Response("There is no such username",status= 500,mimetype='application/json')```

### POSTMAN: 
```json {"username" : "admin"}```
### CURL:
```bash
curl -X DELETE http://127.0.0.1:5000/deleteAdmin -H 'Content-Type:application/json' -d '{"username" : "admin"}'
```
##RESULT:
**html Admin's account deleted**

## <p align="center">Get Users</p>
											

**Endpoint:** /getUsers
**Method:**   GET

No json data required.

## Get Users process

1. The web service checks if the person is logged in and has admin priviledges.
2. The service finds all users from the Users collection, create a new JSON object for every single of them and add them to an array.
   ```python
	documents = Users.find({})
        us = []
        for document in documents:
            us_temp = {"username" : document['username'],"email" : document['email'],"password" : document['password']}
            us.append(us_temp) ```
3. Upon success an array in the form of JSON is returned.
   ```python
   	return jsonify(us), 200
   	```
### POSTMAN: 
Just make a request to the endpoint
### CURL:
```bash
curl -X GET http://127.0.0.1:5000/getUsers -H 'Content-Type:application/json'  '
```
##RESULT:
```json
[
  {
    "email": "a",
    "password": "s3cr3t",
    "username": "a"
  },
  {
    "email": "b",
    "password": "s3cr3t",
    "username": "b"
  },
  {
    "email": "d",
    "password": "s3cr3t",
    "username": "d"
  },
  {
    "email": "asss",
    "password": "s3cr3t",
    "username": "asss"
  },
  {
    "email": "assss",
    "password": "s3cr3t",
    "username": "assss"
  },
  {
    "email": "asssss",
    "password": "s3cr3t",
    "username": "asssss"
  }
]
```

## <p align="center">Get Admins</p>
											

**Endpoint:** /getAdmins
**Method:**   GET

No json data required.

## Get Admins process

1. The web service checks if the person is logged in and has admin priviledges.
2. The service finds all users from the Admins collection, create a new JSON object for every single of them and add them to an array.
   ```python
	documents = Admins.find({})
        ad = []
        for document in documents:
            ad_temp = {"username" : document['username'],"email" : document['email'],"password" : document['password']}
            ad.append(ad_temp) ```
3. Upon success an array in the form of JSON is returned.
   ```python
   	return jsonify(ad), 200
   	```
### POSTMAN: 
Just make a request to the endpoint
### CURL:
```bash
curl -X GET http://127.0.0.1:5000/getAdmins -H 'Content-Type:application/json'  '
```
##RESULT:
```json
[
  {
    "email": "a",
    "password": "a",
    "username": "alex"
  },
  {
    "email": "new_admin",
    "password": "p4ssw0rd",
    "username": "eid3t1c"
  },
  {
    "email": "new_adm1n",
    "password": "p4ssw0rd",
    "username": "eid3t1c8"
  }
]

## <p align="center">Sign Out</p>
											

**Endpoint:** /signout
**Method:**   GET

## Change the global variable flag to 0 as if nobody is logged in.

### POSTMAN: 
Just make a request to the endpoint
### CURL:
```bash
curl -X GET http://127.0.0.1:5000/signout -H 'Content-Type:application/json'
```
##RESULT:
**signed out**

```
## Dockerfile Steps
![Screenshot_2](https://github.com/Pallarope/YpoxreotikiErgasia22_E19129_Alexandros_Pallis/assets/102302619/2fd031da-f777-4f1f-bdde-2d9b7d96dd0c)
- **Step 1:** Specify the base OS image as Ubuntu 20.04.
  ```docker
  FROM ubuntu:20.04
  ```
- **Step 2:** Executes apt-get update in case there is an update for our OS.
  ```docker
  RUN apt-get update
- **Step 3:** Executes apt-get install -y python3 python3-pip in order to install pip3 for python3.
  ```docker
  RUN apt-get install -y python3 python3-pip
- **Step 4:** Executes pip3 install flask pymongo for Pymongo to get installed.
  ```docker
  RUN pip3 install flask pymongo
  - **Step 1:** Specify the base OS image as Ubuntu 20.04.
  ```docker
  FROM ubuntu:20.04
  ```
- **Step 5:** Executes pip3 install datetime for datetime to get installed.
  ```docker
  RUN pip3 install datetime
- **Step 6:** Executes mkdir /app that creates a new directory with the name app.
  ```docker
  RUN mkdir /app
- **Step 7:** Create an exact copy of our web-service inside the directory 'app' in our containter.
  ```docker
  COPY app.py /app/app.py
- **Step 8:** Define port 5000 as the port of our container.
  ```docker
  EXPOSE 5000
- **Step 9:** Define app directory as a working directory.
  ```docker
  WORKDIR /app
- **Step 10:** Executes python3 -u app.py which starts the container.
  ```docker
  ENTRYPOINT ["python3","-u","app.py"]

# docker-compose.yml

![Screenshot_1](https://github.com/Pallarope/YpoxreotikiErgasia22_E19129_Alexandros_Pallis/assets/102302619/6bee67ce-7a88-41b6-8e5b-8225454c670c)

- **Step 1:** Specify the version of Docker Compose.
  ```yaml
  version: '2'
- **Step 2:**  Setting Up MongoDB Service
 In this step, we will configure our MongoDB service using a Docker container.
  ```yaml
  services:
   mongodb:
     image: mongo  # This image will be used for the MongoDB container.
     restart: always  # The container will automatically restart in case of errors.
     container_name: mongodb  # The name of our MongoDB container.
     ports:
       - 27017:27017  # Expose port 27017 for MongoDB connections.
     volumes:
       - ./mongodb/data:/data/db  # Store MongoDB data on the host machine.

- **Step 3:**  Setting Up Flask Service

In this section, we'll configure the Flask service using a Docker container.
```yaml
flask-service:
  build:
    context: ./flask-service  # Build the Flask service using the specified context directory.
  restart: always  # Automatically restart the container in case of errors.
  container_name: flask  # Assign a name to the Flask container.
  depends_on:
    - mongodb  # Make sure the Flask service depends on the MongoDB service.
  ports:
    - 5000:5000  # Map port 5000 from the container to the host system.
  environment:
    - "MONGO_HOSTNAME=mongodb"  # Set the MongoDB hostname as an environment variable.
