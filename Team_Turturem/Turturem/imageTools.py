"""=====================================================
imageTools.py

This is a modification/implementation of the functions and data types
from Mark Guzdial's Media Computation project, taken from the implementation
for Myro in C Python

Revision 2:  
* Some bug fixes
* Removed the alpha component of colors
* Added the ImageWindow class to let us handle displayed images a little better, now we can hide and reshow them. 
* Added the explore method and function, which opens the image in an external viewer, where you can zoom into the image, etc.
* Added a setAllPixels function that changes all pixels to be a single color

"""

from __future__ import print_function
import time, os, sys
import math
from numpy import array

#import graphics

versionInfo = sys.version_info[0]
if versionInfo >= 3:
   import tkinter as tk
   import tkinter.colorchooser as tkColorChooser
   import tkinter.filedialog as tkFileDialog
else:
   import Tkinter as tk
   import tkColorChooser
   import tkFileDialog
try: 	 
   from PIL import Image
except: 	 
   print("WARNING: Image not found; do you need Python Imaging Library?", file=sys.stderr)

try:
   import PIL.ImageTk as ImageTk
except:
   print("WARNING: ImageTk not found; do you need the TkInter Library?", file=sys.stderr)

root = tk.Tk()
root.withdraw()

def update():
   root.update()
 
# ==============================================================

class ImageWindow:
  
   """An ImageWindow is a toplevel window for displaying an image."""
  
   def __init__(self, displayImage, wid, hgt, title = "Image", autoflush = True):
      self.master = None
      self.tkImage = None
      self.imageLabel = None
      self.closed = True
      self.width = wid
      self.height = hgt
      self.title = title
      self.autoflush = autoflush
      self.openWindow(displayImage)
      
      
   def openWindow(self, displayImage):
      self.master = tk.Toplevel(root, 
                                width=self.width, 
                                height=self.height, 
                                bg="gray")
      self.master.protocol("WM_DELETE_WINDOW", self.close)
      self.tkImage = ImageTk.PhotoImage(displayImage)
      self.imageLabel = tk.Label(self.master, image = self.tkImage, bg="gray")
      self.imageLabel.pack()
      self.master.title(self.title)
      self.master.resizable(False, False)
      self.closed = False
      self.master.lift()
      if self.autoflush: 
         update()
       
       
   def update(self, displayImage):
      if self.closed:
         self.openWindow(displayImage)
      else:
         self.tkImage = ImageTk.PhotoImage(displayImage)
         self.imageLabel["image"] = self.tkImage
         if self.autoflush:
            update()
         
         
   def close(self):
      """Close the window"""
  
      if self.closed: 
         return
      self.closed = True
      self.master.destroy()
      self.__autoflush()
  
  
   def isClosed(self):
      return self.closed
  
  
   def isOpen(self):
      return not self.closed
  
  
   def __autoflush(self):
      if self.autoflush:
         update()
  


# ==============================================================

class GraphicsObj(object):
   def __init__(self):
      pass
   
   def convertRange(self, val):
      """Takes in a value, and converts it to be an integer between 0 and 255"""
      if self.isNumeric(val):
         return int(max(min(val, 255), 0))
      else:
         raise TypeError("(GraphicsObj) convertRange: expected numeric input, given: " + str(val))


   def isNumeric(self, value):
      """Takes in a value, and checks if it is one of the valid numeric types,
      int, float, or long, and returns True or False"""
      return isinstance(value, int) or isinstance(value, float) or isinstance(value, long)
   
   
   def isGoodRGB(self, value):
      """Given a value, this function checks to see if it is a list or tuple three long, where
      each value in the triple is an integer between 0 and 255"""
      return   (isinstance(value, tuple) or isinstance(value, list)) and \
               len(value) == 3 and \
               all([ self.isNumeric(x) for x in value ])
               

   
# ==============================================================

