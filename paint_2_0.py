# Source File Name: pant_1_1.py
# Author's Name: Andy Harris
# Last Modified By: Paul Bialo
# Date Last Modified: June 22, 2012
# Program Description: A simple paint program
# Revision History: Version 1.0 - Original version
#                   Version 1.1 - Created GUI, added functionality to line thickness buttons
#                   Version 1.2 - Added functionality to reset button, colour selection, saving, and loading
#                   Version 1.3 - Added functionality to line, ellipse, and rectangle tools as well as fill for those
#                   Version 1.4 - Added spraycan functionality
#                   Version 2.0 - Release version, code cleaned up

# Importing the necessary modules
import pygame
import random
from tkinter import *
import tkinter.messagebox
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

# Button class created for toolbar items.
class Button(pygame.sprite.Sprite):
    def __init__(self, buttonX, buttonY, buttonLength, buttonHeight, buttonIcon):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((buttonLength, buttonHeight))
        self.rect = self.image.get_rect()
        self.rect.centerx = buttonX
        self.rect.centery = buttonY
        self.image = pygame.image.load("img/"+buttonIcon+".gif").convert()

# This function opens a dialog to select the colour used in the drawing    
def OpenColourDialog():
    # Create tkinter toplevel window
    root = Tk()
    # Hide the tkinter window
    root.withdraw()
    # launch the standard colour dialog and assign the colour both as a triple (R,G,B) and as a hexadecimal colour
    rgbcolour,hexcolour = askcolor(color="blue") # set the default colour in the dialog as "blue"
    # Give the main display focus again
    pygame.display.set_mode((640,480))
    # return just the rgb colour value
    return rgbcolour

# This function loads an image from a previously saved file
def loadTheImage():
    # Create tkinter toplevel window
    root = Tk()
    # Hide the tkinter window
    root.withdraw()
    #Get the filename entered - set the title, and the default file types
    fileOpen = askopenfilename(title="Open file", filetypes=[("bmp",".bmp"),('All files', '.*')],initialfile="drawing.bmp")
    # Give the main display focus again
    pygame.display.set_mode((640,480))
    # Ensure that the user did not click "Cancel" and load the image to a variable and return it to the calling function
    if fileOpen:
        canvas = pygame.image.load(fileOpen)
        #Update the window caption to include the filename
        pygame.display.set_caption(str(fileOpen))
        #return the image to be loaded
        return canvas

# This function saves an image displayed on the background to a file
# This function recieves the pygame background as an argument.
def saveTheImage(background):
    # Create tkinter toplevel window
    root = Tk()
    # Hide the tkinter window
    root.withdraw()
    #Get the filename entered
    fileSave = asksaveasfilename(title="Save file",filetypes=[("bmp",".bmp"),('All files', '.*')],initialfile="drawing.bmp")
    # Give the main display focus again
    pygame.display.set_mode((640,480))
    # Ensure that the user did not click "Cancel" and save the image
    if fileSave:
        pygame.image.save(background, fileSave)
        #Update the window caption to include the filename
        pygame.display.set_caption(str(fileSave))

