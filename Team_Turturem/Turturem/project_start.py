# Team Turturem!: Kelli Mandel, Julia Romare
# Final Team Project
# Due date: December 18, 2015
# COMP 123 - 05
# Professor: Katherine Kinnaird
# Resources: www.tutorialspoint.com, www.Zone.effbot.org, Interactive textbook, Introduction to Computing and Programming in Python.

from tkinter import *
from imageTools import *

#-------------------------------------INDEX-------------------------------------
#----------------------------------Dec 16th 2015---------------------------------

#GLOBALS: line 25
#BUTTON RESPONSES: line 50
#IMAGE MANIPULATION:line 114
#STICKER RESPONSES: line 353
#STICKER GUI: line 651
#TEXT RESPONSES: line 852
#CANVAS GUI: line 1128
#MAIN GUI: line 1158

#Description on how we tested the functions can be seen below the headings as shown in the above index.

#-------------------------------------GLOBALS-------------------------------------

stickOptions = None #The menu to open the sticker options
mainWindow = None #The menu that gives options on which function to use
start = None #The entry that asks the file name
canvas = None #The canvas window that previews the image
textGUI = None #The GUI for the text selection window

Undo = None #The undo button

stickPrev = None

myCanvas = None #This is the canvas that appears inside the canvas window (CANVAS)

picture = None #The image that's being manipulated
undopic = None #The image that the 'undo' button converts the image to

h = None #Height of image
w = None #Width of image (NOT including whitespace)
doublew = None #Width of image (including whitespace)

activeStick = None #The active sticker -- defines the sticker the user is currently controling.

Textcolor = makeColor(0,0,0) #The color that text stickers are set at. Default is black.

#--------------------------------BUTTON RESPONSES--------------------------------
#undoResponse() was tested after every image manipulating and add sticker/text function. It was also tested with multiple image manipulations having taken place.
#QuitResponse() was tested by having multiple (or few) windows open.
#Start() tested everytime we ran "Play/Run".

def undoResponse():
    """When UNDO button is pressed, the program will undo the last function done. (this cannot be done multiple times in succession)."""
    global picture
    global undopic
    global Undo
    
    Undo["state"] = DISABLED
    
    picture = makePicture("card.jpg")
    undopic = makePicture("undo.jpg")    
    
    savePicture(undopic,"card.jpg") #This will save the 'undo' file (the file that is always 1 button behind the card file) as the card file, effectively making it so the previous button never happened.
    
    picture = makePicture("card.jpg")
    undopic = makePicture("undo.jpg") 
    
    canvas.destroy() #This closes the canvas
    canvasGUI(picture) #And this reopens it to refresh the preview that the user sees

def QuitResponse():
    """When QUIT button is pressed, the program will terminate."""
    mainWindow.destroy()
    canvas.destroy()
    stickOptions.destroy()
    textGUI.destroy()
    
    
def start():
    """This is a function that will automatically run as the program is booted. It asks the user which image they would like to use and creates an foldable card (that it then calls to a canvas window to show)."""
    
    global picture
    global w
    global h
    global doublew
    global undopic
    
    file = pickAFile()
    pic = makePicture(file) #Creates the image that the user typed.
    w = getWidth(pic)
    h = getHeight(pic)
    doublew = w*2 #Sets global variable to half of the width.
    
    image = makeEmptyPicture(w*2, h) #Creates a canvas that is twice the width.
    
    for x in range(w): #This (and below) will make the first half of the canvas the image given by the user.
        for y in range(h):
            pix = getPixel(pic,x,y)
            newpix = getPixel(image,x,y)
            color = getColor(pix)
            setColor(newpix,color)
            
    savePicture(image,"card.jpg")
    savePicture(image,"undo.jpg") #Saves the undo file
    
    picture = makePicture("card.jpg")
    undopic = makePicture("undo.jpg")
            
    canvasGUI(pic)
    
#-------------------------------------IMAGE MANIPULATION-------------------------------------   
#The image manipulations functions were all tested separately on different images as well as in random successions.


def GrayscaleResponse():
    """Will make the picture grayscale."""
    
    global picture
    global undopic
      
    savePicture(picture,"undo.jpg") #This saves unaffected image to be what the program will refer to if the user chooses to undo this action.
    Undo["state"] = NORMAL

    
    for x in range(w): #Iterates over W and height, H. Must be W so that right side of card is not affected.
        for y in range(h):
            pixel = getPixel(picture,x,y)
            
            r = getRed(pixel) #Finding the RGB components and assign to R, G and B.
            g = getGreen(pixel) 
            b = getBlue(pixel) 
            lumin = (r + g + b) / 3 #Add R and G and B and divide by three to create an average which we call LUMIN. 
            
            setColor(pixel, makeColor(lumin, lumin, lumin))
            
    savePicture(picture,"card.jpg") #These 3 lines update the image and refresh the canvas.
    canvas.destroy()
    canvasGUI(picture) 
    
    
def LightenResponse():
    """Will make the picture lighter."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg")
    Undo["state"] = NORMAL
    
    for x in range(w): #Iterate over W, and height, H.
        for y in range(h):
            pix = getPixel(picture,x,y) #Get pixel, coordinates X,Y, of PICTURE.
            col = getColor(pix)
            col = makeLighter(col) #Makes PIX's color lighter, assign to COL.
            setColor(pix,col) #Set PIX's color to COL. 
            
    savePicture(picture,"card.jpg")
    canvas.destroy()
    canvasGUI(picture)
    
    
def DarkenResponse():
    """Will make the picture darker."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg")
    Undo["state"] = NORMAL
    
    for x in range(w): #Iterate over W, and height, H.
        for y in range(h):
            pix = getPixel(picture,x,y) #Get pixel, coordinates X,Y, of PICTURE.
            col = getColor(pix)
            col = makeDarker(col) #Makes PIX's color darker, assign to COL.
            setColor(pix,col) #Set PIX's color to COL. 
            
    savePicture(picture,"card.jpg")
    canvas.destroy()
    canvasGUI(picture)
    
