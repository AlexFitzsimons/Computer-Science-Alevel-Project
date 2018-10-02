####physics program

##importing required libraries
import sys
import random
import time
import math
import pygame
import os


print("version 4")

###getting pygame ready
##initialising pygame
pygame.init()

##defining the pyagame display
width = ((pygame.display.Info()).current_w)#sets display width to the screen's width resolution
height = ((pygame.display.Info()).current_h)#sets display height to the screen's height resolution
display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)



metersPerPixel = 500000

icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)
icon = pygame.transform.scale(icon, (30, 30))
EAEarth = pygame.transform.scale(pygame.image.load('europe-african-Globe.png'), (int((2*6371000)/metersPerPixel), int((2*6371000)/metersPerPixel)))
AmEarth = pygame.transform.scale(pygame.image.load('American-Globe.png'), (int((2*6371000)/metersPerPixel), int((2*6371000)/metersPerPixel)))
AsEarth = pygame.transform.scale(pygame.image.load('asian-Globe.png'), (int((2*6371000)/metersPerPixel), int((2*6371000)/metersPerPixel)))


##setting up the timing
FPS = 120
FPSClock = pygame.time.Clock()

##predefining colours for later
white = (255, 255, 255)
grey1 = (192, 192, 192)
grey2 = (128, 128, 128)
grey3 = (64, 64, 64)
grey4 = (32, 32, 32)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
orange = (255, 128, 64)

G = 6.67*(10**(-11))

pygame.font.init()

ButtonFont = pygame.font.SysFont("Consolas", 15)
PanelFont = pygame.font.SysFont("Consolas", 16)
SwitchFont = pygame.font.SysFont("Consolas", 14)
InputBoxFont = pygame.font.SysFont("Consolas", 13)
ObjectFont = pygame.font.SysFont("Consolas", 12)

def Positions():

    return X, Y

###the class that defines the button
class Button: 
    ##Initialisation function
    def __init__(self, name, colour, posX, posY, sizeX, sizeY):
        self.name = name
        self.colour = colour
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY
    ##Function to display the button
    def displayButton(self, newColour):
        pygame.draw.rect(display, newColour, ((self.posX, self.posY), (self.sizeX, self.sizeY)))#draws the main rectangular part of the button
        ButtonText = ButtonFont.render(self.name, 1, black)#defines the text to be put on the button
        adjustBy = len(self.name)#adjusting the position of the text on the button depending on the buttons length
        display.blit(ButtonText, ((0.5*self.sizeX)+self.posX-(4*adjustBy), (0.5*self.sizeY)+self.posY-10))
    
    ##function to detect if the mouse if over the button and if it has been clicked 
    def buttonClicked(self, clicked, X, Y):
        if (X >= self.posX) and (X <= (self.posX+self.sizeX)) and (Y >= self.posY) and (Y <= (self.posY+self.sizeY)) and clicked:
            return white, True#button is clicked
        elif (X >= self.posX) and (X <= (self.posX+self.sizeX)) and (Y >= self.posY) and (Y <= (self.posY+self.sizeY)):
            return white, False#button is not clicked but the mouse is on the button
        else:
            return self.colour, False#mouse not on button

###the class that defines the panel
class Panel:
    ##initialisation function
    def __init__(self, type, colour, posX, posY, sizeX, sizeY):
        self.type = type
        self.colour = colour
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY

    #Function to display panel
    def displayPanel(self):
        pygame.draw.rect(display, self.colour, ((self.posX, self.posY), (self.sizeX, self.sizeY)))
        PanelText = PanelFont.render(self.type, 1, grey1)
        if self.sizeX > 0:
            invertX = 0
        else:
            invertX = self.sizeX
        if self.sizeY > 0:
            invertY = 0
        else:
            invertY = self.sizeY
        display.blit(PanelText, (self.posX+4+invertX, self.posY+invertY))
###the class that defines the switch
class Switch:
    ##initialisation function
    def __init__(self, name, colour, posX, posY, state, On, Off):
        self.name = name
        self.colour = colour
        self.posX = posX
        self.posY = posY
        self.state = state
        self.wasClicked = False
        self.On = On
        self.Off = Off

    ##Function to display the switch
    def displaySwitch(self):
        pygame.draw.rect(display, grey3, (self.posX-2, self.posY-2, 86, 44))
        if not self.state:
            pygame.draw.rect(display, self.colour, (self.posX, self.posY, 50, 40))
            textState = self.Off
            SwitchText1 = ButtonFont.render((self.Off), 1, grey1)
            display.blit(SwitchText1, (self.posX+55, self.posY+10))
        else:
            pygame.draw.rect(display, white, (self.posX+32, self.posY, 50, 40))
            textState = self.On
            SwitchText1 = ButtonFont.render((self.On), 1, grey1)
            display.blit(SwitchText1, (self.posX+10, self.posY+10))
        SwitchText2 = ButtonFont.render((self.name + ":"), 1, grey1)
        display.blit(SwitchText2, (self.posX, self.posY-25))

