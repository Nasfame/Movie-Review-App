from flask import Blueprint,request
import json,csv,jwt,time

categories = Blueprint('categories',__name__)

@categories.route('/',methods=['POST'])
def show() :
    with open('data/movie_category.csv', 'r') as f1 :
        f1 = csv.DictReader(f1)
        li = list(f1)
    return json.dumps(li)

@categories.route('/register/<auth_token>', methods=['POST'])
def create(auth_token) :
    if jwt.decode(auth_token, 'hiro')['role']=='' or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    with open('data/movie_category.csv', 'a') as f1 :
        f1 = csv.DictWriter(f1,fieldnames=['id','movie_id','category_id'])
        cnt = json.loads(show())
        values = request.json
        print(values)
        values['id']=len(cnt)+1
        f1.writerow(values)
    return json.dumps("Success")

@categories.route('/id/<auth_token>',methods=['POST'])
def search(auth_token):
    if jwt.decode(auth_token, 'hiro')['role']==''or jwt.decode(auth_token, 'hiro')['time']<time.time() :
        return json.dumps("Authentication error")
    #Time to find category id
    with open('data/categories.csv','r') as f1:
        f1 = list(csv.DictReader(f1))
        print(f1)
        for i in f1:
            if i['category_name']==request.json['category']:
                       return json.dumps({'category_id':i['id']})
        return json.dumps("Unknown Category")

@categories.route('/search/<id>/<auth_token>',methods=['POST'])
def search_cat(id,auth_token):
    if jwt.decode(auth_token, 'hiro')['role'] == '' or jwt.decode(auth_token, 'hiro')['time'] < time.time() :
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    li=[]
    for i in cnt:
        if i['category_id']==id:
            li.append(i)
    if len(li)== 0:
        return json.dumps("Could'nt relate to the existing data")
    else:
        return json.dumps(li)

@categories.route('/modify/<int:id>/<auth_token>', methods=['PATCH'])
def modify(id,auth_token) :
    if jwt.decode(auth_token, 'hiro')['role']!='admin'or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    if id>len(cnt):
        return json.dumps("Couldn't relate to existing data")
    cnt[id - 1] = request.json
    cnt[id-1]['id']=str(id)

    with open('data/movie_category.csv', 'w') as f1 :
        f1 = csv.DictWriter(f1, fieldnames=['id','movie_id','category_id'])
        f1.writeheader()
        f1.writerows(cnt)
    return json.dumps("Modified successfully")

@categories.route('/delete/<int:id>/<auth_token>', methods=['DELETE'])
def delete(id,auth_token):
    if jwt.decode(auth_token, 'hiro')['role'] != 'admin' or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    cnt.pop(id - 1)
    for i in range(len(cnt)) :
        cnt[i]['id'] = str(i + 1)
    with open('data/movie_category.csv', 'w') as f1 :
        f1 = csv.DictWriter(f1, fieldnames=['id','movie_id','category_id'])
        f1.writeheader()
        f1.writerows(cnt)
    return json.dumps("Successfully finished")