def BnWResponse():
    """Will make the picture only BLACK and WHITE. No grey."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg")
    Undo["state"] = NORMAL
    
    for x in range(w): #Iterate over W, and height, H.
        for y in range(h):
            pix = getPixel(picture,x,y) #Get pixel, coordinates X,Y, of PICTURE.
            r = getRed(pix) #Get RGB values of PIX.
            g = getGreen(pix)
            b = getBlue(pix)
            lumin = (r + g + b)/3 #Calculate average, LUMIN, of R plus G plus B.
            if lumin > 127.5: #If LUMIN has a greater value than 127.5 set PIX to white. Otherwise set to black. 
                setColor(pix, makeColor(255, 255, 255))
            else:
                setColor(pix, makeColor(0,0,0))
            
    savePicture(picture,"card.jpg")
    canvas.destroy()
    canvasGUI(picture)
    
    
def EdgeDetectionResponse():
    """Will detect the edges of the picture and make it look like lineart."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg")
    Undo["state"] = NORMAL
    
    for x in range(w-1): #Iterate over W-1 and H-1, because we do not want to access the last edge pixels of the PICTURE.
        for y in range(h-1):
            
            current = getPixel(picture, x, y) #Pixel with coordinates X,Y assigned to CURRENT.
            down = getPixel(picture, x, y+1) #Pixel below to CURRENT, y-coordinate, Y+1, assign variable DOWN.
            right = getPixel(picture, x+1, y) #Pixel right to CURRENT, x-coordinate, X+1, assign variable RIGHT.
            
            current_lumin = (getRed(current) + getBlue(current) + getGreen(current))/3 #Calculate average, LUMIN, RGB values of CURRENT, DOWN and RIGHT. 
            down_lumin = (getRed(down) + getBlue(down) + getGreen(down))/3
            right_lumin = (getRed(right) + getBlue(right) + getGreen(right))/3
            
            if abs(current_lumin - down_lumin) > 2 and abs(current_lumin - right_lumin) > 2: #If difference between CURRENT's and DOWN's LUMIN as well as
                #difference between CURRENT's and RIGHT's is greater than 2, proceed. 
                col = getColor(current)
                col = makeDarker(col) #Make CURRENT's color darker, COL and set CURRENT to COL.
                setColor(current, col)
            if abs(current_lumin - down_lumin) <= 2 or abs(current_lumin - right_lumin) <= 2:#If difference between CURRENT's and DOWN's LUMIN as well as
                #difference between CURRENT's and RIGHT's is equals or smaller than 2, proceed. Means the LUMIN values are close. 
                col = getColor(current)
                col = makeLighter(col) #Make CURRENT's color lighther, COL and set CURRENT to COL.
                setColor(current, col) 
            
    savePicture(picture,"card.jpg")
    canvas.destroy()
    canvasGUI(picture)
    
    
def justRedResponse():
    """Will make every pixel that is insufficiently red grayscale. If a pixel is red enough, it will leave it red."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg")
    Undo["state"] = NORMAL
    
    for x in range(w): #Iterate over W, and height, H. 
        for y in range(h):
            pix = getPixel(picture,x,y)
            r = getRed(pix) #Get RGB values of PIX.
            g = getGreen(pix)
            b = getBlue(pix)
            if (r < b + g + 30): #If the R is smaller than B plus G plus 30, PIX is not red enough. Set PIX's color to the average of the RGB values.
                lumin = (r + g + b) / 3
                setColor(pix, makeColor(lumin, lumin, lumin))
            
    savePicture(picture,"card.jpg")
    canvas.destroy()
    canvasGUI(picture)
    
    
    
def justBlueResponse():
    """Will make every pixel that is insufficiently blue grayscale. If a pixel is blue enough, it will leave it blue."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg")
    Undo["state"] = NORMAL
    
    for x in range(w): #Iterate over W, and height, H.
        for y in range(h):
            pix = getPixel(picture,x,y)
            r = getRed(pix)  #Get RGB values of PIX.
            g = getGreen(pix)
            b = getBlue(pix)
            if b < r + 30 and b < g + 30: #If B is smaller than both R plus 30 and G plus 30, PIX's B value is not high enough. Set PIX's color to the average of the RGB values.
                lumin = (r + g + b) / 3
                setColor(pix, makeColor(lumin, lumin, lumin))
            
    savePicture(picture,"card.jpg")
    canvas.destroy()
    canvasGUI(picture)
    
    
def justGreenResponse():
    """Will make every pixel that is insufficiently green grayscale. If a pixel is green enough, it will leave it green."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg")
    Undo["state"] = NORMAL
    
    for x in range(w): #Iterate over W, and height, H.
        for y in range(h):
            pix = getPixel(picture,x,y)
            r = getRed(pix)  #Get RGB values of PIX.
            g = getGreen(pix)
            b = getBlue(pix)
            if g < r + 45 and g < b + 45: #If G is smaller than both R plus 45 and B plus 45, PIX's G value is not high enough. Set PIX's color to the average of the RGB values.
                lumin = (r + g + b) / 3
                setColor(pix, makeColor(lumin, lumin, lumin))
            
    savePicture(picture,"card.jpg")
    canvas.destroy()
    canvasGUI(picture)
    
def SepiaResponse():
    """Will make the picture sepia."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg") #This saves unaffected image to be what the program will refer to if the user chooses to undo this action.
    Undo["state"] = NORMAL
    
    for x in range(w): #Iterate over W, and height, H.
        for y in range(h):
            pixel = getPixel(picture,x,y)
            
            r = getRed(pixel) #Get PIXEL's RGB values, assign to R, G and B.
            g = getGreen(pixel)
            b = getBlue(pixel)
            
            lumin = (r * 0.299) + (g * 0.587) + (b * 0.114) #The weighted average of R plus G plus B, LUMIN.
            setColor(pixel, makeColor(lumin, lumin, lumin)) #Set PIX's color to LUMIN.
            
            red = getRed(pixel) #Get new RGB values of PIXEL, assign to RED, GREEN and BLUE.
            blue = getBlue(pixel)
            green = getGreen(pixel)
            
            lumin = (red + green + blue)/3 #Average of RED plus GREEN plus BLUE, is LUMIN.
            
            if lumin < 63: #If LUMIN is smaller than 63, change PIXEL's RED by factor 1.1 and BLUE by factor 0.9. 
                setRed(pixel,red*1.1)
                setBlue(pixel,blue*0.9)
                
            if lumin >= 63 and lumin < 192: #If LUMIN is equal to and greater than 63 but smaller than 192, change PIXEL's RED by factor 1.15 and BLUE by factor 0.85. 
                setRed(pixel,red*1.15)
                setBlue(pixel,blue*0.85)
                
            if lumin >= 192: #If LUMIN is equal or greater than 192, change PIXEL's RED by factor 1.08 and BLUE by factor 0.92. 
                setRed(pixel,red*1.08)
                setBlue(pixel,blue*0.92)
            
    savePicture(picture,"card.jpg") #Resaves image and closes/reopens canvas to update preview.
    canvas.destroy()
    canvasGUI(picture)    
    
