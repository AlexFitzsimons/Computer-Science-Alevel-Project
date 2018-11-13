####orbit program
#commenting format*
#*
####title
###large section e.g. description of a class or large while loop
##small section e.g descriptio  of a small for loop or if statement
#single line description
#*

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

###the class that defines the scroll bar - lets the user click and drag to move a slider
class ScrollBar:
    ##initialisation method
    #self allows each object to have it's own unique variables. the other parameters are made when individual scroll bars are made
    def __init__(self, direction, PosX, PosY, length, requiredLength):
        #
        self.direction = direction
        self.PosX = PosX
        self.PosY = PosY
        if self.direction == "H":
            self.SizeX = length
            self.SizeY = 20
            self.innerSX = length/4
            self.innerSY = 14
        else:
            self.SizeX = 20
            self.SizeY = length
            self.innerSX = 14
            self.innerSY = length/4
        self.innerPX = PosX+3
        self.innerPY = PosY+3

    def displayScrollBar(self):
        pygame.draw.rect(display, grey3, (self.PosX, self.PosY, self.SizeX, self.SizeY), 5)
        pygame.draw.rect(display, grey1, (self.innerPX, self.innerPY, self.innerSX, self.innerSY))

    def changeScroll(self, activated, X, Y):
        if activated:
            if self.direction == "H":
                if (X < self.PosX+(self.innerSX/2)):
                    self.innerPX = self.PosX+3

                elif (X > self.PosX+self.SizeX-(self.innerSX/2)):
                    self.innerPX = self.PosX+self.SizeX-self.innerSX

                else:
                    self.innerPX = X-(self.innerSX/2)
            else:
                if (Y < self.PosY+(self.innerSY/2)):
                    self.innerPY = self.PosY+3

                elif (Y > self.PosY+self.SizeY-(self.innerSY/2)):
                    self.innerPY = self.PosY+self.SizeY-self.innerSY

                else:
                    self.innerPY = Y-(self.innerSY/2)


###function to call for exiting the program
def exiting(exit):
    if exit:
        pygame.quit()
        sys.exit()

###GUIs

##panels
pTools = Panel("Tools", grey2, 5, 34, int(width/8), int(height/2))
colourWheel = pygame.transform.scale(colourWheel, (int(pTools.sizeX*(3/4)),int(pTools.sizeX*(3/4))))
lightness = pygame.transform.scale(lightness, ((int(pTools.sizeX/5)-10, int(pTools.sizeX*(4/5)))))
pInfo = Panel("Info", grey2, 5, int(pTools.posY+pTools.sizeY+2), int(width/8), int(height/2)-46)
pSimulation = Panel("Simulation", black, int(pTools.posX+pTools.sizeX+2), 34, int(width/2), 4*height/5)
pTime = Panel("Time", grey2, int(pTools.posX+pTools.sizeX+2), int(pSimulation.posY+pSimulation.sizeY+2), int(width/2), (height-int(pSimulation.posY+pSimulation.sizeY+12)))

topGraph = 34
leftGraph = int(((5*width)/8)+9)
rightGraph = int(((5*width)/8)+9)+int(((3*width)/8)-12)
bottomGraph = int(height/2+34)

pGraph = Panel("Graph 1", white, leftGraph, topGraph, rightGraph-leftGraph, bottomGraph-topGraph)
pExit = Panel("Exit", grey4, int((width/2)-300), int((height/2)-100), 600, 300)
pLearn = Panel("Learn", grey2, int(((5*width)/8)+9), (height/2)+36, int(((3*width)/8)-12), (height/2)-46)
gravitationFormula = pygame.transform.scale(gravitationFormula, (int(((3*width)/8)-112), int((height/2)-146)))
suvatFormula = pygame.transform.scale(suvatFormula, (int(((3*width)/8)-112), int((height/2)-146)))

pInstructions = Panel("instructions", white, int(pTools.posX+pTools.sizeX+2), 34, int(width/2), 4*height/5)
pChangeX = Panel("Change x axis", grey2, leftGraph, topGraph, rightGraph-leftGraph, bottomGraph-topGraph)
pChangeY = Panel("Change y axis", grey2, leftGraph, topGraph, rightGraph-leftGraph, bottomGraph-topGraph)

##buttons
bExit = Button("x", red, width-52, 1, 50, 30)
bMin = Button("_", grey1, width-103, 1, 50, 30)
bEnter = Button("Enter", grey2, (width/2)-150, (height/2)-40, 100, 80)
bOpen = Button("Open", grey2, width/2, (height/2)-40, 100, 80)

bMainMenu = Button("Exit", grey2, 36, 3, 50, 26)
bInstructions = Button("Instructions", grey2, 100, 3, 120, 26)
bInstructions2 = Button("more Instructions", grey2, 235, 3, 170, 26)

bReset = Button("reset", red, pTime.posX+95, pTime.posY+48, 86, 44)
bIncrease = Button(">>+", cyan, bReset.posX+bReset.sizeX+5, pTime.posY+48, 86, 44)
bDecrease = Button(">>-", cyan, bIncrease.posX+bIncrease.sizeX+5, pTime.posY+48, 86, 44)

