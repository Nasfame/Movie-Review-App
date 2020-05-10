from flask import Blueprint,request
import json,csv,jwt,time

movie = Blueprint('movie',__name__)


@movie.route('/',methods=['POST'])
def show() :
    with open('data/movies.csv', 'r') as f1 :
        f1 = csv.DictReader(f1)
        li = list(f1)
    return json.dumps(li)

@movie.route('/register/<auth_token>', methods=['POST'])
def create(auth_token) :
    if jwt.decode(auth_token, 'hiro')['role']=='' or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    with open('data/movies.csv', 'a') as f1 :
        f1 = csv.DictWriter(f1,fieldnames=['id','movie_name','year','duration','user_id'])
        cnt = json.loads(show())
        values = request.json
        print(values)
        values['id']=len(cnt)+1
        f1.writerow(values)
    return json.dumps("Success")

@movie.route('/search/<auth_token>',methods=['POST'])
def search(auth_token) :
    if jwt.decode(auth_token, 'hiro')['role']==''or jwt.decode(auth_token, 'hiro')['time']<time.time() :
        return json.dumps("Authentication error")
    sc = request.json['movie_name']

    cnt = json.loads(show())

    for i in cnt:
        if i['movie_name']==sc:
            flags = "Found in the DB"
            break
        else:
            flags = "Not in the DB"
    return json.dumps(flags)


@movie.route('/modify/<int:id>/<auth_token>', methods=['PATCH'])
def modify(id,auth_token) :
    if jwt.decode(auth_token, 'hiro')['role']!='admin'or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    if id>len(cnt):
        return "movie not in the DB"
    cnt[id - 1] = request.json
    cnt[id-1]['id']=str(id)

    with open('data/movies.csv', 'w') as f1 :
        f1 = csv.DictWriter(f1, fieldnames=['id','movie_name','year','duration','user_id'])
        f1.writeheader()
        f1.writerows(cnt)

    return json.dumps("Modified successfully")

@movie.route('/delete/<int:id>/<auth_token>', methods=['DELETE'])
def delete(id,auth_token):
    if jwt.decode(auth_token, 'hiro')['role'] != 'admin' or jwt.decode(auth_token, 'hiro')['time']<time.time():
        return json.dumps("Authentication error")
    cnt = json.loads(show())
    cnt.pop(id - 1)
    for i in range(len(cnt)) :
        cnt[i]['id'] = str(i + 1)
    with open('data/movies.csv', 'w') as f1 :
        f1 = csv.DictWriter(f1, fieldnames=['id','movie_name','year','duration','user_id'])
        f1.writeheader()
        f1.writerows(cnt)
    return json.dumps("Successfully finished")