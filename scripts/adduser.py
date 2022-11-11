import hashlib
import sys

NORMAL = u"\u001b[0m"
BOLD = u"\u001b[1m"

def main(username:str, password: str):
   print("Add this line to config.py:")
   hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
   print(BOLD)
   print(f"\"{username}\": \"{hash}\",")
   print(NORMAL)

if __name__ == "__main__":
   if len(sys.argv) != 3:
      print("Usage: python adduser.py <username> <password>")
   else:
      main(sys.argv[1], sys.argv[2])