bSave = Button("save", green, int((width/2)-250), int((height/2)+100), 100, 50)
bDontSave = Button("Dont save", red, int((width/2)-50), int((height/2)+100), 100, 50)
bCancel = Button("Cancel", grey3, int((width/2)+150), int((height/2)+100), 100, 50)

bGravity = Button("Gravity", green2, pLearn.posX+110, pLearn.posY+18, 100, 30)
bSuvat = Button("Motion", green2, pLearn.posX+5, pLearn.posY+18, 100, 30)
bKepler = Button("Keplers 2nd law", green2, pLearn.posX+215, pLearn.posY+18, 160, 30)

bX = Button("x", green, pGraph.posX+(pGraph.sizeX/2)-20, pGraph.posY+pGraph.sizeY-25, 40, 20)
bY = Button("y", green, pGraph.posX+5, pGraph.posY+(pGraph.sizeY/2)-20, 20, 40)
VX = "Velocity X (m/s)"
bXvel = Button(VX, yellow, pGraph.posX+30, pGraph.posY+30, 200, 50)
VY = "Velocity Y (m/s)"
bYvel = Button(VY, yellow, pGraph.posX+30, pGraph.posY+90, 200, 50)
T = "Time (s)"
bTime = Button(T, yellow, pGraph.posX+30, pGraph.posY+150, 200, 50)
bStartGraph = Button("Start Graphing!", red, pGraph.posX+(pGraph.sizeX/2)-80, pGraph.posY+(pGraph.sizeY/2)-15, 160, 30)
bStopGraph = Button("Stop Graphing!", red, pGraph.posX+80, pGraph.posY+10, 160, 30)

##switches
sPausePlay = Switch("||/>", green, pTime.posX+5, pTime.posY+50, False, "||", " >", 86, 44)#switch to pause and play
sShowID = Switch("Show ID", yellow,  pTools.posX+5, pTools.posY+50, False, "on", "off")
sShowVel = Switch("Show velocity", yellow, pTools.posX+5, pTools.posY+100, False, "on", "off")
sShowFor = Switch("Show net Force", yellow, pTools.posX+5, pTools.posY+150, False, "on", "off")
sShowTrail = Switch("Show trail", yellow, pTools.posX+5, pTools.posY+200, False, "on", "off")
switches = [sPausePlay, sShowID, sShowVel, sShowFor, sShowTrail]


##ScrollBars
sbIDs = ScrollBar("V", pGraph.posX+pGraph.sizeX-20, pGraph.posY+5, pGraph.sizeY-10, 0)


##assembling the Window GUI
def WindowGUI(clicked, X, Y, clickedLastFrame):
    pygame.draw.rect(display, black, (0,0,width,32))
    pygame.draw.line(display, black, (0,0), (0, height), 2)
    pygame.draw.line(display, black, (width,0), (width, height), 2)
    pygame.draw.line(display, black, (0,height), (width, height), 18)
    pygame.Surface.blit(display, icon, (0,0))
    if not clickedLastFrame:
        colour1, bExitClicked = bExit.buttonClicked(clicked, X, Y)
        colour2, bMinClicked = bMin.buttonClicked(clicked, X, Y)
        bMin.displayButton(colour2)
        bExit.displayButton(colour1)
        exiting(bExitClicked)
        if bMinClicked:
            pygame.display.iconify()
    else:
        bMin.displayButton(grey1)
        bExit.displayButton(red)

def background():
    pygame.draw.rect(display, grey1, (0, 0, width, pSimulation.posY))
    pygame.draw.rect(display, grey1, (0, 0, pSimulation.posX, height))
    pygame.draw.rect(display, grey1, (0, pSimulation.posY+pSimulation.sizeY, width, height))
    pygame.draw.rect(display, grey1, (pSimulation.posX+pSimulation.sizeX, 0, width, height))

inMainMenu = True
clicked = False

