from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image as Im
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Ellipse, Line
from PIL import Image


#im = Image.open("WhatsApp Image 2020-01-04 at 00.39.54.jpeg")
#im.show()

class IPC(FloatLayout):
    selection_tool = ObjectProperty(None)
    resize_tool = ObjectProperty(None)
    crop_tool = ObjectProperty(None)
    laso_tool = ObjectProperty(None)

    def open_file(self):
        image_path='1.jpeg'


class IPCApp(App):
    def build(self):
        return IPC()

if __name__ == '__main__':
    IPCApp().run()