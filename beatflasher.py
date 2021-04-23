import math
import os
import tkinter as tk
import time
from cmu_112_graphics import *

###################################################
# Common Helpers
###################################################

def commonKeyPressed(app, event):
    if event.key == "M" or event.key == "m":
        app.mode = "menuMode"
    elif event.key == "L" or event.key == "l":
        app.mode = "levelSelectMode"
    elif event.key == "I" or event.key == "i":
        app.mode = "instructionMode"
    elif event.key == "S" or event.key == "s":
        app.mode = "scoreMode"
    elif event.key == "H" or event.key == "h":
        app.displayHelp = not app.displayHelp

def switchMode(app, mode):
    if mode == "levelSelectMode":
        refreshLevelList(app)
        app.levelPage = 1
    app.mode = mode

def drawHelpText(app, canvas):
    canvas.create_text(app.width//2, app.height - 30, 
            text="Click 'H' to open shortcuts page.", font="Arial 10 bold")

def drawHelp(app, canvas):
    if app.displayHelp:
        canvas.create_rectangle(30, 30, app.width - 30, app.height - 30, fill="white")

def drawTitle(app, canvas, text):
    canvas.create_text(app.width/2, 30, text=text, 
                        font="Arial 30 bold")

###################################################
# Menu Mode 
###################################################

def getMenuButtonLocation(app, i):
    topY = app.height // 2
    height = 30
    width = 150
    yGap = 10
    x1 = (app.width - width) // 2
    x2 = (app.width + width) // 2
    y1 = i * (height + yGap) + topY
    y2 = y1 + height
    return (x1, y1, x2, y2)

def getClickedMenuButton(app, x, y):
    for i in range(len(app.menuButtons)):
        (x1, y1, x2, y2) = getMenuButtonLocation(app, i)
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            return app.menuButtons[i]
    return None

def menuMode_mousePressed(app, event):
    clickedButton = getClickedMenuButton(app, event.x, event.y)
    if clickedButton != None:
        text, mode = clickedButton
        switchMode(app, mode)

def menuMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def drawMenuTitle(app, canvas):
    canvas.create_text(app.width/2, 30, text="Beat Flasher", 
                        fill="red", font="Arial 30 bold")
    canvas.create_text(app.width/2, 30, text="Beat Flasher", 
                        fill="white", font="Arial 28 bold")

def drawMenuImage(app, canvas):
    pass

def drawMenuButtons(app, canvas):
    for i in range(len(app.menuButtons)):
        x1, y1, x2, y2 = getMenuButtonLocation(app, i)
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", width=2)
        canvas.create_text((x1 + x2)//2, (y1 + y2)//2, 
                text=app.menuButtons[i][0], font="Arial 15 bold")

def menuMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="black")
    drawMenuTitle(app, canvas)
    drawMenuImage(app, canvas)
    drawMenuButtons(app, canvas)
    drawHelpText(app, canvas)
    drawHelp(app, canvas)

###################################################
# Level Select Mode 
###################################################

def getLevelButtonLocation(app, i):
    topY = app.height // 3
    height = 30
    width = 150
    yGap = 10
    x1 = (app.width - width) // 2
    x2 = (app.width + width) // 2
    y1 = i * (height + yGap) + topY
    y2 = y1 + height
    return (x1, y1, x2, y2)

# def getClickedMenuButton(app, x, y):
#     for i in range(len(app.levelButtons)):
#         (x1, y1, x2, y2) = getLevelButtonLocation(app, i)
#         if (x1 <= x <= x2) and (y1 <= y <= y2):
#             return app.levelButtons[i]
#     return None

def refreshLevelList(app):
    app.levelList = []
    for filename in os.listdir("levels/"):
        splits = os.path.splitext(filename)
        if len(splits) == 2 and splits[1] == ".txt":
            app.levelList.append(splits[0])
    app.hasMultipleLevelPages = len(app.levelList) > app.levelsPerPage

def hasPrevLevelPage(app):
    return app.hasMultipleLevelPages and app.levelPage > 0

def hasNextLevelPage(app):
    return (app.hasMultipleLevelPages
                    and app.levelsPerPage * app.levelPage < len(app.levelList))

def drawLevelList(app, canvas):
    start = app.levelPage * app.levelsPerPage
    end = start + app.levelsPerPage
    levelsToDisplay = app.levelList[start:end]
    if hasPrevLevelPage(app):
        (x1, y1, x2, y2) = getLevelButtonLocation(app, 0)
        canvas.create_rectangle(x1, y1, x2, y2, width=2, fill='black')
        canvas.create_text((x1+x2)/2, (y1+y2)/2,
                            text='Previous Page', fill='white')
    for i in range(len(levelsToDisplay)):
        (x1, y1, x2, y2) = getLevelButtonLocation(app, i + 1)
        canvas.create_rectangle(x1, y1, x2, y2, width=2)
        canvas.create_text((x1+x2)/2, (y1+y2)/2, text=levelsToDisplay[i])
    if hasNextLevelPage(app):
        (x1, y1, x2, y2) = getLevelButtonLocation(app, len(levelsToDisplay) + 1)
        canvas.create_rectangle(x1, y1, x2, y2, width=2, fill='black')
        canvas.create_text((x1+x2)/2, (y1+y2)/2,
                            text='Next Page', fill='white')

def drawLevelSelectTitle(app, canvas):
    drawTitle(app, canvas, "Level Select")

def drawLevelSqs(app, canvas):
    pass

def levelSelectMode_mousePressed(app, event):
    pass

def levelSelectMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def levelSelectMode_redrawAll(app, canvas):
    drawLevelSelectTitle(app, canvas)
    drawHelpText(app, canvas)
    drawLevelList(app, canvas)

###################################################
# Instruction Mode 
###################################################

def drawInstructionsTitle(app, canvas):
    drawTitle(app, canvas, "Instructions")

def instructionMode_keyPressed(app, event):
    commonKeyPressed(app, event)




def instructionMode_redrawAll(app, canvas):
    drawInstructionsTitle(app, canvas)
    drawHelpText(app, canvas)

###################################################
# Score Mode 
###################################################

def drawScoresTitle(app, canvas):
    drawTitle(app, canvas, "Scores")

def scoreMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def scoreMode_redrawAll(app,canvas):
    drawScoresTitle(app, canvas)
    drawHelpText(app, canvas)
###################################################
# Game Page 
###################################################


###################################################
# Results Page 
###################################################


###################################################
# Main App 
###################################################

def appStarted(app):
    app.mode = "menuMode"
    createMenuButtons(app)
    app.displayHelp = False
    app.levelsPerPage = 5
   

def createMenuButtons(app):
    buttons = [("Select Level", "levelSelectMode"), 
                ("Instructions", "instructionMode"),
                ("Scores", "scoreMode")]
    app.menuButtons = buttons


runApp(width=500, height=500, mvcCheck=False)