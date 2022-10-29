import logging
import json
from os.path import exists
import config
from werkzeug.urls import url_quote

logger = logging.getLogger(__name__)

class Item():
   def __init__(self, url: str, kind: str, duration: int, fullscreen: bool, background_color: str):
      self.url = url
      self.kind = kind
      self.duration = duration
      self.background_color = background_color
      self.fullscreen = fullscreen
   
   def build_relative_url(self) -> str:
      if self.kind == "url":
         return self.url        
      elif self.kind == "html":
         fullurl = "/htmlfile/"
         url = url_quote(self.url) 
         fullurl += f"{url}"
         return fullurl        
      elif self.kind == "image":
         fullurl = "/image_fullscreen/" if self.fullscreen else "/image_centered/"
         url = url_quote(self.url) 
         bg = url_quote(self.background_color)
         fullurl += f"{url}/{bg}"
         return fullurl        
      else:
         return None

   def build_url(self) -> str:
      if self.kind == "url":
         return self.url        
      elif self.kind == "image":
         return f"http://127.0.0.1:{config.PORT}{self.build_relative_url()}"
      elif self.kind == "html":
         return f"http://127.0.0.1:{config.PORT}{self.build_relative_url()}"
      else:
         return None

class Repository():
   def __init__(self, filename: str):
      self.items = []
      self.filename = filename
      self.load()
      if self.item_count() == 0:
         # Add a few dummy items.
         self.add("splash.html", "html", 60, False, None)
         self.add("RSLopPost.jpg", "image", 60, False, "#001BFE")
         self.add("CoderDojo.png", "image", 60, False, "#FFFFFF")
         self.add("https://www.raspberrypi.org/", "url", 60, False, "#000000")
         self.add("https://roeselare.coderdojobelgium.be/", "url", 60, False, "#000000")

   def add(self, url: str, kind: str, duration: int, fullscreen: bool, background_color: str):
      item = Item(url, kind, duration, fullscreen, background_color)
      self.items.append(item)

   def moveup_by_index(self, index:int) -> None:
      if index < 0 or index >= self.item_count():
         return

      self.items.insert(index - 1, self.items.pop(index))
      # !!!!!!!! self.save()

   def movedown_by_index(self, index:int) -> None:
      if index < 0 or index >= self.item_count():
         return
      self.items.insert(index + 1, self.items.pop(index))
      # !!!!!!!! self.save()

   def delete_by_index(self, index:int) -> None:
      if index < 0 or index >= self.item_count():
         return
      
      self.items.remove(self.items[index])
      # !!!!!!!! self.save()

   def save(self):
      d = [ i.__dict__ for i in self.items ]
      with open(self.filename, "w") as fo:
         fo.write(json.dumps(d))

   def item_count(self) -> int:
      return len(self.items)

   def load(self):
      self.items = []
      if exists(self.filename) == False:
         return
      with open(self.filename, "r") as fi:
         d = fi.read()
         jsn = json.loads(d)
         for jsnitem in jsn:
            item = Item(**jsnitem)
            self.items.append(item)

def main():
   repo = Repository(config.REPOSITORY_FILE)
   print(len(repo.items))
   repo.add("splash.html", "html", 60, False, None)
   repo.add("cat2.jpg", "image", 60, True, "#123456")
   repo.add("https://www.google.com", "url", 60, False, None)
   repo.add("cat1.jpg", "image", 60, False, "#005500")
   repo.add("cat2.jpg", "image", 60, False, "#654321")
   repo.add("cat3.jpg", "image", 60, True, "#000021")
   repo.save()

if __name__ == "__main__":
   main()

