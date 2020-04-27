from PIL import Image,ImageFilter,ImageEnhance

#Napomena
#Funkcije koje pocinju sa prefiksom image moguce je proslediti funkciji applyOperationOnRegion

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
#color je uredjena trojka (r,g,b)-generisace sliku te boje
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
            newImage.paste(f(region),box=(box[0],box[1]))
        else:    
           # newImage.show()
            newImage.paste(f(region,argv),box=(box[0],box[1]))
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

#Pretvara sliku u crno belu
def imageGrayScale(myimage):
    try:
        return myimage.convert('LA')
    except Exception as e:
        print(e)
#Bluruje sliku
#def imageBlur(myImage,CoefBlur):
def imageBlur(myImage,args):
    try:
        CoefBlur=args[0]
        blurred_image = myImage.filter(ImageFilter.GaussianBlur(CoefBlur))
        return blurred_image
    except Exception as e:
        print (e)
#def imageBrightess(myImage,factor), za factor=1 nema promene, za factor>1 posvetljenje, za factor<1 zatamljenje
def imageBrightess(myImage,args):
    try:
        factor=args[0]
        enhancer = ImageEnhance.Brightness(myImage)
        new_image=enhancer.enhance(factor)
        return new_image
    except Exception as e:
        print(e)
#def imagePixelate(myImage,coefPix) coefPix koeficijent pikselizacije odredjuje koliko je slika pikselizovana manji koef-veca pikselizacija
def imagePixelate(myImage,args):
    try:
        coefPix=args[0]
        h,w=myImage.size
        imgSmall = myImage.resize((coefPix,coefPix),resample=Image.BILINEAR)
        result = imgSmall.resize(myImage.size,Image.NEAREST)
        return result
    except Exception as e:
        print(e)
#Na osnovu slike broja in_column i in_row generise matricu slika od date slike, ako su new_width i new_height specifikovani dobija se specifikovana slika inace proslediti None za oba
def generateGridFromImage(myImage,in_column,in_row,new_width,new_height):
    try:
        w,h=myImage.size
        new_image=generateSolidColorImage(w*in_row,h*in_column,(255,255,255))
        #new_image.show()
        for j in range(0,in_column):
            for i in range(0,in_row):
                new_image.paste(myimage,(i*w,j*h))
        if new_height!=None and new_width!=None:
            new_image=new_image.resize((new_width,new_height))
        return new_image
    except Exception as e:
        print(e)
#Primer pokretanja
#Otvorene slike treba zatvoriti metodom close
#myimage=Image.open("1.jpeg")
#myimage=generateGridFromImage(myimage,4,3,None,None)
#myimage.show()
#myimage=applyOperationOnRegion(imagePixelate,myimage,(50,50,250,250),50)
#myimage=imagePixelate(myimage,50,30)
#myimage.show()
#myimage=applyOperationOnRegion(imageBrightess,myimage,(50,50,250,250),1.5)
#myimage.show()
#blurred_image = applyOperationOnRegion(imageBlur,myimage,(50,50,250,250),5)
#blurred_image.show()
#copyOneRegionToAnother(myimage,(0,0,100,50),(200,50)).show()
#myimage=applyOperationOnRegion(imageGrayScale,blurred_image,(270,100,380,250))
#myimage.show()
#saveImage(myimage,"2.jpeg","jpeg")
#watermark=Image.open("watermark.png",mode="r")
#setWatermark(myimage,watermark,(0,0)).show()
#img=generateSolidColorImage(1000,1000,(0,255,255))
#img.show()
#myimage.close()