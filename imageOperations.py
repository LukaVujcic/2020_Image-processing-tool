from PIL import Image  
import PIL
#box1 je uredjena cetvorka (left, top, right, bottom) tj gornji levi cosak je (left,top) a donji desni (right,bottom)-ovim su zadate pozicije regiona koji zelimo da kopiramo
#box2 je uredjena dvojka (x coordinate in upper left, y coordinate in upper left) zadaje gde se na slici lepi gornji levi cosak regiona
def copyOneRegionToAnother(img,box1,box2):
    try:
        region = img.crop(box1)
        newImage=img.copy()
        newImage.paste(region,box2)
        return newImage
    except Exception as e:
        print(e)
#color je uredjena trojka (r,g,b)-cela slika ce biti te boje
def generateSolidColorImage(width,height,color):
    try:
       return Image.new('RGB', (width,height), color)
    except Exception as e:
        print(e)
#Radi custom operaciju f na slici myImage u regionu box
#def applyOperationOnRegion(f,myImage,box,argumenti za f):
def applyOperationOnRegion(f,myImage,box,*argv):
    try:
        region = myImage.crop(box)
        newImage=myImage.copy() #Pravimo novu sliku da ne bi original promenili
        if (len(argv)==0):
            newImage.paste(f(region),box=box)
        else:    
            newImage.paste(f(region,argv),box=box)
        return newImage
    except Exception as e:
        print(e)

#Cuva sliku u zadatom formatu
def saveImage(myImage,url,ext):
    try:
        ext=ext.upper()
        if ext=='BMP' or ext=='JPEG' or ext=='PNG':
            myImage=myImage.convert('RGB')
            myImage.save(url,ext)
    except ValueError:
        print('ValueError')
    except IOError:
        print('IOError')
#Postavlja watermark na sliku
def setWatermark(imageSource,imageWatermark,position):
    try:
        if imageWatermark.format.upper()=='PNG': #Watermark podrzava samo PNG slike
            width, height = imageSource.size
            transparent = Image.new('RGBA', (width, height), (0,0,0,0))
            transparent.paste(imageSource, (0,0))
            transparent.paste(imageWatermark, position, mask=watermark)
            return transparent
        else:
            print("Watermark must be PNG")
            raise Exception
    except Exception as e:
        print(e)

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
#myimage=Image.open("1.jpeg")
#myimage.show()
#copyOneRegionToAnother(myimage,(0,0,100,50),(200,50)).show()
#myimage=applyOperationOnRegion(imageGrayScale,myimage,(40,100,200,200))
#myimage.show()
#saveImage(myimage,"2.jpeg","jpeg")
#watermark=Image.open("watermark.png",mode="r")
#setWatermark(myimage,watermark,(0,0)).show()
#img=generateSolidColorImage(1000,1000,(0,255,255))
#img.show()