#--------------------------------STICKER RESPONSES--------------------------------
#Tested on various sizes of stickers, various stickers and various canvas sizes, including canvases smaller than the stickers.

def upResponse(z):
    """Moves sticker upwards."""
    
    coordinates = myCanvas.coords(stickPrev) #Returns the current coordinates of STICKPREV at MYCANVAS.
    x = coordinates[0] #Access the zero-positioned item in COORDINATES list.
    y = coordinates[1]  
    
    if y - 5 >= 0: # If Y minus 5 is non-negative (still inside the canvas), move STICKPREV 5 pixels upwards. 
        myCanvas.move(stickPrev,0,-5)
    
    return

def downResponse(z):
    """Moves sticker downwards."""
    
    coordinates = myCanvas.coords(stickPrev) #Returns the current coordinates of STICKPREV at MYCANVAS.
    x = coordinates[0]
    y = coordinates[1]  
    
    if y + 5 <= h - getHeight(makePicture(activeStick)): #As long as Y plus 5 is smaller than H minus the height of ACTIVESTICK, move STICKPREV downwards. Keeps sticker in bounds.    
        myCanvas.move(stickPrev,0,5)
    
    return

def leftResponse(z):
    """Moves sticker to the left."""
    
    coordinates = myCanvas.coords(stickPrev) #Returns the current coordinates of STICKPREV at MYCANVAS.
    x = coordinates[0]
    y = coordinates[1]  
    
    if x - 5 >= 0: #If X minus 5 is greater or equal to zero, move STICKPREV 5 pixels to the left. Keeps sticker in bounds.    
        myCanvas.move(stickPrev,-5,0)
    
    return

def rightResponse(z):
    """Moves sticker to the right."""
    
    coordinates = myCanvas.coords(stickPrev) #Returns the current coordinates of STICKPREV at MYCANVAS.
    x = coordinates[0]
    y = coordinates[1]  
    
    if x + 5 <= doublew - getWidth(makePicture(activeStick)): #If X plus 5 is smaller or equal to zero DOUBLEW minus width of ACTIVESTICK, move STICKPREV to the right. Keeps sticker in bounds.
        myCanvas.move(stickPrev,5,0)
    
    return

def returnResponse(z):
    """Calls to ADDSTICKER to the coordinates chosen by user through arrow-key responses."""
    global stickPrev
    
    coordinates = myCanvas.coords(stickPrev) #Returns the current coordinates of STICKPREV at MYCANVAS.
    x = coordinates[0]
    y = coordinates[1]
    
    addSticker(x,y) #Call on ADDSTICKER and give X and Y.
    
def blackreturnResponse(z):
    """Calls to ADDBLACKSTICKER to the coordinates chosen by user through arrow-key responses.""" 
    global stickPrev
    
    coordinates = myCanvas.coords(stickPrev)
    x = coordinates[0]
    y = coordinates[1]
    
    addblackSticker(x,y) #Call on ADDBLACKSTICKER and give X and Y.

        
def stickPlaceResponse(stickChoice):
    """Places the preview of the sticker on the CANVAS and allows user to move and place through arrow-keys and Return. Takes in string, STICKCHOICE.
    For stickers with a white background."""
    global canvas
    global sticker
    global myCanvas
    global stickPrev
    
    stickOpen = Image.open(stickChoice) #Open tkinter compatible version of STICKCHOICE assign to STICKOPEN.
    sticker = ImageTk.PhotoImage(stickOpen) #Creates STICKOPEN as an image.
    
    stickPrev = myCanvas.create_image(0,0,image=sticker,anchor=NW) #Placing STICKER on MYCANVAS.
    
    #Assigns keyboard presses.
    canvas.bind("<Up>", upResponse) 
    canvas.bind("<Left>", leftResponse)
    canvas.bind("<Down>", downResponse)
    canvas.bind("<Right>", rightResponse)
    canvas.bind("<Return>", returnResponse)
    
def blackstickPlaceResponse(stickChoice):
    """Places the preview of the sticker on the CANVAS and allows user to move and place through arrow-keys and Return. Takes in string, STICKCHOICE. 
    For stickers with a black background."""
    
    global canvas
    global sticker
    global myCanvas
    global stickPrev
    
    stickOpen = Image.open(stickChoice)
    sticker = ImageTk.PhotoImage(stickOpen) 
    
    stickPrev = myCanvas.create_image(0,0,image=sticker,anchor=NW)

    #Assigns keyboard presses.    
    canvas.bind("<Up>", upResponse)
    canvas.bind("<Left>", leftResponse)
    canvas.bind("<Down>", downResponse)
    canvas.bind("<Right>", rightResponse)
    canvas.bind("<Return>", blackreturnResponse)
    
def smallstarResponse():
    """Calls to stickPlaceResponse with the small star image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/star_small.jpg"
    
    blackstickPlaceResponse("stickers/star_small.jpg")
    
def medstarResponse():
    """Calls to stickPlaceResponse with the medium star image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/star_med.jpg"  
    
    blackstickPlaceResponse("stickers/star_med.jpg") 
    
def largestarResponse():
    """Calls to stickPlaceResponse with the large star image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/star_large.jpg" 
    
    blackstickPlaceResponse("stickers/star_large.jpg")
    
def smallheartResponse():
    """Calls to stickPlaceResponse with the small heart image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/heart_small.jpg" 
    
    stickPlaceResponse("stickers/heart_small.jpg")
    
