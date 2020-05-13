from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from PIL import Image, ImageFilter ,ImageFont, ImageDraw
import imageOperations as io
import subprocess,os,threading,math
import atexit

image_path="./assets/white.jpeg"
im = Image.open("./assets/white.jpeg")
root_path = os.getcwd() + "/"
old = []
wtp = ""

def make_backup():
    global old
    old.append(im.copy())
    if len(old)>10:
        old.pop(0)

def exit_handler():
    global im
    if im is not None:
        im.close()
        print("Image Closed!")
    subprocess.call(["sudo","umount",root_path + "tmp"])
    subprocess.call(["sudo","rm","-r",root_path + "tmp"])

class TutorialPopup(Popup):
    
    ck_box = ObjectProperty(None)
    lbl1 = ObjectProperty(None)
    lbl2 = ObjectProperty(None)
    icons_img = ObjectProperty(None)
    no_tip = 0
    max_tips = 7

    def close_popup(self):
        if self.ck_box.active:
            try:
                with open("config.txt","w") as f:
                    f.write("0")
                    f.close()
            except IOError:
                print("Warning:Greska pri upisu u config fajl!")
        else:
            try:
                with open("config.txt","w") as f:
                    f.write("1")
            except IOError:
                print("Warning:Greska pri unosu u config fajl!")
        self.dismiss()

    def show_next_tip(self):

        self.no_tip = self.no_tip + 1
        if self.no_tip == self.max_tips:
            self.no_tip -= 1
            return

        if self.no_tip == 0:
            self.icons_img.size_hint = 0,0
            self.lbl1.text = "Here are some things you should know..."

        if self.no_tip == 1:
            self.lbl1.text = ("Use ctrl+c and ctrl+v to copy paste image region and ctrl+z to undo.\n"
                            "Every time you open an image click Reload button so you can see it.\n"
                            "You can save image as png,jpeg or bmp and in any size just by typing it in\nSave file popup.\n")
        if self.no_tip == 2:
            self.lbl1.text = ""
            self.icons_img.pos_hint = {"y":0.15,"x":0.15}
            self.icons_img.size_hint = 0.7,0.7
            self.icons_img.source = "./assets/Tutorial.png"

        if self.no_tip == 3:
            self.icons_img.size_hint = 0,0
            self.lbl1.text = ("0 - Area Selection\n"
                            "1 - Calibration Tool - Must use if image is not 16:9 ration,Use Mouse Click on lower left\nside of the picture and release on upper rigth to Calibrate area selection tool\n"
                            "2 - Adjust Contrast\n"
                            "3 - Text Tool - Select the Area before using. After clicking type your text\ndon't worry if it doesn't show up immediately, pressing enter will print it!\n"
                            "4 - Adjust Color Warmness\n"
                            "5 - Brightness Level\n"
                            "6 - Pixelating Image\n"
                            "7 - Making mini duplicates of the first image put together in a matrix\n")
        if self.no_tip == 4:
            self.lbl2.text = "Welcome to our project!"
            self.lbl1.text = ("8 - Finds Image Contours\n"
                            "9 - Finds Image Edges\n"
                            "10 - Sharpens the Image\n"
                            "11 - UNSharpens the Image!\n"
                            "12 - Blurns the Image\n"
                            "13 - Color Grading - WARNING: Will take a LOT time to finish!\n"
                            "14 - Creates a min filter. Picks the lowest pixel value in a window with the given size\n"
                            "15 - Creates a mode filter. Picks the most frequent pixel value in a box with\nthe given size\n")
        if self.no_tip == 5:
            self.lbl2.text = "Sliders use and Slider Range:"
            self.lbl1.text = ("Don't worry about exact range, you won't crash the program\n"
                            "....Probably\n"
                            "Area Selection: None\n"
                            "Calibration Tool: None\n"
                            "Contrast: First 0 - 30, 10 - Unchanged\n"
                            "Text Tool: First 0 - 172\n"
                            "Color Warmness: First 0-30, 10 - Unchanged\n"
                            "Brightness: First 0 - 20, 10 - Unchanged\n"
                            "Pixelate: First: 1 - 500\n"
                            "Image Matrix: First Second - N x M\n")
        if self.no_tip == 6:
            self.lbl1.text = ("Contours: None\n"
                            "Edges: None\n"
                            "Sharpen: None\n"
                            "Unsharpen: Radius Percent Threshold 1-30 0-500 0-15\n"
                            "Blur: First 0-20\n"
                            "Color Grading: First 0-20\n"
                            "Min: First 0-20\n"
                            "Mode: First 0-20\n")

    def show_previous_tip(self):

        if self.no_tip == 0:
            return

        self.no_tip = self.no_tip - 2
        self.show_next_tip()