class Picture(GraphicsObj):
   """A picture object represents an image, keeping track of the size, source, and pixel values
   of an image"""
     
     
   def __init__(self):
      """Initializes a Picture object with no picture in it
      Inputs: <none>
      Return value: New empty Picture object"""
      self.width = 0
      self.height = 0
      self.image = None
      self.filename = None
      self.mode = None
      self.tkImage = None
      self.dispWindow = None


   def set(self, width, height, data=None, mode="color", value=255):
      """Takes in width, height and other optional inputs, and sets the values of the
      Picture object.
      Input: width, a positive integer for the number of pixels wide
      Input: height, a positive integer for the number of pixels tall
      Input: data, where to find the data for the image, what it is depends on the mode
             If mode is "color" then data is either None or an array of RGB values
             If mode is "image" then data is an image to be copied
             If mode is "jpeg" then data is the name of a file storing an image
             Otherwise data is an array of grayscale or blob values, to be copied as grayscale
      Input: mode, a string describing what kind of information is being passed in
      Input: value, a number indicating the initial value to set the RGB fields to
      No return value
      """
      self.width = width
      self.height = height
      self.mode = mode
      self.filename = '<none>'

      if mode.lower() == "color":
         if data == None:
            if type(value) == int:
               data = array([value] * (height * width * 3), 'B')
            elif len(value) == 3:                 # --- Should check type of data here
               data = array(value * (height * width), 'B')
         self.image = Image.frombuffer("RGB", (self.width, self.height),
                                         data, "raw", "RGB", 0, 1)
      elif mode.lower() == "image": 	 
         self.image = data.copy()
      elif mode.lower() == "jpeg": 	 
         self.image = Image.open(data).resize((width,height),Image.BILINEAR)
         #self.image = Image.open(data)
         self.filename = data
      elif mode.lower() in ["gray", "blob"]:
         self.image = Image.frombuffer("L", (self.width, self.height),
                                         data, 'raw', "L", 0, 1)
      else:
         raise ValueError("(Picture) set: received unknown mode value: " + str(mode))
        
      if self.image.mode != "RGB": # palette
         self.image = self.image.convert("RGB")
             
      self.pixels = self.image.load()
      self.palette = self.image.getpalette()
      if self.pixels == None:
         raise ValueError("(Picture) set: image loading failed, check for Python Imaging Library version 1.1.6")
      #self.image = ImageTk.PhotoImage(self.temp, master=root)


   def load(self, filename):
      """Given a filename, open and read the data from the file into this Picture object
      Input: filename, a string that is the name of a file
      No return value
      """
      #self.image = tk.PhotoImage(file=filename, master=root)
      self.image = Image.open(filename)
      if self.image.mode != "RGB": # palette
         self.image = self.image.convert("RGB")
      self.pixels = self.image.load()
      self.width = self.image.size[0]
      self.height = self.image.size[1]
      self.palette = self.image.getpalette()
      self.filename = filename
      if self.pixels == None:
         raise ValueError("(Picture) load: image loading failed, check for Python Imaging Library version 1.1.6")
       
       
   def __repr__(self):
      """Takes no inputs, and produces a string that accurately describes the picture object"""
      return "<Picture instance ({:d} x {:d})>".format(self.width, self.height)

   
   def getWidth(self):
      """Returns the width of the image in the Picture"""
      return self.width
   
   def getHeight(self):
      """Returns the height of the image in the Picture"""
      return self.height

   
   def getPixel(self, x, y):
      """Takes in the column (x) and row (y) position of a pixel, and returns the
      Pixel object at that location"""
      if self._checkRange(x, y, "getPixel"):
         return Pixel( x, y, self)


   def getColor(self, x, y):
      """Takes in the column (x) and row (y) position of a pixel, and returns the
      Color of the pixel at that location"""
      if self._checkRange(x, y, "getColor"):
         retval = self.pixels[x, y]
         return Color(retval)

   def getRGB(self, x, y):
      """Given the (x, y) location of a pixel, return its color as a tuple of numbers"""
      if self._checkRange(x, y, "getRGB"):
         return self.pixels[x, y][:3]
      
   #def getRGBA(self, x, y):
      #"""Given the (x, y) location of a pixel, return its color as a tuple of numbers, including the alpha component"""
      #if self._checkRange(x, y, "getRGBA"):
         #return self.pixels[x, y]
      
      
   #def getAlpha(self, x, y):
      #"""Given the (x, y) location of a pixel, return its alpha value"""
      #if self._checkRange(x, y, "getAlpha"):
         #return self.pixels[x, y][3]


   def setColor(self, x, y, newColor):
      """Given the (x, y) location of a pixel, and a new Color object, it changes
      the pixel at that location to have the new color.  No return value"""
      if self._checkRange(x, y, "setColor") and isinstance(newColor, Color):
         self.pixels[x, y] = tuple(newColor.getRGB())
      else:
         raise TypeError("(Picture) setColor: expected Color as input, given: " + str(newColor))
         
         
   def setRGB(self, x, y, rgb):
      """Given the (x, y) location of a pixel, and an RGB list/tuple, this sets the 
      color of the given pixel to the specified color"""
      if self._checkRange(x, y, "setRGB") and self.isGoodRGB(rgb):
         self.setColor(x, y, Color(*rgb))
      else:
         raise TypeError("(Picture) setRGB: expected list/tuple of numbers as input, given: " + str(rgb))
      
   def save(self, filename):
      """Given a string filename, write this picture to that file"""
      if isinstance(filename, str):
         self.image.save(filename)
      else:
         raise TypeError("(Picture) save: expected a string as input, giveN: " + str(filename))
      
   def show(self):
      """Create a Toplevel widget to display the picture, if one doesn't already exist,
      and display the picture data in it"""
      if self.dispWindow == None:
         self.dispWindow = ImageWindow(self.image, self.width, self.height, self.filename)
      else:
         self.dispWindow.update(self.image)


   def hide(self):
      """Close the window displaying this picture"""
      if self.dispWindow == None:
         return
      else:
         self.dispWindow.close()
         
      
   def explore(self):
      self.image.show()
      
      
   #def getDisplayableImage(self):
      #tkImage = ImageTk.PhotoImage(self.image)
      #return tkImage
   
   
   
   def _checkRange(self, x, y, funcName):
      """Check whether the input values are valid indices to pixels in this image.
      If they are, then return True, otherwise raise an exception that describes
      what is wrong"""
      if (0 <= x < self.width) and (0 <= y < self.height):
         return True
      else:
         if x < 0:
            errStr = "input x value, {:d}, < 0".format(x)
         elif x >= self.width:
            errStr = "input x value, {:d}, >= {:d}".format(x, self.width)
         elif y < 0:
            errStr = "input y value, {:d}, < 0".format(y)
         elif y >= self.height:
            errStr = "input y value, {:d}, >= {:d}".format(y, self.height)
         else:
            errSTr = "Weird unknown error, contact developers"
         raise ValueError("(Picture) " + funcName + ": " + errStr)
      


# ==============================================================


