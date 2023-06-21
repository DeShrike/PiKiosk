class ViewModel():
    def __init__(self):
        self.title = "Pi Kiosk"
        self.image_name = None
        self.background_color = "#123456"
        self.intro = "Intro tekst"
        self.items = None
        self.users = None
        self.item_count = 0
        self.available_images = None
        self.available_htmls = None
        self.status = None
        self.authenticated = False
        self.username = ""
        self.message = None

    def __repr__(self):
        s = f"Title: {self.title}\n"
        s += f"Item Count: {self.item_count}\n"
        s += f"Status: {self.status}\n"
        s += f"Authenticated: {self.authenticated}\n"
        s += f"User: {self.username}\n"
        return s
