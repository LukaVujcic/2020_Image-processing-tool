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
import os


#im = Image.open("WhatsApp Image 2020-01-04 at 00.39.54.jpeg")
#im.show()

# mkdir -p /mnt/ram
# mount -t ramfs -o size=20m ramfs /mnt/ram
# umount /mnt

image_path=""

class CustomPopup(Popup):

    fc = ObjectProperty(None)

    def close_save_file_popup(self):
        popup.dismiss(force=True)

    def open_image(self):
        image_path=self.fc.selection[0]
        IPC().reload_image()
        self.dismiss()

        os.system("mkdir -p ./tmp")
        os.system("mount -t ramfs -o size=50m ramfs ./tmp")
        os.system("cp " + image_path + " ./tmp/")
                
        c = len(image_path)-1
        while image_path[c]!='/' and c>0:
            c=c-1
        c=c+1
        file_name = image_path[c:]
        
        image_path=image_path [:c]
        image_path=image_path + "tmp/" + file_name

        im = Image.open(image_path)
        #image_reload poziv


    def save_file(self):
        pass

class IPC(FloatLayout):
    selection_tool = ObjectProperty(None)
    resize_tool = ObjectProperty(None)
    crop_tool = ObjectProperty(None)
    laso_tool = ObjectProperty(None)
    save_file_popup = ObjectProperty(None)
    img_id = ObjectProperty(None)
    current_path="./"


    def init(self):
        pass
    
    def reload_image(self):
        self.img_id.source=image_path
        self.img_id.reload() 

    def open_file(self):
        popup = CustomPopup()
        popup.open()

class IPCApp(App):
    
    def build(self):
        return IPC()

if __name__ == '__main__':
    IPCApp().run()