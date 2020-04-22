from PIL import Image  
import PIL
#color je uredjena trojka (r,g,b)
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
        if (len(argv)==0):
            myImage.paste(f(region),box=box)
        else:    
            myImage.paste(f(region,argv),box=box)
        return myImage
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
        if imageWatermark.format.upper()=='PNG':
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
#myimage=Image.open("1.jpeg",mode='r')
#myimage=applyOperationOnRegion(imageGrayScale,myimage,(40,100,200,200))
#myimage.show()
#saveImage(myimage,"2.jpeg","jpeg")
#watermark=Image.open("watermark.png",mode="r")
#setWatermark(myimage,watermark,(0,0)).show()
#img=generateSolidColorImage(1000,1000,(0,255,255))
#img.show()
