import math
import os
import pygame
import shutil
import tkinter as tk
import time
from cmu_112_graphics import *

###################################################
# Citations
###################################################
# Fez Background Image: From https://wallhaven.cc/w/01qpg4
# Purp Background Animation: From https://www.videvo.net/video/glowing-purple-grid-lines-tracking-in/393674/
# Spacetri Background Image: From https://wallhaven.cc/w/427j60

###################################################
# Common Helpers
###################################################

def commonKeyPressed(app, event):
    if event.key == "M" or event.key == "m":
        loadMenu(app)
    elif event.key == "L" or event.key == "l":
        loadLevelSelect(app)
    elif event.key == "I" or event.key == "i":
        loadInstructions(app)
    elif event.key == "S" or event.key == "s":
        loadScoreMode(app)
    elif event.key == "E" or event.key == "e":
        loadSettingsMode(app)
    elif event.key == "H" or event.key == "h":
        app.displayHelp = not app.displayHelp

def drawHelpText(app, canvas):
    canvas.create_rectangle(app.width//2 - 110, app.height - 40, app.width// 2 + 110, app.height - 20, fill="grey")
    canvas.create_text(app.width//2, app.height - 30, 
            text="Click 'H' to open shortcuts page.", font="Arial 10 bold")

def drawHelp(app, canvas):
    if app.displayHelp:
        canvas.create_rectangle(30, 100, app.width - 30, app.height - 100, fill="lightGrey")
        helpLines = [
            "Press any of the following keys",
            "to jump around the app quickly:",
            "",
            "\t• 'M' = Menu Page",
            "\t• 'L' = Load Level Page",
            "\t• 'I' = Instructions Page",
            "\t• 'S' = Scores Page",
            "\t• 'E' = Settings Page",
            "\t• 'H' = Display this shortcuts dialogue",
        ]
        canvas.create_text(app.width//2, app.height//2, 
                          text="\n".join(helpLines), font="Arial 12 bold")

def drawTitle(app, canvas, text):
    canvas.create_text(app.width/2, 30, text=text, 
                        font="Audiowide 30 bold")

# From: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
class Sound(object):
    def __init__(self, path=None):
        self.path = path
        self.loops = 1
        if path != None:
            pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        if self.path != None:
            self.loops = loops
            pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        if self.path != None:
            pygame.mixer.music.stop()

###################################################
# Menu Mode 
###################################################

def loadMenu(app):
    app.menuButtons = [("Select Level", lambda: loadLevelSelect(app)), 
                       ("Instructions", lambda: loadInstructions(app)),
                       ("Scores", lambda: loadScoreMode(app))]
    app.mode = 'menuMode'
    loadBackgroundAnimation(app)

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
        text, action = clickedButton
        action()

def menuMode_timerFired(app):
    if app.backgroundIndex != None:
        app.backgroundIndex = (app.backgroundIndex + 1) % len(app.backgroundImages)

def menuMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def drawMenuTitle(app, canvas):
    canvas.create_text(app.width/2, 30, text="Keyboard Smasher", 
                        fill="red", font="Audiowide 30 bold")
    canvas.create_text(app.width/2, 30, text="Keyboard Smasher", 
                        fill="white", font="Audiowide 28 bold")

def drawMenuImage(app, canvas):
    left = app.width // 2 - 150
    right = app.width // 2 + 150
    step = (right - left) // 3
    y = 145
    app.shapeToDraw[app.shape](app, canvas, left, y, 'up')
    app.shapeToDraw[app.shape](app, canvas, left + step, y, 'down')
    app.shapeToDraw[app.shape](app, canvas, left + 2 * step, y, 'right')
    app.shapeToDraw[app.shape](app, canvas, left + 3 * step, y, 'left')

def drawMenuButtons(app, canvas):
    for i in range(len(app.menuButtons)):
        x1, y1, x2, y2 = getMenuButtonLocation(app, i)
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", width=2)
        canvas.create_text((x1 + x2)//2, (y1 + y2)//2, 
                text=app.menuButtons[i][0], font="Arial 15 bold")
def drawMenuBg(app, canvas):
    if app.background == None:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="black")
    else:
        canvas.create_image(app.width // 2, app.height // 2, 
                        image=app.backgroundImages[app.backgroundIndex])

def menuMode_redrawAll(app, canvas):
    drawMenuBg(app, canvas)
    drawMenuTitle(app, canvas)
    drawMenuImage(app, canvas)
    drawMenuButtons(app, canvas)
    drawHelpText(app, canvas)
    drawHelp(app, canvas)

###################################################
# Settings Mode 
###################################################