###the class that defines the number input box

defaultTimeinterval = 10000/FPS
centerX = width/3
centerY = height/3
###the class that defines the objects in the simulation
class Object():
    def __init__(self, ID, colour, radius, posX, posY, velX, velY, density):

        self.ID = ID
        self.colour = colour
        self.drawRadius = radius
        self.drawPosX = posX
        self.drawPosY = posY
        self.velX = velX
        self.velY = velY
        self.netX = 0
        self.netY = 0
        self.density = density
        self.metricPosX = metersPerPixel*self.drawPosX
        self.metricPosY = metersPerPixel*self.drawPosY
        self.metricRadius = metersPerPixel*self.drawRadius
        self.metricMass = math.pi*(4/3)*(self.metricRadius**3)*self.density


    def displayObject(self):
        pygame.draw.circle(display, self.colour, (round(self.drawPosX+centerX), round(self.drawPosY+centerY)), round(self.drawRadius))

    def showID(self):
        ObjectText = ObjectFont.render(str(self.ID), 1, red)
        display.blit(ObjectText, (self.drawPosX-5+centerX, self.drawPosY-5+centerY))

    def updateUnits(self):
        self.metricRadius = ((3*self.metricMass)/(4*math.pi*self.density))**(1/3)
        self.drawRadius = self.metricRadius/metersPerPixel
        self.drawPosX = self.metricPosX/metersPerPixel
        self.drawPosY = self.metricPosY/metersPerPixel
    
    def showSelected(self):
        pygame.draw.circle(display, orange, (int(round(self.drawPosX+centerX)), int(round(self.drawPosY+centerY))), int(round(self.drawRadius)), 3)

    def changePos(self):
        self.metricPosX += (self.velX*defaultTimeinterval)
        self.metricPosY += (self.velY*defaultTimeinterval)
        self.drawPosX = self.metricPosX/metersPerPixel
        self.drawPosY = self.metricPosY/metersPerPixel

    def bounce(self, leftEdge, topEdge, rightEdge, lowerEdge, bounce):     
        if bounce:
            if (self.drawPosX+self.drawRadius)>=rightEdge:
                self.velX = -self.velX
            if (self.drawPosX-self.drawRadius)<=leftEdge:
                self.velX = -self.velX
            if (self.drawPosY+self.drawRadius)>=lowerEdge:
                self.velY = -self.velY
            if (self.drawPosY-self.drawRadius)<=topEdge:
                self.velY = -self.velY

class ImageObject():
    def __init__(self, ID, type, posX, posY, velX, velY, density):
        self.ID = ID
        self.drawPosX = posX
        self.drawPosY = posY
        self.velX = velX
        self.velY = velY
        self.netX = 0
        self.netY = 0
        self.density = density
        self.metricPosX = metersPerPixel*posX
        self.metricPosY = metersPerPixel*posY
        self.type = type
        self.collided = False
        if self.type == "earth":
            OneInThree  =random.randint(1, 3)
            if OneInThree == 1:
                self.image = EAEarth
            elif OneInThree == 2:
                self.image = AmEarth
            else:
                self.image = AsEarth
            self.metricRadius = 6371000
        self.drawRadius = self.metricRadius/metersPerPixel
        self.metricMass = math.pi*(4/3)*(self.metricRadius**3)*self.density


    def displayObject(self):
        if self.collided:
            pygame.draw.circle(display, grey1, (round(self.drawPosX+centerX), round(self.drawPosY+centerY)), round(self.drawRadius))
        else:
            display.blit(self.image, (round(self.drawPosX+centerX-self.drawRadius), round(self.drawPosY+centerY-self.drawRadius)))
    def showID(self):
        ObjectText = ObjectFont.render(str(self.ID), 1, red)
        display.blit(ObjectText, (self.drawPosX-5+centerX, self.drawPosY-5+centerY))

    def updateUnits(self):
        self.metricRadius = ((3*self.metricMass)/(4*math.pi*self.density))**(1/3)
        self.drawRadius = self.metricRadius/metersPerPixel
        self.drawPosX = self.metricPosX/metersPerPixel
        self.drawPosY = self.metricPosY/metersPerPixel
    
    def showSelected(self):
        pygame.draw.circle(display, orange, (int(round(self.drawPosX+centerX)), int(round(self.drawPosY+centerY))), int(round(self.drawRadius)), 3)

    def changePos(self):
        self.metricPosX += (self.velX*defaultTimeinterval)
        self.metricPosY += (self.velY*defaultTimeinterval)
        self.drawPosX = self.metricPosX/metersPerPixel
        self.drawPosY = self.metricPosY/metersPerPixel

    def bounce(self, leftEdge, topEdge, rightEdge, lowerEdge, bounce):     
        if bounce:
            if (self.drawPosX+self.drawRadius)>=rightEdge:
                self.velX = -self.velX
            if (self.drawPosX-self.drawRadius)<=leftEdge:
                self.velX = -self.velX
            if (self.drawPosY+self.drawRadius)>=lowerEdge:
                self.velY = -self.velY
            if (self.drawPosY-self.drawRadius)<=topEdge:
                self.velY = -self.velY