class Pixel(GraphicsObj):
   """A Pixel represents a particular location and its color, within an overall Picture.
   Every Pixel has a picture to which it belongs"""
   
   
   def __init__(self, x, y, picture):
      """Given a location and a Picture, set up the Pixel object"""
      # Note: note error-checking here because Pixels cannot/should not be created willy-nilly,
      # but are created by the Picture object itself, which should know what it's doing
      self.x = x
      self.y = y
      self.picture = picture
      self.pixels = picture.pixels
      # we might need this, for gifs:
      self.palette = self.picture.image.getpalette()


   def __repr__(self):
      rgb = self.getRGB()
      template = "<Pixel instance (r={:d}, g={:d}, b={:d}) at ({:d}, {:d})>" 
      return ( template.format(rgb[0],
                               rgb[1],
                               rgb[2],
                               self.x, 
                               self.y))
     


   def getX(self):
      """Returns the x position of this Pixel"""
      return self.x
   
   def getY(self):
      """Returns the y position of this Pixel"""
      return self.y
   
   def getColor(self):
      """Returns the color of this Pixel, as a Color object"""
      retval = self.pixels[self.x, self.y]
      return Color(retval)
     

   def getRGB(self):
      """Returns a tuple of the RGB values for this Pixel"""
      return self.pixels[self.x, self.y][:3]

   def getRed(self):
         """Returns the red value for this Pixel"""
         return self.pixels[self.x, self.y][0]

   def getGreen(self):
         """Returns the green value for this Pixel"""
         return self.pixels[self.x, self.y][1]

   def getBlue(self):
         """Returns the blue value for this Pixel"""
         return self.pixels[self.x, self.y][2]

   
   #def getRGBA(self):
      #"""Returns a tuple of the RGB and alpha values for this Pixel"""
      #return self.pixels[self.x, self.y]
   
   #def getAlpha(self):
      #"""Returns the alpha value for this Pixel"""
      #return self.pixels[self.x, self.y][3]


   def setColor(self, newColor):
      """Takes in a new Color object, and sets the color of this Pixel to be the new Color"""
      if isinstance(newColor, Color):
         self.pixels[self.x, self.y] = tuple(newColor.getRGB())
      else:
         raise TypeError("(Pixel) setColor: Expected input to be Color, given: " + str(newColor))
      
      
   def setRGB(self, rgb):
      """Given an list or tuple of integers, specifying RGB values, set this Pixel to have that color"""
      if self.isGoodRGB(rgb):
         self.setColor(Color(*rgb))
      else:
         raise TypeError("(Pixel) setRGB: Expected input to be a list of numbers, given: " + str(rgb))
      
   def setRed(self, value):
      """Given a value, this sets the red part of the Pixel's
      color to be the input value"""
      if isNumeric(value):
         oldColor = self.getRGB()
         self.setRGB( (value, oldColor[1], oldColor[2]) )
      else:
         raise TypeError("setRed: expected numeric input, given: " + str(value))

   def setGreen(self, value):
      """Given a value, this sets the green part of the Pixel's
      color to be the input value"""
      if isNumeric(value):
         oldColor = self.getRGB()
         self.setRGB( (oldColor[0], value, oldColor[2]) )
      else:
         raise TypeError("setGreen: expected numeric input, given: " + str(value))

   def setBlue(self, value):
      """Given a value, this sets the blue part of the Pixel's
      color to be the input value"""
      if isNumeric(value):
         oldColor = self.getRGB()
         self.setRGB( (oldColor[0], oldColor[1], value) )
      else:
         raise TypeError("setBlue: expected numeric input, given: " + str(value))
   
   
   #def setAlpha(self, alpha):
      #"""Sets the alpha value of this pixel to the input value"""
      #if self.isNumeric(alpha):
         #alpha = self.convertRange(alpha)
         #rgba = self.pixels[self.x, self.y]
         #self.pixels[self.x, self.y] = (rgba[0], rgba[1], rgba[2], alpha)
      #else:
         #raise TypeError("(Pixel) setAlpha: expected numeric input, given: " + str(alpha))

   def __eq__(self, other):
      """Compares two Pixels for equality"""
      if isinstance(other, Pixel):
         o1 = self.getRGB()
         o2 = other.getRGB()
         return (o1[0] == o2[0] and 
                 o1[1] == o2[1] and 
                 o1[2] == o2[2])
      else:
         raise TypeError("Pixel equality: both operands must be Pixels, given: " + str(other))
      
      
   def __ne__(self,other):
      """Compares two Pixels for inequality"""
      return not self.__eq__(other)


   def makeLighter(self):
      """Changes the pixel's color to be a lighter version"""
      pixColor = self.getColor()
      pixColor.makeLighter()
      self.setColor(pixColor)

   def makeDarker(self):
      """Changes the pixel's color to be a darker version"""
      pixColor = self.getColor()
      pixColor.makeDarker()
      self.setColor(pixColor)



# ==============================================================

class Color(GraphicsObj):
   """A Color object represents an individual color, as RGB """
   
   def __init__(self, *rgb):
      """
      Returns a Color object. Takes red, green, blue. All values are between 0 and 255).
      """
      #self.alpha = 255
      if len(rgb) == 1:
         self.rgb = rgb[0]
      elif len(rgb) == 3:
         self.rgb = rgb
      else:
         raise TypeError("Color(): inputs must be 3 integers: red, green, blue")
      # Convert rgb values to range from 0 to 255, and to be integers
      self.rgb = tuple([ self.convertRange(val) for val in self.rgb ])
        
        
   def __repr__(self):
      template = "<Color instance (r={:d}, g={:d}, b={:d})>"
      return template.format(self.rgb[0], self.rgb[1], self.rgb[2])

   # Accessors
   def getColor(self):
      """Returns a new Color object that is a copy of this one"""
      return Color(self.rgb)
   
   def setColor(self, color):
      """Sets the color of this Color to be the input Color's values"""
      if isinstance(color, Color):
         self.rgb = color.getRGB()
      else:
         raise TypeError("(Color) setColor: expected Color object as input, given: " + str(color))


   #def getAlpha(self):
      #"""Returns the alpha value of this Color"""
      #return self.alpha
   
   #def setAlpha(self, value):
      #"""Sets the alpha value of this Color to the input, value, which should be an integer between 
      #0 and 255, this converts the value to be that."""
      #if self.isNumeric(value):
         #self.alpha = self.convertRange(value)
      #else:
         #raise TypeError("(Color) setAlpha: expected numeric input, given: " + str(value))
      
     
   def getRed(self):
      """Returns the red value of this Color"""
      return self.rgb[0]
   def getGreen(self):
      """Returns the green value of this Color"""
      return self.rgb[1]
   def getBlue(self):
      """Returns the blue value of this Color"""
      return self.rgb[2]
   
   def getRGB(self):
      """Returns a copy of the tuple containing the RGB values of this color"""
      return tuple(self.rgb[:3])
   
   #def getRGBA(self):
      #"""Returns a tuple that contains the RGB and alpha values of this color"""
      #return (self.rgb[0], self.rgb[1], self.rgb[2], self.alpha)

   def setRGB(self, rgb):
      """Takes in a list or tuple containing red, green, and blue values, and changes the Color object to 
      have those values"""
      if self.isGoodRGB(rgb):
         self.rgb = tuple([ self.convertRange(val) for val in rgb ])
      else:
         raise TypeError("(Color) setRGB: expected list or tuple of numbers, given: " + str(rgb))



   def __eq__(self, other):
      """Given another Color as input, returns True if all three values are the same, otherwise
      returns False"""
      if isinstance(other, Color):
         o1 = self.getRGB()
         o2 = other.getRGB()
         return (o1[0] == o2[0] and 
                 o1[1] == o2[1] and 
                 o1[2] == o2[2])
      else:
         return False
      
      
   def __ne__(self, other):
      """Given another Color as input, returns False if all three values are the same, otherwise
      returns True"""
      return not self.__eq__(other)


   def __sub__(self, other):
      """Given another Color as input, performs subtraction by subtracting the other color's
      red value from this red value, and similarly for green and blue.  Returns a new color
      that is the result of the subtraction."""
      if isinstance(other, Color):
         o1 = self.getRGB()
         o2 = other.getRGB()
         return Color(o1[0] - o2[0], o1[1] - o2[1], o1[2] - o2[2])
      else:
         raise TypeError("Color subtraction: Cannot subtract a non-Color from a Color")
   
   
   def __add__(self, other):
      """Given another Color as input, performs addition by adding the other color's
      red value from this red value, and similarly for green and blue.  Returns a new color
      that is the result of the addition."""
      if isinstance(other, Color):
         o1 = self.getRGB()
         o2 = other.getRGB()
         return Color(o1[0] + o2[0], o1[1] + o2[1], o1[2] + o2[2])
      else:
         raise TypeError("Color addition: Cannot add a non-Color to a Color")


   def makeLighter(self):
      """Modifies the color object to be lighter than it is."""
      self.rgb = tuple([ self.convertRange( ((255 - val) * 0.35) + val ) for val in self.rgb ])

   def makeDarker(self):
      """Modifies this color to be darker than it is."""
      self.rgb = tuple([ self.convertRange( val * 0.65 ) for val in self.rgb ])



