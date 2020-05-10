from flask import Blueprint,request
import json,csv,jwt,time

comment = Blueprint("comment",__name__)

@comment.route('/',methods=['POST'])
def show() :
    with open('data/comment.csv', 'r') as f1 :
        f1 = csv.DictReader(f1)
        li = list(f1)
    return json.dumps(li)

@comment.route('/register/<auth_token>', methods=['POST'])
def create(auth_token) :
    if jwt.decode(auth_token, 'hiro')['role']=='' or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    with open('data/comment.csv', 'a') as f1 :
        f1 = csv.DictWriter(f1,fieldnames=['id','comment','movie_id','user_id'])
        cnt = json.loads(show())
        values = request.json
        print(values)
        values['id']=len(cnt)+1
        f1.writerow(values)
    return json.dumps("Success")

@comment.route('/movie/<id>/<auth_token>',methods=['POST'])
def search(auth_token,id) :
    if jwt.decode(auth_token, 'hiro')['role']==''or jwt.decode(auth_token, 'hiro')['time']<time.time() :
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    flags = "Not in the DB"
    li=[]
    for i in cnt:
        if i['movie_id']==id:
            li.append(i)
    if len(li)>0:
        return json.dumps(li)

    return json.dumps(flags)
@comment.route('/user/<id>/<auth_token>',methods=['POST'])
def search_user(auth_token,id) :
    if jwt.decode(auth_token, 'hiro')['role']==''or jwt.decode(auth_token, 'hiro')['time']<time.time() :
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    flags = "Not in the DB"
    li=[]
    for i in cnt:
        if i['user_id']==id:
            li.append(i)
    if len(li)>0:
        return json.dumps(li)

    return json.dumps(flags)

@comment.route('/modify/<int:id>/<auth_token>', methods=['PATCH'])
def modify(id,auth_token) :
    if jwt.decode(auth_token, 'hiro')['role']!='admin'or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    if id>len(cnt):
        return json.dumps("Comment not in the DB")
    cnt[id - 1] = request.json
    cnt[id-1]['id']=str(id)

    with open('data/comment.csv', 'w') as f1 :
        f1 = csv.DictWriter(f1, fieldnames=['id','comment','movie_id','user_id'])
        f1.writeheader()
        f1.writerows(cnt)
    return json.dumps("Modified successfully")

@comment.route('/delete/<int:id>/<auth_token>', methods=['DELETE'])
def delete(id,auth_token):
    if jwt.decode(auth_token, 'hiro')['role'] != 'admin' or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    cnt.pop(id - 1)
    for i in range(len(cnt)) :
        cnt[i]['id'] = str(i + 1)
    with open('data/comment.csv', 'w') as f1 :
        f1 = csv.DictWriter(f1, fieldnames=['id','comment','movie_id','user_id'])
        f1.writeheader()
        f1.writerows(cnt)
    return json.dumps("Successfully finished")