###function to call for exiting the program
def exiting(exit):
    if exit:
        pygame.quit()
        sys.exit()

###GUIs

##panels
pTools = Panel("Tools", grey2, 5, 34, int(width/8), int(height/2))
pInfo = Panel("Info", grey2, 5, 36+int(height/2), int(width/8), int(height/2)-46)
pSimulation = Panel("Simulation", black, int((width/8)+7), 34, int(width/2), 4*height/5+40)
pTime = Panel("Time", grey2, int((width/8)+7), height-11, int(width/2), -152)

topGraph = 34
leftGraph = int(((5*width)/8)+9)
rightGraph = int(((5*width)/8)+9)+int(((3*width)/8)-12)
bottomGraph = int(height/2+34)

pGraph = Panel("Graph 1", white, leftGraph, topGraph, rightGraph-leftGraph, bottomGraph-topGraph)
pExit = Panel("Exit", grey4, int((width/2)-300), int((height/2)-100), 600, 300)
pLearn = Panel("Learn", grey2, int(((5*width)/8)+9), (height/2)+36, int(((3*width)/8)-12), (height/2)-46)
pInstructions = Panel ("instructions", white, int((width/8)+7), 34, int(width/2), 4*height/5+40)

##buttons
bExit = Button("x", red, width-52, 1, 50, 30)
bMin = Button("_", grey1, width-103, 1, 50, 30)
bEnter = Button("Enter", grey2, (width/2)-150, (height/2)-40, 100, 80)
bOpen = Button("Open", grey2, width/2, (height/2)-40, 100, 80)

bMainMenu = Button("Exit", grey2, 36, 3, 50, 26)
bInstructions = Button("Instructions", grey2, 100, 3, 120, 26)

bReset = Button("reset", red, int((width/8)+111), height-115, 86, 44)
bIncrease = Button(">>+", cyan, int((width/8)+202), height-115, 86, 44)
bDecrease = Button(">>-", cyan, int((width/8)+290), height-115, 86, 44)

bSave = Button("save", green, int((width/2)-250), int((height/2)+100), 100, 50)
bDontSave = Button("Dont save", red, int((width/2)-50), int((height/2)+100), 100, 50)
bCancel = Button("Cancel", grey3, int((width/2)+150), int((height/2)+100), 100, 50)

##switches
sBounce = Switch("Bounce", blue, 10, 100, False, "on", "off")#switch to turn on and off bounce
sPausePlay = Switch("||/>", green, int((width/8)+11), height-115, False, "||", " >")#switch to pause and play
sShowID = Switch("Show ID", yellow,  10, 200, False, "on", "off")
sShowVel = Switch("Show Velocity", yellow, 10, 300, False, "on", "off")
sShowFor = Switch("Show net Force", yellow, 10, 400, False, "on", "off")
switches = [sBounce, sPausePlay, sShowID, sShowVel, sShowFor]


##assembling the Window GUI
def WindowGUI(clicked, X, Y):
    pygame.draw.rect(display, black, (0,0,width,32))
    pygame.draw.line(display, black, (0,0), (0, height), 2)
    pygame.draw.line(display, black, (width,0), (width, height), 2)
    pygame.draw.line(display, black, (0,height), (width, height), 18)
    pygame.Surface.blit(display, icon, (0,0))
    colour1, bExitClicked = bExit.buttonClicked(clicked, X, Y)
    colour2, bMinClicked = bMin.buttonClicked(clicked, X, Y)
    bMin.displayButton(colour2)
    bExit.displayButton(colour1)
    exiting(bExitClicked)
    if bMinClicked:
        pygame.display.iconify()

