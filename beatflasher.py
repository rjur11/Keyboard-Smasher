import math
import os
import tkinter as tk
import time
from cmu_112_graphics import *

###################################################
# Common Helpers
###################################################

def commonKeyPressed(app, event):
    # TODO: Make mode switching consistent.
    if event.key == "M" or event.key == "m":
        app.mode = "menuMode"
    elif event.key == "L" or event.key == "l":
        loadLevelSelect(app)
    elif event.key == "I" or event.key == "i":
        app.mode = "instructionMode"
    elif event.key == "S" or event.key == "s":
        loadScoreMode(app)
    elif event.key == "H" or event.key == "h":
        app.displayHelp = not app.displayHelp

# Handles mode switching from "button-like" things.
def switchMode(app, mode):
    if mode == "levelSelectMode":
        loadLevelSelect(app)
    elif mode == "scoreMode":
        loadScoreMode(app)

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
                and app.levelsPerPage * (app.scoreLevelPage+1) < len(app.scoreLevelList))

def drawScoreLevelList(app, canvas):
    if hasPrevScoreLevelPage(app):
        (x1, y1, x2, y2) = getScoreLevelButtonLocation(app, 0)
        canvas.create_rectangle(x1, y1, x2, y2, width=2, fill='black')
        canvas.create_text((x1+x2)/2, (y1+y2)/2,
                            text='Previous Page', fill='white')
    for i in range(len(app.scoreLevelsToDisplay)):
        (x1, y1, x2, y2) = getScoreLevelButtonLocation(app, i + 1)
        canvas.create_rectangle(x1, y1, x2, y2, width=2)
        canvas.create_text((x1+x2)/2, (y1+y2)/2, text=app.scoreLevelsToDisplay[i])
    if hasNextScoreLevelPage(app):
        (x1, y1, x2, y2) = getScoreLevelButtonLocation(app, len(app.scoreLevelsToDisplay) + 1)
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

def loadLevel(app, level):
    loadLevelFile(app, f'levels/{level}.txt')
    app.currLevelName = level
    app.mode = "gameMode"
    app.readyToStart = True
    app.paused = True
    app.elapsed = 0
    app.progress = 0
    app.missedIndex = 0
    app.notesToDisplay = []
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
    if app.missedIndex == len(app.currLevel):
        loadResultsPage(app)

def gameMode_keyPressed(app, event):
    if app.readyToStart:
        app.readyToStart = False
        app.paused = False
        app.startTime = time.time()
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
        elif bestError < 0.05:
            app.score += 10 * combo_multiplier
            app.combo += 1
            app.noteScores[bestNoteIndex] = ('Perfect',
                                    combo_multiplier, app.combo, 
                                    app.score, elapsed)
        elif bestError < 0.1:
            app.score += 5 * combo_multiplier
            app.combo += 1
            app.noteScores[bestNoteIndex] = ('Good',
                                combo_multiplier, app.combo, app.score, elapsed)
        else:
            app.score += 2 * combo_multiplier
            app.combo = 0
            app.noteScores[bestNoteIndex] = ('OK', 
                                    combo_multiplier, app.combo, 
                                    app.score, elapsed)
        app.max_combo = max(app.combo, app.max_combo)

def drawTopBar(app, canvas):
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