###animation loop
while True:
    ##assembling main menu
    objects = []
    paused = False
    state = True

    newDensity = 5500
    newRadius = 10
    
    wasClicked = False
    clicked = False
    number = 0
    heldD=0
    heldI=0
    ClickedLastFrame = False
    opening = False
    fileNames = []
    buttons = []
    data = []
    fileNames = os.listdir("saves\\")
    fileNames.remove("NumberOfSaves.txt")
    activated = False
    currentHUE = [0.7, 0.7, 0.7]
    reduce = 255
    for count, filename in enumerate(fileNames):
        buttons.append(Button(filename, grey2, (width/2)-350, (count*60)+40, 300, 50))
    while inMainMenu:
        display.fill(grey1)
        X = list(pygame.mouse.get_pos())[0]#gets x coordinate of mouse
        Y = list(pygame.mouse.get_pos())[1]#gets y coordinate of mouse
        for event in pygame.event.get():
            if event.type == quit:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clicked = list(pygame.mouse.get_pressed())[0]
        WindowGUI(clicked, X, Y, ClickedLastFrame)

        if not opening:
            colour3, bEnterClicked = bEnter.buttonClicked(clicked, X, Y)
            bEnter.displayButton(colour3)
            if bEnterClicked:
                inMainMenu = False 
                
            colour11, bOpenClicked = bOpen.buttonClicked(clicked, X, Y)
            bOpen.displayButton(colour11)
            if bOpenClicked:
                opening = True
        else:
            for item in buttons:
                colour12, buttonClicked = item.buttonClicked(clicked, X, Y)
                item.displayButton(colour12)
                if buttonClicked:
                    file = open("saves\\" + item.name, "r")
                    data = eval(file.readline())
                    inMainMenu = False

        pygame.display.update()
        FPSClock.tick(FPS)
    time.sleep(0.5)

    for item in data:
        if item[0] > number:
            number = item[0]+1
        metricradius = (((3*item[1])/(4*math.pi*item[6]))**(1/3))
        Radius = metricradius/metersPerPixel
        objects.append(Object(item[0], grey1, Radius, (item[2]/metersPerPixel), (item[3]/metersPerPixel), item[4], item[5], item[6]))

    
    ##simulation
    zoom = False
    changeDensity = False
    VarX = [T, -1]
    VarY = [VX, 0]
    changeXaxis = False
    changeYaxis = False
    started = False
    XMetricCoords = []
    YMetricCoords = []         
    runKepler = False
    stop = False
    objectXExists=False
    objectYExists=False

    while not inMainMenu:
        ##inputs
        X = list(pygame.mouse.get_pos())[0]#gets x coordinate of mouse
        Y = list(pygame.mouse.get_pos())[1]#gets y coordinate of mouse
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    sPausePlay.state = not sPausePlay.state
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                if event.button == 5:
                    if not changeDensity:
                        if zoom:
                            metersPerPixel /= 1.05
                        if newRadius <= 150:
                            newRadius *= 1.05
                    else:
                        newDensity *= 1.001
                if event.button == 4:
                    if not changeDensity:
                        if zoom:
                            metersPerPixel *= 1.05
                        if newRadius >= 3:
                            newRadius /= 1.05
                    else:
                        newDensity /= 1.001
            
            elif event.type == quit:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] and keys[pygame.K_z]:
            zoom = True
            runKepler = False
            sShowTrail.state = False
            
            changeDensity = False
            centerX = X
            centerY = Y
        elif  keys[pygame.K_LSHIFT] and keys[pygame.K_d]:
            changeDensity = True
            zoom = False
        else:
            zoom = False
            changeDensity = False
        clicked = list(pygame.mouse.get_pressed())[0]
        rightClicked = list(pygame.mouse.get_pressed())[2]

        pSimulation.displayPanel()


        leftEdge = pSimulation.posX
        topEdge = pSimulation.posY
        rightEdge = pSimulation.posX+pSimulation.sizeX
        lowerEdge = pSimulation.posY+pSimulation.sizeY

        if not paused:
            for self in objects:
                for other in objects:
                    if other != self:
                        x = self.metricPosX-other.metricPosX
                        y = self.metricPosY-other.metricPosY
                        distance = math.sqrt((x**2)+(y**2))

                        force = 6.67*(10**(-11))*(self.metricMass*other.metricMass)/(distance**2)
                        acc = force/self.metricMass

                        self.netX = (x/distance * force)/(10**22)
                        self.netY = (y/distance * force)/(10**22)

                        self.velX -= acc * (x/distance) * Timeinterval
                        self.velY -= acc * (y/distance) * Timeinterval

                        momentumX = self.velX*self.metricMass + other.velX*other.metricMass
                        momentumY = self.velY*self.metricMass + other.velY*other.metricMass

                        if distance <= (self.metricRadius + other.metricRadius):
                            combinedDensity = (self.density+other.density)/2
                            if self.metricRadius > other.metricRadius:
                                self.metricMass += other.metricMass
                                try:
                                    objects.remove(other)
                                except:
                                    pass
                                self.density = combinedDensity
                                self.velX = momentumX/self.metricMass
                                self.velY = momentumY/self.metricMass
                                try:
                                    self.collided = True
                                except:
                                    pass
                            else:
                                other.metricMass += self.metricMass
                                try:
                                    objects.remove(self)
                                except:
                                    pass
                                other.density = combinedDensity
                                other.velX = momentumX/other.metricMass
                                other.velY = momentumY/other.metricMass
                                try:
                                    other.collided = True
                                except:
                                    pass
        
        for self in objects:
            if not paused:
                self.changePos()
            self.updateUnits()
            self.displayObject()
            if sShowVel.state:
                pygame.draw.line(display, magenta, (int(self.drawPosX+centerX), int(self.drawPosY+centerY)), (int(self.drawPosX+(self.velX/100)+centerX), int(self.drawPosY+(self.velY/100)+centerY)))
            if sShowFor.state:
                pygame.draw.line(display, cyan, (self.drawPosX+centerX, self.drawPosY+centerY), ((int(self.drawPosX-self.netX)+centerX), int(self.drawPosY-self.netY)+centerY), 2)
            if sShowID.state:
                self.showID()
            self.netX = 0
            self.netY = 0
            if not zoom:
                if sShowTrail.state:
                    self.trail.append((self.drawPosX+centerX, self.drawPosY+centerY))
                    if len(self.trail)>1000:
                        del self.trail[0]
                    if len(self.trail)>1:
                        pygame.draw.lines(display, self.colour, False, self.trail, 2)
            else:
                self.trail = []

        if (X-newRadius>leftEdge) and (X+newRadius<rightEdge) and (Y-newRadius>topEdge) and (Y+newRadius<lowerEdge):
            pygame.draw.circle(display, blue, (X,Y), int(newRadius), 2)
            if clicked and not ClickedLastFrame:
                ClickedLastFrame = True
                initialY = Y-0
                initialX = X-0
            elif clicked and ClickedLastFrame:
                ClickedLastFrame = True
                pygame.draw.circle(display, grey1, (initialX, initialY), int(newRadius))
                pygame.draw.line(display, green, (initialX, initialY), (X, Y), 3)
                pygame.draw.circle(display, yellow, (X, Y), int(newRadius), 2)
            elif not clicked and ClickedLastFrame:
                ClickedLastFrame = False
                if newRadius < 150 and newRadius > 3:
                    objects.append(Object(number, currentcolour, int(newRadius), initialX-centerX, initialY-centerY, (initialX-X)*100, (initialY-Y)*100, newDensity))
                    number += 1
            elif not clicked and not ClickedLastFrame:
                ClickedLastFrame = False

        if runKepler:
            try:
                pygame.draw.polygon(display, blue, pointList1)
            except:
                pass
            try:
                pygame.draw.polygon(display, green, pointList2)
            except:
                pass
        

        background()

        pTools.displayPanel()        
        pInfo.displayPanel()
        pTime.displayPanel()
        pGraph.displayPanel()
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
        if VarX[0] != "Time (s)":#this is used so that measures that dont belong to an object get the right label
            Xaxis = PanelFont.render("x axis = " + VarX[0] + " of object " + str(VarX[1]), 1, black)#text telling the user what variables are being measured on the X axis
            display.blit(Xaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+5))#diaplaying that text
        else:
            Xaxis = PanelFont.render("x axis = " + VarX[0], 1, black)#text telling the user what variables are being measured on the X axis
            display.blit(Xaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+5))#text telling the user what variables are being measured on the X axis

        if VarY[0] != "Time (s)":
            Yaxis = PanelFont.render("y axis = " + VarY[0] + " of object " + str(VarY[1]), 1, black)#text telling the user what variables are being measured on the Y axis
            display.blit(Yaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+20))#text telling the user what variables are being measured on the Y axis
        else:
            Yaxis = PanelFont.render("y axis = " + VarY[0], 1, black)#text telling the user what variables are being measured on the Y axis
            display.blit(Yaxis, (pGraph.posX+(pGraph.sizeX/2)-100, pGraph.posY+20))#text telling the user what variables are being measured on the Y axis

        if bXClicked:
            changeXaxis = True
        if bYClicked:
            changeYaxis = True

        IDButtons = []
        adjust = 30
        for self in objects:
            IDButtons.append(Button(str(self.ID), orange,  pGraph.posX+300, pGraph.posY+adjust, 200, 50))
            adjust += 60

        if changeXaxis and not started:
            pChangeX.displayPanel()
            sbIDs.displayScrollBar()
            if clicked:
                if X>sbIDs.PosX and X<sbIDs.PosX+sbIDs.SizeX and Y>sbIDs.PosY and Y<sbIDs.PosY+sbIDs.SizeY:
                    activated = True
                elif activated:
                    activated = True
                else:
                    activated = False
            else:
                activated = False

            sbIDs.changeScroll(activated, X, Y)

            colour19, bXvelClicked = bXvel.buttonClicked(clicked, X, Y)
            bXvel.displayButton(colour19)

            colour20, bYvelClicked = bYvel.buttonClicked(clicked, X, Y)
            bYvel.displayButton(colour20)

            colour21, bTimeClicked = bTime.buttonClicked(clicked, X, Y)
            bTime.displayButton(colour21)


            for n in IDButtons:
                colour23, IDButtonClicked = n.buttonClicked(clicked, X, Y)
                if(VarX[0] != T):
                    n.displayButton(colour23)
                    if IDButtonClicked:
                        VarX[1] = int(n.name)
                        changeXaxis = False
                else:
                    n.displayButton(grey4)

            if bXvelClicked:
                VarX[0] = VX
                changeXaxis = False
                if VarX[1] == -1:
                    VarX[1] = 0

            if bYvelClicked:
                VarX[0] = VY
                if VarX[1] == -1:
                    VarX[1] = 0
                changeXaxis = False

            if bTimeClicked:
                VarX[0] = T
                VarX[1] = -1
                changeXaxis = False

        if changeYaxis and not started:
            pChangeY.displayPanel()

            colour19, bXvelClicked = bXvel.buttonClicked(clicked, X, Y)
            bXvel.displayButton(colour19)

            colour20, bYvelClicked = bYvel.buttonClicked(clicked, X, Y)
            bYvel.displayButton(colour20)

            colour21, bTimeClicked = bTime.buttonClicked(clicked, X, Y)
            bTime.displayButton(colour21)

            for n in IDButtons:
                colour23, IDButtonClicked = n.buttonClicked(clicked, X, Y)
                if(VarY[0] != T):
                    n.displayButton(colour23)
                    if IDButtonClicked:
                        VarY[1] = int(n.name)
                        changeYaxis = False
                else:
                    n.displayButton(grey4)


            if bXvelClicked:
                VarY[0] = VX
                if VarY[1] == -1:
                    VarY[1] = 0
                changeYaxis = False

            if bYvelClicked:
                VarY[0] = VY
                if VarY[1] == -1:
                    VarY[1] = 0
                changeYaxis = False

            if bTimeClicked:
                VarY[0] = T
                VarY[1] = -1
                changeYaxis = False
        colour22, bStartGraphClicked = bStartGraph.buttonClicked(clicked, X, Y)
        if started:
            objectXExists=False
            objectYExists=False
            if objects != []:
                for self in objects:
                    if self.ID == VarX[1]:
                        objectXExists = True
                        if VarX[0] == VX:
                            XMetricCoords.append(self.velX)
                        elif VarX[0] == VY:
                            XMetricCoords.append(self.velY)
                    elif self.ID == VarY[1]:
                        objectYExists = True
                        if VarY[0] == VX:
                            YMetricCoords.append(-self.velX)
                        elif VarY[0] == VY:
                            YMetricCoords.append(-self.velY)

                screenCoords = []
                XGraphCoords = []
                YGraphCoords = []
                if not paused and not stop:
                    if VarY[0] == T:
                        YMetricCoords.append(-timeElapsed)
                        objectYExists = True
                    if VarX[0] == T:
                        XMetricCoords.append(timeElapsed)
                        objectXExists = True

                if not objectXExists or not objectYExists:
                   stop = True

                minMetX = min(XMetricCoords)
                lowerX = PanelFont.render(str(round(minMetX, 1)), 1, black)
                display.blit(lowerX, (originX, originY+30))

                maxMetX = max(XMetricCoords)
                upperX = PanelFont.render(str(round(maxMetX, 1)), 1, black)
                display.blit(upperX, (originX+pGraph.sizeX-150, originY+30))

                lineSizeX = maxMetX-minMetX

                minMetY = min(YMetricCoords)
                upperY = PanelFont.render(str(round(-minMetY, 1)), 1, black)
                display.blit(upperY, (originX-30, originY-pGraph.sizeX+200))

                maxMetY = max(YMetricCoords)
                lowerY = PanelFont.render(str(round(-maxMetY, 1)), 1, black)
                display.blit(lowerY, (originX-50, originY-15))

                if objectXExists and objectYExists:
                    lineSizeY = maxMetY-minMetY

                    graphWidth = pGraph.sizeX-100
                    graphHeight = pGraph.sizeY-100
                
                    if lineSizeX > 0:
                        WRatio = lineSizeX/graphWidth
                    else:
                        WRatio = 1

                    if lineSizeY > 0:
                        HRatio = lineSizeY/graphHeight
                    else:
                        HRatio = 1
            
                    for n in range(len(XMetricCoords)):
                        XGraphCoords.append((XMetricCoords[n]/WRatio)-(minMetX/WRatio))
                        YGraphCoords.append((YMetricCoords[n]/HRatio)-(maxMetY/HRatio))

                    for n in range(len(XGraphCoords)):
                        screenCoords.append(((XGraphCoords[n]+originX), YGraphCoords[n]+originY))

                    savedCoords = screenCoords
                try:
                    pygame.draw.lines(display, blue, False, savedCoords, 2)
                except:
                    pass

                colour24, bStopGraphClicked = bStopGraph.buttonClicked(clicked, X, Y)
                bStopGraph.displayButton(colour24)
                if bStopGraphClicked:
                    started = False
                    stop = False
                    area = pygame.Rect(pGraph.posX, pGraph.posY, pGraph.sizeX, pGraph.sizeY)
                    subSurface = display.subsurface(area)
                    pygame.image.save(subSurface, "savedGraph.jpg")

                if VarY[0] == T:
                    timeElapsed += Timeinterval

                if VarX[0] == T:
                    timeElapsed += Timeinterval
        elif objectXExists and objectYExists:
            bStartGraph.displayButton(colour22)
            timeElapsed = 0
        else:
            if objects != []:
                for self in objects:
                    if self.ID == VarX[1]:
                        objectXExists = True
                    elif self.ID == VarY[1]:
                        objectYExists = True

                if not paused and not stop:
                    if VarY[0] == T:
                        objectYExists = True
                    if VarX[0] == T:
                        objectXExists = True
        print(objectXExists, objectYExists)
                    
        if bStartGraphClicked:
            started = True
            XMetricCoords = []
            YMetricCoords = []
            timeElapsed = 0




        colour15, bGravityClicked = bGravity.buttonClicked(clicked, X, Y)
        bGravity.displayButton(colour15)

        colour16, bSuvatClicked = bSuvat.buttonClicked(clicked, X, Y)
        bSuvat.displayButton(colour16)

        colour25, bKeplerClicked = bKepler.buttonClicked(clicked, X, Y)
        bKepler.displayButton(colour25)

        if bGravityClicked:
            display.blit(gravitationFormula, (pLearn.posX+50, pLearn.posY+50))
        elif bSuvatClicked:
            display.blit(suvatFormula, (pLearn.posX+50, pLearn.posY+50))
        elif bKeplerClicked:
            if len(objects) != 2:
                learnText = LearnFont.render("There must be exactly 2 objects", 1, black)
                learnText2 = LearnFont.render(" in the simulation for this!", 1, black)
                display.blit(learnText, (pLearn.posX+30, pLearn.posY+150))
                display.blit(learnText2, (pLearn.posX+30, pLearn.posY+200))
            else:
                if not runKepler:
                    if (objects[0].metricMass) > (objects[1].metricMass):
                        testObject = 1
                        centerObject = 0
                    else:
                        testObject = 0
                        centerObject = 1
                    pointList1 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                    pointList2 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                    timePassed = 0
                    runKepler = True
                    reps = 0
        else:
            learnText = LearnFont.render("click on the buttons above to see the formulas", 1, grey3)
            display.blit(learnText, (pLearn.posX+30, pLearn.posY+100))

        if len(objects)!=2 and runKepler:
                learnText = LearnFont.render("There must be exactly 2 objects", 1, black)
                learnText2 = LearnFont.render(" in the simulation for this!", 1, black)
                display.blit(learnText, (pLearn.posX+30, pLearn.posY+150))
                display.blit(learnText2, (pLearn.posX+30, pLearn.posY+200))
                runKepler = False
        if runKepler:
            learnText = LearnFont.render("A radius vector joining any two objects, sweeps", 1, black)
            learnText2 = LearnFont.render("out equal areas in equal lengths of time.", 1, black)
            learnText3 = LearnFont.render("green area = blue area", 1, black)
            display.blit(learnText, (pLearn.posX+30, pLearn.posY+150))
            display.blit(learnText2, (pLearn.posX+30, pLearn.posY+200))
            display.blit(learnText3, (pLearn.posX+30, pLearn.posY+250))
            if timePassed < 120:
                pointList1.append(((objects[testObject].drawPosX+centerX),(objects[testObject].drawPosY+centerY)))
            if timePassed >240 and timePassed<360:
                pointList2.append(((objects[testObject].drawPosX+centerX),(objects[testObject].drawPosY+centerY)))
            if timePassed > 380:
                timePassed = 0
                pointList1 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                pointList2 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                reps += 1

            timePassed+=1
            if reps > 3:
                runKepler = False
                pointList1 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                pointList2 = [(objects[centerObject].drawPosX+centerX, objects[centerObject].drawPosY+centerY)]
                reps = 0


        ##displaying the switches
        for switch in switches:
            if clicked and X>(switch.posX-2) and Y>(switch.posY-2) and X<(switch.posX+82) and Y<(switch.posY+42):
                switch.wasClicked = True
            elif switch.wasClicked and not clicked:
                switch.state = not switch.state
                switch.wasClicked = False
            switch.displaySwitch()

        pygame.draw.rect(display, grey1, (pTools.posX+3, sShowTrail.posY+45, pTools.sizeX-8, int(pTools.sizeX*(4/5)+10)))
        pygame.draw.rect(display, black, (pTools.posX+3, sShowTrail.posY+45, pTools.sizeX-8, int(pTools.sizeX*(4/5)+10)), 2)
        display.blit(colourWheel, (sShowFor.posX+3, sShowTrail.posY+55))
        display.blit(lightness, (pTools.posX+pTools.sizeX*(4/5), sShowTrail.posY+50))
        pygame.draw.rect(display, black, (pTools.posX+pTools.sizeX*(4/5), sShowTrail.posY+50, int(pTools.sizeX/5)-10, int(pTools.sizeX*(4/5))), 2)

        if X>sShowFor.posX+3 and X<(int(pTools.sizeX*(3/4)))+sShowFor.posX+3 and Y>sShowTrail.posY+55 and Y<sShowTrail.posY+55+(int(pTools.sizeX*(3/4))):
            if clicked:
                currentR = list(display.get_at((X, Y)))[0]/255
                currentG = list(display.get_at((X, Y)))[1]/255
                currentB = list(display.get_at((X, Y)))[2]/255
                currentHUE = [currentR, currentG, currentB]

        if X>pTools.posX+pTools.sizeX*(4/5) and X<pTools.posX+pTools.sizeX*(4/5)+int(pTools.sizeX/5)-10 and Y>sShowTrail.posY+50 and Y<sShowTrail.posY+50+int(pTools.sizeX*(4/5)):
            
            if clicked:
                reduce = list(display.get_at((X,Y)))[0]
        currentcolour = (int(currentHUE[0]*reduce), int(currentHUE[1]*reduce), int(currentHUE[2]*reduce))

        pygame.draw.rect(display, currentcolour, (pTools.posX+5, sShowTrail.posY+55+int(pTools.sizeX*(4/5)+10), 50, 50))
        pygame.draw.rect(display, black, (pTools.posX+5, sShowTrail.posY+55+int(pTools.sizeX*(4/5)+10), 50, 50), 2)
        paused = sPausePlay.state

            
        radiusLabel = PanelFont.render("Current Radius:", 1, black)
        radiusInfo = PanelFont.render("  " + str(int(metersPerPixel*newRadius)) + " m", 1, black)
        densityLabel = PanelFont.render("Current Density:", 1, black)
        densityInfo = PanelFont.render("  " + str(int(newDensity))+" Kg/m^3", 1, black)
        scaleLabel = PanelFont.render("Current Scale:", 1, black)
        scaleInfo = PanelFont.render("  " + str(int(metersPerPixel))+" meters per pixel", 1, black)
        timeLabel = PanelFont.render("Current speed of time:", 1, black)
        timeInfo = PanelFont.render("  x"+str(int(round(FPS*Timeinterval, 3))), 1, black)


        display.blit(radiusLabel, (8, 50+int(height/2)))
        display.blit(radiusInfo, (8, 70+int(height/2)))
        display.blit(densityLabel, (8, 100+int(height/2)))
        display.blit(densityInfo, (8, 120+int(height/2)))
        display.blit(scaleLabel, (8, 150+int(height/2)))
        display.blit(scaleInfo, (8, 170+int(height/2)))
        display.blit(timeLabel, (8, 200+int(height/2)))        
        display.blit(timeInfo, (8, 220+int(height/2)))

        colour5, bResetClicked = bReset.buttonClicked(clicked, X, Y) 
        bReset.displayButton(colour5)
        if bResetClicked:
            objects = []
            number = 0
            newDensity = 5500
            newRadius = 10
        
        if not started:
            colour6, bIncreaseClicked = bIncrease.buttonClicked(clicked, X, Y)
        else:
            colour6 = grey4
            bIncreaseClicked = False
        bIncrease.displayButton(colour6)
        if bIncreaseClicked and (heldI == 0 or heldI > FPS):
            Timeinterval *= 2
            heldI+=1
        elif not bIncreaseClicked:
            heldI=0

        if not started:
            colour7, bDecreaseClicked = bDecrease.buttonClicked(clicked, X, Y)
        else:
            colour7 = grey4
            bDecreaseClicked = False
        bDecrease.displayButton(colour7)
        if bDecreaseClicked and (heldD == 0 or heldD > FPS):
            Timeinterval /= 2
            heldD+=1
        elif not bDecreaseClicked:
            heldD=0

        WindowGUI(clicked, X, Y, ClickedLastFrame)
        colour4, bMainMenuClicked = bMainMenu.buttonClicked(clicked, X, Y)
        bMainMenu.displayButton(colour4)

        colour13, bInstructionsClicked = bInstructions.buttonClicked(clicked, X, Y)
        bInstructions.displayButton(colour13)

        if bInstructionsClicked:
            pInstructions.displayPanel()

            ##tool bar instructions
            InsToolBar = PanelFont.render("1) Tool bar - This panel gives you options to affect the simulation screen", 1, black)
            display.blit(InsToolBar, (pInstructions.posX+5, pInstructions.posY+30))
            pygame.draw.line(display, black, (pInstructions.posX+5, pInstructions.posY+30), (pTools.posX+50, pTools.posY+10), 3)

            InsShowID = PanelFont.render("a) Show ID - View the ID of each object", 1, black)
            display.blit(InsShowID, (pInstructions.posX+20, pInstructions.posY+90))
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+90), (sShowID.posX, sShowID.posY), 3)

            InsShowVel = PanelFont.render("b) Show velocity - View the velocity of each object", 1, black)
            display.blit(InsShowVel, (pInstructions.posX+20, pInstructions.posY+120))
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+120), (sShowVel.posX, sShowVel.posY), 3)

            InsShowFor = PanelFont.render("c) Show net force - View the net force acting on each object", 1, black)
            display.blit(InsShowFor, (pInstructions.posX+20, pInstructions.posY+150))
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+150), (sShowFor.posX, sShowFor.posY), 3)

            #Info panel instructions
            InsInfo = PanelFont.render("2) Information Panel - This lets you vie information about the current time in the simulation", 1, black)
            display.blit(InsInfo, (pInstructions.posX+5, pInstructions.posY+300))
            pygame.draw.line(display, black, (pInstructions.posX+5, pInstructions.posY+300), (pInfo.posX, pInfo.posY), 3)

            InsCurrRad =  PanelFont.render("a) Current radius is the radius of the pointer used to insert objects in m", 1, black)
            display.blit(InsCurrRad, (pInstructions.posX+20, pInstructions.posY+330))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+330), (50, 50+int(height/2)), 3)

            InsCurrDens =  PanelFont.render("b) Current density is the density selected for the next object in Kg/m^3", 1, black)
            display.blit(InsCurrDens, (pInstructions.posX+20, pInstructions.posY+360))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+360), (50, 100+int(height/2)), 3)

            InsCurrScale = PanelFont.render("c) Current Scale is the number of meters in a pixel", 1, black)
            display.blit(InsCurrScale, (pInstructions.posX+20, pInstructions.posY+390))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+390), (50, 150+int(height/2)), 3)

            InsCurrTime = PanelFont.render("d) Current speed of time is how quickly the simulation is going", 1, black)
            display.blit(InsCurrTime, (pInstructions.posX+20, pInstructions.posY+410))
            pygame.draw.line(display, black, (pInstructions.posX+20, pInstructions.posY+410), (50, 200+int(height/2)), 3)

            #Time Panel instructions
            InsTime = PanelFont.render("3) Time Panel - adjust the flow of time", 1, black)
            display.blit(InsTime, (pInstructions.posX+5, pInstructions.posY+500))
            pygame.draw.line(display, black, (pInstructions.posX+5, pInstructions.posY+510), (pTime.posX, pTime.posY), 3)

            InsPause = PanelFont.render("a) Pause/Play switch - stop and start the flow of time", 1, black)
            display.blit(InsPause, (pInstructions.posX+20, pInstructions.posY+530))
            pygame.draw.line(display, green, (pInstructions.posX+20, pInstructions.posY+540), (sPausePlay.posX+30, sPausePlay.posY), 3)

            InsReset = PanelFont.render("b) Reset button - deletes all objects on the screen", 1, black)
            display.blit(InsReset, (pInstructions.posX+35, pInstructions.posY+560))
            pygame.draw.line(display, red, (pInstructions.posX+35, pInstructions.posY+570), (bReset.posX+30, bReset.posY), 3)

            InsIncrease = PanelFont.render("c) >>+ - speed up the flow of time", 1, black)
            display.blit(InsIncrease, (pInstructions.posX+50, pInstructions.posY+590))
            pygame.draw.line(display, cyan, (pInstructions.posX+50, pInstructions.posY+600), (bIncrease.posX+30, bIncrease.posY), 3)

            InsDecrease = PanelFont.render("d) >>- - slow down the flow of time", 1, black)
            display.blit(InsDecrease, (pInstructions.posX+65, pInstructions.posY+620))
            pygame.draw.line(display, cyan, (pInstructions.posX+65, pInstructions.posY+630), (bDecrease.posX+30, bDecrease.posY), 3)

        colour14, bInstructions2clicked = bInstructions2.buttonClicked(clicked, X, Y)
        bInstructions2.displayButton(colour14)

        if bInstructions2clicked:
            pInstructions.displayPanel()

            Ins1 = PanelFont.render("How to use the simulation:", 1, black)
            display.blit(Ins1, (pInstructions.posX+5, pInstructions.posY+30))

            Ins2 = PanelFont.render("1) Move the mouse over the black simulation screen. you should see a blue circle where the mouse is.", 1, black)
            display.blit(Ins2, (pInstructions.posX+5, pInstructions.posY+60))

            Ins3 = PanelFont.render("2) Use the scroll wheel to change the size of the blue circle", 1, black)
            display.blit(Ins3, (pInstructions.posX+5, pInstructions.posY+90))

            Ins4 = PanelFont.render("3) Left click on the simulation screen to add an object the same size as the blue circle", 1, black)
            display.blit(Ins4, (pInstructions.posX+5, pInstructions.posY+120))

            Ins5 = PanelFont.render("4) Left click and drag on the simulation screen to adjust the object's initial velocity", 1, black)
            display.blit(Ins5, (pInstructions.posX+5, pInstructions.posY+150))

            Ins6 = PanelFont.render("5) You can add multiple objects into the simulation at a time. They will automatically iteract by gravity", 1, black)
            display.blit(Ins6, (pInstructions.posX+5, pInstructions.posY+180))

            Ins7 = PanelFont.render("6) Holding down shift and z will let you zoom in and out by using the scroll wheel", 1, black)
            display.blit(Ins7, (pInstructions.posX+5, pInstructions.posY+210))

            Ins8 = PanelFont.render("7) Holding down shift and d will let you change the density of the next object using the scroll wheel", 1, black)
            display.blit(Ins8, (pInstructions.posX+5, pInstructions.posY+240))

        if bMainMenuClicked:
            done = False
            while not done:
                for event in pygame.event.get():
                    if event.type == quit:
                        pygame.quit()
                        sys.exit()
                X = list(pygame.mouse.get_pos())[0]#gets x coordinate of mouse
                Y = list(pygame.mouse.get_pos())[1]#gets y coordinate of mouse
                clicked = list(pygame.mouse.get_pressed())[0]
                pExit.displayPanel()

                colour8, bCancelClicked = bCancel.buttonClicked(clicked, X, Y)
                bCancel.displayButton(colour8)

                colour9, bDontSaveClicked = bDontSave.buttonClicked(clicked, X ,Y)
                bDontSave.displayButton(colour9)

                colour10, bSaveClicked = bSave.buttonClicked(clicked, X, Y)
                bSave.displayButton(colour10)

                if bCancelClicked:
                    done = True
                    cancelText = PanelFont.render("ok", 1, grey1)
                    display.blit(cancelText, (width/2, height/2))
                elif bDontSaveClicked:
                    dontSaveText = PanelFont.render("ok", 1, grey1)
                    display.blit(dontSaveText, (width/2, height/2))
                    done = True
                    inMainMenu = True
                    objects = []
                    number = 0
                elif bSaveClicked:
                    
                    done = True
                    file = open("saves\\NumberOfSaves.txt", "r")
                    FileID = str(int(file.readline())+1)
                    FileName = "simulation" + FileID
                    file = open("saves\\NumberOfSaves.txt", "w")
                    file.write(FileID)
                    file.close()
                    file = open("saves\\"+FileName+".txt", "w")
                    data = []
                    for item in objects:
                        data.append([item.ID, item.metricMass, item.metricPosX, item.metricPosY, item.velX, item.velY, item.density])
                    file.write(str(data))
                    file.close()
                    SaveText = PanelFont.render("saving as: "+FileName, 1, grey1)
                    display.blit(SaveText, (width/2-100, height/2))

                    inMainMenu = True
                    objects = []
                    number = 0
                else:
                    promptText = PanelFont.render("Do you want to save this siulation?", 1, grey1)
                    display.blit(promptText, (width/2-100, height/2))
                pygame.display.update()
                FPSClock.tick(FPS)
            time.sleep(1.5)
        if clicked:
            ClickedLastFrame = True
        else:
            ClickedLastFrame = False
        pygame.display.update()
        FPSClock.tick(FPS)