####orbit programS

###setup
##importing required libraries
import sys #for exiting python
import time #for waiting periods of time
import math #for quickly performing mathematical functions
import pygame #for all graphics, animation and event handling during the program
import os #used later for listing the files in a folder
import ctypes #see next line of code

#compenstates for the adjustments made by some computers with high PDI displays that squash application displays down
ctypes.windll.user32.SetProcessDPIAware() 

###getting pygame ready
##initialising pygame
pygame.init()
pygame.display.init()

##defining the pyagame display
#sets the screensize to the resolution of the monitor used and puts the display in full screen
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#sets display width to the screen's width resolution
width = int(((pygame.display.Info()).current_w))
#sets display height to the screen's height resolution
height = int(((pygame.display.Info()).current_h))

#loads the image for the icon
icon = pygame.image.load('icon.jpg')
#sets the program icon to the image we just loaded in 
pygame.display.set_icon(icon)
#re-scales the icon to fit in the corner of the page
icon = pygame.transform.scale(icon, (30, 30))

#loads the image for the gravitation formulas used later to teach about newtons law of gravitation
gravitationFormula = pygame.image.load('formulas.jpg')
#loads the image for the suvat formulas used later to teach about motion
suvatFormula = pygame.image.load('suvat.jpg')

#loads the image of the colour wheel used to select object colours
colourWheel = pygame.image.load('ColourWheel.png')
#loads the lightness scale - also used to select object colours
lightness = pygame.image.load('lightness.jpg')

##setting up the timing
#sets the number of frames that pass each second to be 120
FPS = 120
#sets the pygame animation clock up
FPSClock = pygame.time.Clock()

##predefining colours for later
#the colours are defined in the following format:
#colour = (red(0-255), green(0-255), blue(0-255))
white = (255, 255, 255)
grey1 = (192, 192, 192)
grey2 = (128, 128, 128)
grey3 = (64, 64, 64)
grey4 = (32, 32, 32)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
green2 = (0, 150, 0)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
orange = (255, 128, 64)

#tells pygame to get the font system for making text ready
pygame.font.init()

#these are the fonts I have defined. The first parameter "consolas" is the text style that I have chosen
#the second parameter, an integer, is the font size   
ButtonFont = pygame.font.SysFont("Consolas", 15)
PanelFont = pygame.font.SysFont("Consolas", 16)
SwitchFont = pygame.font.SysFont("Consolas", 14)
InputBoxFont = pygame.font.SysFont("Consolas", 13)
ObjectFont = pygame.font.SysFont("Consolas", 12)
LearnFont = pygame.font.SysFont("Consolas", 24)

###the class that defines the button - a part of the user interface that allows the user to select the button by clicking.
###When it is being clicked, the corresponding value is true, when it is not clicked it is false 
class Button: 
    ##Initialisation method
    #the self parameter means that variable with self. infront is unique to an individual button. The other parameters are the ones that we input to create as many buttons as we want later
    def __init__(self, name, colour, posX, posY, sizeX, sizeY):
        #this defines the name of the button tha will be displayed
        self.name = name
        #this defines the default colour that the button will be
        self.colour = colour
        #this defines the position in the x axis the button will be on the screen
        self.posX = posX
        #this defines the position in the y axis the button will be on the screen
        self.posY = posY
        #this defines the width of the button
        self.sizeX = sizeX
        #this defines the height of the button
        self.sizeY = sizeY

    ##method to display the button
    #The newColour will change the colour of the button we use this later to indicate to the user if the mouse is on the button.
    #self references all the variables unique to the object tha we defined earlier
    def displayButton(self, newColour):
        #draws the main rectangular part of the button to the display based on the values we initialised it with and the updated values
        pygame.draw.rect(display, newColour, ((self.posX, self.posY), (self.sizeX, self.sizeY)))
        #defines the text and the colour of the text to be put on the button
        ButtonText = ButtonFont.render(self.name, 1, black)
        #adjusting the position of the text on the button depending on the buttons length
        adjustBy = len(self.name)
        #draws the text to the display so that it is on the button in the correct place
        display.blit(ButtonText, ((0.5*self.sizeX)+self.posX-(4*adjustBy), (0.5*self.sizeY)+self.posY-10))
    
    ##method to detect if the mouse if over the button and if it has been clicked 
    #clicked a variable asking whether or not the left mouse button is down at this instant
    #X is the position in the x axis on the screen of the mouse
    #X is the position in the y axis on the screen of the mouse
    #self references all the variables unique to the object tha we defined earlier
    def buttonClicked(self, clicked, X, Y):
        #asks if the mouse is within the reigon of the button and the mouse button is down
        if (X >= self.posX) and (X <= (self.posX+self.sizeX)) and (Y >= self.posY) and (Y <= (self.posY+self.sizeY)) and clicked:
            #button is clicked so make the display colour white and set button clicked to true
            return white, True
        #asks if the mouse is within the reigon of the button and the mouse button is up (since if it was down it would have gone through the if statement)
        elif (X >= self.posX) and (X <= (self.posX+self.sizeX)) and (Y >= self.posY) and (Y <= (self.posY+self.sizeY)):
            #button is not clicked but the mouse is on the button so still display white but  set button clicked to false
            return white, False
        #if none of the previous conditions are then the mouse must not be on the button. whether or not the button is clicked is irrelevant
        else:
            #don't change the button colour and set button clicked to false
            return self.colour, False

###the class that defines the panel
###panels create different sections on the display so the user can easily know what they are interacting with.
class Panel:
    ##initialisation method
    #self creates variables unique to each panel. The other parameters are assigned values when we create the individual panels.
    def __init__(self, type, colour, posX, posY, sizeX, sizeY):
        #defines the name given at the top of the panel
        self.type = type
        #defines the colour of the panel
        self.colour = colour
        #defines the x position of the panel
        self.posX = posX
        #defines the y position of the panel
        self.posY = posY
        #defines the width of the panel
        self.sizeX = sizeX
        #defines the height of the panel
        self.sizeY = sizeY

    #method to display panel
    #self references the variables that are unique to each panel
    def displayPanel(self):
        #draws the rectangle with with the colours, positions and sizes we initialised them with
        pygame.draw.rect(display, self.colour, ((self.posX, self.posY), (self.sizeX, self.sizeY)))
        #defines the text that will be displayed and its colour. 
        PanelText = PanelFont.render(self.type, 1, grey1)
        #displays the text at the top of the panel
        display.blit(PanelText, (self.posX+4, self.posY))

###the class that defines the switch - a part of the user interface that allows the user to toggle things in the program.
###this is done by clicking the switch
class Switch:
    ##initialisation method
    #self creates variables unique to each switch. The other parameters are assigned values when we create the individual switches.
    #the switch has default sizes of x=46 and y=24 but can be changed before initialisation
    def __init__(self, name, colour, posX, posY, state, On, Off, sizeX = 46, sizeY = 24):
        #defines the name of the switch
        self.name = name
        #defines the default colour of the switch
        self.colour = colour
        #defines the x position of the switch
        self.posX = posX
        #defines the y position of the switch
        self.posY = posY
        #defines the initial state of the switch
        self.state = state
        #defines the name of the on position
        self.On = On
        #defines the name of the off position
        self.Off = Off
        #defines the width of the switch
        self.sizeX = sizeX
        #defines the height of the switch
        self.sizeY = sizeY
        #defines the boolean value of it's clicked state last frame
        self.wasClicked = False

    ##method to display the switch
    #self references the variable that are unique to each individual switch
    def displaySwitch(self):
        #draws the rectangle that will be displayed behind the switch
        pygame.draw.rect(display, grey3, (self.posX-2, self.posY-2, self.sizeX, self.sizeY))
        #asks if the state is false
        if not self.state:
            #since the switch is off draw the rectangle in the default colour and the off position
            pygame.draw.rect(display, self.colour, (self.posX, self.posY, (self.sizeX/2)-4, (self.sizeY)-4))
            #defines the text to be the name of the off position
            SwitchText1 = ButtonFont.render((self.Off), 1, grey1)
            #displays the text of the off position
            display.blit(SwitchText1, (self.posX+(9*len(self.name)), self.posY-25))
        else:
            #since the switch is on draw the retangle as white and in the on position
            pygame.draw.rect(display, white, (self.posX+self.sizeX/2, self.posY, (self.sizeX/2)-4, (self.sizeY)-4))
            #defines the text to be the name of the on position
            SwitchText1 = ButtonFont.render((self.On), 1, grey1)
            #displays the text of the on position
            display.blit(SwitchText1, (self.posX+(9*len(self.name)), self.posY-25))
        #creates the text for the name of the switch
        SwitchText2 = ButtonFont.render((self.name + ":"), 1, grey1)
        #displays the name text
        display.blit(SwitchText2, (self.posX, self.posY-25))

#creates an initial value for the number of metric meters in every pixel on the simulation
metersPerPixel = 500000
#creates an initial value for the number of simulation seconds that pass every frame 10000 simulation seconds every second is (10000/fps) simulation seconds every frame
Timeinterval = 10000/FPS
#defines the x position of the center of the universe created. This is the point around which you will be able to zoom in the x axis
centerX = width/3
#defines the y position of the center of the universe created. This is the point around which you will be able to zoom in the y axis
centerY = height/3