def gameMode_redrawAll(app, canvas):
    if app.readyToStart:
        canvas.create_text(app.width/2, app.height/2, 
                    text="Press any key to start.", font="Arial 30 bold")
        return None
    drawTopBar(app, canvas)
    arrowHeight = 60
    arrowWidth = 50
    verticalCenter = 100

    startingVerticalCenter = app.height + arrowHeight

    leftCenter = app.width / 5
    leftLeft = leftCenter - arrowHeight / 2
    leftRight = leftCenter + arrowHeight / 2
    leftTop = verticalCenter - arrowWidth / 2
    leftMiddle = verticalCenter
    leftBottom = verticalCenter + arrowWidth / 2
    canvas.create_polygon(leftLeft, leftMiddle,
                          leftRight, leftTop,
                          leftRight, leftBottom,
                          outline='green', fill='lightGreen', width=3)

    downCenter = 2 * app.width / 5
    downLeft = downCenter - arrowWidth / 2
    downMiddle = downCenter
    downRight = downCenter + arrowWidth / 2
    downTop = verticalCenter - arrowHeight / 2
    downBottom = verticalCenter + arrowHeight / 2
    canvas.create_polygon(downLeft, downTop,
                          downRight, downTop,
                          downMiddle, downBottom,
                          outline='purple', fill='violet', width=3)

    upCenter = 3 * app.width / 5
    upLeft = upCenter - arrowWidth / 2
    upMiddle = upCenter
    upRight = upCenter + arrowWidth / 2
    upTop = verticalCenter - arrowHeight / 2
    upBottom = verticalCenter + arrowHeight / 2
    canvas.create_polygon(upLeft, upBottom,
                          upMiddle, upTop,
                          upRight, upBottom,
                          outline='red', fill='pink', width=3)

    rightCenter = 4 * app.width / 5
    rightLeft = rightCenter - arrowHeight / 2
    rightRight = rightCenter + arrowHeight / 2
    rightTop = verticalCenter - arrowWidth / 2
    rightMiddle = verticalCenter
    rightBottom = verticalCenter + arrowWidth / 2
    canvas.create_polygon(rightLeft, rightBottom,
                          rightLeft, rightTop,
                          rightRight, rightMiddle,
                          outline='blue', fill='lightBlue', width=3)
    
    # Draw the upcoming notes in the proper position on the page.
    for direction, proportion in app.notesToDisplay:
        noteVerticalCenter = verticalCenter + proportion * (
            startingVerticalCenter - verticalCenter
        )
        if direction == 'left':
            top = noteVerticalCenter - arrowWidth / 2
            middle = noteVerticalCenter
            bottom = noteVerticalCenter + arrowWidth / 2
            canvas.create_polygon(leftLeft, middle,
                                  leftRight, top,
                                  leftRight, bottom,
                                  outline='green', fill='lightGreen', width=3)
        elif direction == 'down':
            top = noteVerticalCenter - arrowHeight / 2
            bottom = noteVerticalCenter + arrowHeight / 2
            canvas.create_polygon(downLeft, top,
                                  downRight, top,
                                  downMiddle, bottom,
                                  outline='purple', fill='violet', width=3)
        elif direction == 'up':
            top = noteVerticalCenter - arrowHeight / 2
            bottom = noteVerticalCenter + arrowHeight / 2
            canvas.create_polygon(upLeft, bottom,
                                  upMiddle, top,
                                  upRight, bottom,
                                  outline='red', fill='pink', width=3)
        elif direction == 'right':
            top = noteVerticalCenter - arrowWidth / 2
            middle = noteVerticalCenter
            bottom = noteVerticalCenter + arrowWidth / 2
            canvas.create_polygon(rightLeft, bottom,
                                  rightLeft, top,
                                  rightRight, middle,
                                  outline='blue', fill='lightBlue', width=3)
    

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
    app.resultsButtons = [('Settings', lambda: None),
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

###################################################
# Main App 
###################################################

def appStarted(app):
    app.mode = "menuMode"
    createMenuButtons(app)
    app.displayHelp = False
    app.levelsPerPage = 5
    app.arrowDirection = 'Up'
    app.arrowSpeed = 1
    app.arrowShape = 'Triangle'
    app.keyBinds = {
            'Left': 'left',
            'Right': 'right',
            'Up': 'up',
            'Down': 'down'
        }
    app.timerDelay = 25

def createMenuButtons(app):
    buttons = [("Select Level", "levelSelectMode"), 
                ("Instructions", "instructionMode"),
                ("Scores", "scoreMode")]
    app.menuButtons = buttons


runApp(width=500, height=500, mvcCheck=False)