# ==============================================================
# A small class for iterating over the pixels in a Picture


class PixelIterator:
   """An iterator class for iterating over the Pixels in a Picture"""
   
   def __init__(self, picture):
      """Given the picture it refers to, it stores it away for future use"""
      self.myPicture = picture
      
   def __iter__(self):
      """Start at row 0 and column 0"""
      self.row = 0
      self.col = 0
      return self
   
   
   def __next__(self):
      """Return the next Pixel
      This assumes that when we need to first check if the row or column values are out of bounds, 
      and to update them appropriately if so, before accessing the next pixel"""
      if self.row == self.myPicture.getHeight():
         self.row = 0
         self.col = self.col + 1
         
      if self.col == self.myPicture.getWidth():
         raise StopIteration
      else:
         nextPix = self.myPicture.getPixel(self.col, self.row)
         self.row = self.row + 1
         return nextPix
  

# ==============================================================
# Below this are functions that manipulate images

# ----------------------------------------------------------------
# Picture functions

def loadPicture(filename):
    """ Loads a picture from a filename. """
    picture = Picture()
    picture.load(filename)
    return picture


def copyPicture(picture):
    """ Takes a Picture object and returns a copy. """
    if isinstance(picture, Picture):
       newPicture = Picture()
       newPicture.set(getWidth(picture), getHeight(picture),
                      picture.image, mode = "image")
       return newPicture
    else:
       raise TypeError("copyPicture: expected Picture object as input, given: " + str(picture))

# Call the function by another name, too
duplicatePicture = copyPicture


def makePicture(*args):
   """
   Takes zero or more args to make a picture.
   
   makePicture() - makes a 0x0 image
   makePicture(width, height)
   makePicture("filename")
   makePicture("http://image")
   makePicture(width, height, data)
   makePicture(width, height, data, "mode")
   """
   if len(args) == 0:
      retval = Picture()
   elif len(args) == 1:
      filename = args[0]
      if isinstance(filename, str):
         retval = Picture()
         if filename.startswith("http://"):
            filename, message = urllib.urlretrieve(filename)
         retval.load(filename)
      else:
         raise TypeError("makePicture: single input must be a filename or URL, given: " + str(filename))
   elif len(args) == 2:
      x = args[0]
      y = args[1]
      if isNumeric(x) and isNumeric(y):
         retval = Picture()
         retval.set(x, y)
      else:
         raise TypeError("makePicture: two inputs must be numeric, given: " + str(x) + " and " + str(y))
   elif len(args) == 3:
      x = args[0]
      y = args[1]
      if isNumeric(x) and isNumeric(y):
         if type(args[2]) in [Color, Pixel]:
            retval = Picture()
            retval.set(x, y, value=args[2].getRGB())
         elif type(args[2]) == int:
            retval = Picture()
            retval.set(x, y, value=args[2])
         elif type(args[2]) in [list, tuple]: # Undocumented
            retval = Picture()
            retval.set(x, y, value=args[2])
         else:
            template = "makePicture: third input has unknown type: {:s} is '{:s}'; should be Color, Pixel, or integer"
            raise TypeError(template.format(args[2], type(args[2])))
      else:
         raise TypeError("makePicture: first two inputs must be numeric, given: " + str(x) + " and " + str(y))
   elif len(args) == 4:
      x = args[0]
      y = args[1]
      array = args[2]
      mode = args[3]
      retval = Picture()
      retval.set(x, y, array, mode)
   
   return retval


def makeEmptyPicture(wid, hgt):
   """Takes a width and height in pixels, and returns a blank picture with those dimensions"""
   return makePicture(wid, hgt)


def savePicture(picture, filename):
   """Given a Picture and a string filename, write the picture to a file with that filename"""
   if isinstance(picture, Picture) and isinstance(filename, str):
      picture.save(filename)
   elif not isinstance(picture, Picture):
      raise TypeError("savePicture: expected first input to be a Picture, given: " + str(picture))
   else:
      raise TypeError("savePicture: expected second input to be a string, given: " + str(filename))
      
      
# define a second name for this function
def writePictureTo(pic, file):
   savePicture(pic, file)




def show(picture, name="default"):
   """Given a picture object, display it in a window.  Note that this automatically
   updates if the picture has changed, ensuring that the most recent version is always displayed"""
   picture.show()
   