def background():
    pygame.draw.rect(display, grey1, (0, 0, width, 34))
    pygame.draw.rect(display, grey1, (0, 0, int((width/8)+7),height))
    pygame.draw.rect(display, grey1, (0, height, width, -165))
    pygame.draw.rect(display, grey1, (width, 0, -int(((3*width)/8)-8), height))

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
    rightClicked = False
    wasRightClicked = False
    number = 0
    heldD=0
    heldI=0
    ClickedLastFrame = False
    rightClickedLastFrame = False
    count = 0
    opening = False
    fileNames = []
    buttons = []
    data = []
    fileNames = os.listdir("saves\\")
    fileNames.remove("NumberOfSaves.txt")
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
        WindowGUI(clicked, X, Y)

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
        metricradius = (((3*item[1])/(4*math.pi*item.density))**(1/3))
        Radius = metricradius/metersPerPixel
        objects.append(Object(item[0], grey1, Radius, (item[2]/metersPerPixel)-centerX, (item[3]/metersPerPixel)-centerY, item[4], item[5], 1))
    
    ##simulation
    zoom = False
    changeDensity = False
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

        ##counting for slower animation
        count += 1

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

                        force = G*(self.metricMass*other.metricMass)/(distance**2)
                        acc = force/self.metricMass



                        self.netX = (x/distance * force)/(10**22)
                        self.netY = (y/distance * force)/(10**22)

                        self.velX -= acc * (x/distance) * defaultTimeinterval
                        self.velY -= acc * (y/distance) * defaultTimeinterval

                        momentumX = self.velX*self.metricMass + other.velX*other.metricMass
                        momentumY = self.velY*self.metricMass + other.velY*other.metricMass

                        if distance <= (self.metricRadius + other.metricRadius):
                            combinedDensity = (self.density+other.density)/2
                            if self.metricRadius > other.metricRadius:
                                self.metricMass += other.metricMass
                                objects.remove(other)
                                self.density = combinedDensity
                                self.velX = momentumX/self.metricMass
                                self.velY = momentumY/self.metricMass
                                try:
                                    self.collided = True
                                except:
                                    pass
                            else:
                                other.metricMass += self.metricMass
                                objects.remove(self)
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
            self.bounce(leftEdge, topEdge, rightEdge, lowerEdge, sBounce.state)
            if sShowVel.state:
                pygame.draw.line(display, magenta, (int(self.drawPosX+centerX), int(self.drawPosY+centerY)), (int(self.drawPosX+(self.velX/10)+centerX), int(self.drawPosY+(self.velY/10)+centerY)))
            if sShowFor.state:
                print(self.netX, self.netY)
                pygame.draw.line(display, cyan, (self.drawPosX+centerX, self.drawPosY+centerY), ((int(self.drawPosX-self.netX)+centerX), int(self.drawPosY-self.netY)+centerY), 2)
            if sShowID.state:
                self.showID()
            self.netX = 0
            self.netY = 0

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
                    objects.append(Object(number, grey1, int(newRadius), initialX-centerX, initialY-centerY, (initialX-X), (initialY-Y), newDensity))
                    number += 1
            elif not clicked and not ClickedLastFrame:
                ClickedLastFrame = False

            if rightClicked and not rightClickedLastFrame:
                rightClickedLastFrame = True
                initialY = Y+0
                initialX = X+0
            elif rightClicked and rightClickedLastFrame:
                rightClickedLastFrame = True
                pygame.draw.circle(display, grey1, (initialX, initialY), int(newRadius))
                pygame.draw.line(display, green, (initialX, initialY), (X, Y), 3)
                pygame.draw.circle(display, yellow, (X, Y), int(newRadius), 2)
            elif not rightClicked and rightClickedLastFrame:
                rightClickedLastFrame = False
                if newRadius < 150 and newRadius > 3:
                    objects.append(ImageObject(number, "earth", initialX-centerX, initialY-centerY, (initialX-X), (initialY-Y), 5500))
                    number += 1
            elif not rightClicked and not rightClickedLastFrame:
                rightClickedLastFrame = False

        

        background()

        pTools.displayPanel()        
        pInfo.displayPanel()
        pTime.displayPanel()
        pGraph.displayPanel()
        pLearn.displayPanel()

        ##displaying the switches
        for switch in switches:
            if clicked and X>(switch.posX-2) and Y>(switch.posY-2) and X<(switch.posX+82) and Y<(switch.posY+42):
                switch.wasClicked = True
            elif switch.wasClicked and not clicked:
                switch.state = not switch.state
                switch.wasClicked = False
            switch.displaySwitch()

        paused = sPausePlay.state

            
        radiusLabel = PanelFont.render("Current Radius:", 1, black)
        radiusInfo = PanelFont.render("  " + str(int(metersPerPixel*newRadius)) + " m", 1, black)
        densityLabel = PanelFont.render("Current Density:", 1, black)
        densityInfo = PanelFont.render("  " + str(int(newDensity))+" Kg/m^3", 1, black)
        scaleLabel = PanelFont.render("Current Scale:", 1, black)
        scaleInfo = PanelFont.render("  " + str(int(metersPerPixel))+" meters per pixel", 1, black)
        
        display.blit(radiusLabel, (8, 50+int(height/2)))
        display.blit(radiusInfo, (8, 70+int(height/2)))
        display.blit(densityLabel, (8, 100+int(height/2)))
        display.blit(densityInfo, (8, 120+int(height/2)))
        display.blit(scaleLabel, (8, 150+int(height/2)))
        display.blit(scaleInfo, (8, 170+int(height/2)))


        colour5, bResetClicked = bReset.buttonClicked(clicked, X, Y) 
        bReset.displayButton(colour5)
        if bResetClicked:
            objects = []
            number = 0
            newDensity = 5500
            newRadius = 10
        
        colour6, bIncreaseClicked = bIncrease.buttonClicked(clicked, X, Y)
        bIncrease.displayButton(colour6)
        
        if bIncreaseClicked and (heldI == 0 or heldI > FPS):
            defaultTimeinterval *= 2
            heldI+=1
        elif not bIncreaseClicked:
            heldI=0

        colour7, bDecreaseClicked = bDecrease.buttonClicked(clicked, X, Y)
        bDecrease.displayButton(colour7)
        if bDecreaseClicked and (heldD == 0 or heldD > FPS):
            defaultTimeinterval /= 2
            heldD+=1
        elif not bDecreaseClicked:
            heldD=0

        speedvalue = ButtonFont.render("x"+str(int(round(FPS*defaultTimeinterval, 3))), 1, black)
        display.blit(speedvalue, (bDecrease.posX+bDecrease.sizeX+4, bDecrease.posY))

        WindowGUI(clicked, X, Y)
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

            InsBounce = PanelFont.render("a) Bounce - Toggle weather or not the objects bounce off the sides of the simulation panel", 1, black)
            display.blit(InsBounce, (pInstructions.posX+20, pInstructions.posY+60))
            pygame.draw.line(display, blue, (pInstructions.posX+20, pInstructions.posY+60), (sBounce.posX, sBounce.posY), 3)

            InsShowID = PanelFont.render("b) Show ID - View the ID of each object", 1, black)
            display.blit(InsShowID, (pInstructions.posX+20, pInstructions.posY+90))
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+90), (sShowID.posX, sShowID.posY), 3)

            InsShowVel = PanelFont.render("c) Show velocity - View the velocity of each object", 1, black)
            display.blit(InsShowVel, (pInstructions.posX+20, pInstructions.posY+120))
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+120), (sShowVel.posX, sShowVel.posY), 3)

            InsShowFor = PanelFont.render("c) Show net force - View the net force acting on each object", 1, black)
            display.blit(InsShowFor, (pInstructions.posX+20, pInstructions.posY+150))
            pygame.draw.line(display, yellow, (pInstructions.posX+20, pInstructions.posY+150), (sShowFor.posX, sShowFor.posY), 3)

            #Info panel instructions
            InsInfo = PanelFont.render("2) Information Panel - This lets you vie information about the current time in the simulation", 1, black)
            display.blit(InsInfo, (pInstructions.posX+5, pInstructions.posY+200))
            pygame.draw.line(display, black, (pInstructions.posX+5, pInstructions.posY+200), (pInfo.posX+40, pInfo.posY), 3)

            InsCurrRad =  PanelFont.render("a) Current radius is the radius of the pointer used to insert objects", 1, black)
            display.blit(InsCurrRad, (pInstructions.posX+20, pInstructions.posY+230))
            #pygame.draw.line(display, )



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
                        data.append([item.ID, item.metricMass, item.metricPosX, item.metricPosY, item.velX, item.velY])
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
            time.sleep(2)
        pygame.display.update()
        FPSClock.tick(FPS)