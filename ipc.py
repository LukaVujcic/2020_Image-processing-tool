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
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from PIL import Image, ImageFilter ,ImageFont, ImageDraw
import imageOperations as io
import os
import atexit


image_path="./assets/white.jpeg"
im = Image.open("./assets/white.jpeg")
old = None
input=""

def exit_handler():
    global im
    if im is not None:
        im.close()
        print("Image Closed!")
    os.system("sudo umount tmp")
    os.system("sudo rm -r tmp")

class CustomPopup(Popup):

    fc = ObjectProperty(None)
    txt_input = ObjectProperty(None)

    def update_text_input(self):
        for i in self.fc.selection:
            self.txt_input.text=i

    def close_save_file_popup(self):
        popup.dismiss()

    def open_image(self):

        global image_path
        global im

        for i in self.fc.selection:
            image_path=i

        if os.system("cd tmp")!=0:
            os.system("sudo mkdir -p ./tmp")
            os.system("sudo mount -t ramfs -o size=50m ramfs ./tmp")
        os.system("sudo cp " + image_path + " ./tmp/")
                
        c = len(image_path)-1
        while image_path[c]!='/' and c>0:
            c=c-1
        c=c+1
        file_name = image_path[c:]
        
        image_path=image_path [:c]
        image_path=image_path + "tmp/" + file_name

        im = Image.open(image_path)
        #IPC().reload_image() ne radi iz nekog razloga mora da se pozove iz IPC klase
        self.dismiss()


    def save_file(self):

        self.dismiss()

        if self.txt_input!="":
            url=self.txt_input.text
            ext=self.txt_input.text[self.txt_input.text.index('.')+1:]
        try:
            ext=ext.upper()
            if ext=='BMP' or ext=='JPEG' or ext=='PNG':
                image=im.convert('RGB')
                image.save(url,ext)
                pass
        except ValueError:
            print('ValueError')
        except IOError:
            print('IOError')