def repaint(picture):
   """Maintained for backwards compatibility, in the past this was the one that updated the
   picture's changes, now it just acts the same as show"""
   picture.show()


def hide(picture):
   """Closes the window displaying a picture"""
   picture.hide()
   
   
def explore(picture):
   """Opens a view of the picture using an external program, Preview on Macs."""
   picture.explore()
   

def getWidth(picture):
   """Given a Picture object, return the width of the picture"""
   if isinstance(picture, Picture):
      return picture.getWidth()
   else:
      raise TypeError("getWidth: expected Picture as input, given: " + str(picture))
   
 
def getHeight(picture):
   """Given a Picture object, return the height of the picture"""
   if isinstance(picture, Picture):
      return picture.getHeight()
   else:
      raise TypeError("getHeight: expected Picture as input, given: " + str(picture))


def getPixel(picture, x, y):
   """Given a Picture object and the (x, y) location of a pixel, return the Pixel at that location"""
   if isinstance(picture, Picture):
      return picture.getPixel(x, y)
   else:
      raise TypeError("getPixel: expected Picture as input, given: " + str(picture))


def getPixels(picture):
   """Given a Picture object, it returns an iterator object for the Pixels in the picture"""
   if isinstance(picture, Picture):
      pixIter = PixelIterator(picture)
      return pixIter
   else:
      raise TypeError("getPixels: expected Picture as input, given: " + str(picture))
 
  
def setAllPixels(picture, color):
   """Sets all pixels of a picture to one color"""
   if isinstance(picture, Picture):
      if isinstance(color, Color):
         for x in range(picture.getWidth()):
            for y in range(picture.getHeight()):
               pix = getPixel(picture, x, y)
               setColor(pix, color)
      else:
         raise TypeError("setAllPixels: expected Color as input, given: " + str(color))
   else:
      raise TypeError("setAllPixels: expected Picture as input, given: " + str(picture))
  
  

def addRect(pic, startX, startY, width, height, color = Color(0, 0, 0)):
   """Takes in a picture object, the upper left coordinates where the rectangle should be drawn,
   the width and height of the rectangle, and an optional color (defaults to black), and it draws
   the outline of a rectangle at that location.  It checks for locations out of bounds, and stops
   at the edge of the picture."""
   leftX = max(0, startX)
   rightX = min(pic.getWidth(), startX + width)
   topY = max(0, startY)
   bottomY = min(pic.getHeight(), startY + height)
   # draw top and bottom lines
   for x in range(leftX, rightX + 1):
      px1 = getPixel(pic, x, topY)
      px2 = getPixel(pic, x, bottomY)
      setColor(px1, color)
      setColor(px2, color)
   # draw left and right lines
   for y in range(topY, bottomY + 1):
      px1 = getPixel(pic, leftX, y)
      px2 = getPixel(pic, rightX, y)
      setColor(px1, color)
      setColor(px2, color)
         
         
def addRectFilled(pic, startX, startY, width, height, color = Color(0, 0, 0)):
   leftX = max(0, startX)
   rightX = min(pic.getWidth(), startX + width)
   topY = max(0, startY)
   bottomY = min(pic.getHeight(), startY + height)
   for x in range(leftX, rightX + 1):
      for y in range(topY, bottomY + 1):
         px = getPixel(pic, x, y)
         setColor(px, color)
   

# -------------------------------------------------------------------------
def addLine(pic, x0, y0, x1, y1, color = Color(0, 0, 0)):
   """This takes in a picture, the two endpoints of a line, and a color for the line to be draw in.
   This derives from the Xiaolin Wu line-drawing algorithm, as posted on Wikipedia and also on
   rosettacode (the second shows how to blend the line color with the existing background
   colors)"""
   
   wid = getWidth(pic)
   hgt = getHeight(pic)
   
   # if the line is vertical then draw the vertical line simply
   if x0 == x1:
      _drawVerticalLine(pic, x0, y0, x1, y1, color)
      return
   
   # is the line steep or not
   steep = abs(y1 - y0) > abs(x1 - x0)

   # if the line is steep then we swap x and y values for the purposes of the looping
   # so that the main looping happens over the dominant direction.  "x" refers to the dominant
   # direction of the line, not necessarily the x dimension of the picture
   if steep:   
      x0, y0 = y0, x0
      x1, y1 = y1, x1
      wid, hgt = hgt, wid
      
   # make sure that the first point is the leftmost/lower point
   if x0 > x1:
      x0, x1 = x1, x0
      y0, y1 = y1, y0

   # compute gradient/slope of the line
   dx = x1 - x0
   dy = y1 - y0
   gradient = dy / dx
   yIntercept = y0 - gradient * x0
   

   # handle first endpoint
   xend = round(x0)
   yend = y0 + gradient * (xend - x0)
   xgap = 1 - _fracPart(x0 + 0.5)
   
   xpxl1 = xend   # this will be used in the main loop
   ypxl1 = math.floor(yend)
   
   # compute brightness for two pixels of first endpoint
   bright2 = _fracPart(yend) * xgap
   bright1 =  1 - bright2
   
   # choose which pixel
   if steep:
      _plotLine(pic, ypxl1, xpxl1, color, bright1)
      _plotLine(pic, ypxl1 + 1, xpxl1, color, bright2)
   else:
      _plotLine(pic, xpxl1, ypxl1  , color, bright2)
      _plotLine(pic, xpxl1, ypxl1 + 1, color, bright2)
   
   
   interY = yend + gradient # first y-intersection for the main loop

   # handle second endpoint
   xend = round(x1)
   yend = y1 + gradient * (xend - x1)
   xgap = _fracPart(x1 + 0.5)
   xpxl2 = xend     # this will be used in the main loop
   ypxl2 = math.floor(yend)
   bright2 = _fracPart(yend) * xgap
   bright1 = 1 - bright2
   if steep:
      _plotLine(pic, ypxl2, xpxl2, color, bright1)
      _plotLine(pic, ypxl2 + 1, xpxl2,  color, bright2)
   else:
      _plotLine(pic, xpxl2, ypxl2,  color, bright1)
      _plotLine(pic, xpxl2, ypxl2+1, color, bright2)


   # main loop
   for x in range(xpxl1 + 1, xpxl2):
      interYInt = math.floor(interY)
      bright2 = _fracPart(interY)
      bright1 = 1 - bright2
      if steep:
         _plotLine(pic, interYInt, x, color, bright1)
         _plotLine(pic, interYInt + 1, x, color, bright2)
      else:
         _plotLine(pic, x, interYInt,  color, bright1)
         _plotLine(pic, x, interYInt + 1, color, bright2)
      interY = interY + gradient
