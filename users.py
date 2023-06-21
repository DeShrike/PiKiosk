import logging
import json
from os.path import exists
import config

logger = logging.getLogger(__name__)

class User():
   def __init__(self, username: str, hash: str, logoncount: int, lastlogon: str):
      self.username = username
      self.hash = hash
      self.logoncount = logoncount
      self.lastlogon = lastlogon

   def __repr__(self) -> str:
      return f"User('{self.username}', '{self.hash}', {self.logoncount}, '{self.lastlogon}')"

class Users():
   def __init__(self, filename: str):
      self.users = []
      self.filename = filename
      self.load()
      if len(self.users) == 0:
         # Add a default user.
         self.add("admin", "admin")

   def add(self, username: str, hash: str):
      user = User(username, hash, 0, None)
      self.users.append(user)

   # def delete_by_index(self, index:int) -> None:
   #    if index < 0 or index >= self.item_count:
   #       return

   #    self.items.remove(self.items[index])
   #    self.save()

   def save(self):
      d = [ i.__dict__ for i in self.users ]
      with open(self.filename, "w") as fo:
         fo.write(json.dumps(d))

   def load(self):
      self.users = []
      if exists(self.filename) == False:
         return
      with open(self.filename, "r") as fi:
         d = fi.read()
         jsn = json.loads(d)
         for jsnitem in jsn:
            user = User(**jsnitem)
            self.users.append(user)

def main():
   users = Users(config.USERS_FILE)
   print(len(users.users))
   print(users.users)
   users.save()

if __name__ == "__main__":
   main()