###the class that defines the objects in the simulation - these are the planets that the user will put into the simulation
class Object:
    ##initialisation method
    #self allows each object to have it's own unique variables. The other parameters are defined later when the objects are added in by the user
    def __init__(self, ID, colour, radius, posX, posY, velX, velY, density):
        #defines the ID of each object - used to tell the difference between objects
        self.ID = ID
        #defines the colour of the object
        self.colour = colour
        #defines the radius of the circle that will be drawn onto the screen
        self.drawRadius = radius
        #defines the x position that the circle will be drawn onto
        self.drawPosX = posX
        #defines the y position that the circle will be drawn onto
        self.drawPosY = posY
        #defines the x velocity that the object will have
        self.velX = velX
        #defines the y velocity that the object will have
        self.velY = velY
        #defines the net force in the x direction. The force acting on the object will change as it interacts by gravity with other objects
        self.netX = 0
        #defines the net force in the y direction. The force acting on the object will change as it interacts by gravity with other objects
        self.netY = 0
        #defines the density of the object (this is mass/volume)
        self.density = density
        #defines the x position in meters used for calculations later
        self.metricPosX = metersPerPixel*self.drawPosX
        #defines the y position in meters used for calculations later
        self.metricPosY = metersPerPixel*self.drawPosY
        #defines the radius of the object in meters used for calculations later
        self.metricRadius = metersPerPixel*self.drawRadius
        #definest the mass of the object in kilograms used for calculations later
        self.metricMass = math.pi*(4/3)*(self.metricRadius**3)*self.density
        #sets the array holding previous points the object has been to be empty
        self.trail = []
        #sets the net force to 0
        self.netForce = 0

    ##display method
    #self references all variables unique to each object
    def displayObject(self):
        #draws a circe based on the draw radius, draw positions and colour
        pygame.draw.circle(display, self.colour, (round(self.drawPosX+centerX), round(self.drawPosY+centerY)), round(self.drawRadius))

    ##method to display the ID of teh object on the object
    def showID(self):
        #creates the text of the ID that will be displayed on top of the objects
        ObjectText = ObjectFont.render(str(self.ID), 1, red)
        #displays the ID in the position of the object
        display.blit(ObjectText, (self.drawPosX-5+centerX, self.drawPosY-5+centerY))

    ##method that updates the units that were defined earlier
    def updateUnits(self):
        #changes the metric radius based on the mass and density - this changes when objects collide 
        self.metricRadius = ((3*self.metricMass)/(4*math.pi*self.density))**(1/3)
        #updates the draw radius to match the metric radius
        self.drawRadius = self.metricRadius/metersPerPixel
        #updates the x draw position to match the metric x position - this changes when objects have a non-zero x velocity
        self.drawPosX = self.metricPosX/metersPerPixel
        #updates the y draw position to match the metric y position - this changes when objects have a non-zero y velocity
        self.drawPosY = self.metricPosY/metersPerPixel

    ##method that 
    def changePos(self):
        #changes the metric X position based on it's x velocity and the time between frames
        self.metricPosX += (self.velX*Timeinterval)
        #changes the metric y position based on it's y velocity and the time between frames
        self.metricPosY += (self.velY*Timeinterval)
        #updates the x draw position to match the metric x position - this changes when objects have a non-zero x velocity
        self.drawPosX = self.metricPosX/metersPerPixel
        #updates the y draw position to match the metric y position - this changes when objects have a non-zero y velocity
        self.drawPosY = self.metricPosY/metersPerPixel




###function to call for exiting the program
#takes the parameter exit (true is if they do want to exit, false is if they don't)
def exiting(exit):
    #asks if the user wants to exit
    if exit:
        #closes pygame
        pygame.quit()
        #closes python
        sys.exit()

###GUIs - these are being defined by creating objects with the classes made earlier

##panels
#tool panel - will have switches and a colour chooser for customising the simulation
pTools = Panel("Tools", grey2, 5, 34, int(width/8), int(height/2))
#colour wheel - not a panel but is an image that sits on top of the tool bar panel
colourWheel = pygame.transform.scale(colourWheel, (int(pTools.sizeX*(3/4)),int(pTools.sizeX*(3/4))))
#lightness - not a panel but is an image that sits on top of the tool bar panel
lightness = pygame.transform.scale(lightness, ((int(pTools.sizeX/5)-10, int(pTools.sizeX*(4/5)))))
#information panel - will have general information about the current simulation
pInfo = Panel("Info", grey2, 5, int(pTools.posY+pTools.sizeY+2), int(width/8), int(height/2)-46)
#simulation panel - will contain the objects and is the main visual part of the whole program
pSimulation = Panel("Simulation", black, int(pTools.posX+pTools.sizeX+2), 34, int(width/2), 4*height/5)
#time panel - switches and buttons to pause/play, speed up, slow down and reset the simulation
pTime = Panel("Time", grey2, int(pTools.posX+pTools.sizeX+2), int(pSimulation.posY+pSimulation.sizeY+2), int(width/2), (height-int(pSimulation.posY+pSimulation.sizeY+12)))

##these define the boundary that the graph panel will be in
topGraph = 34
leftGraph = int(((5*width)/8)+9)
rightGraph = int(((5*width)/8)+9)+int(((3*width)/8)-12)
bottomGraph = int(height/2+34)

#graph panel - will contain the graphing feature
pGraph = Panel("Graph 1", white, leftGraph, topGraph, rightGraph-leftGraph, bottomGraph-topGraph)
#exit panel - the panel that only shows up when the user wants to exit the simulation -also contains simulation saving features
pExit = Panel("Exit", grey4, int((width/2)-300), int((height/2)-100), 600, 300)
#learn panel - shows the equations of motion, gravity and keplers second law
pLearn = Panel("Learn", grey2, int(((5*width)/8)+9), (height/2)+36, int(((3*width)/8)-12), (height/2)-46)
#gravitation formula - not a panel but is one of the images that will be displayed on the learn panel
gravitationFormula = pygame.transform.scale(gravitationFormula, (int(((3*width)/8)-112), int((height/2)-146)))
#suvat formula = not a panel but is one of the images that will be displayed on the learn panel
suvatFormula = pygame.transform.scale(suvatFormula, (int(((3*width)/8)-112), int((height/2)-146)))
#instruction panel - the panel that will contain instructions on how to use the program
pInstructions = Panel("instructions", white, int(pTools.posX+pTools.sizeX+2), 34, int(width/2), 4*height/5)
#the panel that will appear when the user wants to change the x axis of the graph
pChangeX = Panel("Change x axis", grey2, leftGraph, topGraph, rightGraph-leftGraph, bottomGraph-topGraph)
#the panel that will appear when the user wants to change the Y axis of the graph
pChangeY = Panel("Change y axis", grey2, leftGraph, topGraph, rightGraph-leftGraph, bottomGraph-topGraph)

##window and top bar buttons
#the button for exiting the program
bExit = Button("x", red, width-52, 1, 50, 30)
#the button th minimise the program
bMin = Button("_", grey1, width-103, 1, 50, 30)
#the button to enter a new simulation
bEnter = Button("Enter", grey2, (width/2)-150, (height/2)-40, 100, 80)
#the button to open a saved simulaton
bOpen = Button("Open", grey2, width/2, (height/2)-40, 100, 80)
#the button to go back to main menu
bMainMenu = Button("Exit", grey2, 36, 3, 50, 26)
#the button to display the first set of instructions
bInstructions = Button("Instructions", grey2, 100, 3, 120, 26)
#the button to display the second set of instructions
bInstructions2 = Button("more Instructions", grey2, 235, 3, 170, 26)
#the button that resets the simulation

##time buttons
bReset = Button("reset", red, pTime.posX+95, pTime.posY+48, 86, 44)
#the button that speeds up the flow of time
bIncrease = Button(">>+", cyan, bReset.posX+bReset.sizeX+5, pTime.posY+48, 86, 44)
#the button that slows down the flow of time
bDecrease = Button(">>-", cyan, bIncrease.posX+bIncrease.sizeX+5, pTime.posY+48, 86, 44)
#the button that exits and saves the current simulation

##exiting buttons
bSave = Button("save", green, int((width/2)-250), int((height/2)+100), 100, 50)
#the button that exits and does not save the current simulation
bDontSave = Button("Dont save", red, int((width/2)-50), int((height/2)+100), 100, 50)
#the button that cancles the exit of the simulation
bCancel = Button("Cancel", grey3, int((width/2)+150), int((height/2)+100), 100, 50)

##learn panel buttons
#the button that displays the formula for gravity in the learn panel
bGravity = Button("Gravity", green2, pLearn.posX+110, pLearn.posY+18, 100, 30)
#the button that displays the formulas of motion in the learn panel
bSuvat = Button("Motion", green2, pLearn.posX+5, pLearn.posY+18, 100, 30)
#the button that starts the demonstration of keplers second law
bKepler = Button("Keplers 2nd law", green2, pLearn.posX+215, pLearn.posY+18, 160, 30)
#the button that lets you change the x axis of the graph

##graphing buttons
bX = Button("x", green, pGraph.posX+(pGraph.sizeX/2)-20, pGraph.posY+pGraph.sizeY-25, 40, 20)
#the button that lets you change the y axis of the graph
bY = Button("y", green, pGraph.posX+5, pGraph.posY+(pGraph.sizeY/2)-20, 20, 40)
#VX - not a button but is the text that will be displayed if any of the axes are the x velocity of an object
VX = "Velocity X (m/s)"
#the button that changes an axis to be the x velocity of an object
bXvel = Button(VX, yellow, pGraph.posX+30, pGraph.posY+30, 200, 50)
#VX - not a button but is the text that will be displayed if any of the axes are the y velocity of an object
VY = "Velocity Y (m/s)"
#the button that changes an axis to be the y velocity of an object
bYvel = Button(VY, yellow, pGraph.posX+30, pGraph.posY+90, 200, 50)
#T - not a button but is the text that will be displayed if any of the axes are Time
T = "Time (s)"
#the button that changes an axis to time
bTime = Button(T, yellow, pGraph.posX+30, pGraph.posY+150, 200, 50)
#F - not a button but is the text that will be disp[layed if any of the axes are force
F = "Net Force (10^24 N)"
#the button that changes an axis to net force
bForce = Button(F, yellow, pGraph.posX+30, pGraph.posY+210, 200, 50)

#the button that starts the graphing
bStartGraph = Button("Start Graphing!", red, pGraph.posX+(pGraph.sizeX/2+120), pGraph.posY+50, 160, 30)
#the button that stops the graphing
bStopGraph = Button("Stop Graphing!", red, pGraph.posX+80, pGraph.posY+10, 160, 30)

##switches
#switch to pause and play
sPausePlay = Switch("||/>", green, pTime.posX+5, pTime.posY+50, False, "||", " >", 86, 44)
#switch to shoiw the IDs of the objects
sShowID = Switch("Show ID", yellow,  pTools.posX+5, pTools.posY+50, False, "on", "off")
#switch to show the velocities of the objects
sShowVel = Switch("Show velocity", yellow, pTools.posX+5, pTools.posY+100, False, "on", "off")
#switch to show the net forces acting on the objects
sShowFor = Switch("Show net Force", yellow, pTools.posX+5, pTools.posY+150, False, "on", "off")
#switch to show the previous path of the objects
sShowTrail = Switch("Show trail", yellow, pTools.posX+5, pTools.posY+200, False, "on", "off")
#the array holding the switches
switches = [sPausePlay, sShowID, sShowVel, sShowFor, sShowTrail]