# End of addLine



def _drawVerticalLine(pic, x0, y0, x1, y1, color):
   """helper function takes in same inputs as addline, but handles the special case where the line is vertical.  Wu's algorithm doesn't handle that case"""
   hgt = getHeight(pic)
   
   # make sure that the first point is the smaller value
   if y0 > y1:
      y0, y1 = y1, y0
   
   if y0 < 0:
      y0 = 0
   if y1 >= hgt:
      y1 = hgt - 1
   
   for y in range(y0, y1+1):
      pix = getPixel(pic, x0, y)
      setColor(pix, color)
   

def _plotLine(pic, x, y, lineColor, brightLevel):
   """Given a picture, a location in the picture, the color of the line, and how bright that color
   should be at this location, this function (1) checks to make sure that the location is a valid one
   in the picture. If it isn't, nothing happens. If it is, then it blends the line's color with the
   color of the pixel at (x, y), using aweighted blend where the line's color is weighted by
   brightLevel, and the pixel's color by (1 - brightLevel)"""
   if (0 <= x) and (x < getWidth(pic)) and (0 <= y) and (y < getHeight(pic)):
      pix = getPixel(pic, x, y)
      (r1, g1, b1) = getRGB(lineColor)
      (r2, g2, b2) = getRGB(pix)
      newR = (r1 * brightLevel) + (r2 * (1 - brightLevel))
      newG = (g1 * brightLevel) + (g2 * (1 - brightLevel))
      newB = (b1 * brightLevel) + (b2 * (1 - brightLevel))
      setColor(pix, Color(newR, newG, newB))

   
    
def _fracPart(v):
   """Compute the fractional part of the input number"""
   return v - math.floor(v)



# -------------------------------------------------------------------------

def addOval(pic, x0, y0, boundWid, boundHgt, color = Color(0, 0, 0)):
   """Takes in a picture, a point in the picture, and a width and height, plus an optional color.
   It considers the point and width/height as specifying a rectangle, and it draws an ellipse that
   would sit inside the rectangle with its four sides touching the middle of each side of the
   rectangle. This uses Bresenham's algorithm for ellipses, as described by Ruslan Cray on his
   blog."""
   
   wid = boundWid / 2
   hgt = boundHgt / 2
   xMid = x0 + wid
   yMid = y0 + hgt
   
   a2 = wid * wid
   b2 = hgt * hgt
   fa2 = 4 * a2
   fb2 = 4 * b2
   
   # first half
   x = 0
   y = hgt
   sigma = 2 * b2 + a2 * (1 - 2 * hgt)
   while (b2 * x) <= (a2 * y):
      _plotPixel(pic, xMid + x, yMid + y, color)
      _plotPixel(pic, xMid - x, yMid + y, color)
      _plotPixel(pic, xMid + x, yMid - y, color)
      _plotPixel(pic, xMid - x, yMid - y, color)
      if (sigma >= 0):
         sigma += fa2 * (1 - y)
         y -= 1
      sigma += b2 * ((4 * x) + 6)
      x += 1
   
   # second half 
   x = wid
   y = 0
   sigma = 2 * a2 + b2 * (1 - 2 * wid)
   while (a2 * y) <= (b2 * x):
      _plotPixel(pic, xMid + x, yMid + y, color)
      _plotPixel(pic, xMid - x, yMid + y, color)
      _plotPixel(pic, xMid + x, yMid - y, color)
      _plotPixel(pic, xMid - x, yMid - y, color)
      if (sigma >= 0):
         sigma += fb2 * (1 - x)
         x -= 1
      sigma += a2 * ((4 * y) + 6)
      y += 1



def _plotPixel(pic, x, y, color):
   """This function takes a picture, a pixel position, and a color. It changes the pixel to have
   the input color. This is much like setColor, except that it operates on the whole picture. But
   it does check to see if the (x, y) coordinates are valid first."""
   if (0 <= x) and (x < getWidth(pic)) and (0 <= y) and (y < getHeight(pic)):
      pix = getPixel(pic, x, y)
      setColor(pix, color)
      
      
# -------------------------------------------------------------------------
   
def addOvalFilled(pic, startX, startY, boundWid, boundHgt, color = Color(0, 0, 0)):
   """Takes in a picture, a point in the picture, and a width and height, plus an optional color.
   It considers the point and width/height as specifying a rectangle, and it draws an ellipse that
   would sit inside the rectangle with its four sides touching the middle of each side of the
   rectangle. This uses an algorithm posted to stackoverflow or efficient drawing of filled ellipses."""
   
   wid = int(boundWid / 2)
   hgt = int(boundHgt / 2)
   xMid = startX + wid
   yMid = startY + hgt
   
   bound = wid * hgt * wid * hgt
   for y in range(-hgt, hgt + 1):
      dy = y  * wid
      for x in range(-wid, wid + 1):
         dx = x * hgt
         if (dx*dx+dy*dy) <= bound:
             _plotPixel(pic, xMid + x, yMid + y, color)
   


# -------------------------------------------------------------------------

