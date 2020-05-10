from flask import Flask, request
import csv,json,jwt,time
from blueprint_movie import movie
from blueprint_comment import comment
from blueprint_categories import categories

flag = False
app = Flask(__name__)
app.register_blueprint(movie,url_prefix='/movie')
app.register_blueprint(comment,url_prefix='/comment')
app.register_blueprint(categories,url_prefix='/categories')

@app.route('/users')
def hello_world() :
    return json.dumps('Hello Guys!')

@app.route('/users/details')
def listing() :
    with open('data/users.csv', 'r') as f1 :
        f1 = csv.DictReader(f1)
        li = list(f1)
    return json.dumps(li)

@app.route('/users/register', methods=['POST'])
def create() :
    if flag == False :
        return json.dumps("Authentication error")
    with open('data/users.csv', 'a') as f1 :
        f1 = csv.DictWriter(f1,fieldnames=['id','name','contact_number','address','password','role'])
        cnt = json.loads(listing())
        values = request.json
        print(values)
        values['id']=len(cnt)+1
        values['role']='user'
        f1.writerow(values)
    return json.dumps("Success")

@app.route('/users/login',methods=['POST'])
def login():
    login_data = list(request.json.values())
    db = json.loads(listing())
    values=[]
    role=''
    for i in db:
        values.append([i['name'],i['password']])
        if i['name']== login_data[0]:
            role = i['role']
    payload = {'username':login_data[0],'status':'LO','role':role,'time':time.time()+3600}  # Logged Out

    if login_data in values:
        global flag
        flag=True
        payload['status']='LI'   # Logged In
        encode_jwt = jwt.encode(payload,'hiro')
        return {'auth_token':encode_jwt.decode()}
    else:
        encode_jwt = jwt.encode(payload, 'hiro')
        return {'auth_token':encode_jwt.decode()}

@app.route('/users/modify/<id>/<auth_token>', methods=['PATCH'])
def edit(id,auth_token) :
    decoded = jwt.decode(auth_token,'hiro')
    if flag==False:
        return json.dumps("Service QUiting!")
    if decoded['status']=='LO':
        return json.dumps("Process encountered a rail road spike")
    id = int(id)
    cnt = json.loads(listing())
    if id>len(cnt):
        return json.dumps("User not in the DB")
    cnt[id - 1]['password'] = request.json['password']
    if decoded['username'] == cnt[id-1]['name'] or decoded['role']=='admin':
        with open('data/users.csv', 'w') as f1 :
            f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'contact_number', 'address', 'password','role'])
            f1.writeheader()
            f1.writerows(cnt)
        return json.dumps("Modified password successfully")
    else:
        return json.dumps("Don't Trick me Mister!")

@app.route('/users/delete/<int:id>/<auth_token>', methods=['DELETE'])
def delete(id,auth_token) :
    decoded = jwt.decode(auth_token, 'hiro')
    if decoded['status']=='LI':
        cnt = json.loads(listing())
        cnt.pop(id - 1)
        for i in range(len(cnt)) :
            cnt[i]['id'] = str(i + 1)
        if decoded['username'] == cnt[id - 1]['name'] or decoded['role'] == 'admin' :
            with open('data/users.csv', 'w') as f1 :
                f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'contact_number','address','password','role'])
                f1.writeheader()
                f1.writerows(cnt)
            return json.dumps("Deleted")
    else:
        return json.dumps("Authentication error")


if __name__ == '__main__' :
    app.run(debug=True)