class RadioButton(object):
    def __init__(self, x, y, label, isEnabled, whenClicked):
        self.x = x
        self.y = y
        self.label = label
        self.isEnabled = isEnabled
        self.whenClicked = whenClicked
    
    def _getButtonLocation(self):
        x1 = self.x - 10
        y1 = self.y - 10
        x2 = self.x + 10
        y2 = self.y + 10
        return x1, y1, x2, y2

    def drawButton(self, canvas):
        x1, y1, x2, y2 = self._getButtonLocation()
        if self.isEnabled():
            fill = 'black'
        else:
            fill = 'white'
        canvas.create_rectangle(x1, y1, x2, y2, fill=fill, width=2)
        canvas.create_text(x2 + 5, (y1 + y2) // 2, text=self.label, anchor='w')

    def handleClick(self, x, y):
        x1, y1, x2, y2 = self._getButtonLocation()
        if x1 <= x <= x2 and y1 <= y <= y2:
            self.whenClicked()
    
    def handleKey(self, key):
        return False

class KeybindButton(object):
    def __init__(self, x, y, label, getBinding, setBinding):
        self.x = x
        self.y = y
        self.label = label
        self.getBinding = getBinding
        self.setBinding = setBinding
        self.isActive = False
    
    def _getButtonLocation(self):
        x1 = self.x - 25
        y1 = self.y - 15
        x2 = self.x + 25
        y2 = self.y + 15
        return x1, y1, x2, y2

    def drawButton(self, canvas):
        x1, y1, x2, y2 = self._getButtonLocation()
        if self.isActive:
            fill = 'lightGreen'
        else:
            fill = 'pink'
        canvas.create_rectangle(x1, y1, x2, y2, fill=fill, width=2)
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.getBinding())
        canvas.create_text(x2 + 5, (y1 + y2) // 2, text=self.label, anchor='w')

    def handleClick(self, x, y):
        x1, y1, x2, y2 = self._getButtonLocation()
        if x1 <= x <= x2 and y1 <= y <= y2:
            self.isActive = True
    
    def handleKey(self, key):
        if self.isActive:
            self.setBinding(key)
            self.isActive = False
            return True
        return False

def settingsMode_mousePressed(app, event):
    for button in app.settingsButtons:
        button.handleClick(event.x, event.y)

def settingsMode_keyPressed(app, event):
    keyHandledByButton = False
    for button in app.settingsButtons:
        if button.handleKey(event.key):
            keyHandledByButton = True
    if keyHandledByButton:
        return None
    commonKeyPressed(app, event)

def drawSettingsButtons(app, canvas):
    for button in app.settingsButtons:
        button.drawButton(canvas)

def drawRowLabels(app, canvas):
    def drawRowLabel(y, text):
        canvas.create_text(10, y, text=text, anchor='w', font='Arial 10 bold')
    drawRowLabel(100, 'Arrow Direction:')
    drawRowLabel(170, 'Arrow Speed:')
    drawRowLabel(240, 'Keybindings:')
    drawRowLabel(310, 'Arrow Shape:')
    drawRowLabel(380, 'Background:')

def settingsMode_redrawAll(app, canvas):
    drawTitle(app, canvas, 'Settings')
    drawRowLabels(app, canvas)
    drawSettingsButtons(app, canvas)
    drawHelpText(app, canvas)
    drawHelp(app, canvas)

def loadSettingsMode(app):
    app.mode = 'settingsMode'
    
    directionY = 100
    directionLeft = app.width // 2 - 100
    directionRight = app.width - 60
    directionStep = (directionRight - directionLeft) // 3
    def getDirectionIsEnabled(direction):
        def isEnabled():
            return app.travelDirection == direction
        return isEnabled
    def getDirectionWhenClicked(direction):
        def whenClicked():
            app.travelDirection = direction
        return whenClicked
    directionButtons = [
        RadioButton(directionLeft, directionY, 'Up', getDirectionIsEnabled('up'), getDirectionWhenClicked('up')),
        RadioButton(directionLeft + directionStep, directionY, 'Down', getDirectionIsEnabled('down'), getDirectionWhenClicked('down')),
        RadioButton(directionLeft + 2 * directionStep, directionY, 'Left', getDirectionIsEnabled('left'), getDirectionWhenClicked('left')),
        RadioButton(directionLeft + 3 * directionStep, directionY, 'Right', getDirectionIsEnabled('right'), getDirectionWhenClicked('right')),
    ]

    def getSpeedIsEnabled(speed):
        def isEnabled():
            return app.arrowSpeed == speed
        return isEnabled
    def getSpeedWhenClicked(speed):
        def whenClicked():
            app.arrowSpeed = speed
        return whenClicked
    speedY = 170
    speedLeft = app.width // 2 - 100
    speedRight = app.width - 60
    speedStep = (speedRight - speedLeft) // 4
    speedButtons = [
        RadioButton(speedLeft, speedY, '1', getSpeedIsEnabled(1), getSpeedWhenClicked(1)),
        RadioButton(speedLeft + speedStep, speedY, '2', getSpeedIsEnabled(2), getSpeedWhenClicked(2)),
        RadioButton(speedLeft + 2 * speedStep, speedY, '3', getSpeedIsEnabled(3), getSpeedWhenClicked(3)),
        RadioButton(speedLeft + 3 * speedStep, speedY, '4', getSpeedIsEnabled(4), getSpeedWhenClicked(4)),
        RadioButton(speedLeft + 4 * speedStep, speedY, '5', getSpeedIsEnabled(5), getSpeedWhenClicked(5)),
    ]

    keyY = 240
    keyLeft = app.width // 2 - 100
    keyRight = app.width - 80
    keyStep = (keyRight - keyLeft) // 3
    def getGetBinding(direction):
        def getBinding():
            for key in app.keyBinds:
                if app.keyBinds[key] == direction:
                    return key
            return None
        return getBinding
    def getSetBinding(direction):
        def setBinding(key):
            keyBindKeyToDelete = None
            for keyBindKey in app.keyBinds:
                if app.keyBinds[keyBindKey] == direction:
                    keyBindKeyToDelete = keyBindKey
            if keyBindKeyToDelete != None:
                del app.keyBinds[keyBindKeyToDelete]
            app.keyBinds[key] = direction
        return setBinding
    keyButtons = [
        KeybindButton(keyLeft, keyY, 'Left', getGetBinding('left'), getSetBinding('left')),
        KeybindButton(keyLeft + keyStep, keyY, 'Right', getGetBinding('right'), getSetBinding('right')),
        KeybindButton(keyLeft + 2 * keyStep, keyY, 'Up', getGetBinding('up'), getSetBinding('up')),
        KeybindButton(keyLeft + 3 * keyStep, keyY, 'Down', getGetBinding('down'), getSetBinding('down')),
    ]

    shapeY = 310
    shapeLeft = app.width // 2 - 100
    shapeRight = app.width - 60
    shapeStep = (shapeRight - shapeLeft) // 3
    def getShapeIsEnabled(shape):
        def isEnabled():
            return app.shape == shape
        return isEnabled
    def getShapeWhenClicked(shape):
        def whenClicked():
            app.shape = shape
        return whenClicked
    shapeButtons = [
        RadioButton(shapeLeft, shapeY, 'Arrow', getShapeIsEnabled('arrow'), getShapeWhenClicked('arrow')),
        RadioButton(shapeLeft + shapeStep, shapeY, 'Triangle', getShapeIsEnabled('triangle'), getShapeWhenClicked('triangle')),
        RadioButton(shapeLeft + 2 * shapeStep, shapeY, 'Square', getShapeIsEnabled('square'), getShapeWhenClicked('square')),
        RadioButton(shapeLeft + 3 * shapeStep, shapeY, 'Circle', getShapeIsEnabled('circle'), getShapeWhenClicked('circle')),
    ]

    backgroundDirs = os.listdir('bgs/')
    bgY = 380
    bgLeft = app.width // 2 - 100
    bgRight = app.width - 60
    bgStep = (bgRight - bgLeft) // (len(backgroundDirs))
    def getBgIsEnabled(i):
        def isEnabled():
            if i == None:
                return app.background == None
            return app.background == backgroundDirs[i]
        return isEnabled
    def getBgWhenClicked(i):
        def whenClicked():
            if i == None:
                app.background = None
                return None
            app.background = backgroundDirs[i]
        return whenClicked
    bgButtons = ([RadioButton(bgLeft, bgY, 'None', getBgIsEnabled(None), getBgWhenClicked(None))] +
        [RadioButton(bgLeft + (i + 1) * bgStep, bgY, backgroundDirs[i], getBgIsEnabled(i), getBgWhenClicked(i)) for i in range(len(backgroundDirs))])

    app.settingsButtons = directionButtons + speedButtons + keyButtons + shapeButtons + bgButtons

###################################################
# Level Select Mode 
###################################################

def loadLevelSelect(app):
    refreshLevelList(app)
    app.mode = "levelSelectMode"

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

# Fetches levels from current page to display as "buttons".
def fetchLevelsToDisplay(app):
    start = app.levelPage * app.levelsPerPage
    end = start + app.levelsPerPage
    app.levelsToDisplay = app.levelList[start:end]

# Handles determining which "button" was pressed including next/previous page
# "buttons".
def getClickedLevelButton(app, x, y):
    for i in range(len(app.levelsToDisplay)+2):
        (x1, y1, x2, y2) = getLevelButtonLocation(app, i)
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            if i == 0:
                if hasPrevLevelPage(app):
                    return i
                else:
                    return None
            if i == len(app.levelsToDisplay)+1:
                if hasNextLevelPage(app):
                    return i
                else:
                    return None
            if i - 1 < len(app.levelsToDisplay):
                return i
    return None

# Pulls list of relevant level files and populates a list of levels from the
# filenames.
def refreshLevelList(app):
    app.levelPage = 0
    app.levelList = []
    for filename in os.listdir("levels/"):
        splits = os.path.splitext(filename)
        if len(splits) == 2 and splits[1] == ".txt":
            app.levelList.append(splits[0])
    fetchLevelsToDisplay(app)
    app.hasMultipleLevelPages = len(app.levelList) > app.levelsPerPage

def hasPrevLevelPage(app):
    return app.hasMultipleLevelPages and app.levelPage > 0

def hasNextLevelPage(app):
    return (app.hasMultipleLevelPages
                and app.levelsPerPage * (app.levelPage+1) < len(app.levelList))

def drawLevelList(app, canvas):
    if hasPrevLevelPage(app):
        (x1, y1, x2, y2) = getLevelButtonLocation(app, 0)
        canvas.create_rectangle(x1, y1, x2, y2, width=2, fill='black')
        canvas.create_text((x1+x2)/2, (y1+y2)/2,
                            text='Previous Page', fill='white')
    for i in range(len(app.levelsToDisplay)):
        (x1, y1, x2, y2) = getLevelButtonLocation(app, i + 1)
        canvas.create_rectangle(x1, y1, x2, y2, width=2)
        canvas.create_text((x1+x2)/2, (y1+y2)/2, text=app.levelsToDisplay[i])
    if hasNextLevelPage(app):
        (x1, y1, x2, y2) = getLevelButtonLocation(app, len(app.levelsToDisplay) + 1)
        canvas.create_rectangle(x1, y1, x2, y2, width=2, fill='black')
        canvas.create_text((x1+x2)/2, (y1+y2)/2,
                            text='Next Page', fill='white')

def drawLevelSelectTitle(app, canvas):
    drawTitle(app, canvas, "Level Select")

def drawLevelCreationHelpText(app, canvas):
    canvas.create_text(app.width // 2, app.height // 5, text="Press 'C' to create your own level!", font='Arial 16')

def levelSelectMode_mousePressed(app, event):
    clicked = getClickedLevelButton(app, event.x, event.y)
    if clicked != None:
        if clicked == 0:
            app.levelPage -= 1 
            fetchLevelsToDisplay(app)
        elif clicked == len(app.levelsToDisplay)+1:
            app.levelPage += 1
            fetchLevelsToDisplay(app)
        else:
            loadLevel(app, app.levelsToDisplay[clicked-1])

def levelSelectMode_keyPressed(app, event):
    commonKeyPressed(app, event)
    if event.key == 'c' or event.key == 'C':
        loadLevelCreation(app)

def levelSelectMode_redrawAll(app, canvas):
    drawLevelSelectTitle(app, canvas)
    drawLevelCreationHelpText(app, canvas)
    drawLevelList(app, canvas)
    drawHelpText(app, canvas)
    drawHelp(app, canvas)

###################################################
# Level Creation Mode
###################################################

def promptForSong(app):
    app.song = app.getUserInput(('What song would you like to use? Enter a path. Press \'cancel\' to not use a song.\n'
                                 'Careful, if you get the filename wrong, the game will crash!!!'))
    if app.song != None:
        app.sound = Sound(app.song)

def loadLevelCreation(app):
    app.mode = 'levelCreation'
    app.paused = True
    app.readyToStart = True
    app.customLevel = []
    app.animationsToDisplay = []
    promptForSong(app)

def levelToString(level):
    result = ""
    for direction, startTime, endTime in level:
        result += (f'{direction},{startTime},'
                     f'{endTime if endTime != None else ""}\n')
    return result
    
def saveLevel(app):
    levelName = app.getUserInput('What would you like to name your level?')
    if (levelName == None):
        return None
    filename = f'levels/{levelName}.txt'
    f = open(filename, 'w')
    f.write(levelToString(app.customLevel))
    f.close()
    if app.song != None:
        extension = os.path.splitext(app.song)[-1]
        shutil.copyfile(app.song, f'songs/{levelName}{extension}')

def saveAndQuitLevelCreation(app):
    saveLevel(app)
    loadLevelSelect(app)

def levelCreation_keyPressed(app, event):
    if app.readyToStart:
        app.paused = False
        app.readyToStart = False
        app.startTime = time.time()
        if app.song != None:
            app.sound.start()
        return None
    if event.key in app.keyBinds:
        keyDirection = app.keyBinds[event.key]
        startAnimation(app, keyDirection)
        app.customLevel.append((keyDirection, time.time() - app.startTime, None))
    elif event.key == "S" or event.key == "s":
        app.sound.stop()
        saveAndQuitLevelCreation(app)

def levelCreation_timerFired(app):
    if app.paused:
        return None
    updateAnimations(app)
    if app.song != None and not app.sound.isPlaying():
        saveAndQuitLevelCreation(app)

def levelCreation_redrawAll(app, canvas):
    if app.readyToStart:
        canvas.create_text(app.width/2, app.height/2, 
                    text="Press any key to start.", font="Audiowide 20 bold")
        return None
    else:
        canvas.create_text(app.width/2, app.height/2, 
                    text=("Use your chosen direction keys to create arrow "
                     "patterns.\nPress 'S' to save and exit level creation."), 
                     font="Arial 12 bold")
        drawAnimations(app, canvas)
        return None


###################################################
# Instruction Mode 
###################################################

def loadInstructions(app):
    app.mode = 'instructionMode'
    app.currentInstructionIndex = 0
    app.instructions = [
        ('Instructions', ['To cycle through the different instructions pages,',
                          'please use the left and right arrow keys. If you’ve',
                          'reached the final page and click right again, you',
                          'will return to the main menu. The pages are as ',
                          'follows:',
                          '\t• Level Select',
                          '\t• Game Mode',
                          '\t• Results Page',
                          '\t• Level Creation',
                          '\t• High Scores',
                          '\t• Settings']),
        ('Select Level', ['All playable levels can be found on this page.',
                          'You are able to click on any level title to start',
                          'playing that level. Each page will hold up to five',
                          'titles. Feel free to click through the “next” and',
                          '“previous” pages to access other levels.',
                          '\nYou will also be able to access level creation',
                          'mode by clicking “C” or the settings page by',
                          'clicking “S”.']),
        ('Game Mode', ['Once you’ve selected your level, click any key to',
        'start the game.The game “board” is set up with a top bar that tracks',
        'your score over the course of the game, your combo count (which will',
        'reset when you miss an arrow), and a level progress tracker.',
        '\nTo score points, you must accurately line up the scrolling arrows',
        'with the corresponding static arrows by pressing the arrow key that',
        'matches that arrow’s direction at the correct time. The more accurate',
        'you are at lining up the arrows, the better your score is. Scoring',
        'works as follows:',
        '\t• Perfect (< 0.05 seconds): 10 points',
        '\t• Good (< 0.1 seconds): 5 points',
        '\t• Ok (> 0.1 seconds): 2 points',
        '\t• Miss( > 0.2 seconds): -5 points',
        '\t• Combo multiplier: score * 0.1, up to a max combo of 4x',
        '\nThe level will be completed if you successfully make it through the',
        'entire arrow pattern. Press Q during a level to return to menu.']),
        ('Results Page', ['The results page will provide an overview of the',
                          'level you just completed. It tracks your total',
                          'score, time spent in the level, your highest combo,',
                          'and the totals of each type of “accuracy”',
                          '(aka Perfect, Good, Ok, Miss).',
                          '\nYou will also see a graph that tracks two things',
                          'over the course of the level: your combo (in black)',
                          'and your total score (in blue).',
                          '\nFinally, you will have the opportunity to adjust',
                          'your game settings, replay that level, return to',
                          'the level select page, or save your score in',
                          'the high scores list.']),
        ('Level Creation', ['To access the Level Creation page, click "C" on',
                            'the Level Select screen. You will be prompted to',
                            'press any key to begin. Once you have, you will',
                            'then be able to press your assigned arrow keys',
                            'in whatever pattern you would like, and the app',
                            'will track it.',
                            "",
                            'When you are done creating your level, click "S"',
                            'and you will be able to name your level.',
                            'You will then be returned to the Select Level',
                            'page, where your masterpiece will be waiting to',
                            'be played!']),
        ('High Scores', ['You will be able to access the high scores lists of',
                         'every playable level within the app. Once you’ve',
                         'saved a score from your results page, head to the',
                         'high scores page and select the level title you’d',
                         'like to access. It will take you to the top 10',
                         'scores on that level.']),
        ('Settings', ['The settings page will allow you to customize many',
                      'parts of the game, including arrow direction (the',
                      'direction the arrows scroll across the page),',
                      'arrow speed (the speed at which the arrows scroll',
                      'across the page), key binds (want to use WASD instead',
                      'of arrow keys?), arrow shape, and backgrounds.'])
    ]

def drawInstructionsTitle(app, canvas):
    drawTitle(app, canvas, "Instructions")

def instructionMode_keyPressed(app, event):
    commonKeyPressed(app, event)
    if event.key == 'Left' and app.currentInstructionIndex > 0:
        app.currentInstructionIndex -= 1
    elif event.key == 'Right':
        if app.currentInstructionIndex == len(app.instructions) - 1:
            loadMenu(app)
        else:
            app.currentInstructionIndex += 1

def drawInstructionNavigation(app, canvas):
    canvas.create_text(app.width // 2, app.height // 5, text='Press the left and right arrow keys to change instruction pages.')
    canvas.create_text(app.width // 2, app.height // 5 + 20, text=f'Page: {app.currentInstructionIndex + 1} / {len(app.instructions)}')

def drawInstructions(app, canvas):
    instructionTitle, instructionLines = app.instructions[app.currentInstructionIndex]
    instructionText = "\n".join(instructionLines)
    canvas.create_text(app.width // 2, app.height // 5 + 50, text=instructionTitle, font='Audiowide 16 bold')
    canvas.create_text(app.width // 2, app.height // 5 + 100, text=instructionText, font='Arial 10', anchor="n")

def instructionMode_redrawAll(app, canvas):
    drawInstructionsTitle(app, canvas)
    drawInstructionNavigation(app, canvas)
    drawInstructions(app, canvas)
    #drawHelpText(app, canvas)
    drawHelp(app, canvas)

###################################################
# Score Mode 
###################################################

def loadScoreMode(app):
    refreshScoreLevelList(app)
    app.activeScorePage = None
    app.mode = "scoreMode"

def getScoreLevelButtonLocation(app, i):
    topY = app.height // 3
    height = 30
    width = 150
    yGap = 10
    x1 = (app.width - width) // 2
    x2 = (app.width + width) // 2
    y1 = i * (height + yGap) + topY
    y2 = y1 + height
    return (x1, y1, x2, y2)

# Fetches levels from current page to display as "buttons".
def fetchScoreLevelsToDisplay(app):
    start = app.scoreLevelPage * app.levelsPerPage
    end = start + app.levelsPerPage
    app.scoreLevelsToDisplay = app.scoreLevelList[start:end]

# Handles determining which "button" was pressed including next/previous page
# "buttons".
def getClickedScoreLevelButton(app, x, y):
    for i in range(len(app.scoreLevelsToDisplay)+2):
        (x1, y1, x2, y2) = getScoreLevelButtonLocation(app, i)
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            if i == 0:
                if hasPrevScoreLevelPage(app):
                    return i
                else:
                    return None
            if i == len(app.scoreLevelsToDisplay)+1:
                if hasNextScoreLevelPage(app):
                    return i
                else:
                    return None
            if i - 1 < len(app.scoreLevelsToDisplay):
                return i
    return None

# Pulls list of relevant level files and populates a list of levels from the
# filenames.
def refreshScoreLevelList(app):
    app.scoreLevelPage = 0
    app.scoreLevelList = []
    for filename in os.listdir("scores/"):
        splits = os.path.splitext(filename)
        if len(splits) == 2 and splits[1] == ".txt":
            app.scoreLevelList.append(splits[0])
    fetchScoreLevelsToDisplay(app)
    app.hasMultipleScoreLevelPages = len(app.scoreLevelList) > app.levelsPerPage

def hasPrevScoreLevelPage(app):
    return app.hasMultipleScoreLevelPages and app.scoreLevelPage > 0

def hasNextScoreLevelPage(app):
    return (app.hasMultipleScoreLevelPages
                and (app.levelsPerPage * 
                        (app.scoreLevelPage+1) < len(app.scoreLevelList)))

def drawScoreLevelList(app, canvas):
    if hasPrevScoreLevelPage(app):
        (x1, y1, x2, y2) = getScoreLevelButtonLocation(app, 0)
        canvas.create_rectangle(x1, y1, x2, y2, width=2, fill='black')
        canvas.create_text((x1+x2)/2, (y1+y2)/2,
                            text='Previous Page', fill='white')
    for i in range(len(app.scoreLevelsToDisplay)):
        (x1, y1, x2, y2) = getScoreLevelButtonLocation(app, i + 1)
        canvas.create_rectangle(x1, y1, x2, y2, width=2)
        canvas.create_text((x1+x2)/2, (y1+y2)/2, 
                          text=app.scoreLevelsToDisplay[i])
    if hasNextScoreLevelPage(app):
        (x1, y1, x2, y2) = getScoreLevelButtonLocation(app, 
                                len(app.scoreLevelsToDisplay) + 1)
        canvas.create_rectangle(x1, y1, x2, y2, width=2, fill='black')
        canvas.create_text((x1+x2)/2, (y1+y2)/2,
                            text='Next Page', fill='white')

def getTopScores(app):
    scoresToGet = 10
    filename = f'scores/{app.activeScorePage}.txt'
    f = open(filename, 'r')
    scoreList = []
    for line in f.read().splitlines():
        name, score = line.split(',')
        scoreList.append((name, float(score)))
    return sorted(scoreList, key=lambda entry: entry[1], reverse=True)[:scoresToGet]

def drawActiveScorePage(app, canvas):
    canvas.create_text(app.width // 2, 80, text=f'{app.activeScorePage}:',
                       font='Arial 20 bold underline', fill='red')

    topScores = getTopScores(app)
    for i in range(len(topScores)):
        name, score = topScores[i]
        left = app.width // 2 - 200
        right = app.width // 2 + 200
        y = 150 + 30 * i
        canvas.create_text(left, y, text=f'{name}', font='Arial 16', anchor='sw')
        canvas.create_text(right, y, text=f'{int(score)}', font='Arial 16', anchor='se')
        canvas.create_line(left, y, right, y, width=2)

def drawScoresTitle(app, canvas):
    drawTitle(app, canvas, "Scores")

def scoreMode_mousePressed(app, event):
    if app.activeScorePage != None:
        app.activeScorePage = None
        return
    clicked = getClickedScoreLevelButton(app, event.x, event.y)
    if clicked != None:
        if clicked == 0:
            app.scoreLevelPage -= 1 
            fetchScoreLevelsToDisplay(app)
        elif clicked == len(app.scoreLevelsToDisplay)+1:
            app.scoreLevelPage += 1
            fetchScoreLevelsToDisplay(app)
        else:
            app.activeScorePage = app.scoreLevelsToDisplay[clicked-1]

def scoreMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def scoreMode_redrawAll(app,canvas):
    drawScoresTitle(app, canvas)
    if app.activeScorePage == None:
        drawScoreLevelList(app, canvas)
    else:
        drawActiveScorePage(app, canvas)
    drawHelpText(app, canvas)
    drawHelp(app, canvas)

###################################################
# Game Mode 
###################################################

def getStartTime(note):
    return note[1]

# Takes a string that represents a level and creates a resulting list holding
# tuples of the direction, start time, and optional end time of each note.
def parseLevel(levelString):
    result = []
    for line in levelString.splitlines():
        splits = line.split(",")
        direction = splits[0]
        startTime = float(splits[1])
        endTime = splits[2] or None
        if endTime != None:
            endTime = float(endTime)
        result.append((direction, startTime, endTime))
    result.sort(key=getStartTime) # Sort by the startTime.
    return result

def loadLevelFile(app, filename):
    f = open(filename, "r")
    app.currLevel = parseLevel(f.read())
    f.close()

def loadBackgroundAnimation(app):
    app.backgroundIndex = None
    if app.background == None:
        return None
    directory = 'bgs/' + app.background
    app.backgroundImages = [ImageTk.PhotoImage(app.loadImage(directory + '/' + filename)) for filename in os.listdir(directory)]
    app.backgroundIndex = 0

def loadSong(app, level):
    for f in os.listdir('songs'):
        root = os.path.splitext(f)[0]
        if root == level:
            app.sound = Sound(f'songs/{f}')
            return None
    app.sound = Sound()

def loadLevel(app, level):
    loadLevelFile(app, f'levels/{level}.txt')
    loadBackgroundAnimation(app)
    loadSong(app, level)
    app.currLevelName = level
    app.mode = "gameMode"
    app.readyToStart = True
    app.paused = True
    app.elapsed = 0
    app.progress = 0
    app.missedIndex = 0
    app.notesToDisplay = []
    app.animationsToDisplay = []
    app.noteScores = [None for note in app.currLevel]
    app.score = 0
    app.combo = 0
    app.max_combo = 0
    app.misses = [] # Store the times that the misses occurred.

# Binary search to find the start index and end index for the slice of notes
# that occur between start time and end time.
def getNotesWithinTimeRange(notes, startTime, endTime):
    # Find the index where all of the notes that occur before have a time
    # earlier than start time, and all notes that occur after have a time equal
    # to or later than start time.
    low = 0
    high = len(notes)
    while low < high:
        mid = (low + high) // 2
        if notes[mid][1] < startTime:
            low = mid + 1
        elif notes[mid][1] > startTime:
            high = mid
        else:
            low = mid
            high = mid
    startIndex = low

    # Find the index where all of the notes that occur before have a time equal 
    # to or earlier than end time, and all notes that occur after have a time 
    # later than end time.
    low = startIndex
    high = len(notes)
    while low < high:
        mid = (low + high) // 2
        if notes[mid][1] <= endTime:
            low = mid + 1
        elif notes[mid][1] > endTime:
            high = mid
    endIndex = high
    return startIndex, endIndex

# Fetch the notes that we may have to render on the page and include them in a
# list along with the proportion up the page where they should be rendered.
#
# Also updates the overall progress within the level.
def getNotesWithinSeconds(app, seconds):
    currTime = time.time()
    elapsed = currTime - app.startTime
    startIndex, endIndex = getNotesWithinTimeRange(app.currLevel,
                                                    elapsed, elapsed + seconds)
    app.progress = startIndex / len(app.currLevel) # updates level progress.
    notes = app.currLevel[startIndex:endIndex]
    directionsWithProportions = [(direction, (startTime - elapsed) / seconds)
                                 for (direction, startTime, endTime) in notes]
    return directionsWithProportions

def updateAnimations(app):
    i = 0
    while i < len(app.animationsToDisplay):
        shape, direction, index, scoreCategory = app.animationsToDisplay[i]
        newIndex = index + 1
        if newIndex >= len(app.arrowAnimations[shape][direction]):
            app.animationsToDisplay.pop(i)
        else:
            app.animationsToDisplay[i] = (shape, direction, newIndex, scoreCategory)
            i += 1

def gameMode_timerFired(app):
    if app.paused:
        return None
    
    elapsed = time.time() - app.startTime
    app.elapsed = elapsed

    # Determine the number of seconds for which each note appears on the page
    # and find the notes that may need to be rendered.
    speedToSecondsOnPage = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 11: 0.1}
    secondsOnPage = speedToSecondsOnPage[app.arrowSpeed]
    app.notesToDisplay = getNotesWithinSeconds(app, secondsOnPage)

    # Finds the notes that can no longer possibly earn points and marks them
    # as misses.
    while (app.missedIndex < len(app.currLevel) and
            app.currLevel[app.missedIndex][1] < elapsed - 0.2):
        if app.noteScores[app.missedIndex] == None:
            combo_multiplier = 1 + min(app.combo * 0.1, 3)
            app.score -= 5
            app.combo = 0
            app.noteScores[app.missedIndex] = ('Miss',
                                    combo_multiplier, app.combo, app.score, elapsed)
        app.missedIndex += 1
    # Once all notes have been finished, ends level and loads results.
    if app.missedIndex == len(app.currLevel) and not app.sound.isPlaying():
        loadResultsPage(app)
    
    # Update the background image index.
    if app.backgroundIndex != None:
        app.backgroundIndex = (app.backgroundIndex + 1) % len(app.backgroundImages)
    
    # Update the animations to display.
    updateAnimations(app)

def startAnimation(app, direction, scoreCategory=None):
    for i in range(len(app.animationsToDisplay)):
        shape, currDirection, index, scoreCategory = app.animationsToDisplay[i]
        if currDirection == direction:
            app.animationsToDisplay[i] = (shape, currDirection, 0, scoreCategory)
            return None
    app.animationsToDisplay.append((app.shape, direction, 0, scoreCategory))

def gameMode_keyPressed(app, event):
    if app.readyToStart:
        app.readyToStart = False
        app.paused = False
        app.startTime = time.time()
        app.sound.start()
        return None
    if event.key in app.keyBinds:
        elapsed = time.time() - app.startTime
        keyDirection = app.keyBinds[event.key]
        threshold = 0.2
        # Find all candidate notes.
        startIndex, endIndex = getNotesWithinTimeRange(app.currLevel,
                                elapsed - threshold, elapsed + threshold)
        # Get the closest relevant note from our candidate notes.
        bestNoteIndex = None
        bestError = None
        for i in range(startIndex, endIndex):
            direction, startTime, endTime = app.currLevel[i]
            if app.noteScores[i] == None and direction == keyDirection:
                currError = abs(startTime - elapsed)
                if bestError == None or currError < bestError:
                    bestNoteIndex = i
                    bestError = currError
        
        # Update score information based on error.
        combo_multiplier = 1 + min(app.combo * 0.1, 3)
        if bestError == None:
            app.score -= 5
            app.misses.append((elapsed, app.score))
            app.combo = 0
            scoreCategory = 'Miss'
        elif bestError < 0.05:
            app.score += 10 * combo_multiplier
            app.combo += 1
            app.noteScores[bestNoteIndex] = ('Perfect',
                                    combo_multiplier, app.combo, 
                                    app.score, elapsed)
            scoreCategory = 'Perfect!'
        elif bestError < 0.1:
            app.score += 5 * combo_multiplier
            app.combo += 1
            app.noteScores[bestNoteIndex] = ('Good',
                                combo_multiplier, app.combo, app.score, elapsed)
            scoreCategory = 'Good'
        else:
            app.score += 2 * combo_multiplier
            app.combo = 0
            app.noteScores[bestNoteIndex] = ('OK', 
                                    combo_multiplier, app.combo, 
                                    app.score, elapsed)
            scoreCategory = 'ok'
        app.max_combo = max(app.combo, app.max_combo)
        startAnimation(app, keyDirection, scoreCategory)
    elif event.key == "Q" or event.key == "q":
        app.sound.stop()
        loadMenu(app)

def drawBackground(app, canvas):
    if app.backgroundIndex != None:
        canvas.create_image(app.width // 2, app.height // 2, image=app.backgroundImages[app.backgroundIndex])

def drawTopBar(app, canvas):
    # Create a white background rectangle so that the top bar text is readable.
    canvas.create_rectangle(0, 0, app.width, 40, fill='white')
    score_x = 0
    score_y = 20
    canvas.create_text(score_x, score_y,
                        anchor='w',
                        font='Arial 16 bold',
                        text=f'Score: {int(app.score):,}')
    
    combo_x = app.width / 2
    combo_y = 20
    canvas.create_text(combo_x, combo_y,
                        font='Arial 16 bold',
                        text=f'Combo: {app.combo}')

    progress_x = app.width
    progress_y = 20
    canvas.create_text(progress_x, progress_y,
                        anchor='e',
                        font='Arial 16 bold',
                        text=f'P: {int(100 * app.progress)}%')

def getNoteLocation(app, canvas, direction, proportion):
    verticalCenter = 100
    startingVerticalCenter = app.height + 70
    leftCenter = app.width / 5
    downCenter = 2 * app.width / 5
    upCenter = 3 * app.width / 5
    rightCenter = 4 * app.width / 5
    noteVerticalCenter = verticalCenter + proportion * (startingVerticalCenter - verticalCenter)
    if direction == 'left':
        x, y = leftCenter, noteVerticalCenter
    elif direction == 'down':
        x, y = downCenter, noteVerticalCenter
    elif direction == 'up':
        x, y = upCenter, noteVerticalCenter
    elif direction == 'right':
        x, y = rightCenter, noteVerticalCenter
    # We potentially want to rotate about the center of our app.
    cx, cy = app.width // 2, app.height // 2
    dx, dy = x - cx, y - cy
    if app.travelDirection == 'left':
        return dy + cx, -dx + cy
    elif app.travelDirection == 'down':
        return -dx + cx, -dy + cy
    elif app.travelDirection == 'up':
        return dx + cx, dy + cy
    elif app.travelDirection == 'right':
        return -dy + cx, dx + cy

def drawAnimations(app, canvas):
    for shape, direction, index, scoreCategory in app.animationsToDisplay:
        x, y = getNoteLocation(app, canvas, direction, 0)
        canvas.create_image(x, y, image=ImageTk.PhotoImage(app.arrowAnimations[shape][direction][index]))
        if scoreCategory != None:
            if direction == 'up':
                fill='red'
            elif direction == 'down':
                fill='purple'
            elif direction == 'right':
                fill='blue'
            elif direction == 'left':
                fill='green'
            canvas.create_text(x + 40 + index, y,
                               text=scoreCategory,
                               fill=fill,
                               angle=30 + 0.5 * index,
                               font='Audiowide 14')

def gameMode_redrawAll(app, canvas):
    if app.readyToStart:
        canvas.create_text(app.width/2, app.height/2, 
                    text="Press any key to start.", font="Audiowide 20 bold")
        return None
    drawBackground(app, canvas)
    drawTopBar(app, canvas)

    leftX, leftY = getNoteLocation(app, canvas, 'left', 0)
    app.shapeToDraw[app.shape](app, canvas, leftX, leftY, 'left')

    downX, downY = getNoteLocation(app, canvas, 'down', 0)
    app.shapeToDraw[app.shape](app, canvas, downX, downY, 'down')

    upX, upY = getNoteLocation(app, canvas, 'up', 0)
    app.shapeToDraw[app.shape](app, canvas, upX, upY, 'up')

    rightX, rightY = getNoteLocation(app, canvas, 'right', 0)
    app.shapeToDraw[app.shape](app, canvas, rightX, rightY, 'right')

    # Draw the upcoming notes in the proper position on the page.
    for direction, proportion in app.notesToDisplay:
        noteX, noteY = getNoteLocation(app, canvas, direction, proportion)
        app.shapeToDraw[app.shape](app, canvas, noteX, noteY, direction)
    
    drawAnimations(app, canvas)

###################################################
# Note Style Helpers
###################################################

def drawArrowNote(app, canvas, x, y, direction):
    arrowHeight = 60
    arrowWidth = 50
    arrowThiccness = 12
    outline, fill = app.directionColors[direction]
    # Let's figure out where the points are if our center is at (0, 0) and
    # our arrow points 'up'. This allows us to get the other directions
    # using a simple rotation by 90 degrees.
    dx1 = 0
    dx2 = arrowWidth // 2
    dx3 = dx2
    dx4 = arrowThiccness // 2
    dx5 = dx4
    dx6 = dx5 - arrowThiccness
    dx7 = dx6
    dx8 = -arrowWidth // 2
    dx9 = dx8
    dy1 = -arrowHeight // 2
    dy2 = -arrowThiccness
    dy3 = 0
    slope = (dy2 - dy1) / (dx2 - dx1)
    dy4 = dy1 + slope * dx4 + arrowThiccness
    dy5 = arrowHeight // 2
    dy6 = dy5
    dy7 = dy4
    dy8 = dy3
    dy9 = dy2
    dxdys = [(dx1, dy1), (dx2, dy2), (dx3, dy3), (dx4, dy4), (dx5, dy5), (dx6, dy6), (dx7, dy7), (dx8, dy8), (dx9, dy9)]
    if direction == 'left':
        xys = [(x + dy, y - dx) for (dx, dy) in dxdys]
    elif direction == 'down':
        xys = [(x - dx, y - dy) for (dx, dy) in dxdys]
    elif direction == 'up':
        xys = [(x + dx, y + dy) for (dx, dy) in dxdys]
    elif direction == 'right':
        xys = [(x - dy, y + dx) for (dx, dy) in dxdys]
    canvas.create_polygon(xys, outline=outline, fill=fill, width = 3)

def drawTriangleNote(app, canvas, x, y, direction):
    arrowHeight = 60
    arrowWidth = 50
    outline, fill = app.directionColors[direction]
    if direction == 'left':
        x1 = x - arrowHeight // 2
        x2 = x1 + arrowHeight
        x3 = x2
        y1 = y
        y2 = y - arrowWidth // 2
        y3 = y2 + arrowWidth
    elif direction == 'down':
        x1 = x - arrowWidth // 2
        x2 = x1 + arrowWidth
        x3 = x
        y1 = y - arrowHeight // 2
        y2 = y1
        y3 = y2 + arrowHeight
    elif direction == 'up':
        x1 = x - arrowWidth // 2
        x2 = x
        x3 = x1 + arrowWidth
        y1 = y + arrowHeight // 2
        y2 = y1 - arrowHeight
        y3 = y1
    elif direction == 'right':
        x1 = x - arrowHeight // 2
        x2 = x1 + arrowHeight
        x3 = x1
        y1 = y - arrowWidth // 2
        y2 = y
        y3 = y1 + arrowWidth
    canvas.create_polygon(x1, y1, x2, y2, x3, y3,
                          outline=outline, fill=fill, width=3)

def drawSquareNote(app, canvas, x, y, direction):
    noteSideLength = 50
    x1 = x - noteSideLength // 2
    x2 = x1 + noteSideLength
    y1 = y - noteSideLength // 2
    y2 = y1 + noteSideLength
    outline, fill = app.directionColors[direction]
    canvas.create_rectangle(x1, y1, x2, y2, outline=outline, fill=fill, width=3)

def drawCircleNote(app, canvas, x, y, direction):
    noteR = 30
    x1 = x - noteR
    x2 = x + noteR
    y1 = y - noteR
    y2 = y + noteR
    outline, fill = app.directionColors[direction]
    canvas.create_oval(x1, y1, x2, y2, outline=outline, fill=fill, width=3)

###################################################
# Results Page 
###################################################

def saveScore(app):
    name = None
    while name == None or ',' in name:
        name = app.getUserInput('What is your name?')
        if (name == None):
            return None
        if (',' in name):
            app.showMessage("Names don't contain commas, silly!")
    filename = f'scores/{app.currLevelName}.txt'
    f = open(filename, 'a')
    f.write(f'{name},{app.score}\n')
    f.close()

def loadResultsPage(app):
    app.mode = 'resultsPage'
    # Get a dictionary to hold counts for each of the possible note scores.
    app.counts = {
            'Perfect': 0,
            'Good': 0,
            'OK': 0,
            'Miss': 0,
            'Total': len(app.currLevel)
        }
    for score, _, _, _, _ in app.noteScores:
        app.counts[score] += 1
    app.resultsButtons = [('Settings', lambda: loadSettingsMode(app)),
                          ('Level Select', lambda: loadLevelSelect(app)),
                          ('Replay', lambda: loadLevel(app, app.currLevelName)),
                          ('Save Score', lambda: saveScore(app))]

def getResultsButtonLocation(app, i):
    rows = 2
    cols = 2
    topY = 2 * app.height // 3
    botY = app.height
    leftX = 0
    rightX = 2 * app.width // 3
    height = 30
    width = 150
    row = i // cols
    col = i % cols
    sectionX1 = leftX + col * (rightX - leftX) / cols
    sectionX2 = sectionX1 + (rightX - leftX) / cols
    sectionY1 = topY + row * (botY - topY) / rows
    sectionY2 = sectionY1 + (botY - topY) / rows
    x1 = (sectionX1 + sectionX2) / 2 - width / 2
    x2 = x1 + width
    y1 = (sectionY1 + sectionY2) / 2 - height / 2
    y2 = y1 + height
    return (x1, y1, x2, y2)

def getClickedResultsButton(app, x, y):
    for i in range(len(app.resultsButtons)):
        (x1, y1, x2, y2) = getResultsButtonLocation(app, i)
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            return app.resultsButtons[i]
    return None

def resultsPage_mousePressed(app, event):
    clickedButton = getClickedResultsButton(app, event.x, event.y)
    if clickedButton != None:
        text, action = clickedButton
        action()

def resultsPage_keyPressed(app, event):
    commonKeyPressed(app, event)

def getTimeFromScore(score):
    return score[4]

def getTimeFromMiss(miss):
    return miss[0]

# Assemble a list of all interesting events in sorted order of when they
# occurred.
def mergeNoteScoresAndMisses(app):
    scoresIndex = 0
    missesIndex = 0
    result = []
    sortedScores = sorted(app.noteScores, key=getTimeFromScore)
    sortedMisses = sorted(app.misses, key=getTimeFromMiss)
    # Modified mergesort merge that tracks combo information over time.
    while scoresIndex < len(sortedScores) and missesIndex < len(sortedMisses):
        _, _, combo, noteScore, noteTime = sortedScores[scoresIndex]
        missTime, missScore = sortedMisses[missesIndex]
        if noteTime < missTime:
            result.append((noteTime, combo, noteScore))
            scoresIndex += 1
        elif missTime < noteTime:
            result.append((missTime, 0, missScore))
            missesIndex += 1
        else: # This should never happen (fingers crossed).
            assert(False)
    # Exhaust remaining list.
    while scoresIndex < len(sortedScores):
        _, _, combo, noteScore, noteTime = sortedScores[scoresIndex]
        result.append((noteTime, combo, noteScore))
        scoresIndex += 1
    while missesIndex < len(sortedMisses):
        missTime, missScore = sortedMisses[missesIndex]
        result.append((missTime, combo, missScore))
        missesIndex += 1
    return result

def plotLineOverTime(canvas,
                     x1, y1,
                     x2, y2,
                     data,
                     getTime,
                     getValue,
                     totalTime,
                     fill):
    if len(data) < 2:
        return None
    minValue = None
    maxValue = 0 # We would like to always "start" from 0, so make sure that it
                 # appears on our y-axis
    for entry in data:
        value = getValue(entry)
        if minValue == None or value < minValue:
            minValue = value
        if maxValue == None or value > maxValue:
            maxValue = value
    if maxValue == minValue:
        return None
    minValue = min(minValue, 0)
    firstTime = getTime(data[0])
    firstValue = getValue(data[0])
    lastX = x1 + (x2 - x1) * (firstTime / totalTime) # convert time to distance.
    lastY = y2 - (y2 - y1) * ((firstValue - minValue) / (maxValue - minValue)) # convert value to height.
    zeroY = y2 - (y2 - y1) * ((0 - minValue) / (maxValue - minValue))
    canvas.create_line(x1, zeroY, lastX, lastY, fill=fill)
    for entry in data[1:]:
        nextTime = getTime(entry)
        nextValue = getValue(entry)
        nextX = x1 + (x2 - x1) * (nextTime / totalTime)
        nextY = y2 - (y2 - y1) * ((nextValue - minValue) / (maxValue - minValue))
        canvas.create_line(lastX, lastY, nextX, nextY, fill=fill)
        lastX = nextX
        lastY = nextY
    canvas.create_line(lastX, lastY, x2, lastY, fill=fill) # fill in remaining graph.

def drawGraph(app, canvas):
    x1 = 30
    y1 = 30
    x2 = app.width - 30
    y2 = app.height / 3 - 30
    canvas.create_rectangle(x1, y1, x2, y2)
    mergedEvents = mergeNoteScoresAndMisses(app)
    if len(mergedEvents) <= 1:
        canvas.create_text(app.width / 2, (y1 + y2) / 2,
                            font='Arial 20 bold',
                            text='Wow, that was a cool level.')
        return None
    plotLineOverTime(canvas, x1, y1, x2, y2, mergedEvents,
                     lambda entry: entry[0],
                     lambda entry: entry[1], app.elapsed, 'black')
    plotLineOverTime(canvas, x1, y1, x2, y2, mergedEvents,
                     lambda entry: entry[0],
                     lambda entry: entry[2], app.elapsed, 'blue')

def drawTotals(app, canvas):
    top_y = app.height / 3
    bot_y = 2 * app.height / 3
    left = 10
    score_y = top_y + (bot_y - top_y) / 6
    canvas.create_text(left, score_y,
                        anchor='w',
                        font='Arial 16 bold',
                        text=f'Total Score: {int(app.score):,}')
    time_y = top_y + 3 * (bot_y - top_y) / 6
    canvas.create_text(left, time_y,
                        anchor='w',
                        font='Arial 16 bold',
                        text=f'Total Time: {int(app.elapsed)}s')
    combo_y = top_y + 5 * (bot_y - top_y) / 6
    canvas.create_text(left, combo_y,
                        anchor='w',
                        font='Arial 16 bold',
                        text=f'Highest Combo: {app.max_combo}')

def drawResultsButtons(app, canvas):
    for i in range(len(app.resultsButtons)):
        x1, y1, x2, y2 = getResultsButtonLocation(app, i)
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", width=2)
        canvas.create_text((x1 + x2)//2, (y1 + y2)//2, 
                text=app.resultsButtons[i][0], font="Arial 15 bold")

def drawCounts(app, canvas):
    top_y = app.height / 3
    bot_y = 3 * app.height / 4
    right = app.width - 20
    countsList = [(score, app.counts[score]) for score in app.counts]
    for i in range(len(countsList)):
        score, count = countsList[i]
        y = top_y + (1 + 2 * i) * (bot_y - top_y) / (2 * len(countsList)) # halfway down each cell.
        canvas.create_text(right, y,
                        anchor='e',
                        font='Arial 16 bold',
                        text=f'{score}: {count}')

def resultsPage_redrawAll(app, canvas):
    drawGraph(app, canvas)
    drawTotals(app, canvas)
    drawResultsButtons(app, canvas)
    drawCounts(app, canvas)
    # We omit the help text because it overlaps with the navigation buttons.
    drawHelp(app, canvas)

###################################################
# Main App 
###################################################

# From: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def generateAnimation(app, shape, direction):
    result = []
    baseImage = app.loadImage(f'images/{shape}_{direction}.png').convert("RGBA")
    for i in range(9):
        transparentImage = Image.new(mode="RGBA", size=baseImage.size)
        for x in range(transparentImage.width):
            for y in range(transparentImage.height):
                r, g, b, a = baseImage.getpixel((x, y))
                if a != 0:
                    transparentImage.putpixel((x, y), (r, g, b, 255 - 30 * i))
                else:
                    transparentImage.putpixel((x, y), (r, g, b, a))
        result.append(app.scaleImage(transparentImage, 1 + i / 9))
    return result

def loadArrowAnimations(app):
    app.arrowAnimations = {}
    for shape in app.shapeToDraw:
        for direction in app.directionColors:
            if shape not in app.arrowAnimations:
                app.arrowAnimations[shape] = {}
            app.arrowAnimations[shape][direction] = generateAnimation(app, shape, direction)

def appStarted(app):
    app.displayHelp = False
    app.levelsPerPage = 5
    app.arrowSpeed = 1
    app.background = None
    app.travelDirection = 'up'
    app.shape = 'arrow'
    app.shapeToDraw = {
        'arrow': drawArrowNote,
        'triangle': drawTriangleNote,
        'square': drawSquareNote,
        'circle': drawCircleNote
    }
    app.keyBinds = {
            'Left': 'left',
            'Right': 'right',
            'Up': 'up',
            'Down': 'down'
        }
    app.directionColors = {
        'left': ('green', 'lightGreen'),
        'down': ('purple', 'violet'),
        'up': ('red', 'pink'),
        'right': ('blue', 'lightBlue')
    }
    app.timerDelay = 25
    pygame.mixer.init()
    app.sound = Sound()
    loadArrowAnimations(app)
    loadMenu(app)

def appStopped(app):
    app.sound.stop()

runApp(width=500, height=500)