def addArc(pic, x0, y0, boundWid, boundHgt, startTheta, deltaTheta, color = Color(0, 0, 0)):
   """Takes in a picture, a point in the picture, and a width and height, and two angles, plus an
   optional color. It considers the point and width/height as specifying a rectangle, and it draws
   part of an ellipse inside the rectangle bounding box. It starts drawing at startTheta, where 0
   is straight right, 90 is straight up, etc. And it draws an arc with angle deltaTheta. All angle
   values are given in degrees. This is a variation of the addOval function"""

   if deltaTheta > 0:
      endTheta = startTheta + deltaTheta
   else:
      endTheta = startTheta
      startTheta = startTheta + deltaTheta
      if startTheta < 0:
         startTheta = startTheta + 360
   wid = boundWid / 2
   hgt = boundHgt / 2
   xMid = x0 + wid
   yMid = y0 + hgt
   
   a2 = wid * wid
   b2 = hgt * hgt
   fa2 = 4 * a2
   fb2 = 4 * b2
   
   # first half
   x = 0
   y = hgt
   sigma = 2 * b2 + a2 * (1 - 2 * hgt)
   while (b2 * x) <= (a2 * y):
      _plotPixelInArc(pic, xMid + x, yMid + y, color, startTheta, endTheta)
      _plotPixelInArc(pic, xMid - x, yMid + y, color, startTheta, endTheta)
      _plotPixelInArc(pic, xMid + x, yMid - y, color, startTheta, endTheta)
      _plotPixelInArc(pic, xMid - x, yMid - y, color, startTheta, endTheta)
      if (sigma >= 0):
         sigma += fa2 * (1 - y)
         y -= 1
      sigma += b2 * ((4 * x) + 6)
      x += 1
   
   # second half 
   x = wid
   y = 0
   sigma = 2 * a2 + b2 * (1 - 2 * wid)
   while (a2 * y) <= (b2 * x):
      _plotPixelInArc(pic, xMid + x, yMid + y, color, startTheta, endTheta)
      _plotPixelInArc(pic, xMid - x, yMid + y, color, startTheta, endTheta)
      _plotPixelInArc(pic, xMid + x, yMid - y, color, startTheta, endTheta)
      _plotPixelInArc(pic, xMid - x, yMid - y, color, startTheta, endTheta)
      if (sigma >= 0):
         sigma += fb2 * (1 - x)
         x -= 1
      sigma += a2 * ((4 * y) + 6)
      y += 1

def _plotPixelInArc(pic, x, y, color, startTheta, endTheta):
   """This function takes a picture, a pixel position, and a color. It changes the pixel to have
   the input color. This is much like setColor, except that it operates on the whole picture. But
   it does check to see if the (x, y) coordinates are valid first."""
   if (0 <= x) and (x < getWidth(pic)) and (0 <= y) and (y < getHeight(pic)):
      # check here the ratio of x/y 
      pix = getPixel(pic, x, y)
      setColor(pix, color)


# ----------------------------------------------------------------
# Pixel functions


def getX(pixel):
   """Given a Pixel object, return its x position"""
   if isinstance(pixel, Pixel):
      return pixel.getX()
   else:
      raise TypeError("getX: expected a Pixel as input, given: " + str(pixel))

def getY(pixel):
   """Given a Pixel object, return its x position"""
   if isinstance(pixel, Pixel):
      return pixel.getY()
   else:
      raise TypeError("getY: expected a Pixel as input, given: " + str(pixel))

def getColor(pixel):
   """Given a Pixel object, return its color as a Color object"""
   if isinstance(pixel, Pixel):
      return pixel.getColor()
   else:
      raise TypeError("getColor: expected a Pixel as input, given: " + str(pixel))
      




def setRGB(pixel, rgb):
   """Given a Pixel object and a tuple or list containing red, green, and blue values,
   this changes the pixel's color to be the RGB value"""
   if isinstance(pixel, Pixel) and isGoodRGB(rgb):
      pixel.setRGB(rgb)
   elif not isinstance(pixel, Pixel):
      raise TypeError("setRGB: expected a Pixel as input, given: " + str(pixel))
   else:
      raise TypeError("setRGB: expected a list of three numbers, given: " + str(rgb))
   


def setRed(pixel, value):
   """Given a Pixel object and a value, this sets the red part of the Pixel's
   color to be the input value"""
   if isinstance(pixel, Pixel) and isNumeric(value):
      oldColor = pixel.getRGB()
      pixel.setRGB( (value, oldColor[1], oldColor[2]) )
   elif not isinstance(pixel, Pixel):
      raise TypeError("setRed: expected a Pixel as input, given: " + str(pixel))
   else:
      raise TypeError("setRed: expected numeric input, given: " + str(value))


def setGreen(pixel, value):
   """Given a Pixel object and a value, this sets the green part of the Pixel's
   color to be the input value"""
   if isinstance(pixel, Pixel) and isNumeric(value):
      oldColor = pixel.getRGB()
      pixel.setRGB( (oldColor[0], value, oldColor[2]) )
   elif not isinstance(pixel, Pixel):
      raise TypeError("setGreen: expected a Pixel as input, given: " + str(pixel))
   else:
      raise TypeError("setGreen: expected numeric input, given: " + str(value))



def setBlue(pixel, value):
   """Given a Pixel object and a value, this sets the blue part of the Pixel's
   color to be the input value"""
   if isinstance(pixel, Pixel) and isNumeric(value):
      oldColor = pixel.getRGB()
      pixel.setRGB( (oldColor[0], oldColor[1], value) )
   elif not isinstance(pixel, Pixel):
      raise TypeError("setBlue: expected a Pixel as input, given: " + str(pixel))
   else:
      raise TypeError("setBlue: expected numeric input, given: " + str(value))


#def setAlpha(pixel, value):
   #"""Given a Pixel object and a value, this sets the alpha part of the Pixel's
   #color to be the input value"""
   #if isinstance(pixel, Pixel) and isNumeric(value):
      #pixel.setAlpha(value)
   #elif not isinstance(pixel, Pixel):
      #raise TypeError("setAlpha: expected a Pixel as input, given: " + str(pixel))
   #else:
      #raise TypeError("setAlpha: expected numeric input, given: " + str(value))


def setColor(pixel, color):
   """Given a Pixel object and a Color object, this sets the Pixel's color"""   
   if isinstance(pixel, Pixel) and isinstance(color, Color):
      pixel.setColor(color)
   elif not isinstance(pixel, Pixel):
      raise TypeError("setColor: expected a Pixel as input, given: " + str(pixel))
   else:
      raise TypeError("setColor: expected Color object as input, given: " + str(color))





