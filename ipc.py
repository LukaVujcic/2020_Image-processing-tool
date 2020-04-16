from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image as Im
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ObjectProperty
from PIL import Image


#im = Image.open("WhatsApp Image 2020-01-04 at 00.39.54.jpeg")
#im.show()

class IPC(FloatLayout):
    selection_tool = ObjectProperty(None)
    resize_tool = ObjectProperty(None)
    crop_tool = ObjectProperty(None)
    laso_tool = ObjectProperty(None)
    save_file_popup = ObjectProperty(None)
    lab = ObjectProperty(None)

    def close_save_file_popup(self):
        #TODO
        #self.save_file_popup.dismiss(force=True)
        #tmp solution
        self.save_file_popup.size_hint=0,0
        self.save_file_popup.pos_hint={"x":1,"y":1}
        print("Cao")


class IPCApp(App):
    def build(self):
        return IPC()

if __name__ == '__main__':
    IPCApp().run()