class CustomPopup(Popup):

    fc = ObjectProperty(None)
    txt_input = ObjectProperty(None)
    img_w = ObjectProperty(None)
    img_h = ObjectProperty(None)

    def update_text_input(self):
        for i in self.fc.selection:
            self.txt_input.text=i

    def open_image(self):

        global image_path
        global im

        for i in self.fc.selection:
            image_path=i

        if os.system("cd " +root_path+"tmp")!=0:
            subprocess.call(["sudo","mkdir","-p",root_path+"tmp"])
            subprocess.call(["sudo","mount","-t","ramfs","-o","size=50m","ramfs",root_path+"tmp"])
        subprocess.call(["sudo","cp",image_path,root_path+"tmp/"])

        c = len(image_path)-1
        while image_path[c]!='/' and c>0:
            c=c-1
        c=c+1
        file_name = image_path[c:]
        
        image_path=root_path
        image_path=image_path + "tmp/" + file_name
        im = Image.open(image_path)
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
                image=im.resize((int(self.img_w.text),int(self.img_h.text)))
                image.save(url,ext)
        except ValueError:
            print('ValueError')
        except IOError:
            print('IOError')

class IPC(FloatLayout):
    selection_tool = ObjectProperty(None)
    calibration_tool = ObjectProperty(None)
    crop_tool = ObjectProperty(None)
    save_file_popup = ObjectProperty(None)
    text_tool = ObjectProperty(None)
    greyscale_tool = ObjectProperty(None)
    pixelate_tool = ObjectProperty(None)
    brightness_tool = ObjectProperty(None)
    grid_tool = ObjectProperty(None)
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
    tmp_box = (0,0,0,0)
    image_begin = [0.3,0.15]
    image_end = [1,0.8]
    active_tool = None
    show_tutorial = 1
    shift_pressed = False
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if len(modifiers)>0 and modifiers[0] == 'ctrl':
            if keycode[1] == 'z':
                self.undo()
            if keycode[1] == 'c':
                self.copy()
            if keycode[1] == 'v':
                self.paste()

        if keycode[1]=='enter':
            self.draw_text()
        if len(keycode[1])==1 or keycode[1]=='spacebar':
            global wtp
            if keycode[1]!='shift':
                if self.shift_pressed == True:
                    wtp = wtp + text.upper()
                    print(text.upper())
                else:
                    wtp = wtp + text
        if keycode[1]=='shift':
            self.shift_pressed = True
        if keycode[1]=='backspace':
            wtp = wtp[:len(wtp)-1]
        
    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1]=='shift':
            self.shift_pressed = False

    def __init__(self,**kwargs):
        """Makes Program Puck up Input."""
        super(IPC, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        try:
            with open("config.txt","r") as f:
                self.show_tutorial = f.readline()
                f.close()
        except IOError:
            print("WARNING: Greska pri citanju config fajla.")
            self.show_tutorial = 1

        if self.show_tutorial[0] == "1":
            def g():
                popup = TutorialPopup()
                popup.open()
            tutorial = threading.Timer(1.5,g)
            tutorial.start()
    
    def P(self):
        return abs(self.area_start[0]-self.area_end[0]) * abs(self.area_start[1]-self.area_end[1])

    def clear_wtp(self):
        global wtp
        wtp = ""

    def undo(self,*args):
        global old
        global im
        if len(old)>=1:
            im=old[-1]
            old.pop(-1)
            self.save_temp_image()
        
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
            #print(self.area_start)
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
            #print(self.area_end)
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
        width,height = im.size
        popup.img_w.text,popup.img_h.text = str(width),str(height)
        popup.open()

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
        except ValueError:
            print('ValueError')
        except IOError:
            print('IOError')

    def open_help(self):
        popup = TutorialPopup()
        popup.open()

    def activate_selection_tool(self):
        self.active_tool=self.selection_tool
    
    def activate_calibration_tool(self):
        self.active_tool=self.calibration_tool

    def greyscale_image(self):
        global im
        make_backup()
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
        make_backup()
        im=im.filter(ImageFilter.CONTOUR)
        self.save_temp_image()
    
    def filter_image_find_edges(self):
        global im
        make_backup()
        im=im.filter(ImageFilter.FIND_EDGES)
        self.save_temp_image()

    def filter_image_sharpen(self):
        global im
        make_backup()
        im=im.filter(ImageFilter.SHARPEN)
        self.save_temp_image()

    def filter_image_smooth(self):
        global im
        make_backup()
        im=im.filter(ImageFilter.SMOOTH)
        self.save_temp_image()

    def filter_image_blur(self):
        global im
        make_backup()
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
        make_backup()
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
        make_backup()
        self.slider1.min=1
        self.slider1.max=20
        self.lbl1.text="Strength: "
        im=im.filter(ImageFilter.ModeFilter(int(self.slider1.value)))
        self.save_temp_image()

    def filter_image_min(self):
        global im
        make_backup()
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
        make_backup()
        self.lbl1.text="Size: "
        self.slider1.max = 172
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("./assets/freefont/FreeMono.ttf", int(self.slider1.value))
        global wtp
        draw.text((self.area_start[0], self.area_start[1]), wtp,fill=(int(self.cp.color[0]*255),int(self.cp.color[1]*255),int(self.cp.color[2])*255), font=font)
        self.save_temp_image()

    def copy(self):
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        self.tmp_box = (int(self.area_start[0]),int(self.area_start[1]),int(self.area_end[0]),int(self.area_end[1]))
        print(self.tmp_box)

    def paste(self):
        global im
        make_backup()
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        im=io.copyOneRegionToAnother(im,self.tmp_box,(int(self.area_start[0]),int(self.area_start[1])))
        self.save_temp_image()

    def set_image_brightness(self):
        global im
        make_backup()
        self.lbl1.text="Strength: "
        self.slider1.min=0
        self.slider1.max=20
        x = self.slider1.value
        if x<=10:
            param = x/100
        else :
            param = x-9
        print(param)
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        if self.P() < 50:
            im=io.applyOperationOnRegion(io.imageBrightness,im,(0,0,im.width,im.height),int(self.slider1.value),param)
        else:
            im=io.applyOperationOnRegion(io.imageBrightness,im,(int(self.area_start[0]),int(self.area_start[1]),int(self.area_end[0]),int(self.area_end[1])),int(self.slider1.value),param)
        self.save_temp_image()

    def pixelate_image(self):
        global im
        make_backup()
        self.lbl1.text="Strength: "
        self.slider1.min=1
        self.slider1.max=500
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        if self.P() < 50:
            im=io.applyOperationOnRegion(io.imagePixelate,im,(0,0,im.width,im.height),int(self.slider1.value))
        else:
            im=io.applyOperationOnRegion(io.imagePixelate,im,(int(self.area_start[0]),int(self.area_start[1]),int(self.area_end[0]),int(self.area_end[1])),int(self.slider1.value))
        self.save_temp_image()

    def make_grid(self):
        global im
        make_backup()
        self.slider1.text="N: "
        self.slider2.text="M: "
        self.slider1.max = 20
        self.slider2.max = 20
        width,height=im.size
        im=io.generateGridFromImage(im,math.floor(self.slider1.value),math.floor(self.slider2.value),width,height)
        self.save_temp_image()

    def set_color_warmness(self):
        global im
        make_backup()
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        self.slider1.max = 30
        self.slider1.text="Strength: "
        param = self.slider1.value/10
        if self.P() < 50:
             im=io.applyOperationOnRegion(io.imageColor,im,(0,0,im.width,im.height),param)
        else:
            im=io.applyOperationOnRegion(io.imageColor,im,(int(self.area_start[0]),int(self.area_start[1]),int(self.area_end[0]),int(self.area_end[1])),param)
        self.save_temp_image()

    def set_image_contrast(self):
        global im
        make_backup()
        self.area_start[0],self.area_end[0] = min (self.area_start[0],self.area_end[0]), max(self.area_start[0],self.area_end[0])
        self.area_start[1],self.area_end[1] = min (self.area_start[1],self.area_end[1]), max(self.area_start[1],self.area_end[1])
        self.slider1.max = 30
        self.slider1.text="Strength: "
        param = self.slider1.value/10
        if self.P() < 50:
             im=io.applyOperationOnRegion(io.imageContrast,im,(0,0,im.width,im.height),param)
        else:
            im=io.applyOperationOnRegion(io.imageContrast,im,(int(self.area_start[0]),int(self.area_start[1]),int(self.area_end[0]),int(self.area_end[1])),param)
        self.save_temp_image()

    def image_color_grade(self):
        global im
        make_backup()
        self.slider1.max = 20
        self.slider1.text = "Strength: "
        if self.slider1.value <= 10:
            strength = self.slider1.value/100
        else:
            strength = self.slider1.value/20
        red, green, blue = self.cp.color[0]*255, self.cp.color[1]*255, self.cp.color[2]*255
        w,h = im.size
        for i in range(0,w):
            for j in range(0,h):
                pixel = im.getpixel((i,j))
                new_pixel = (int(pixel[0] * (1-strength) + red * strength),int(pixel[1] * (1-strength) + green * strength),int(pixel[2] * (1 - strength) + blue * strength))
                im.putpixel((i,j),new_pixel)
        self.save_temp_image()

class IPCApp(App):
    def build(self):
        return IPC()

if __name__ == '__main__':
    Window.size = (1280, 720)
    atexit.register(exit_handler)
    IPCApp().run()