def medheartResponse():
    """Calls to stickPlaceResponse with the medium heart image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/heart_med.jpg" 
    
    stickPlaceResponse("stickers/heart_med.jpg")
    
def largeheartResponse():
    """Calls to stickPlaceResponse with the large heart image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/heart_large.jpg" 
    
    stickPlaceResponse("stickers/heart_large.jpg")
    
def smallheartsResponse():
    """Calls to stickPlaceResponse with the small hearts image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/hearts_small.jpg" 
    
    blackstickPlaceResponse("stickers/hearts_small.jpg")
    
def medheartsResponse():
    """Calls to stickPlaceResponse with the medium hearts image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/hearts_med.jpg" 
    
    blackstickPlaceResponse("stickers/hearts_med.jpg")
    
def largeheartsResponse():
    """Calls to stickPlaceResponse with the large hearts image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/hearts_large.jpg" 
    
    blackstickPlaceResponse("stickers/hearts_large.jpg")
    
def smallsparklesResponse():
    """Calls to stickPlaceResponse with the small sparkles image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/sparkles_small.jpg" 
    
    blackstickPlaceResponse("stickers/sparkles_small.jpg")
    
def medsparklesResponse():
    """Calls to stickPlaceResponse with the medium sparkles image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/sparkles_med.jpg" 
    
    blackstickPlaceResponse("stickers/sparkles_med.jpg")
    
def largesparklesResponse():
    """Calls to stickPlaceResponse with the large sparkles image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/sparkles_large.jpg" 
    
    blackstickPlaceResponse("stickers/sparkles_large.jpg")
    
def smalltophatResponse():
    """Calls to stickPlaceResponse with the small tophat image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/tophat_small.jpg" 
    
    stickPlaceResponse("stickers/tophat_small.jpg")
    
def medtophatResponse():
    """Calls to stickPlaceResponse with the medium tophat image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/tophat_med.jpg" 
    
    stickPlaceResponse("stickers/tophat_med.jpg")
    
def largetophatResponse():
    """Calls to stickPlaceResponse with the large tophat image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    
    global activeStick
    activeStick = "stickers/tophat_large.jpg" 
    
    stickPlaceResponse("stickers/tophat_large.jpg")
    
    
def addSticker(x,y):
    """Pastes the sticker (with white background) onto the image file at the coordinates X,Y."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg") #This saves unaffected image to be what the program will refer to if the user chooses to undo this action.
    Undo["state"] = NORMAL
    
    placed_sticker = makePicture(activeStick) #Converts ACTIVESTICK to a picture, assign to PLACED_STICKER.
    
    if getWidth(placed_sticker) > doublew or getHeight(placed_sticker) > h: #If sticker is larger than canvas it will refresh canvas and not allow sticker placement.
        canvas.destroy()
        canvasGUI(picture)    
    else:
        targetX = int(x) 
        for sourceX in range(getWidth(placed_sticker)): #Iterate over width and height of PLACED_STICKER.
            targetY = int(y)
            for sourceY in range(getHeight(placed_sticker)):
                srcPixel = getPixel(placed_sticker, sourceX, sourceY) #Get pixel with coordinates SOURCEX, SOURCEY of PLACED_STICKER, assign to SRCPIXEL.
                tgtPixel = getPixel(picture, targetX, targetY)  #Get pixel with coordinates TARGETX, TARGETY of PICTURE, assign to TGTPIXEL.
                r = getRed(srcPixel) #Get RGB values from SRCPIXEL.
                g = getGreen(srcPixel)
                b = getBlue(srcPixel)
                if (r + g + b) < 630: #Will not paste white sections onto image.
                    setColor(tgtPixel, getColor(srcPixel))
                targetY = targetY + 1 #Update TARGETY, and TARGETX, by adding 1.
            targetX = targetX + 1    
        
    savePicture(picture,"card.jpg") #These 3 lines update the image and refresh the canvas.
    canvas.destroy()
    canvasGUI(picture)  
    
def addblackSticker(x,y):
    """Pastes the sticker (with black background) onto the image file at the coordinates X,Y."""
    global picture
    global undopic
    
    savePicture(picture,"undo.jpg") #This saves unaffected image to be what the program will refer to if the user chooses to undo this action.
    Undo["state"] = NORMAL
    
    placed_sticker = makePicture(activeStick) #Same proceure as ADDSTICKER().
    
    if getWidth(placed_sticker) > doublew or getHeight(placed_sticker) > h:
        canvas.destroy()
        canvasGUI(picture)    
    else:
        targetX = int(x) 
        for sourceX in range(getWidth(placed_sticker)):
            targetY = int(y)
            for sourceY in range(getHeight(placed_sticker)):
                srcPixel = getPixel(placed_sticker, sourceX, sourceY)
                tgtPixel = getPixel(picture, targetX, targetY)
                r = getRed(srcPixel)
                g = getGreen(srcPixel)
                b = getBlue(srcPixel)
                if (r + g + b) > 140: #Will not paste black sections onto image.
                    setColor(tgtPixel, getColor(srcPixel))
                targetY = targetY + 1
            targetX = targetX + 1    
        
    savePicture(picture,"card.jpg") #These 3 lines update the image and refresh the canvas.
    canvas.destroy()
    canvasGUI(picture)  
    
#-------------------------------------STICKER GUI-------------------------------------
#Tested by clicking all the buttons in various orders.
    