# ----------------------------------------------------------------
# Shared Pixel/Color functions


def getRed(pixOrColor):
   """Given either a Pixel or a Color, return the red part of the color"""
   if isinstance(pixOrColor, Pixel) or isinstance(pixOrColor, Color):
      return pixOrColor.getRed()
   else:
      raise TypeError("getRed function: expected input to be a Pixel or a Color, given: " + str(pixOrColor))


def getGreen(pixOrColor):
   """Given either a Pixel or a Color, return the green part of the color"""
   if isinstance(pixOrColor, Pixel) or isinstance(pixOrColor, Color):
      return pixOrColor.getGreen()
   else:
      raise TypeError("getGreen function: expected input to be a Pixel or a Color, given: " + str(pixOrColor))


def getBlue(pixOrColor):
   """Given either a Pixel or a Color, return the green part of the color"""
   if isinstance(pixOrColor, Pixel) or isinstance(pixOrColor, Color):
      return pixOrColor.getBlue()
   else:
      raise TypeError("getBlue function: expected input to be a Pixel or a Color, given: " + str(pixOrColor))


#def getAlpha(pixOrColor):
   #"""Given either a Pixel or a Color, return the alpha part of the color"""
   #if isinstance(pixOrColor, Pixel) or isinstance(pixOrColor, Color):
      #return pixOrColor.getAlpha()
   #else:
      #raise TypeError("getAlpha: expected input to be a Pixel or a Color, given: " + str(pixOrColor))


def getRGB(pixOrColor):
   """Given either a Pixel or a Color, return the color as a tuple of numbers"""
   if isinstance(pixOrColor, Pixel) or isinstance(pixOrColor, Color):
      return pixOrColor.getRGB()
   else:
      raise TypeError("getRGB: expected input to be a Pixel or a Color, given: " + str(pixOrColor))


#def getRGBA(pixOrColor):
   #"""Given either a Pixel or a Color, return the color as a tuple of numbers, including the alpha component"""
   #if isinstance(pixOrColor, Pixel) or isinstance(pixOrColor, Color):
      #return pixOrColor.getRGBA()
   #else:
      #raise TypeError("getRGBA: expected input to be a Pixel or a Color, given: " + str(pixOrColor))


def getGray(pixel):
   """Given a Pixel or a Color, compute and return its gray value the average of its red, green, and blue values"""
   if isinstance(pixel, Pixel):
      avgVal = sum(pixel.getRGB()) / 3
      return int(avgVal)
   else:
      raise TypeError("getGray: expected a Pixel or a Color as input, given: " + str(pixel))



# ----------------------------------------------------------------
# Color functions

def makeColor(red, green, blue):
   """Takes three inputs, integers in the range from 0 to 255, representing the red, green, and
   blue values of a color, and it builds and returns a Color object with that color."""
   if isNumeric(red) and isNumeric(green) and isNumeric(blue):
      return Color(red, green, blue)
   else:
      templ = "makeColor: all inputs expected to be numeric, given: {:d}, {:d}, {:d}"
      raise TypeError(templ.format(red, green, blue))
                      
                      

def distance(color1, color2):
   """Given two Color objects, this computes the distance between the colors, assuming
   that each color is a point in three-dimensional state, and using a 3D version of the
   Pythagorean theorem to compute distance."""
   if isinstance(color1, Color) and isinstance(color2, Color):
      (r1, g1, b1) = color1.getRGB()
      (r2, g2, b2) = color2.getRGB()
      dist = math.sqrt( (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2 )
      return dist
   else:
      raise TypeError("distance: Both inputs must be Color objects, given: " + str(color1) + " and " + str(color2))
   
   

def makeDarker(color):
   """Given a Color object, this darkens the color and returns it"""
   if isinstance(color, Color):
      newColor = color.getColor()
      newColor.makeDarker()
      return newColor
   else:
      raise TypeError("makeDarker: expected input to be a Color, given: " + str(color))
 
   
def makeLighter(color):
   """Given a Color object, this lightns the color and returns it"""
   if isinstance(color, Color):
      newColor = color.getColor()
      newColor.makeLighter()
      return newColor
   else:
      raise TypeError("makeLighter: expected input to be a Color, given: " + str(color))


def pickAFile():
   """Creates a dialog window for selecting a file.  Returns a string which is the filename, returning
   an empty string if no file was selected"""
   update()
   result = tkFileDialog.askopenfilename() # filetypes = [('image file', '*.jpg'), ('image file', '*.jpeg')])
   if result == None:
      print("Warning: no file selected, returning an empty string")
      return ""
   else:
      return result
   

def pickAColor():
   """Creates a dialog window for selecting a color (system specific in its details). It creates a color object from the user's chosen color, and returns it"""
   update()
   result = tkColorChooser.askcolor(color="#FFFFFF", title = "Pick A Color")
   update()
   if result[0] == None:
      print("Warning: no color selected, returning white")
      return makeColor(255, 255, 255)
   else:
      colorTuple = result[0]
      return Color(colorTuple)
   
   
   
   

# ----------------------------------------------------------------
# Utility functions


#def convertRange(val):
   #"""Takes in a value, and converts it to be an integer between 0 and 255"""
   #if isNumeric(val):
      #return int(max(min(val, 255), 0))
   #else:
      #raise TypeError("convertRange: expected numeric input, given: " + str(val))


def isNumeric(value):
   """Takes in a value, and checks if it is one of the valid numeric types,
   int, float, or long, and returns True or False"""
   return isinstance(value, int) or isinstance(value, float) or isinstance(value, long)


def isGoodRGB(value):
   """Given a value, this function checks to see if it is a list or tuple three long, where
   each value in the triple is an integer between 0 and 255"""
   return   (isinstance(value, tuple) or isinstance(value, list)) and \
            len(value) == 3 and \
            all([ isNumeric(x) for x in value ])
            


# ==============================================================
# Below this are predefined colors

black = Color(0, 0, 0)
white = Color(255, 255, 255)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
cyan = Color(0, 255, 255)
magenta = Color(255, 0, 255)
yellow = Color(255, 255, 0)
pink = Color(255, 175, 175)