##assembling the Window GUI
def WindowGUI(clicked, X, Y, clickedLastFrame):
    ##the rectangle and 3 lines draws the outline of the program that will have the window buttons on
    pygame.draw.rect(display, black, (0,0,width,32))
    pygame.draw.line(display, black, (0,0), (0, height), 2)
    pygame.draw.line(display, black, (width,0), (width, height), 2)
    pygame.draw.line(display, black, (0,height), (width, height), 18)
    #displays the logo in the top right of the screen
    pygame.Surface.blit(display, icon, (0,0))
    #asks if the mouse button was not clicked in the last fram
    if not clickedLastFrame:
        #runs the method fo detectinmg button clicks on the exit button
        colour1, bExitClicked = bExit.buttonClicked(clicked, X, Y)
        #runs the method fo detectinng button clicks on the minimise button
        colour2, bMinClicked = bMin.buttonClicked(clicked, X, Y)
        #runs the method for displaying the minimise button
        bMin.displayButton(colour2)
        #runsa the method for displaying the exit button
        bExit.displayButton(colour1)
        #runs the exit procedure
        exiting(bExitClicked)
        #asks if the minimise button was clicked
        if bMinClicked:
            #minimises the program
            pygame.display.iconify()
    else:
        #displays the button as grey
        bMin.displayButton(grey1)
        #displays the button as red
        bExit.displayButton(red)

###function for drawing the background of the display
def background():
    ##leaves a space where the simulation will be displayed so that the objects that move past the edge will go under the background
    pygame.draw.rect(display, grey1, (0, 0, width, pSimulation.posY))
    pygame.draw.rect(display, grey1, (0, 0, pSimulation.posX, height))
    pygame.draw.rect(display, grey1, (0, pSimulation.posY+pSimulation.sizeY, width, height))
    pygame.draw.rect(display, grey1, (pSimulation.posX+pSimulation.sizeX, 0, width, height))

#variable that tells us if we are in the main menu
inMainMenu = True
#variable that tells us if the left mouse button is clicked
clicked = False