def StickerResponse():
    """The user will be given an option of various 'stickers' that they can place on the image to give it a nice effect. These can be hearts, stars, sayings, ect."""
    
    global stickOptions
    
    stickOptions = Toplevel(root) 
    stickOptions.title("Sticker Options")      
    
    stickLabel = Label(stickOptions) #A label introducing the program.
    stickLabel.config(text = "Please select the sticker\n you would like to add.",
                     font = "Arial 10 bold",
                     bg = "#FFFFFF")
    stickLabel.grid(row = 0, column = 1)
    
    
    starOpen = Image.open("stickers/star_preview.jpg") #Opens and creates a tkinter-compatible image.
    star = ImageTk.PhotoImage(starOpen)      
    
    starLabel = Label(stickOptions) #Places preview of STAR for user to see.
    starLabel.config(image = star)
    starLabel.grid(row = 1, column = 1) 
    
    #The following are buttons to select, with varying size options. Each call to their own Response functions:
    
    smallstar = Button(stickOptions) 
    smallstar["text"] = "Star (small)"
    smallstar["font"] = "Arial 12"
    smallstar["bg"] = "#997711"
    smallstar["fg"] = "blue"
    smallstar.grid(row = 3, column = 0) 
    
    smallstar["command"] = smallstarResponse  
    
    medstar = Button(stickOptions) 
    medstar["text"] = "Star (medium)"
    medstar["font"] = "Arial 12"
    medstar["bg"] = "#997711"
    medstar["fg"] = "blue"
    medstar.grid(row = 3, column = 1) 
    
    medstar["command"] = medstarResponse
    
    bigstar = Button(stickOptions) 
    bigstar["text"] = "Star (large)"
    bigstar["font"] = "Arial 12"
    bigstar["bg"] = "#997711"
    bigstar["fg"] = "blue"
    bigstar.grid(row = 3, column = 2) 
    
    bigstar["command"] = largestarResponse      
    
    heartOpen = Image.open("stickers/heart_preview.jpg") #Opens and creates a tkinter-compatible image.
    heart = ImageTk.PhotoImage(heartOpen)      
    
    heartLabel = Label(stickOptions) #Places preview of HEART for user to see.
    heartLabel.config(image = heart)
    heartLabel.grid(row = 5, column = 1)
    
    #The following are buttons to select, with varying size options. Each call to their own Response functions:
    
    smallheart = Button(stickOptions) 
    smallheart["text"] = "Heart (small)"
    smallheart["font"] = "Arial 12"
    smallheart["bg"] = "#997711"
    smallheart["fg"] = "blue"
    smallheart.grid(row = 6, column = 0) 
    
    smallheart["command"] = smallheartResponse    
    
    medheart = Button(stickOptions) 
    medheart["text"] = "Heart (medium)"
    medheart["font"] = "Arial 12"
    medheart["bg"] = "#997711"
    medheart["fg"] = "blue"
    medheart.grid(row = 6, column = 1) 
    
    medheart["command"] = medheartResponse 
    
    bigheart = Button(stickOptions) 
    bigheart["text"] = "Heart (large)"
    bigheart["font"] = "Arial 12"
    bigheart["bg"] = "#997711"
    bigheart["fg"] = "blue"
    bigheart.grid(row = 6, column = 2) 
    
    bigheart["command"] = largeheartResponse   
    
    heartsOpen = Image.open("stickers/hearts_preview.jpg") #Opens and creates a tkinter-compatible image.
    hearts = ImageTk.PhotoImage(heartsOpen)      
    
    heartsLabel = Label(stickOptions) #Places preview of HEARTS for user to see.
    heartsLabel.config(image = hearts)
    heartsLabel.grid(row = 7, column = 1)     
    
    #The following are buttons to select, with varying size options. Each call to their own Response functions:
    
    smallhearts = Button(stickOptions) 
    smallhearts["text"] = "Hearts (small)"
    smallhearts["font"] = "Arial 12"
    smallhearts["bg"] = "#997711"
    smallhearts["fg"] = "blue"
    smallhearts.grid(row = 8, column = 0) 
    
    smallhearts["command"] = smallheartsResponse    
    
    medhearts = Button(stickOptions) 
    medhearts["text"] = "Hearts (medium)"
    medhearts["font"] = "Arial 12"
    medhearts["bg"] = "#997711"
    medhearts["fg"] = "blue"
    medhearts.grid(row = 8, column = 1) 
    
    medhearts["command"] = medheartsResponse 
    
    bighearts = Button(stickOptions) 
    bighearts["text"] = "Hearts (large)"
    bighearts["font"] = "Arial 12"
    bighearts["bg"] = "#997711"
    bighearts["fg"] = "blue"
    bighearts.grid(row = 8, column = 2) 
    
    bighearts["command"] = largeheartsResponse  
    
    sparklesOpen = Image.open("stickers/sparkles_preview.jpg") #Opens and creates a tkinter-compatible image.
    sparkles = ImageTk.PhotoImage(sparklesOpen)      
    
    sparklesLabel = Label(stickOptions) #Places preview of SPARKLES for user to see.
    sparklesLabel.config(image = sparkles)
    sparklesLabel.grid(row = 9, column = 1)  
    
    #The following are buttons to select, with varying size options. Each call to their own Response functions:
    
    smallsparkles = Button(stickOptions) 
    smallsparkles["text"] = "sparkles (small)"
    smallsparkles["font"] = "Arial 12"
    smallsparkles["bg"] = "#997711"
    smallsparkles["fg"] = "blue"
    smallsparkles.grid(row = 10, column = 0) 
    
    smallsparkles["command"] = smallsparklesResponse    
    
    medsparkles = Button(stickOptions) 
    medsparkles["text"] = "sparkles (medium)"
    medsparkles["font"] = "Arial 12"
    medsparkles["bg"] = "#997711"
    medsparkles["fg"] = "blue"
    medsparkles.grid(row = 10, column = 1) 
    
    medsparkles["command"] = medsparklesResponse 
    
    bigsparkles = Button(stickOptions) 
    bigsparkles["text"] = "sparkles (large)"
    bigsparkles["font"] = "Arial 12"
    bigsparkles["bg"] = "#997711"
    bigsparkles["fg"] = "blue"
    bigsparkles.grid(row = 10, column = 2) 
    
    bigsparkles["command"] = largesparklesResponse
    
    tophatOpen = Image.open("stickers/tophat_preview.jpg") #Opens and creates a tkinter-compatible image.
    tophat = ImageTk.PhotoImage(tophatOpen)      
    
    tophatLabel = Label(stickOptions) #Places preview of TOPHAT for user to see.
    tophatLabel.config(image = tophat) 
    tophatLabel.grid(row = 11, column = 1)
    
    #The following are buttons to select, with varying size options. Each call to their own Response functions:
    
    smalltophat = Button(stickOptions) 
    smalltophat["text"] = "tophat (small)"
    smalltophat["font"] = "Arial 12"
    smalltophat["bg"] = "#997711"
    smalltophat["fg"] = "blue"
    smalltophat.grid(row = 12, column = 0) 
    
    smalltophat["command"] = smalltophatResponse    
    
    medtophat = Button(stickOptions) 
    medtophat["text"] = "tophat (medium)"
    medtophat["font"] = "Arial 12"
    medtophat["bg"] = "#997711"
    medtophat["fg"] = "blue"
    medtophat.grid(row = 12, column = 1) 
    
    medtophat["command"] = medtophatResponse 
    
    bigtophat = Button(stickOptions) 
    bigtophat["text"] = "tophat (large)"
    bigtophat["font"] = "Arial 12"
    bigtophat["bg"] = "#997711"
    bigtophat["fg"] = "blue"
    bigtophat.grid(row = 12, column = 2) 
    
    bigtophat["command"] = largetophatResponse
    
    
    stickOptions.mainloop()
    
