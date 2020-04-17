from PIL import Image  
import PIL
#Radi custom operaciju f na slici myImage u regionu box
def applyOperationOnRegion(f,myImage,box):
    try:
        region = myImage.crop(box)
        myImage.paste(f(region),box=box)
        return myImage
    except Exception as e:
        print(e)

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
#Open IMAGE fja vec postoji
'''
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
'''
#Pretvara sliku u crno belu
def imageGrayScale(myimage):
    return myimage.convert('LA')
#Primer pokretanja
#myimage=Image.open("1.jpeg",mode='r')
#myimage=applyOperationOnRegion(imageGrayScale,myimage,(40,100,200,200))
#myimage.show()
#SaveImage(myimage,"2.jpeg","jpeg")