###program loop
while True:
    ##getting ready for main menu

    #array - holds all of the planets inside of it
    objects = []
    #variable - tells us if the simulation is pasued
    paused = False

    #variable - the mouse button state in the last frame
    ClickedLastFrame = False
    #variable - the mouse button state in this frame
    clicked = False

    #variable - the number of planets in the simulation
    number = 0
    #variable - the number of frames the decrease flow of time button was held for
    heldD=0
    #variale - the number of frames the increase flow of time button was held for
    heldI=0
    
    #variable - is the user trying to open a file
    opening = False
    #array - contains the file names of the simulations that have been saved
    fileNames = []
    #array - contains the buttons that allow you to select the file to open
    buttons = []
    #array - contains the data of the simulation that the user is trying to open
    data = []
    #updates filenames to include all files in the saves folder
    fileNames = os.listdir("saves\\")
    #removes the file that just holds the number of saves
    fileNames.remove("NumberOfSaves.txt")
    
    #variable - is the scroll bar clicked on
    activated = False

    #the ratio between RGB values for the colour picker
    currentHUE = [0.7, 0.7, 0.7]
    #the multiplier that changes the RGB ratios to an actual colour value
    reduce = 255
    
    ##loop that creates buttons based on the files in filenames
    #enumerate keeps hold of the number of loops in count and the current value from fileNames in filename
    for count, filename in enumerate(fileNames):
        buttons.append(Button(filename, grey2, (width/2)-350, (count*60)+40, 300, 50))

    ### main menu animation loop
    while inMainMenu:
        #fills the background with grey
        display.fill(grey1)
        #gets x coordinate of mouse
        X = list(pygame.mouse.get_pos())[0]
        #gets y coordinate of mouse
        Y = list(pygame.mouse.get_pos())[1]
        ##event handling
        #iterates through all possible events
        for event in pygame.event.get():
            #asks if the event is quit
            if event.type == quit:
                #quits the program
                exiting(True)
            #asks if event is a key press
            if event.type == pygame.KEYDOWN:
                #asks if the key is escape
                if event.key == pygame.K_ESCAPE:
                    #quits the program
                    exiting(True)
        #updates clicked to be the left mouse button state
        clicked = list(pygame.mouse.get_pressed())[0]
        #displays the boarder of the window
        WindowGUI(clicked, X, Y, ClickedLastFrame)

        ##open or enter?
        #asks if the use does not want to open a saved simulation
        if not opening:
            #runs method to detect button clicks on enter button
            colour3, bEnterClicked = bEnter.buttonClicked(clicked, X, Y)
            #runs method for displaying the enter button
            bEnter.displayButton(colour3)
            #asks if the enter button is clicked
            if bEnterClicked:
                #changes inMainMenu to false since the user has clicked to enter the simulation
                inMainMenu = False 
                
            #runs method to detect button clicks on open button 
            colour11, bOpenClicked = bOpen.buttonClicked(clicked, X, Y)
            #runs method to display button on open button
            bOpen.displayButton(colour11)
            #asks if the open button is clicked
            if bOpenClicked:
                #changes opening to true so that we can select a file to open
                opening = True
        else:
            #iterates through buttons - the array that holds each file's button
            for item in buttons:
                #runs the method that detects button clicks on the current button in the loop
                colour12, buttonClicked = item.buttonClicked(clicked, X, Y)
                #runs the method for displaying the bcurrent button in the loop
                item.displayButton(colour12)
                #asks if that button was clicked
                if buttonClicked:
                    #opens the file corresponding to tha button that was clicked
                    file = open("saves\\" + item.name, "r")
                    #eval turns a string in the format of an array into an actual array and this is assigned to data
                    data = eval(file.readline())
                    #changes inMainMenu to false since the user has clicked to open a simulation
                    inMainMenu = False
        
        # this updates the screen so anything drawn to the display is actually shown on the users monitor 
        pygame.display.update()
        # waits for 1/FPS seconds
        FPSClock.tick(FPS)

    #waits for half a second
    time.sleep(0.5)
    
    ##loop adds the data from the file opened (if there is any) to the objects array
    #iterates through data
    for item in data:
        #asks if the planets ID is greater than the number of objects
        if item[0] > number:
            #sets number equal to the ID of that object +1
            number = item[0]+1
        #calculates the metric radius from the
        metricradius = (((3*item[1])/(4*math.pi*item[6]))**(1/3))
        #calculates the radius of which to draw the circle 
        Radius = metricradius/metersPerPixel
        #adds the planet to objects
        objects.append(Object(item[0], grey1, Radius, (item[2]/metersPerPixel), (item[3]/metersPerPixel), item[4], item[5], item[6]))
    
    ##setting up simulation

    #the density of any new object that is added in
    newDensity = 5500
    #the radius of any new object that is added in
    newRadius = 10
    #currently zooming is set to false
    zoom = False
    #currently changing density is set to false
    changeDensity = False
    #default graph x variable is set to [T, -1]. T is Time and -1 indicates that the varable chosen is not object specific
    VarX = [T, -1]
    #default graph y variable is set to [VX 0]. VX is X velocity and 0 indicates that the vaiable chosen will be based on object 0
    VarY = [VX, 0]
    #currently changing X axis is set to False
    changeXaxis = False
    #current;y chaning Y axis is set to False
    changeYaxis = False
    #Started the graph is set to False
    started = False
    #the metric X coordinates for the graph will be stored in this array
    XMetricCoords = []
    #the metric Y coordinates for the graph will be stored in this array
    YMetricCoords = []     
    #currently running keplers second law demo is set to False
    runKepler = False
    #graph is stopping is set to False
    stop = False
    #Objects required for the x axis of the graph is set to false
    objectXExists=False
    #Objects required for the Y axis of the graph is set to false
    objectYExists=False

    ###running the simulation
    while not inMainMenu:
        ##inputs
        #gets x coordinate of mouse
        X = list(pygame.mouse.get_pos())[0]#gets x coordinate of mouse
        #gets Y coordinate of mouse
        Y = list(pygame.mouse.get_pos())[1]#gets y coordinate of mouse
        ##event handling
        #iterates through all possible events
        for event in pygame.event.get():
            #asks if the event is a key press
            if event.type == pygame.KEYDOWN:
                #asks if the key pressed is escape
                if event.key == pygame.K_ESCAPE:
                    #quits the program
                    exiting(True)
                #asks ifthe key that was pressed is the space bar
                if event.key == pygame.K_SPACE:
                    #toggles the pause variable
                    paused = not paused
                    #toggles the pause switch
                    sPausePlay.state = not sPausePlay.state
            #asks if the event is a mouse button action
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                #asks if mouse wheel is scrolling down
                if event.button == 5:
                    #asks if we are not currently changing the density
                    if not changeDensity:
                        #asks if we are currently zooming
                        if zoom:
                            #reduces metersPerPixel by a factor of 1.05
                            metersPerPixel /= 1.05
                        #asks if newRadius is less than or equal to 150 so that the input circle is not too big
                        if newRadius <= 150:
                            #increases newRadius by a factor of 1.05
                            newRadius *= 1.05
                    else:
                        #increases new density by a factor of 1.05
                        newDensity *= 1.05
                #asks if mouse wheel is scrolling up
                if event.button == 4:
                    #asks if we are not currently changing density
                    if not changeDensity:
                        #asks if we are currently zooming
                        if zoom:
                            #increases metersPerPixel by a factor of 1.05
                            metersPerPixel *= 1.05
                        #asks if newRadius is less than 3 so the input circle is not too small
                        if newRadius >= 3:
                            #reduces newRadius by a factor of 1.05
                            newRadius /= 1.05
                    else:
                        #reduces newDensity by a factor of 1.05
                        newDensity /= 1.05
            
            #asks if the event is quit
            elif event.type == quit:
                #exits the program
                exiting(True)

        #makes a list of all keys that are presses
        keys = pygame.key.get_pressed()
        #asks if the left shift key is pressed and the z key is pressed
        if keys[pygame.K_LSHIFT] and keys[pygame.K_z]:
            #sets zoom to true
            zoom = True
            #sets run kepler to false
            runKepler = False
            #sets show trail to false
            sShowTrail.state = False

            #sets change density to false
            changeDensity = False
            #sets the center x to the mouse x position
            centerX = X
            #sets the center y to the mouse y position
            centerY = Y
        #asks if the left shift key is pressed and the d key is pressed
        elif  keys[pygame.K_LSHIFT] and keys[pygame.K_d]:
            #sets change density to True
            changeDensity = True
            #sets zoom to False
            zoom = False
        else:
            #sets zoom to false
            zoom = False
            #sets change density to False
            changeDensity = False
        #updates clicked to be the left mouse button state
        clicked = list(pygame.mouse.get_pressed())[0]

        #runs the method that displays the simulation panel
        pSimulation.displayPanel()

        ##next 4 lines defines the reigon that objects can be added into
        leftEdge = pSimulation.posX
        topEdge = pSimulation.posY
        rightEdge = pSimulation.posX+pSimulation.sizeX
        lowerEdge = pSimulation.posY+pSimulation.sizeY

        #asks if the simulation is not paused
        if not paused:
            #iterates through objects - the list of planets
            for self in objects:
                self.netForce = 0
                #iterates through objects - a nested loop
                for other in objects:
                    #asks if other object does not equal self object
                    if other != self:
                        ##calculating measures of the objects motion
                        #calculating the momentum in the x direction - used for collisions later
                        momentumX = self.velX*self.metricMass + other.velX*other.metricMass
                        #calculating the momentum in the y direction - used for collisions later
                        momentumY = self.velY*self.metricMass + other.velY*other.metricMass
                        
                        #x is the distance in the x direction between the two objects
                        x = self.metricPosX-other.metricPosX
                        #y is the distance in the y direction between the two objects
                        y = self.metricPosY-other.metricPosY
                        #here I use pythagoras theorem to find the magnitude of the distance between the centers of the two objects
                        distance = math.sqrt((x**2)+(y**2))

                        #This equation finds the force acting on self object through gravity
                        #although it is equal to the force acting on other object, it is calculated when the other object is calculating it's forces when other becomes self (in the outer for loop)
                        force = 6.67*(10**(-11))*(self.metricMass*other.metricMass)/(distance**2)
                        #adds the force to the net force attribute
                        self.netForce += force
                        #calculating acceleration of the object from the force and the mass of the object
                        acc = force/self.metricMass

                        #calculating the force in the X direction - used for showing the force on the simulation later
                        self.netX = (x/distance * force)/(10**22)
                        #we divide by 10 to the power of 22 because the number wouyld be so big that it would crash if we tried to draw a line of that size - also it wouldn't fit on the screen
                        #calculating the force in the X direction - used for showing the force on the simulation later
                        self.netY = (y/distance * force)/(10**22)

                        #calculating the x velocity after the acceleration has taken place
                        self.velX -= acc * (x/distance) * Timeinterval
                        #calculating the Y velocity after the acceleration has taken place
                        self.velY -= acc * (y/distance) * Timeinterval

                        ##detecting collisions
                        #asks if the distance between the two objects is les than the sum of the radii of the two objects - if they are touching or closer
                        if distance <= (self.metricRadius + other.metricRadius):
                            ##calculating the density of the object after the collision
                            #the total mass is calculated
                            totalMass = self.metricMass+other.metricMass
                            #the percentage of the total that self object is, is calculated here
                            selfPercent = self.metricMass/totalMass
                            #the percentage of the total that other object is, is calculated here
                            otherPercent = other.metricMass/totalMass
                            #the density of the combined object is calculated here
                            combinedDensity = ((selfPercent*self.density)+(otherPercent*other.density))

                            #asks if the self radius is greater than the other radius
                            if self.metricRadius > other.metricRadius:
                                #adds other's mass onto self
                                self.metricMass += other.metricMass
                                try:
                                    #removes other from objects
                                    objects.remove(other)
                                except:
                                    pass
                                #assigns the combined density to self
                                self.density = combinedDensity
                                #calculates the x velocity of the object after a collision
                                #since momentum of two objects in a closed system remains constant, we use the momentum that was calculated earlier
                                self.velX = momentumX/self.metricMass
                                #calculates the y velocity of the object after a collision 
                                self.velY = momentumY/self.metricMass

                            else:
                                #adds self's mass onto other
                                other.metricMass += self.metricMass
                                try:
                                    #removes self from the list of objects
                                    objects.remove(self)
                                except:
                                    pass
                                #assigns the combined density to other
                                other.density = combinedDensity
                                #calculates the x velocity of the object after a collision
                                #since momentum of two objects in a closed system remains constant, we use the momentum that was calculated earlier
                                other.velX = momentumX/other.metricMass
                                #calculates the y velocity of the object after a collision
                                other.velY = momentumY/other.metricMass

        #calculating new positions of the objects
        #iterates through objects
        for self in objects:
            #asks if the simulation is paused
            if not paused:
                #as it is paused, don't move any objects
                self.changePos()
            #update any units that need to be updated
            self.updateUnits()
            #asks if we are not currently zooming
            if not zoom:
                #asks if the switch for showing the trail of each object is on
                if sShowTrail.state:
                    #adds the position of each object to the
                    self.trail.append((self.drawPosX+centerX, self.drawPosY+centerY))
                    #asks if the length of the trail is greater than 1000
                    if len(self.trail)>1000:
                        #deletes the point at the oldest end of the trail
                        del self.trail[0]
                    #asks if the length of the trail is greater than 1
                    if len(self.trail)>1:
                        #draws the trail
                        pygame.draw.lines(display, self.colour, False, self.trail, 2)
            else:
                #resets the trail
                self.trail = []

            #display the objects
            self.displayObject()
            #asks if the switch for showing the velocity of the objects is on
            if sShowVel.state:
                #draws a line from self object to a point in space - the line will point in the direction of the velocity and the length is always in proportion to the velocity of the object
                pygame.draw.line(display, magenta, (int(self.drawPosX+centerX), int(self.drawPosY+centerY)), (int(self.drawPosX+(self.velX/100)+centerX), int(self.drawPosY+(self.velY/100)+centerY)))
            #asks if the switch for showing the net force acting on each object is on
            if sShowFor.state:
                #draws a line from self object to a point in space - the line will point in the direction of the force and the length is always in proportion to the force acting on the object
                pygame.draw.line(display, cyan, (self.drawPosX+centerX, self.drawPosY+centerY), ((int(self.drawPosX-self.netX)+centerX), int(self.drawPosY-self.netY)+centerY), 2)
            #asks if the switch for showing the ID of each object is on
            if sShowID.state:
                #displays the ID of the object
                self.showID()
            #sets netX to 0
            self.netX = 0
            #sets netY to 0
            self.netY = 0

        ##this section is used for adding objects into the simulation
        #asks if the cursor is within the simulation boundary
        if (X-newRadius>leftEdge) and (X+newRadius<rightEdge) and (Y-newRadius>topEdge) and (Y+newRadius<lowerEdge):
            #draws a blue circle around the cursor - used to indicate the size and position of the object to be added in next
            pygame.draw.circle(display, blue, (X,Y), int(newRadius), 2)
            #asks if the mouse is clicked in this frame but also not clicked in the last frame
            if clicked and not ClickedLastFrame:
                #sets clicked last frame to true so that when next frame comes around we know that the mouse has been held
                ClickedLastFrame = True
                #sets initialY equal to the Y position of the mouse so we know where the planet is to be placed
                initialY = Y
                #sets initialX equal to the x position of the mouse
                initialX = X
            #asks if the mouse is clicking in this frame and in the last frame
            elif clicked and ClickedLastFrame:
                #sets clicked last frame to true so that when next frame comes around we know that the mouse has been held
                ClickedLastFrame = True
                #draws a circle where it will be positioned
                pygame.draw.circle(display, currentcolour, (initialX, initialY), int(newRadius))
                #draws a line from the mouse to the initial position to indicate the speed and direction of the object
                #the direction is inverted so that the mouse and line don't cover where the planet will be travelling 
                pygame.draw.line(display, green, (initialX, initialY), (X, Y), 3)
                #draws a yellow circle around the mouse
                pygame.draw.circle(display, yellow, (X, Y), int(newRadius), 2)
            #asks if the mouse has just been released
            elif not clicked and ClickedLastFrame:
                #sets clicked last frame to false
                ClickedLastFrame = False
                #adds the planet into the simulation by appending it to the list of planets
                objects.append(Object(number, currentcolour, int(newRadius), initialX-centerX, initialY-centerY, (initialX-X)*100, (initialY-Y)*100, newDensity))
                #increments the number of objects by 1
                number += 1
            #asks if not recent clicks have been made
            elif not clicked and not ClickedLastFrame:
                #sets clicked last frame to false
                ClickedLastFrame = False

        #asks if we want to run the keplers second law demo 
        if runKepler:
            try:
                #draws the area set out by the point list for the blue area
                pygame.draw.polygon(display, blue, pointList1)
            except:
                pass
            try:
                #draws the area set out by the point list for the green area
                pygame.draw.polygon(display, green, pointList2)
            except:
                pass
        
        #draws the background to the non-simulation panels
        #as stated before it is in front of the simulation panel so planets pass underneath it
        background()

        #displays the tool panel
        pTools.displayPanel()   
        #displays the information panel
        pInfo.displayPanel()
        #displays the time panel
        pTime.displayPanel()
        #displays the graph panel
        pGraph.displayPanel()
        #displays the learn panel
        pLearn.displayPanel()



        ### Graphing
        
        ##drawing the axes

        #defines the origin position of the graph
        originX = pGraph.posX+50
        originY = pGraph.posY+pGraph.sizeY-50

        #draws X axis
        pygame.draw.line(display, black, (originX, pGraph.posY+50), (originX, originY), 2)

        #draws button X
        colour17, bXClicked = bX.buttonClicked(clicked, X, Y)
        bX.displayButton(colour17)

        #draws Y axis
        pygame.draw.line(display, black, (originX, originY), (pGraph.posX+pGraph.sizeX-50, originY), 2)

        #draws button Y
        colour18, bYClicked = bY.buttonClicked(clicked, X, Y)
        bY.displayButton(colour18)

        ##this section shows what the x and y axes are representing
        #this is used so that measures that dont belong to an object get the right label
        if VarX[0] != "Time (s)":
            #text telling the user what variables are being measured on the X axis
            Xaxis = PanelFont.render("x axis = " + VarX[0] + " of object " + str(VarX[1]), 1, black)
            #diaplaying that text
            display.blit(Xaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+5))

        else:
            #text telling the user what variables are being measured on the X axis
            Xaxis = PanelFont.render("x axis = " + VarX[0], 1, black)
            #text telling the user what variables are being measured on the X axis
            display.blit(Xaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+5))

        if VarY[0] != "Time (s)":
            #text telling the user what variables are being measured on the Y axis
            Yaxis = PanelFont.render("y axis = " + VarY[0] + " of object " + str(VarY[1]), 1, black)
            #text telling the user what variables are being measured on the Y axis
            display.blit(Yaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+20))

        else:
            #text telling the user what variables are being measured on the Y axis
            Yaxis = PanelFont.render("y axis = " + VarY[0], 1, black)
            #text telling the user what variables are being measured on the Y axis
            display.blit(Yaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+20))

        #asks if the change x axis button is clicked
        if bXClicked:
            
            changeXaxis = True
        #asks if the change Y axis button is clicked
        if bYClicked:
            #sets the changeYaxis variable to true
            changeYaxis = True

        #creates an empty array used later for storing the buttons with the IDs of the objects
        IDButtons = []
        
        #adjusts the position of the buttons 
        adjust = 30
        for self in objects:
            IDButtons.append(Button(str(self.ID), orange,  pGraph.posX+250, pGraph.posY+adjust, 200, 20))
            adjust += 30

        size = (len(objects)*(50))+30

        #does the user want to change the Y axis and is the graph not started
        if changeXaxis and not started:
            #display the change x panel
            pChangeX.displayPanel()

            #detect mouse click on the X velocity button
            colour19, bXvelClicked = bXvel.buttonClicked(clicked, X, Y)
            #display button
            bXvel.displayButton(colour19)

            #detect mouse click on the Y velocity button
            colour20, bYvelClicked = bYvel.buttonClicked(clicked, X, Y)
            #display button
            bYvel.displayButton(colour20)

            #detect mouse click on the time button
            colour21, bTimeClicked = bTime.buttonClicked(clicked, X, Y)
            #display button
            bTime.displayButton(colour21)

            #detect mouse click on the force button
            colour26, bForceClicked = bForce.buttonClicked(clicked, X, Y)
            #display button
            bForce.displayButton(colour26)

            #iterate through the buttons
            for n in IDButtons:
                #detect mouse click on n button
                colour23, IDButtonClicked = n.buttonClicked(clicked, X, Y)
                #is variable on x axis not time
                if(VarX[0] != T):
                    #is the button within the graph panel
                    if n.posY+n.sizeY < pGraph.posY+pGraph.sizeY:
                        #display the button
                        n.displayButton(colour23)
                    #is the button clicked
                    if IDButtonClicked:
                        #set the object for the x axis to the name of the button
                        VarX[1] = int(n.name)
                        #stop changing the x axis
                        changeXaxis = False
                else:
                    #is the button within the graph panel
                    if n.posY+n.sizeY< pGraph.posY+pGraph.sizeY:
                        #display the button but blanked out
                        n.displayButton(grey4)

            #is the button for the X velocity clicked
            if bXvelClicked:
                #set the type of variable for the x axis to the x velocity
                VarX[0] = VX
                #is the object of the x axis equal to -1
                if VarX[1] == -1:
                    #set the object of the x axis to 0
                    VarX[1] = 0
                #stop changing the x axis
                changeXaxis = False
            
            #is the button for the Y velocity clicked
            if bYvelClicked:
                #set the type of variable for the x axis to the Y velocity
                VarX[0] = VY
                #is the object of the x axis -1
                if VarX[1] == -1:
                    #set the object of the x axis to 0
                    VarX[1] = 0
                #stop chaning the x axis
                changeXaxis = False

            #is the button for time clicked
            if bTimeClicked:
                #set the x axis variable to time
                VarX[0] = T
                #set the x axis object to -1
                VarX[1] = -1
                #stop changing the x axis
                changeXaxis = False

            #is the button for Force clicked
            if bForceClicked:
                #set the x axis variable to net force
                VarX[0] = F
                #is the object of the x axis -1
                if VarX[1] == -1:
                    #set object of the x axis to 0
                    VarX[1] = 0
                changeXaxis = False


        #does the user want to change the Y axis and is the graph not started
        if changeYaxis and not started:
            #display the change y axis panel
            pChangeY.displayPanel()

            #detect click on X velocity button
            colour19, bXvelClicked = bXvel.buttonClicked(clicked, X, Y)
            #display the button
            bXvel.displayButton(colour19)

            #detect click on Y velocity button
            colour20, bYvelClicked = bYvel.buttonClicked(clicked, X, Y)
            bYvel.displayButton(colour20)

            #detect click on time button
            colour21, bTimeClicked = bTime.buttonClicked(clicked, X, Y)
            bTime.displayButton(colour21)

            #detect click on force button
            colour26, bForceClicked = bForce.buttonClicked(clicked, X, Y)
            bForce.displayButton(colour26)

            #iterate through the buttons
            for n in IDButtons:
                #detect n button being clicked
                colour23, IDButtonClicked = n.buttonClicked(clicked, X, Y)
                #is the variable for the y axis not time
                if(VarY[0] != T):
                    #is n button within the graph panel
                    if n.posY+n.sizeY< pGraph.posY+pGraph.sizeY:
                        #display the button
                        n.displayButton(colour23)
                    #is the button clicked
                    if IDButtonClicked:
                        #set the object for the y axis equal to the name of the button
                        VarY[1] = int(n.name)
                        #stop changing the y axis
                        changeYaxis = False
                else:
                    #is the button within the graph panel
                    if n.posY+n.sizeY< pGraph.posY+pGraph.sizeY:
                        #display the button but blanked out
                        n.displayButton(grey4)

            #is the x velocity button clicked
            if bXvelClicked:
                #set the variable for y axis to x velocity
                VarY[0] = VX
                #is the object for the y axis -1
                if VarY[1] == -1:
                    #set object for y axis to 0
                    VarY[1] = 0
                #stop changing y axis
                changeYaxis = False

            #is the Y velocity button clicked
            if bYvelClicked:
                #set variable for y axis to Y velocity
                VarY[0] = VY
                #is the object for the y axis -1
                if VarY[1] == -1:
                    #set object for y axis to 0
                    VarY[1] = 0
                #stop changing Y axis
                changeYaxis = False

            #is the time button clicked
            if bTimeClicked:
                #set variable for y axis to time
                VarY[0] = T
                #set object for y axis to -1
                VarY[1] = -1
                #stop changing Y axis
                changeYaxis = False

            #is the button for Force clicked
            if bForceClicked:
                #set the y axis variable to net force
                VarY[0] = F
                #is the object of the y axis -1
                if VarY[1] == -1:
                    #set object of the y axis to 0
                    VarY[1] = 0
                changeYaxis = False

        #detects the start graphing button being clicked
        colour22, bStartGraphClicked = bStartGraph.buttonClicked(clicked, X, Y)

        #asks has the graphing started
        if started:
            #object for X axis has not been verified so set to false
            objectXExists=False
            #object for Y axis has not been verified so set to false
            objectYExists=False
            #asks is objects not empty
            if objects != []:


                ##binary search - the IDs of the objects will be in order so binary search works - it is also more efficient than linear search
                #variable that tells us if the search is finished
                found = False
                #if the object we are looking for exists it will always remain in the nextSearch list
                nextSearch = objects
                #loops untill the object is found(or untill it is found that it doesn't exist)
                while not found:
                    #asks if nextSearch has more than 1 object
                    if len(nextSearch) > 1:
                        #finding halfway point in the list
                        index = int(len(nextSearch)/2)
                        if VarX[1] < nextSearch[index].ID:
                            #discards the higher section
                            nextSearch = nextSearch[:index]
                        #asks if the ID we are looking for is greater than the one we are looking at right now
                        elif VarX[1] > nextSearch[index].ID:
                            #discards the lower section
                            nextSearch = nextSearch[index:]
                        else:
                            #object is found
                            found = True
                            #returns the index of the object in the list of objects
                            Xindex = objects.index(nextSearch[index])
                            #object exists
                            objectXExists = True
                    else:
                        #asks if the object we are looking at is the one we are looking for
                        if nextSearch != []:
                            if VarX[1] == nextSearch[0].ID:
                                #object is found
                                found = True
                                #returns the index of the object in the list of objects
                                Xindex = objects.index(nextSearch[0])
                                #object exists
                                objectXExists = True
                            else:
                                #object was not found but we finished the search
                                found = True
                                #object cannot exist
                                objectXExists = False
                        else:
                            #object was not found but we finished the search
                            found = True
                            #object cannot exist
                            objectXExists = False


                #variable that tells us if the search is finished
                found = False
                #if the object we are looking for exists it will always remain in the nextSearch list
                nextSearch = objects
                #loops untill the object is found(or untill it is found that it doesn't exist)
                while not found:
                    #asks if nextSearch has more than 1 object
                    if len(nextSearch) > 1:
                        #finding halfway point in the list
                        index = int(len(nextSearch)/2)
                        if VarY[1] < nextSearch[index].ID:
                            #discards the higher section
                            nextSearch = nextSearch[:index]
                        #asks if the ID we are looking for is greater than the one we are looking at right now
                        elif VarY[1] > nextSearch[index].ID:
                            #discards the lower section
                            nextSearch = nextSearch[index:]
                        else:
                            #object is found
                            found = True
                            #returns the index of the object in the list of objects
                            Yindex = objects.index(nextSearch[index])
                            #object exists
                            objectYExists = True
                    else:
                        #asks if the object we are looking at is the one we are looking for
                        if nextSearch != []:
                            if VarY[1] == nextSearch[0].ID:
                                #object is found
                                found = True
                                #returns the index of the object in the list of objects
                                Yindex = objects.index(nextSearch[0])
                                #object exists
                                objectYExists = True
                            else:
                                #object was not found but we finished the search
                                found = True
                                #object cannot exist
                                objectYExists = False
                        else:
                            #object was not found but we finished the search
                            found = True
                            #object cannot exist
                            objectYExists = False

                #asks if there is an object to be measured for the x axis
                if objectXExists:
                    #asks if the variable is the x velocity of the object
                    if VarX[0] == VX:
                        #adds the x velocity to the list of coordinates 
                        XMetricCoords.append(objects[Xindex].velX)
                    #asks if the variable is the y velocity of the object
                    elif VarX[0] == VY:
                        #adds the y velocity to the list of coordinates
                        XMetricCoords.append(objects[Xindex].velY)
                    #asks if the variable if the net force acting on the object
                    elif VarX[0] == F:
                        ##adds the net force to the list of coordinates
                        XMetricCoords.append(objects[Xindex].netForce/(10**24))
                #asks if there is an object to be measured for the x axis
                if objectYExists:
                    if VarY[0] == VX:
                        YMetricCoords.append(-objects[Yindex].velX)
                    elif VarY[0] == VY:
                        YMetricCoords.append(-objects[Yindex].velY)
                    elif VarY[0] == F:
                        YMetricCoords.append(-objects[Yindex].netForce/(10**24))




                #coordinates to be displayed on the screen
                screenCoords = []
                #x coordinates to be displayed on the screen 
                XGraphCoords = []
                #y coordinates to be displayed on the screen
                YGraphCoords = []
                #is the simulation not paused and is the graph not stopped
                if not paused and not stop:
                    #is the Y axis variable Time
                    if VarY[0] == T:
                        #adds the current time to the list of coordinates
                        YMetricCoords.append(-timeElapsed)
                        #object does exist
                        objectYExists = True
                    #is the X axis variable Time
                    if VarX[0] == T:
                        #adds the current time to the list of coordinates
                        XMetricCoords.append(timeElapsed)
                        #object does exist
                        objectXExists = True

                    #asks if object X does't exist or if object Y doesn't exist
                    if not objectXExists or not objectYExists:
                        #stops the graphing
                        stop = True

                    #minimum x coordinate
                    minMetX = min(XMetricCoords)
                    #text to be displayed at the start of the x axis
                    lowerX = PanelFont.render(str(round(minMetX, 1)), 1, black)
                    #displays the text
                    display.blit(lowerX, (originX, originY+30))
    
                    #maximum x coordinate
                    maxMetX = max(XMetricCoords)
                    #text to be displayed at the end of the x axis
                    upperX = PanelFont.render(str(round(maxMetX, 1)), 1, black)
                    #displays the text
                    display.blit(upperX, (originX+pGraph.sizeX-150, originY+30))

                    #size of the line in the x direction
                    lineSizeX = maxMetX-minMetX

                    #minimum y coordinate
                    minMetY = min(YMetricCoords)
                    #text to be displayed at the start of the y axis
                    upperY = PanelFont.render(str(round(-minMetY, 1)), 1, black)
                    #maximum y coordinate
                    display.blit(upperY, (originX-50, originY-pGraph.sizeY+100))

                    #maximum y coordinate
                    maxMetY = max(YMetricCoords)
                    #text to be displayed at the end of the y axis
                    lowerY = PanelFont.render(str(round(-maxMetY, 1)), 1, black)
                    #displays the text
                    display.blit(lowerY, (originX-50, originY-15))

                    #size of the line in the y direction
                    lineSizeY = maxMetY-minMetY
                    #asks if both objects exists
                    if objectXExists and objectYExists:
                        #sets the width of the graph equal to the width of the panel-100
                        graphWidth = pGraph.sizeX-100
                        #sets the height of the graph equal to the height of the panel-100
                        graphHeight = pGraph.sizeY-100

                        #asks if the line size in the x direction is greater than 0
                        if lineSizeX > 0:
                            #calculates the width ratio
                            WRatio = lineSizeX/graphWidth
                        else:
                            WRatio = 1

                        #asks if the line size in the y direction is greater than 0
                        if lineSizeY > 0:
                            #calculates height ratio
                            HRatio = lineSizeY/graphHeight
                        else:
                            HRatio = 1

                        #loops for the number of coordinates
                        for n in range(len(XMetricCoords)):
                            #converts metric to graph coorodinate and adds the results to the lists of graph coordinates
                            XGraphCoords.append((XMetricCoords[n]/WRatio)-(minMetX/WRatio))
                            YGraphCoords.append((YMetricCoords[n]/HRatio)-(maxMetY/HRatio))

                        #loops for the number of coordinates
                        for n in range(len(XGraphCoords)):
                            #combines the x and y coordinates 
                            screenCoords.append(((XGraphCoords[n]+originX), YGraphCoords[n]+originY))

                        #sets saveCoords equal to the screen coordinates 
                        savedCoords = screenCoords
                try:
                    #draws the line onto the graph
                    pygame.draw.lines(display, blue, False, savedCoords, 2)
                except:
                    pass

                #detects stop graphing button being clicked
                colour24, bStopGraphClicked = bStopGraph.buttonClicked(clicked, X, Y)
                #displays the stop graphing button
                bStopGraph.displayButton(colour24)
                #asks is the stop graphing button clicked
                if bStopGraphClicked:
                    #graphing is not started
                    started = False
                    #graphing is stopped
                    stop = True
                    #the area to be caputured is defined here
                    area = pygame.Rect(pGraph.posX, pGraph.posY, pGraph.sizeX, pGraph.sizeY)
                    #creates a subsurface of the display
                    subSurface = display.subsurface(area)
                    #saves an image called savedGrapg.jpg with the most recent graph in it
                    pygame.image.save(subSurface, "savedGraph.jpg")

                #is the variable for the y axis Time
                if VarY[0] == T:
                    #adds the time interval onto the time elapsed
                    timeElapsed += Timeinterval

                #is the variable for the x axis Time
                if VarX[0] == T:
                    #adds the time interval onto the time elapsed
                    timeElapsed += Timeinterval
        #asks do both objects exist
        elif objectXExists and objectYExists:
            #displays the button to start graphing
            bStartGraph.displayButton(colour22)
            #resets the time elapsed
            timeElapsed = 0
        else:
            #if the objects array is not empty
            if objects != []:
                #iterate through objects
                for self in objects:
                    #is the object equal to the variable for the X axis
                    if self.ID == VarX[1]:
                        #object does exist
                        objectXExists = True
                    #is the object equal to the variable for the Y axis
                    elif self.ID == VarY[1]:
                        #object does exist
                        objectYExists = True
                #asks if not paused and not stopped
                if not paused and not stop:
                    #asks if the Y axis variable is Time
                    if VarY[0] == T:
                        #there isn't an object required for Time so object for Y axis does exist
                        objectYExists = True
                    #asks if the Y axis variable is Time
                    if VarX[0] == T:
                        #there isn't an object required for Time so object for X axis does exist
                        objectXExists = True

        #asks if the start graph button is clicked           
        if bStartGraphClicked:
            #sets started to true
            started = True
            #resets the graph values for x
            XMetricCoords = []
            #resets the graph values for y
            YMetricCoords = []
            #sets the time elapsed to 0
            timeElapsed = 0

        #detects gravity button being clicked
        colour15, bGravityClicked = bGravity.buttonClicked(clicked, X, Y)
        #displays gravity button
        bGravity.displayButton(colour15)

        #detects suvat button being clicked
        colour16, bSuvatClicked = bSuvat.buttonClicked(clicked, X, Y)
        #displays suvat button
        bSuvat.displayButton(colour16)

        #detects the keplers second law button being clicked
        colour25, bKeplerClicked = bKepler.buttonClicked(clicked, X, Y)
        #displays the keplers second law button
        bKepler.displayButton(colour25)

        #asks if the gravity button is clicked
        if bGravityClicked:
            #displays the gravitation formula
            display.blit(gravitationFormula, (pLearn.posX+50, pLearn.posY+50))
        #asks if the suvat button is clicked
        elif bSuvatClicked:
            #displays the motion formulas
            display.blit(suvatFormula, (pLearn.posX+50, pLearn.posY+50))
        #asks if keplers second law button is clicked
        elif bKeplerClicked:
            #asks if demonstration is not running
            if not runKepler:
                #asks if the length of objects is not 0 or 1
                if not(len(objects) == 0 or len(objects) == 1):
                    #asks if object0's mass is greater than object1's mass
                    if (objects[0].metricMass) > (objects[1].metricMass):
                        #this is the ID of the orbiting object
                        testObject = 1
                        #this is the ID of the center object
                        centerObject = 0
                    else:
                        #this is the ID of the orbiting object
                        testObject = 0
                        #this is the ID of the center object
                        centerObject = 1
                    #resets the point lists
                    pointList1 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                    pointList2 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                #sets the amount of time passed to 0
                timePassed = 0
                #run kepler is set to true
                runKepler = True
                #there have been 0 repeats
                reps = 0
        else:
            #creates text to instruct the user on how to use the learn panel
            learnText = LearnFont.render("click on the buttons above to see the formulas", 1, grey3)
            #displays the text
            display.blit(learnText, (pLearn.posX+30, pLearn.posY+100))

        #asks if the number of objects is not 2 and kepler is running
        if len(objects)!=2 and runKepler:
            #creates error text
            learnText = LearnFont.render("There must be exactly 2 objects", 1, black)
            #creates more error text
            learnText2 = LearnFont.render(" in the simulation for this!", 1, black)
            #displays error text
            display.blit(learnText, (pLearn.posX+30, pLearn.posY+150))
            #displays more error text
            display.blit(learnText2, (pLearn.posX+30, pLearn.posY+200))
            #kepler demonstration is stopped
            runKepler = False
        
        ##this section runs the kepler demonstration
        #asks if we want to run the kepler demonstration
        if runKepler:
            #creates the first line of text
            learnText = LearnFont.render("A radius vector joining any two objects, sweeps", 1, black)
            #creates the second line of text
            learnText2 = LearnFont.render("out equal areas in equal lengths of time.", 1, black)
            #creates the third line of text
            learnText3 = LearnFont.render("green area = blue area", 1, black)
            #displays the first line of text
            display.blit(learnText, (pLearn.posX+30, pLearn.posY+150))
            #displays the second line of text
            display.blit(learnText2, (pLearn.posX+30, pLearn.posY+200))
            #displays the third line of text
            display.blit(learnText3, (pLearn.posX+30, pLearn.posY+250))

            #asks if the time passed is greater than1 second
            if timePassed < FPS:
                #appends the position of the object to the point list
                pointList1.append(((objects[testObject].drawPosX+centerX),(objects[testObject].drawPosY+centerY)))
            #asks if the time passed is greater than 2 seconds but less than 3 seconds
            if timePassed >2*FPS and timePassed<3*FPS:
                #adds the position of the object to the other point list
                pointList2.append(((objects[testObject].drawPosX+centerX),(objects[testObject].drawPosY+centerY)))
            #asks if the time passed is greater than 3.3 seconds
            if timePassed > 3.3*FPS:
                #sets time passed to 0
                timePassed = 0
                #resets the point lists to only have the center points of the obejcts in the lists 
                pointList1 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                pointList2 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                #adds 1 to repeats
                reps += 1

            #increases time Passed by 1 (measured in frames)
            timePassed+=1

            #asks if the number of repeats if greater than 4
            if reps > 4:
                #sets run kepler to false so it stops the demonstration
                runKepler = False
                #resets the point lists to only have the center points of the obejcts in the lists 
                pointList1 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                pointList2 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                #sets repeats to 0
                reps = 0


        ##displaying the switches
        for switch in switches:
            #asks if the left mouse button is clicked and the cursor is within the switch
            if clicked and X>(switch.posX-2) and Y>(switch.posY-2) and X<(switch.posX+82) and Y<(switch.posY+42):
                #sets switch was clicked to True
                switch.wasClicked = True
            #asks if the switch was clicked in the last fram but is not clicked in this frame
            elif switch.wasClicked and not clicked:
                #toggles the switch
                switch.state = not switch.state
                #sets switch was clicked ti False
                switch.wasClicked = False
            #displays the switvh
            switch.displaySwitch()

        #draws a grey rectangle for the colour wheel to be drawn on top of
        pygame.draw.rect(display, grey1, (pTools.posX+3, sShowTrail.posY+45, pTools.sizeX-8, int(pTools.sizeX*(4/5)+10)))
        #draws a black outline for the rectangle
        pygame.draw.rect(display, black, (pTools.posX+3, sShowTrail.posY+45, pTools.sizeX-8, int(pTools.sizeX*(4/5)+10)), 2)
        #displays the colour wheel onto the rectangle
        display.blit(colourWheel, (sShowFor.posX+3, sShowTrail.posY+55))
        #displays the lightness scale onto the rectangle
        display.blit(lightness, (pTools.posX+pTools.sizeX*(4/5), sShowTrail.posY+50))
        #displays a black outline for the lightness scale
        pygame.draw.rect(display, black, (pTools.posX+pTools.sizeX*(4/5), sShowTrail.posY+50, int(pTools.sizeX/5)-10, int(pTools.sizeX*(4/5))), 2)

        #asks if the cursor is within the colour wheel
        if X>sShowFor.posX+3 and X<(int(pTools.sizeX*(3/4)))+sShowFor.posX+3 and Y>sShowTrail.posY+55 and Y<sShowTrail.posY+55+(int(pTools.sizeX*(3/4))):
            #asks if the left mouse button is clicked
            if clicked:
                #sets the current red value 
                currentR = list(display.get_at((X, Y)))[0]/255
                #sets the current green vlaue
                currentG = list(display.get_at((X, Y)))[1]/255
                #sets the current blue value
                currentB = list(display.get_at((X, Y)))[2]/255
                #puts the colour values in a list
                currentHUE = [currentR, currentG, currentB]

        #asks if the cursor is within the lightness scale
        if X>pTools.posX+pTools.sizeX*(4/5) and X<pTools.posX+pTools.sizeX*(4/5)+int(pTools.sizeX/5)-10 and Y>sShowTrail.posY+50 and Y<sShowTrail.posY+50+int(pTools.sizeX*(4/5)):
            #asks if the left mouse button is clicked
            if clicked:
                #gets the lightness value
                reduce = list(display.get_at((X,Y)))[0]

        #makes the current colour by multiplying the ratios of the RGB values by the lightness value
        currentcolour = (int(currentHUE[0]*reduce), int(currentHUE[1]*reduce), int(currentHUE[2]*reduce))

        #draws a rectangle to show the current colour
        pygame.draw.rect(display, currentcolour, (pTools.posX+5, sShowTrail.posY+55+int(pTools.sizeX*(4/5)+10), 50, 50))
        #draws a rectangle to outline the colour preview
        pygame.draw.rect(display, black, (pTools.posX+5, sShowTrail.posY+55+int(pTools.sizeX*(4/5)+10), 50, 50), 2)

        #sets paused equal to the state that the pause button is in
        paused = sPausePlay.state

        ##creating text to be displayed on the information panel    
        radiusLabel = PanelFont.render("Current Radius:", 1, black)
        radiusInfo = PanelFont.render("  " + str(int(metersPerPixel*newRadius)) + " m", 1, black)
        densityLabel = PanelFont.render("Current Density:", 1, black)
        densityInfo = PanelFont.render("  " + str(int(newDensity))+" Kg/m^3", 1, black)
        scaleLabel = PanelFont.render("Current Scale:", 1, black)
        scaleInfo = PanelFont.render("  " + str(int(metersPerPixel))+" meters per pixel", 1, black)
        timeLabel = PanelFont.render("Current speed of time:", 1, black)
        timeInfo = PanelFont.render("  x"+str(int(round(FPS*Timeinterval, 3))), 1, black)

        ##displaying the text onto the information panel 
        display.blit(radiusLabel, (8, 50+int(height/2)))
        display.blit(radiusInfo, (8, 70+int(height/2)))
        display.blit(densityLabel, (8, 100+int(height/2)))
        display.blit(densityInfo, (8, 120+int(height/2)))
        display.blit(scaleLabel, (8, 150+int(height/2)))
        display.blit(scaleInfo, (8, 170+int(height/2)))
        display.blit(timeLabel, (8, 200+int(height/2)))        
        display.blit(timeInfo, (8, 220+int(height/2)))

        #detects the reset button being clicked
        colour5, bResetClicked = bReset.buttonClicked(clicked, X, Y) 
        #displays the reset button
        bReset.displayButton(colour5)

        #asks if the reset button is clicked
        if bResetClicked:
            #deletes all objects by setting the list of objects to an empty array
            objects = []
            #number of planets is now 0
            number = 0
            #density is reset
            newDensity = 5500
            #radius is reset
            newRadius = 10
            #meters per pixel is reset
            metersPerPixel = 500000
            #center X is reset
            centerX = width/3
            #center Y is reset
            centerY = height/3
            #Time interval is reset
            Timeinterval = 10000/FPS

        #asks if the graphing is not started
        if not started:
            #allows the increase time interval to be clicked
            colour6, bIncreaseClicked = bIncrease.buttonClicked(clicked, X, Y)
        else:
            #increase time interval button can't be clicked
            colour6 = grey4
            bIncreaseClicked = False
        #displays the increase time interval button
        bIncrease.displayButton(colour6)

        #asks if the increase time interval button is clicked and asks if it has not been held or has been held for a second
        if bIncreaseClicked and (heldI == 0 or heldI > FPS):
            #multiplies the time interval by 2
            Timeinterval *= 2
            #adds 1 to the held variable
            heldI+=1
        #asks if the button is not clicked
        elif not bIncreaseClicked:
            #sets the held variable to 0
            heldI=0

        #asks if the graphing is not started
        if not started:
            #allows the decrease time interval to be clicked
            colour7, bDecreaseClicked = bDecrease.buttonClicked(clicked, X, Y)
        else:
            #decrease time interval button can't be clicked
            colour7 = grey4
            bDecreaseClicked = False
        #displays the decrease time interval button
        bDecrease.displayButton(colour7)

        #asks if the decrease time interval button is clicked and asks if it has not been held or has been held for a second
        if bDecreaseClicked and (heldD == 0 or heldD > FPS):
            #divides the time interval by 2
            Timeinterval /= 2
            #adds 1 to the held variable
            heldD+=1
        #asks if the button is not clicked
        elif not bDecreaseClicked:
            #sets the held variable to 0
            heldD=0

        #displays the boarder
        WindowGUI(clicked, X, Y, ClickedLastFrame)
        
        #detects the main menu button being clicked
        colour4, bMainMenuClicked = bMainMenu.buttonClicked(clicked, X, Y)
        #displays the main menu button
        bMainMenu.displayButton(colour4)

        #detects the instruction button being clicked
        colour13, bInstructionsClicked = bInstructions.buttonClicked(clicked, X, Y)
        #displays the instructions button
        bInstructions.displayButton(colour13)

        if bInstructionsClicked:
            #displays the instructions panel
            pInstructions.displayPanel()

            ##tool bar instructions

            #creates the next instruction
            InsToolBar = PanelFont.render("1) Tool bar - This panel gives you options to affect the simulation screen", 1, black)
            #displays the next instruction
            display.blit(InsToolBar, (pInstructions.posX+5, pInstructions.posY+30))
            #draws a line from the instruction to the switch
            pygame.draw.line(display, black, (pInstructions.posX+5, pInstructions.posY+30), (pTools.posX+50, pTools.posY+10), 3)

            #creates the next instruction
            InsShowID = PanelFont.render("a) Show ID - View the ID of each object", 1, black)
            #displays the next instruction
            display.blit(InsShowID, (pInstructions.posX+20, pInstructions.posY+90))
            #draws a line from the instruction to the switch
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+90), (sShowID.posX, sShowID.posY), 3)

            #creates the next instruction
            InsShowVel = PanelFont.render("b) Show velocity - View the velocity of each object", 1, black)
            #displays the next instruction
            display.blit(InsShowVel, (pInstructions.posX+20, pInstructions.posY+120))
            #draws a line from the instruction to the switch
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+120), (sShowVel.posX, sShowVel.posY), 3)

            #creates the next instruction
            InsShowFor = PanelFont.render("c) Show net force - View the net force acting on each object", 1, black)
            #displays the next instruction
            display.blit(InsShowFor, (pInstructions.posX+20, pInstructions.posY+150))
            #draws a line from the instruction to the switch
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+150), (sShowFor.posX, sShowFor.posY), 3)

            #creates the next instruction
            InsShowTrail = PanelFont.render("c) Show net trial - see the path that each object traces", 1, black)
            #displays the next instruction
            display.blit(InsShowTrail, (pInstructions.posX+20, pInstructions.posY+180))
            #draws a line from the instruction to the switch
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+180), (sShowTrail.posX, sShowTrail.posY), 3)

            #Info panel instructions

            #creates the next instruction
            InsInfo = PanelFont.render("2) Information Panel - This lets you view information about the current time in the simulation", 1, black)
            #displays the next instruction
            display.blit(InsInfo, (pInstructions.posX+5, pInstructions.posY+300))
            pygame.draw.line(display, black, (pInstructions.posX+5, pInstructions.posY+300), (pInfo.posX, pInfo.posY), 3)

            #creates the next instruction
            InsCurrRad =  PanelFont.render("a) Current radius is the radius of the pointer used to insert objects in m", 1, black)
            #displays the next instruction
            display.blit(InsCurrRad, (pInstructions.posX+20, pInstructions.posY+330))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+330), (50, 50+int(height/2)), 3)

            #creates the next instruction
            InsCurrDens =  PanelFont.render("b) Current density is the density selected for the next object in Kg/m^3", 1, black)
            #displays the next instruction
            display.blit(InsCurrDens, (pInstructions.posX+20, pInstructions.posY+360))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+360), (50, 100+int(height/2)), 3)

            #creates the next instruction
            InsCurrScale = PanelFont.render("c) Current Scale is the number of meters in a pixel", 1, black)
            #displays the next instruction
            display.blit(InsCurrScale, (pInstructions.posX+20, pInstructions.posY+390))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+390), (50, 150+int(height/2)), 3)

            #creates the next instruction
            InsCurrTime = PanelFont.render("d) Current speed of time is how quickly the simulation is going", 1, black)
            #displays the next instruction
            display.blit(InsCurrTime, (pInstructions.posX+20, pInstructions.posY+410))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+410), (50, 200+int(height/2)), 3)

            #Time Panel instructions

            #creates the next instruction
            InsTime = PanelFont.render("3) Time Panel - adjust the flow of time", 1, black)
            #displays the next instruction
            display.blit(InsTime, (pInstructions.posX+5, pInstructions.posY+500))
            pygame.draw.line(display, black, (pInstructions.posX+5, pInstructions.posY+510), (pTime.posX, pTime.posY), 3)

            #creates the next instruction
            InsPause = PanelFont.render("a) Pause/Play switch - stop and start the flow of time", 1, black)
            #displays the next instruction
            display.blit(InsPause, (pInstructions.posX+20, pInstructions.posY+530))
            pygame.draw.line(display, green, (pInstructions.posX+20, pInstructions.posY+540), (sPausePlay.posX+30, sPausePlay.posY), 3)

            #creates the next instruction
            InsReset = PanelFont.render("b) Reset button - deletes all objects on the screen", 1, black)
            #displays the next instruction
            display.blit(InsReset, (pInstructions.posX+35, pInstructions.posY+560))
            pygame.draw.line(display, red, (pInstructions.posX+35, pInstructions.posY+570), (bReset.posX+30, bReset.posY), 3)

            #creates the next instruction
            InsIncrease = PanelFont.render("c) >>+ - speed up the flow of time", 1, black)
            #displays the next instruction
            display.blit(InsIncrease, (pInstructions.posX+50, pInstructions.posY+590))
            pygame.draw.line(display, cyan, (pInstructions.posX+50, pInstructions.posY+600), (bIncrease.posX+30, bIncrease.posY), 3)

            #creates the next instruction
            InsDecrease = PanelFont.render("d) >>- - slow down the flow of time", 1, black)
            #displays the next instruction
            display.blit(InsDecrease, (pInstructions.posX+65, pInstructions.posY+620))
            pygame.draw.line(display, cyan, (pInstructions.posX+65, pInstructions.posY+630), (bDecrease.posX+30, bDecrease.posY), 3)

        colour14, bInstructions2clicked = bInstructions2.buttonClicked(clicked, X, Y)
        bInstructions2.displayButton(colour14)

        #asks if the second instructions button is clicked
        if bInstructions2clicked:
            #displays the instructions panel
            pInstructions.displayPanel()

            #creates sub title text
            Ins1 = PanelFont.render("How to use the simulation:", 1, black)
            #displays subtitle text
            display.blit(Ins1, (pInstructions.posX+5, pInstructions.posY+30))

            #creates the next instruction
            Ins2 = PanelFont.render("1) Move the mouse over the black simulation screen. you should see a blue circle where the mouse is.", 1, black)
            #displays the next instruction
            display.blit(Ins2, (pInstructions.posX+5, pInstructions.posY+60))

            #creates the next instruction
            Ins3 = PanelFont.render("2) Use the scroll wheel to change the size of the blue circle", 1, black)
            #displays the next instruction
            display.blit(Ins3, (pInstructions.posX+5, pInstructions.posY+90))

            #creates the next instruction
            Ins4 = PanelFont.render("3) Left click on the simulation screen to add an object the same size as the blue circle", 1, black)
            #displays the next instruction
            display.blit(Ins4, (pInstructions.posX+5, pInstructions.posY+120))

            #creates the next instruction
            Ins5 = PanelFont.render("4) Left click and drag on the simulation screen to adjust the object's initial velocity", 1, black)
            #displays the next instruction
            display.blit(Ins5, (pInstructions.posX+5, pInstructions.posY+150))

            #creates the next instruction
            Ins6 = PanelFont.render("5) You can add multiple objects into the simulation at a time. They will automatically iteract by gravity", 1, black)
            #displays the next instruction
            display.blit(Ins6, (pInstructions.posX+5, pInstructions.posY+180))

            #creates the next instruction
            Ins7 = PanelFont.render("6) Holding down shift and z will let you zoom in and out by using the scroll wheel", 1, black)
            #displays the next instruction
            display.blit(Ins7, (pInstructions.posX+5, pInstructions.posY+210))

            #creates the next instruction
            Ins8 = PanelFont.render("7) Holding down shift and d will let you change the density of the next object using the scroll wheel", 1, black)
            #displays the next instruction
            display.blit(Ins8, (pInstructions.posX+5, pInstructions.posY+240))

        #asks if the main menu button isw clicked
        if bMainMenuClicked:
            #sets done equal to false
            done = False
            #loops untill done is equal to True
            while not done:
                #iterates through all possible pygame events:
                for event in pygame.event.get():
                    #asks if the type of event is quit
                    if event.type == quit:
                        #quits pygame
                        pygame.quit()
                        #quits python
                        sys.exit()
                #gets x coordinate of mouse
                X = list(pygame.mouse.get_pos())[0]
                #gets y coordinate of mouse
                Y = list(pygame.mouse.get_pos())[1]
                #gets left mouse button state
                clicked = list(pygame.mouse.get_pressed())[0]
                #displays the exit panel
                pExit.displayPanel()

                #calls method for detecting button click on the cancel button
                colour8, bCancelClicked = bCancel.buttonClicked(clicked, X, Y)
                #displays the cancel button
                bCancel.displayButton(colour8)

                #calls method for detecting button click on the dont save button
                colour9, bDontSaveClicked = bDontSave.buttonClicked(clicked, X ,Y)
                #displays the dont save button
                bDontSave.displayButton(colour9)

                #calls method for detecting button click on the save button
                colour10, bSaveClicked = bSave.buttonClicked(clicked, X, Y)
                #displays the save button
                bSave.displayButton(colour10)

                #asks if the cancel button has just been clicked
                if bCancelClicked:
                    #sets done to true to end the loop
                    done = True
                    #creates confirmation text
                    cancelText = PanelFont.render("ok", 1, grey1)
                    #displays confirmation text
                    display.blit(cancelText, (width/2, height/2))
                #asks if the don't save button is clicked
                elif bDontSaveClicked:
                    #creates confirmation text
                    dontSaveText = PanelFont.render("ok", 1, grey1)
                    #displays confirmation text
                    display.blit(dontSaveText, (width/2, height/2))
                    #sets done to true to end the loop
                    done = True
                    #sets in main menue to true so that we go back to the main menu
                    inMainMenu = True
                    #resets the objects
                    objects = []
                    #changes number to be 0
                    number = 0
                #asks if the save button is clicked
                elif bSaveClicked:
                    #sets done to true
                    done = True
                    #opens the number of saves file into file variable to be read
                    file = open("saves\\NumberOfSaves.txt", "r")
                    #adds 1 to the number of saved files
                    FileID = str(int(file.readline())+1)
                    #names the new save as "simulation" with the corresponding simulation ID
                    FileName = "simulation" + FileID
                    #opens the number of saves file into file variable to be written to
                    file = open("saves\\NumberOfSaves.txt", "w")
                    #writes the new number of saves to the number of saves file
                    file.write(FileID)
                    #saves and closes the number of saves file
                    file.close()
                    #creates a new file with the new file name
                    file = open("saves\\"+FileName+".txt", "w")
                    #sets data to be an empty array
                    data = []
                    #iterates through all of the planets in the simulation
                    for item in objects:
                        #appends the data of the item that the loop is currently on to the data 
                        data.append([item.ID, item.metricMass, item.metricPosX, item.metricPosY, item.velX, item.velY, item.density])
                    #writes the data to the file
                    file.write(str(data))
                    #saves and closes the file
                    file.close()
                    #creates the confirmation text
                    SaveText = PanelFont.render("saving as: "+FileName, 1, grey1)
                    #displays the confirmation text
                    display.blit(SaveText, (width/2-100, height/2))

                    #sets in main menu to true to we can go to main menu
                    inMainMenu = True
                    #resests the objects
                    objects = []
                    #changes number to be 0
                    number = 0
                else:
                    #creates a prompt text
                    promptText = PanelFont.render("Do you want to save this siulation?", 1, grey1)
                    #displays the prompt text
                    display.blit(promptText, (width/2-100, height/2))

                # this updates the screen so anything drawn to the display is actually shown on the users monitor 
                pygame.display.update()
                # waits for 1/FPS seconds
                FPSClock.tick(FPS)
            #waits for 1.5 seconds
            time.sleep(1.5)
        #asks if the left mouse button is clicked 
        if clicked:
            ClickedLastFrame = True
        else:
            ClickedLastFrame = False
        # this updates the screen so anything drawn to the display is actually shown on the users monitor 
        pygame.display.update()
        # waits for 1/FPS seconds
        FPSClock.tick(FPS)