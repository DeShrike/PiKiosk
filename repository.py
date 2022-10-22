import logging
import json
from os.path import exists
from config import *

logger = logging.getLogger(__name__)

class Item():
   def __init__(self, url: str, kind: str, duration: int, fullscreen: bool, background_color: str):
      self.url = url
      self.kind = kind
      self.duration = duration
      self.background_color = background_color
      self.fullscreen = fullscreen

class Repository():
   def __init__(self, filename: str):
      self.items = []
      self.filename = filename
      self.load()

   def add(self, url: str, kind: str, duration: int, fullscreen: bool, background_color: str):
      item = Item(url, kind, duration, fullscreen, background_color)
      self.items.append(item)

   def save(self):
      d = [ i.__dict__ for i in self.items ]
      with open(self.filename, "w") as fo:
         fo.write(json.dumps(d))

   def load(self):
      self.items = []
      if exists(self.filename) == False:
         return
      with open(self.filename, "r") as fi:
         d = fi.read()
         j = json.loads(d)
         for i in j:
            item = Item(**i)
            self.items.append(item)

def main():
   repo = Repository(REPOSITORY_FILE)
   print(len(repo.items))
   repo.add("testimg.jpg", "image", 60, True, "#123456")
   repo.add("https://www.google.com", "url", 60, False, None)
   repo.add("cat.jpeg", "image", 60, False, "#005500")
   repo.add("testimg.jpg", "image", 60, False, "#654321")
   repo.add("tired_cat.jpg", "image", 60, True, "#000021")
   repo.save()

if __name__ == "__main__":
   main()