#--------------------------------TEXT RESPONSES--------------------------------
#Tested by clicking all the buttons in various orders.

def txtPlaceResponse(stickChoice):
    """Takes string, STICKCHOICE, and turns it into an image to be placed on the canvas to be moved."""
    global canvas
    global sticker
    global myCanvas
    global stickPrev
        
    
    stickOpen = Image.open(stickChoice) #Open tkinter compatible version of STICKCHOICE assign to STICKOPEN.
    sticker = ImageTk.PhotoImage(stickOpen)  #Creates STICKOPEN as an image. 
    
    if getWidth(makePicture(stickChoice)) <= w: #As long as STICKCHOICE's width does not exceed half of the canvas, STICKCHOICE will be placed on the right side of the canvas.
        stickPrev = myCanvas.create_image(w,0,image=sticker,anchor=NW)
    else: #Places STICKCHOICE as far right as it can without exceeding canvas width.
        stickPrev = myCanvas.create_image(doublew - getWidth(makePicture(stickChoice)),0,image=sticker,anchor=NW)
    
    #Arrow-key bindings to move and place STICKPREV.
    canvas.bind("<Up>", upResponse)
    canvas.bind("<Left>", leftResponse)
    canvas.bind("<Down>", downResponse)
    canvas.bind("<Right>", rightResponse)
    canvas.bind("<Return>", returnResponse)

def smallhbdResponse():
    """Calls to stickPlaceResponse with the small HBD image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hbd_small.jpg" 
    
    txtPlaceResponse("text/hbd_small.jpg")
    
def medhbdResponse():
    """Calls to stickPlaceResponse with the medium HBD image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hbd_med.jpg" 
    
    txtPlaceResponse("text/hbd_med.jpg")
    
def largehbdResponse():
    """Calls to stickPlaceResponse with the large HBD image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hbd_large.jpg" 
    
    txtPlaceResponse("text/hbd_large.jpg")
    
def smallhanniResponse():
    """Calls to stickPlaceResponse with the small HANNI image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hanni_small.jpg" 
    
    txtPlaceResponse("text/hanni_small.jpg")
    
def medhanniResponse():
    """Calls to stickPlaceResponse with the medium HANNI image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hanni_med.jpg" 
    
    txtPlaceResponse("text/hanni_med.jpg")
    
def largehanniResponse():
    """Calls to stickPlaceResponse with the large HANNI image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hanni_large.jpg" 
    
    txtPlaceResponse("text/hanni_large.jpg")
    
def smallgwsResponse():
    """Calls to stickPlaceResponse with the small GWS image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/gws_small.jpg" 
    
    txtPlaceResponse("text/gws_small.jpg")
    
def medgwsResponse():
    """Calls to stickPlaceResponse with the medium GWS image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/gws_med.jpg" 
    
    txtPlaceResponse("text/gws_med.jpg")
    
def largegwsResponse():
    """Calls to stickPlaceResponse with the large GWS image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/gws_large.jpg" 
    
    txtPlaceResponse("text/gws_large.jpg")
    
def smallhholiResponse():
    """Calls to stickPlaceResponse with the small HHOLI image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hholi_small.jpg" 
    
    txtPlaceResponse("text/hholi_small.jpg")
    