class IPC(FloatLayout):
    selection_tool = ObjectProperty(None)
    resize_tool = ObjectProperty(None)
    crop_tool = ObjectProperty(None)
    laso_tool = ObjectProperty(None)
    save_file_popup = ObjectProperty(None)
    text_tool = ObjectProperty(None)
    contour_tool = ObjectProperty(None)
    find_edges_tool = ObjectProperty(None)
    sharpen_tool = ObjectProperty(None)
    smooth_tool = ObjectProperty(None)
    blur_tool = ObjectProperty(None)
    unsharp_tool = ObjectProperty(None)
    mode_filter_tool = ObjectProperty(None)
    min_filter_tool = ObjectProperty(None)
    cp = ObjectProperty(None)
    lbl1 = ObjectProperty(None)
    lbl2 = ObjectProperty(None)
    lbl3 = ObjectProperty(None)
    slider1 = ObjectProperty(None)
    slider2 = ObjectProperty(None)
    slider3 = ObjectProperty(None)
    img_id = ObjectProperty(None)
    current_path="./"
    area_start = [0,0]
    area_end = [0,0]
    image_begin = [0.3,0.15]
    image_end = [1,0.8]
    active_tool = None
    calibration_tool = 1

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if len(modifiers)>0 and modifiers[0] == 'ctrl' and keycode[1] == 'z':
            self.undo()
        
        #if keycode[1]=='enter':

        #global input
        #input = input + keycode[1]
        #print(keycode[1])

    
    def init(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
    
    def P(self):
        return abs(self.area_start[0]-self.area_end[0]) * abs(self.area_start[1]-self.area_end[1])

    def make_backup(self):
        global old
        old=im.copy()

    def undo(self,*args):
        #if args[0]==122 and args[3]==['ctrl']:
        global old
        global im
        im=old
        self.save_temp_image()
        
    #Window.bind(on_key_down=key_action)

    def adjust_selection(self):
        global im
        if self.area_start[0]<0:
            self.area_start[0]=0
        if self.area_start[1]<0:
            self.area_start[1]=0
        if self.area_end[0]>im.width:
            self.area_end[0]=im.width
        if self.area_end[1]>im.height:
            self.area_end[1]=im.height

    def update_labels(self):
        self.lbl1.text = self.lbl1.text[:self.lbl1.text.index(" ")] + " " + str(int(self.slider1.value))
        self.lbl2.text = self.lbl2.text[:self.lbl2.text.index(" ")] + " " + str(int(self.slider2.value))
        self.lbl3.text = self.lbl3.text[:self.lbl3.text.index(" ")] + " " + str(int(self.slider3.value))

    def on_touch_down(self,touch):
        global im
        if (self.active_tool == self.selection_tool) and (touch.osx>0.3 and touch.osy<0.95):
            self.area_start = [1-(touch.osx-self.image_begin[0])*(1/(self.image_begin[0]-self.image_end[0]))*im.width,-((touch.osy-self.image_end[1])*(1/(self.image_end[1]-self.image_begin[1]))*im.height)]
            #print(self.area_start[0]/im.width,self.area_start[1]/im.height)
            self.adjust_selection()
            print(self.area_start)
        if (self.active_tool == self.calibration_tool) and (touch.osx>0.25 and touch.osy<0.95):
            self.image_begin[0],self.image_begin[1] = touch.osx,touch.osy
            print(self.image_begin)
        if self.disabled and self.collide_point(*touch.pos):
            return True
        for child in self.children[:]:
            if child.dispatch('on_touch_down', touch):
                return True

    def on_touch_up(self,touch):
        global im
        if (self.active_tool == self.selection_tool) and (touch.osx>0.3 and touch.osy<0.95):
            self.area_end = [-(1-(touch.sx-self.image_begin[0])*(1/(self.image_end[0]-self.image_begin[0]))*im.width),-((touch.sy-self.image_end[1])*(1/(self.image_end[1]-self.image_begin[1]))*im.height)]
            #print(self.area_start[0]/im.width,self.area_start[1]/im.height)
            self.adjust_selection()
            print(self.area_end)
            if self.P() < 50:
                self.area_end[0],self.area_end[1],self.area_start[0],self.area_start[1] = 0,0,0,0
        if (self.active_tool == self.calibration_tool) and (touch.osx>0.25 and touch.osy<0.95):
            self.image_end[0],self.image_end[1] = touch.sx,touch.sy
            print(self.image_end)
        if self.disabled:
            return
        for child in self.children[:]:
            if child.dispatch('on_touch_up', touch):
                return True
        
    def reload_image(self):
        global image_path
        self.img_id.source=image_path
        self.img_id.reload()

    def open_file(self):
        popup = CustomPopup()
        popup.open()
        self.init()

    def save_temp_image(self):
        global image_path
        url=image_path
        ext=image_path[image_path.index('.')+1:]
        try:
            ext=ext.upper()
            if ext=='BMP' or ext=='JPEG' or ext=='PNG':
                image=im.convert('RGB')
                image.save(url,ext)
                self.reload_image()
                pass
        except ValueError:
            print('ValueError')
        except IOError:
            print('IOError')

    def activate_selection_tool(self):
        self.active_tool=self.selection_tool
    
    def activate_calibration_tool(self):
        self.active_tool=self.calibration_tool

    def greyscale_image(self):
        global im
        self.make_backup()
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        print(self.area_start)
        print(self.area_end)
        if self.P() < 50:
             im=io.applyOperationOnRegion(io.imageGrayScale,im,(0,0,im.width,im.height))
        else:
            im=io.applyOperationOnRegion(io.imageGrayScale,im,(int(self.area_start[0]),int(self.area_start[1]),int(self.area_end[0]),int(self.area_end[1])))
        self.save_temp_image()
    
    def filter_image_countour(self):
        global im
        self.make_backup()
        im=im.filter(ImageFilter.CONTOUR)
        self.save_temp_image()
    
    def filter_image_find_edges(self):
        global im
        self.make_backup()
        im=im.filter(ImageFilter.FIND_EDGES)
        self.save_temp_image()

    def filter_image_sharpen(self):
        global im
        self.make_backup()
        im=im.filter(ImageFilter.SHARPEN)
        self.save_temp_image()

    def filter_image_smooth(self):
        global im
        self.make_backup()
        im=im.filter(ImageFilter.SMOOTH)
        self.save_temp_image()
    
    def filter_image_blur(self):
        global im
        self.make_backup()
        self.lbl1.text="Strength: "
        self.slider1.min=1
        self.slider1.max=20
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        if self.P() < 50:
             im=io.applyOperationOnRegion(io.imageBlur,im,(0,0,im.width,im.height),int(self.slider1.value))
        else:
            im=io.applyOperationOnRegion(io.imageBlur,im,(int(self.area_start[0]),int(self.area_start[1]),int(self.area_end[0]),int(self.area_end[1])),int(self.slider1.value))
        self.save_temp_image()

    def filter_image_unsharp(self):
        global im
        self.make_backup()
        self.lbl1.text="Radius: "
        self.lbl2.text="Percent: "
        self.lbl3.text="Threshold: "
        self.slider1.min = 1
        self.slider1.max = 30
        self.slider2.min = 0
        self.slider2.max = 500
        self.slider3.min = 0
        self.slider3.max = 15
        im=im.filter(ImageFilter.UnsharpMask(int(self.slider1.value),int(self.slider2.value),int(self.slider3.value)))
        self.save_temp_image()

    def filter_image_mode(self):
        global im
        self.make_backup()
        self.slider1.min=1
        self.slider1.max=20
        self.lbl1.text="Strength: "
        im=im.filter(ImageFilter.ModeFilter(int(self.slider1.value)))
        self.save_temp_image()

    def filter_image_min(self):
        global im
        self.make_backup()
        self.slider1.min=1
        self.slider1.max=20
        self.lbl1.text="Strength: "
        x = int(self.slider1.value)
        if x % 2 == 0:
            x = x+1
        im=im.filter(ImageFilter.MinFilter(x))
        self.save_temp_image()

    def draw_text(self):
        global im
        self.make_backup()
        self.lbl1.text="Size: "
        self.slider1.max = 172
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("./assets/freefont/FreeMono.ttf", int(self.slider1.value))
        s=input()
        draw.text((self.area_start[0], self.area_start[1]), s,fill=(int(self.cp.color[0]),int(self.cp.color[1]),int(self.cp.color[2])), font=font)
        self.save_temp_image()

class IPCApp(App):
    
    def build(self):
        return IPC()

if __name__ == '__main__':
    Window.size = (1280, 720)
    atexit.register(exit_handler)
    IPCApp().run()