import pyrebase
import json
import uuid
from datetime import datetime


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
        posting_time = str(datetime.now())[:19]
        information = {
            "title": title,
            "contents": contents,
            "uid": uid,
            "time": posting_time,
        }
        self.db.child("diary_list").child(diary_id).set(information)
        self.storage.child(diary_id).put(file)

    def edit_post(self, title, contents, pid):
        changed_info = {"title": title, "contents": contents}
        self.db.child("diary_list").child(pid).update(changed_info)

    def edit_post_with_image(self, title, contents, pid, file):
        changed_info = {"title": title, "contents": contents}
        self.db.child("diary_list").child(pid).update(changed_info)
        self.storage.child(pid).put(file)

    def post_list(self):
        post_lists = self.db.child("diary_list").get().val()
        temp = sorted(
            list(post_lists.items()), key=lambda x: x[1]["time"], reverse=True
        )
        post_lists.clear()
        post_lists.update(temp)
        return post_lists

    def post_detail(self, pid):
        post = self.db.child("diary_list").get().val()[pid]
        post_id = pid
        return post, post_id

    def get_image(self, pid):
        image = self.storage.child(pid).get_url(None)
        return image

    def delete_post(self, pid):
        self.db.child("diary_list").child(pid).set({})
