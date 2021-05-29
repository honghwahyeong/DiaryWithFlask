import pyrebase
import json
import uuid


class DBModule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.storage = firebase.storage()

    def login(self, uid, pwd):
        users = self.db.child("users").get().val()
        try:
            userinfo = users[uid]
            if userinfo["pwd"] == pwd:
                return True
            else:
                return False
        except:
            return False

    def signin_verification(self, uid):
        users = self.db.child("users").get().val()
        for i in users:
            if uid == i:
                return False
        return True

    def signin(self, _id_, pwd, name, email):
        information = {"pwd": pwd, "uname": name, "email": email}
        if self.signin_verification(_id_):
            self.db.child("users").child(_id_).set(information)
            return True
        else:
            return False

    def write_post(self, title, contents, uid, file):
        diary_id = str(uuid.uuid4())[:12]
        information = {"title": title, "contents": contents, "uid": uid}
        self.db.child("diary_list").child(diary_id).set(information)
        self.storage.child(diary_id).put(file)

    def post_list(self):
        post_lists = self.db.child("diary_list").get().val()
        print(post_lists)
        return post_lists

    def post_detail(self, pid):
        post = self.db.child("diary_list").get().val()[pid]
        return post

    def get_uset(self, uid):
        pass