# The main function of the program. Begins with initializing the program state before beginning the main loop
def main():       
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint 2.0")

    # The background surface will actually be the toolbar area
    background = pygame.Surface(screen.get_size())
    background.fill((211, 211, 211))

    # The canvas surface is where all drawing will occur
    canvas = pygame.Surface((440, 480))
    canvas.fill((255, 255, 255))       
    # canvasRect is used to check collision within the canvas
    canvasRect = pygame.Rect(0, 0, 440, 480)

    # Creating the tool buttons
    pencilButton = Button(466, 30, 32, 32, "pencil_selected")
    spraybrushButton = Button(503, 30, 32, 32, "spraybrush_unselected")
    lineButton = Button(540, 30, 32, 32, "line_unselected")
    rectangleButton = Button(466, 67, 32, 32, "rectangle_unselected")
    ellipseButton = Button(503, 67, 32, 32, "ellipse_unselected")
    filledButton = Button(540, 67, 32, 32, "filled_unselected")    
    # Used to 'unselect' all tools when a new tool is selected
    def unselectTools():
        pencilButton.image = pygame.image.load("img/pencil_unselected.gif").convert()
        spraybrushButton.image = pygame.image.load("img/spraybrush_unselected.gif").convert()
        lineButton.image = pygame.image.load("img/line_unselected.gif").convert()
        rectangleButton.image = pygame.image.load("img/rectangle_unselected.gif").convert()
        ellipseButton.image = pygame.image.load("img/ellipse_unselected.gif").convert()
        
    # Creating the thickness buttons
    thickness1Button = Button(614, 30, 32, 32, "thickness1_selected")
    thickness2Button = Button(614, 67, 32, 32, "thickness2_unselected")
    thickness3Button = Button(614, 104, 32, 32, "thickness3_unselected")
    thickness4Button = Button(614, 141, 32, 32, "thickness4_unselected")
    thickness5Button = Button(614, 178, 32, 32, "thickness5_unselected")   
    # Used to 'unselect' all thicknesses when new thickness is selected
    def unselectThickness():
        thickness1Button.image = pygame.image.load("img/thickness1_unselected.gif").convert()
        thickness2Button.image = pygame.image.load("img/thickness2_unselected.gif").convert()
        thickness3Button.image = pygame.image.load("img/thickness3_unselected.gif").convert()
        thickness4Button.image = pygame.image.load("img/thickness4_unselected.gif").convert()
        thickness5Button.image = pygame.image.load("img/thickness5_unselected.gif").convert()
    
    # Creating the remainder of the buttons
    colourButton = Button(503, 141, 106, 106, "colour_large")    
    clearButton = Button(466, 450, 32, 32, "clear")
    saveButton = Button(503, 450, 32, 32, "save")
    loadButton = Button(540, 450, 32, 32, "load")
    
    # Packs up the sprites into a group 
    allSprites = pygame.sprite.Group(pencilButton, spraybrushButton, lineButton, rectangleButton, ellipseButton, filledButton,
    thickness1Button, thickness2Button, thickness3Button, thickness4Button, thickness5Button, colourButton, clearButton,
    saveButton, loadButton)
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Preset variables
    lineStart = (0, 0)
    drawColour = (0, 0, 0)
    lineWidth = 1
    selectedTool = "pencil"
    rectangleStarted = False
    ellipseStarted = False
    lineStarted = False
    fill = False
    
    # The main loop of the program
    while keepGoing:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            
            # Functionality for pressing on the various toolbar icons
            # When a thickness button is selected:
            if thickness1Button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectThickness()
                thickness1Button.image = pygame.image.load("img/thickness1_selected.gif").convert()
                lineWidth = 1                 
            if thickness2Button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectThickness()
                thickness2Button.image = pygame.image.load("img/thickness2_selected.gif").convert()
                lineWidth = 2
            if thickness3Button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectThickness()
                thickness3Button.image = pygame.image.load("img/thickness3_selected.gif").convert()
                lineWidth = 3
            if thickness4Button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectThickness()
                thickness4Button.image = pygame.image.load("img/thickness4_selected.gif").convert()
                lineWidth = 4
            if thickness5Button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectThickness()
                thickness5Button.image = pygame.image.load("img/thickness5_selected.gif").convert()
                lineWidth = 5
            
            # When the colour button is pressed:
            if colourButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                newColour = OpenColourDialog()
                if newColour:
                    drawColour = newColour
            
            # When the save button is pressed:
            if saveButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                saveTheImage(canvas)

            # When the load button is pressed:
            if loadButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                loadedCanvas = loadTheImage()
                if loadedCanvas:
                    canvas = loadedCanvas
            
            # When the clear button is pressed:
            if clearButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                # A messagebox appears to verify
                if tkinter.messagebox.askokcancel("Clear canvas?", "Are you sure you want to clear the canvas?"):
                    canvas.fill((255, 255, 255))
                    rectangleStarted = False
                    ellipseStarted = False
                    lineStarted = False
                    
            # When the pencil button is pressed:
            if pencilButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectTools()
                pencilButton.image = pygame.image.load("img/pencil_selected.gif").convert()
                selectedTool = "pencil"
            
            # When the line button is pressed:
            if lineButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectTools()
                lineButton.image = pygame.image.load("img/line_selected.gif").convert()
                selectedTool = "line"
                
            # When the spraybrush button is pressed:
            if spraybrushButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectTools()
                spraybrushButton.image = pygame.image.load("img/spraybrush_selected.gif").convert()
                selectedTool = "spraybrush"
                
            # When the rectangle button is pressed:
            if rectangleButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectTools()
                rectangleButton.image = pygame.image.load("img/rectangle_selected.gif").convert()
                selectedTool = "rectangle"
                rectangleStarted = False

            # When the ellipse button is pressed:
            if ellipseButton.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
                unselectTools()
                ellipseButton.image = pygame.image.load("img/ellipse_selected.gif").convert()
                selectedTool = "ellipse"
                ellipseStarted = False                
            
            # When the fill button is pressed:
            if filledButton.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed() == (1, 0, 0) and fill == False:
                    filledButton.image = pygame.image.load("img/filled_selected.gif").convert()
                    fill = True
                elif pygame.mouse.get_pressed() == (1, 0, 0) and fill == True:
                    filledButton.image = pygame.image.load("img/filled_unselected.gif").convert()
                    fill = False            
                          
            # Using the various tools on the canvas:
            # The pencil tool
            if selectedTool == "pencil":                
                lineEnd = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.line(canvas, drawColour, lineStart, lineEnd, lineWidth)
                lineStart = lineEnd
                
            # The spraybrush tool
            # Made up a sort of algorithm to try to mimic a random spray (more spray spots towards center point)
            if selectedTool == "spraybrush":                
                lineEnd = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    spraycanPos = pygame.mouse.get_pos()
                    sprayCounter = 0
                    while sprayCounter <= (5 * lineWidth):
                        spraycanX = spraycanPos[0] + random.randrange(-10-lineWidth, 10+lineWidth)
                        spraycanY = spraycanPos[1] + random.randrange(-10-lineWidth, 10+lineWidth)
                        pygame.draw.line(canvas, drawColour, (spraycanX, spraycanY), (spraycanX, spraycanY), 1)
                        sprayCounter = sprayCounter + 1
                    sprayCounter = 0
                    while sprayCounter <= (10 * lineWidth):
                        spraycanX = spraycanPos[0] + random.randrange(-7-lineWidth, 7+lineWidth)
                        spraycanY = spraycanPos[1] + random.randrange(-7-lineWidth, 7+lineWidth)
                        pygame.draw.line(canvas, drawColour, (spraycanX, spraycanY), (spraycanX, spraycanY), 1)
                        sprayCounter = sprayCounter + 1
                    sprayCounter = 0                  
                    while sprayCounter <= (15 * lineWidth):
                        spraycanX = spraycanPos[0] + random.randrange(-4-lineWidth, 4+lineWidth)
                        spraycanY = spraycanPos[1] + random.randrange(-4-lineWidth, 4+lineWidth)
                        pygame.draw.line(canvas, drawColour, (spraycanX, spraycanY), (spraycanX, spraycanY), 1)
                        sprayCounter = sprayCounter + 1                    
                lineStart = lineEnd
                
            # The line tool
            if selectedTool == "line":
                if pygame.mouse.get_pressed() == (1, 0, 0) and lineStarted == False and canvasRect.collidepoint(pygame.mouse.get_pos()):
                    lineStart = pygame.mouse.get_pos()
                    lineStarted = True
                elif pygame.mouse.get_pressed() == (1, 0, 0) and lineStarted == True and canvasRect.collidepoint(pygame.mouse.get_pos()):
                    lineEnd = pygame.mouse.get_pos()
                    pygame.draw.line(canvas, drawColour, lineStart, lineEnd, lineWidth)
                    lineStarted = False
                
            # The rectangle tool
            if selectedTool == "rectangle":
                if pygame.mouse.get_pressed() == (1, 0, 0) and rectangleStarted == False and canvasRect.collidepoint(pygame.mouse.get_pos()):
                    rectangleStart = pygame.mouse.get_pos()
                    rectangleStarted = True
                elif pygame.mouse.get_pressed() == (1, 0, 0) and rectangleStarted == True and canvasRect.collidepoint(pygame.mouse.get_pos()):
                    rectangleEnd = pygame.mouse.get_pos()
                    rectangleHeight = rectangleEnd[1] - rectangleStart[1]
                    rectangleWidth = rectangleEnd[0] - rectangleStart[0]
                    if fill == False:
                        pygame.draw.rect(canvas, drawColour, (rectangleStart, (rectangleWidth, rectangleHeight)), lineWidth)
                    else:
                        pygame.draw.rect(canvas, drawColour, (rectangleStart, (rectangleWidth, rectangleHeight)), 0)
                    rectangleStarted = False

            # The ellipse tool
            if selectedTool == "ellipse":
                if pygame.mouse.get_pressed() == (1, 0, 0) and ellipseStarted == False and canvasRect.collidepoint(pygame.mouse.get_pos()):
                    ellipseStart = pygame.mouse.get_pos()
                    ellipseStarted = True
                elif pygame.mouse.get_pressed() == (1, 0, 0) and ellipseStarted == True and canvasRect.collidepoint(pygame.mouse.get_pos()):
                    ellipseEnd = pygame.mouse.get_pos()
                    ellipseHeight = ellipseEnd[1] - ellipseStart[1]
                    ellipseWidth = ellipseEnd[0] - ellipseStart[0]
                    # This to work through an error where the ellipse has a negative width or height although I still get the error periodically.
                    # It seems to happen when I drag with this tool selected.
                    ellipseRect = pygame.Rect(ellipseStart, (ellipseWidth, ellipseHeight))
                    ellipseRect.normalize()
                    if fill == False:
                        pygame.draw.ellipse(canvas, drawColour, ellipseRect, lineWidth)
                    else:
                        pygame.draw.ellipse(canvas, drawColour, ellipseRect, 0)
                    ellipseStarted = False                    
            
        # Updating the drawing        
        screen.blit(background, (0, 0))
        screen.blit(canvas, (0, 0))		
        allSprites.draw(background)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