def medhholiResponse():
    """Calls to stickPlaceResponse with the medium HHOLI image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hholi_med.jpg" 
    
    txtPlaceResponse("text/hholi_med.jpg")
    
def largehholiResponse():
    """Calls to stickPlaceResponse with the large HHOLI image, as well as asigns the global varible ACTIVESTICK to the sticker selected."""
    global activeStick
    
    activeStick = "text/hholi_large.jpg" 
    
    txtPlaceResponse("text/hholi_large.jpg")
    
def textResponse():
    """The user will be asked to add text to the image."""
    global textGUI
    
    textGUI = Toplevel(root) #Creates new tkinter window, assign to TEXTGUI.
    
    textGUI.title("Text Options")  
    

    MyLabel = Label(textGUI) #Explains how to use text.
    MyLabel.config(text = "Once a text option is selected,\n use the arrow keys to position\n and return to place.\n NOTE: the white background of\n text will not be placed.",
                     font = "Arial 10 bold",
                     bg = "#FFFFFF")
    MyLabel.grid(row = 0, column = 1)   
    

    
    hbdOpen = Image.open("text/hbd_preview.jpg") #Opens and creates a tkinter-compatible image.
    hbd = ImageTk.PhotoImage(hbdOpen)      
    
    hbdLabel = Label(textGUI)
    hbdLabel.config(image = hbd)
    hbdLabel.grid(row = 1, column = 1)     
    
    smallhbd = Button(textGUI) #Create button in TEXTGUI and assign to SMALLHBD.
    smallhbd["text"] = "Happy Birthday(small)" #Change text, font, background color and foreground color. 
    smallhbd["font"] = "Arial 12"
    smallhbd["bg"] = "#997711"
    smallhbd["fg"] = "blue"
    smallhbd.grid(row = 2, column = 0) #Puts SMALLHBD into grid position.    
    
    smallhbd["command"] = smallhbdResponse #If SMALLHBD gets clicked, execute SMALLHBDRESPONSE.
    
    medhbd = Button(textGUI) #Create button in TEXTGUI and assign to MEDHBD.
    medhbd["text"] = "Happy Birthday(med)" #Same procedure as for SMALLHBD (line 988-995).
    medhbd["font"] = "Arial 12"
    medhbd["bg"] = "#997711"
    medhbd["fg"] = "blue"
    medhbd.grid(row = 2, column = 1) 
    
    medhbd["command"] = medhbdResponse #If MEDHBD get clicked, execute MEDHBDRESPONSE.
    
    largehbd = Button(textGUI) #Create button in TEXTGUI and assign to LARGEHBD. 
    largehbd["text"] = "Happy Birthday(large)" #Same procedure as for SMALLHBD (line 988-995).
    largehbd["bg"] = "#997711"
    largehbd["fg"] = "blue"
    largehbd.grid(row = 2, column = 2)  
    
    largehbd["command"] = largehbdResponse #If LARGEHBD get clicked, execute LARGEHBDRESPONSE.
    
    hanniOpen = Image.open("text/hanni_preview.jpg") #Opens and creates a tkinter-compatible image.
    hanni = ImageTk.PhotoImage(hanniOpen)      
    
    hanniLabel = Label(textGUI)
    hanniLabel.config(image = hanni)
    hanniLabel.grid(row = 3, column = 1)      
    
    smallhanni = Button(textGUI) #Same procedure like the HBD's buttons but for Happy Anniversary stickers.
    smallhanni["text"] = "Happy Anniversary(small)"  
    smallhanni["font"] = "Arial 12"
    smallhanni["bg"] = "#997711"
    smallhanni["fg"] = "blue"
    smallhanni.grid(row = 4, column = 0)     
    
    smallhanni["command"] = smallhanniResponse #Execute SMALLHANNIRESPONSE.
    
    medhanni = Button(textGUI)
    medhanni["text"] = "Happy Anniversary(med)"
    medhanni["font"] = "Arial 12"
    medhanni["bg"] = "#997711"
    medhanni["fg"] = "blue"
    medhanni.grid(row = 4, column = 1) 
    
    medhanni["command"] = medhanniResponse #Execute MEDHANNIRESPONSE.
    
    largehanni = Button(textGUI) 
    largehanni["text"] = "Happy Anniversary(large)"
    largehanni["font"] = "Arial 12"
    largehanni["bg"] = "#997711"
    largehanni["fg"] = "blue"
    largehanni.grid(row = 4, column = 2)  
    
    largehanni["command"] = largehanniResponse #Execute LARGEHANNIRESPONSE. 
    
    gwsOpen = Image.open("text/gws_preview.jpg") #Opens and creates a tkinter-compatible image.
    gws = ImageTk.PhotoImage(gwsOpen)      
    
    gwsLabel = Label(textGUI)
    gwsLabel.config(image = gws)
    gwsLabel.grid(row = 5, column = 1)      
    
    smallgws = Button(textGUI) #Same procedure like the HBD's buttons but for Get Well Soon. stickers.
    smallgws["text"] = "Get Well Soon(small)"
    smallgws["font"] = "Arial 12"
    smallgws["bg"] = "#997711"
    smallgws["fg"] = "blue"
    smallgws.grid(row = 6, column = 0)     
    
    smallgws["command"] = smallgwsResponse #Execute SMALLGWSRESPONSE.
    
    medgws = Button(textGUI) 
    medgws["text"] = "Get Well Soon(med)"
    medgws["font"] = "Arial 12"
    medgws["bg"] = "#997711"
    medgws["fg"] = "blue"
    medgws.grid(row = 6, column = 1) 
    
    medgws["command"] = medgwsResponse #Execute MEDGWSRESPONSE.
    
    largegws = Button(textGUI) 
    largegws["text"] = "Get Well Soon(large)"
    largegws["font"] = "Arial 12"
    largegws["bg"] = "#997711"
    largegws["fg"] = "blue"
    largegws.grid(row = 6, column = 2)  
    
    largegws["command"] = largegwsResponse #Execute LARGEGWSRESPONSE.  
    
    hholiOpen = Image.open("text/hholi_preview.jpg") #Opens and creates a tkinter-compatible image.
    hholi = ImageTk.PhotoImage(hholiOpen)      
    
    hholiLabel = Label(textGUI)
    hholiLabel.config(image = hholi)
    hholiLabel.grid(row = 7, column = 1)      
    
    smallhholi = Button(textGUI) #Same procedure like the HBD's buttons but for Happy Holidays stickers.
    smallhholi["text"] = "Happy Holidays(small)"
    smallhholi["font"] = "Arial 12"
    smallhholi["bg"] = "#997711"
    smallhholi["fg"] = "blue"
    smallhholi.grid(row = 8, column = 0)     
    
    smallhholi["command"] = smallhholiResponse #Execute SMALLHHOLIRESPONSE.
    
    medhholi = Button(textGUI) 
    medhholi["text"] = "Happy Holidays(med)"
    medhholi["font"] = "Arial 12"
    medhholi["bg"] = "#997711"
    medhholi["fg"] = "blue"
    medhholi.grid(row = 8, column = 1) 
    
    medhholi["command"] = medhholiResponse #Execute MEDHHOLIRESPONSE.
    
    largehholi = Button(textGUI) 
    largehholi["text"] = "Happy Holidays(large)"
    largehholi["font"] = "Arial 12"
    largehholi["bg"] = "#997711"
    largehholi["fg"] = "blue"
    largehholi.grid(row = 8, column = 2)  
    
    largehholi["command"] = largehholiResponse #Execute LARGEHHOLIRESPONSE.      
    
    textGUI.mainloop()
    
#--------------------------------CANVAS GUI--------------------------------
#Tested with various card.jpg shapes and sizes.
    
def canvasGUI(pic):
    
    global canvas #Declare global variables.
    global picture
    global w
    global h
    global doublew
    global myCanvas
    global sticker
    global stickPrev
    
    canvas = Toplevel(root) #Create an additional window, and assign to CANVAS. 

    canvas.title("The Card") #Set CANVAS's title to 'The Card'.    
    
    photoOpen = Image.open("card.jpg") #Opens card.jpg as tkinter compatible image file, to PHOTOOPEN.
    photo = ImageTk.PhotoImage(photoOpen)      
    
    myCanvas = Canvas(canvas)
    myCanvas["width"] = doublew #Set MYCANVAS's width to DOUBLEW and height to H.
    myCanvas["height"] = h
    myCanvas["bg"] = "#BBBBBB"
    myCanvas.create_image(0, 0, image = photo, anchor = NW) #Places PHOTO on MYCANVAS.
    myCanvas.grid(row = 1, column = 1) 
    
    canvas.mainloop() 
    
#--------------------------------MAIN GUI--------------------------------
#Pressed all the buttons and checked if they called on the right functions.

def GUIMain():
    """The main window of our program. This window will hold all the important buttons and entries— such as which image they want to use and how they would like to manipulate it."""
    
    global mainWindow #Declare global variables. 
    global start
    global myCanvas
    global picture
    global undopic
    global Undo
    
    mainWindow = Tk() #Greate main GUI window. 
    mainWindow.title("Greeting Card Creator")
    
    MyLabel = Label(mainWindow) #A label introducing the program.
    MyLabel.config(text = "Welcome to our greeting card creator!",
                     font = "Arial 18 bold",
                     bg = "#FFFFFF")
    MyLabel.grid(row = 0, column = 0)   
    
    #Comments for GRAYSCALE is compatible with all following buttons.
    Grayscale = Button(mainWindow) #Create button in MAINWINDOW. 
    Grayscale["text"] = "Grayscale" #Change the button's text, font, background color and foreground color.
    Grayscale["font"] = "Arial 12"
    Grayscale["bg"] = "#997711"
    Grayscale["fg"] = "blue"
    Grayscale.grid(row = 1, column = 0) #Put button in the grid. 
    
    Grayscale["command"] = GrayscaleResponse #Makes the image grayscale.
    
    Lighten = Button(mainWindow) 
    Lighten["text"] = "Lighten"
    Lighten["font"] = "Arial 12"
    Lighten["bg"] = "#997711"
    Lighten["fg"] = "blue"
    Lighten.grid(row = 5, column = 0) 
    
    Lighten["command"] = LightenResponse #Makes the image lighter. 
    
    Darken = Button(mainWindow) 
    Darken["text"] = "Darken"
    Darken["font"] = "Arial 12"
    Darken["bg"] = "#997711"
    Darken["fg"] = "blue"
    Darken.grid(row = 6, column = 0) 
    
    Darken["command"] = DarkenResponse #Makes the image darker. 
    
    EdgeDetection = Button(mainWindow) 
    EdgeDetection["text"] = "Sketchify!"
    EdgeDetection["font"] = "Arial 12"
    EdgeDetection["bg"] = "#997711"
    EdgeDetection["fg"] = "blue"
    EdgeDetection.grid(row = 7, column = 0) 
    
    EdgeDetection["command"] = EdgeDetectionResponse  #Creates lines around the image's edges.
    

    MyLabel = Label(mainWindow) #Explains single out functions.
    MyLabel.config(text = "Single out buttons make all but specified color grayscale.",
                     font = "Arial 10 bold",
                     bg = "#FFFFFF")
    MyLabel.grid(row = 8, column = 0)   
    
    
    justRed = Button(mainWindow) 
    justRed["text"] = "Single out red"
    justRed["font"] = "Arial 12"
    justRed["bg"] = "#997711"
    justRed["fg"] = "blue"
    justRed.grid(row =9, column = 0) 
    
    justRed["command"] = justRedResponse  #Makes every pixel with insufficient Red grayscale.
    
    justBlue = Button(mainWindow) 
    justBlue["text"] = "Single out blue"
    justBlue["font"] = "Arial 12"
    justBlue["bg"] = "#997711"
    justBlue["fg"] = "blue"
    justBlue.grid(row = 10, column = 0) 
    
    justBlue["command"] = justBlueResponse #Makes every pixel with insufficient Blue grayscale.
    
    justGreen = Button(mainWindow) 
    justGreen["text"] = "Single out green"
    justGreen["font"] = "Arial 12"
    justGreen["bg"] = "#997711"
    justGreen["fg"] = "blue"
    justGreen.grid(row = 11, column = 0) 
    
    justGreen["command"] = justGreenResponse #Makes every pixel with insufficient Green grayscale.
    
    BnW = Button(mainWindow) 
    BnW["text"] = "High Contrast (B&W)"
    BnW["font"] = "Arial 12"
    BnW["bg"] = "#997711"
    BnW["fg"] = "blue"
    BnW.grid(row = 3, column = 0) 
    
    BnW["command"] = BnWResponse #Makes the image black and white. 
    
    Sepia = Button(mainWindow) 
    Sepia["text"] = "Sepia"
    Sepia["font"] = "Arial 12"
    Sepia["bg"] = "#997711"
    Sepia["fg"] = "blue"
    Sepia.grid(row = 2, column = 0) 
    
    Sepia["command"] = SepiaResponse #Makes the image sepia. 
    
    Sticker = Button(mainWindow) 
    Sticker["text"] = "Add stickers"
    Sticker["font"] = "Arial 12"
    Sticker["bg"] = "#997711"
    Sticker["fg"] = "blue"
    Sticker.grid(row = 12, column = 0) 
    
    Sticker["command"] = StickerResponse #Allows the user to add stickers to their picture 
    
    Text = Button(mainWindow)
    Text["text"] = "Add text"
    Text["font"] = "Arial 12"
    Text["bg"] = "#997711"
    Text["fg"] = "blue"
    Text.grid(row = 13, column = 0) 
    
    Text["command"] = textResponse #Allows the user to add text to their picture. 
    
    
    
    Undo = Button(mainWindow) 
    Undo.config(text = "Undo",
                     font = "Arial 12",
                     bg = "#FFFFFF",
                     state = DISABLED)      
    Undo.grid(row = 14, column = 0) 
    
    Undo["command"] = undoResponse    
    

    MyLabel = Label(mainWindow) #Explains the save function
    MyLabel.config(text = "Card is saved to folder that contains project_start.py as 'card.jpg'",
                     font = "Arial 10 bold",
                     bg = "#FFFFFF")
    MyLabel.grid(row = 15, column = 0)   
    
    
    
    Quit = Button(mainWindow) #Same procedure as line 1147-1152.
    Quit["text"] = "Save & Quit"
    Quit["font"] = "Arial 12"
    Quit["bg"] = "#997711"
    Quit["fg"] = "blue"
    Quit.grid(row = 16, column = 0) 
    
    Quit["command"] = QuitResponse  #Will terminate the program.
    
    start()
    
    mainWindow.mainloop()
    
#-----------------------------------------------------------------------------

GUIMain()