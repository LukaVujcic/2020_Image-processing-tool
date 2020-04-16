from PIL import Image  
import PIL
#Cuva sliku u zadatom formatu
def SaveImage(myImage,url,ext):
    try:
        ext=ext.upper()
        if ext=='BMP' or ext=='JPEG' or ext=='PNG':
            myImage=myImage.convert('RGB')
            myImage.save(url,ext)
    except ValueError:
        print('ValueError')
    except IOError:
        print('IOError')
#Otvara sliku sa date url adrese i vraca pillow objekat Image
def OpenImage(url):
    try:
        myImage=Image.open(url,mode='r')
        return myImage
    except ValueError:
        print('ValueError')
    except FileNotFoundError:
        print('Image not found')
    except PIL.UnidentifiedImageError:
        print('Image cannot be opened and identified')
#Primer pokretanja
#myimage=OpenImage('1.jpeg')
#SaveImage(myimage,"2","bmp")