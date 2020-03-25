from kivy.app import App
from kivy.uix.widget import Widget
from PIL import Image


im = Image.open("WhatsApp Image 2020-01-04 at 00.39.54.jpeg")
im.show()

class PongGame(Widget):
    pass


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()