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

def fetchLevelsToDisplay(app):
    start = app.levelPage * app.levelsPerPage
    end = start + app.levelsPerPage
    app.levelsToDisplay = app.levelList[start:end]

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

def drawScoresTitle(app, canvas):
    drawTitle(app, canvas, "Scores")

def scoreMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def scoreMode_redrawAll(app,canvas):
    drawScoresTitle(app, canvas)
    drawHelpText(app, canvas)
###################################################
# Game Mode 
###################################################

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
    result.sort(key=lambda note: note[1]) # Sort by the startTime.
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

def getNotesWithinTimeRange(notes, startTime, endTime):
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
            high = mid + 1
    startIndex = low
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

def getNotesWithinSeconds(app, seconds):
    currTime = time.time()
    elapsed = currTime - app.startTime
    startIndex, endIndex = getNotesWithinTimeRange(app.currLevel,
                                                    elapsed, elapsed + seconds)
    app.progress = startIndex / len(app.currLevel)
    notes = app.currLevel[startIndex:endIndex]
    directionsWithProportions = [(direction, (startTime - elapsed) / seconds)
                                 for (direction, startTime, endTime) in notes]
    return directionsWithProportions

def gameMode_timerFired(app):
    if app.paused:
        return None
    elapsed = time.time() - app.startTime
    app.elapsed = elapsed
    speedToSecondsOnPage = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 11: 0.1}
    secondsOnPage = speedToSecondsOnPage[app.arrowSpeed]
    app.notesToDisplay = getNotesWithinSeconds(app, secondsOnPage)
    while (app.missedIndex < len(app.currLevel) and
            app.currLevel[app.missedIndex][1] < elapsed - 0.2):
        if app.noteScores[app.missedIndex] == None:
            combo_multiplier = 1 + min(app.combo * 0.1, 3)
            app.score -= 5
            app.combo = 0
            app.noteScores[app.missedIndex] = ('Miss',
                                    combo_multiplier, app.combo, app.score, elapsed)
        app.missedIndex += 1
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
        startIndex, endIndex = getNotesWithinTimeRange(app.currLevel,
                                elapsed - threshold, elapsed + threshold)
        bestNoteIndex = None
        bestError = None
        for i in range(startIndex, endIndex):
            direction, startTime, endTime = app.currLevel[i]
            if app.noteScores[i] == None and direction == keyDirection:
                currError = abs(startTime - elapsed)
                if bestError == None or currError < bestError:
                    bestNoteIndex = i
                    bestError = currError
        combo_multiplier = 1 + min(app.combo * 0.1, 3)
        if bestError == None:
            app.score -= 5
            app.misses.append((elapsed, app.score))
            app.combo = 0
        elif bestError < 0.05:
            app.score += 10 * combo_multiplier
            app.combo += 1
            app.noteScores[bestNoteIndex] = ('Perfect',
                                    combo_multiplier, app.combo, app.score, elapsed)
        elif bestError < 0.1:
            app.score += 5 * combo_multiplier
            app.combo += 1
            app.noteScores[bestNoteIndex] = ('Good',
                                combo_multiplier, app.combo, app.score, elapsed)
        else:
            app.score += 2 * combo_multiplier
            app.combo = 0
            app.noteScores[bestNoteIndex] = ('OK', 
                                    combo_multiplier, app.combo, app.score, elapsed)
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

def loadResultsPage(app):
    app.mode = 'resultsPage'
    app.counts = {
            'Perfect': 0,
            'Good': 0,
            'OK': 0,
            'Miss': 0,
            'Total': len(app.currLevel)
        }
    for score, _, _, _, _ in app.noteScores:
        app.counts[score] += 1

def resultsPage_mouseClicked(app, event):
    pass

def getTimeFromScore(score):
    return score[4]

def getTimeFromMiss(miss):
    return miss[0]

def mergeNoteScoresAndMisses(app):
    scoresIndex = 0
    missesIndex = 0
    result = []
    sortedScores = sorted(app.noteScores, key=getTimeFromScore)
    sortedMisses = sorted(app.misses, key=getTimeFromMiss)
    while scoresIndex < len(sortedScores) and missesIndex < len(sortedMisses):
        _, _, combo, _, noteTime = sortedScores[scoresIndex]
        missTime, _ = sortedMisses[missesIndex]
        if noteTime < missTime:
            result.append((noteTime, combo))
            scoresIndex += 1
        elif missTime < noteTime:
            result.append((missTime, 0))
            missesIndex += 1
        else: # This should never happen (fingers crossed).
            assert(False)
    while scoresIndex < len(sortedScores):
        _, _, combo, _, noteTime = sortedScores[scoresIndex]
        result.append((noteTime, combo))
        scoresIndex += 1
    while missesIndex < len(sortedMisses):
        missTime, _ = sortedMisses[missesIndex]
        result.append((missTime, combo))
        missesIndex += 1
    return result

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
    maxTime = app.elapsed
    maxCombo = app.max_combo
    firstTime, firstCombo = mergedEvents[0]
    lastX = x1 + (x2 - x1) * (firstTime / maxTime)
    lastY = y2 - (y2 - y1) * (firstCombo / maxCombo)
    canvas.create_line(x1, y2, lastX, lastY)
    for nextTime, nextCombo in mergedEvents[1:]:
        nextX = x1 + (x2 - x1) * (nextTime / maxTime)
        nextY = y2 - (y2 - y1) * (nextCombo / maxCombo)
        canvas.create_line(lastX, lastY, nextX, nextY)
        lastX = nextX
        lastY = nextY
    canvas.create_line(lastX, lastY, x2, lastY)

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

def drawButtons(app, canvas):
    pass

def drawCounts(app, canvas):
    top_y = app.height / 3
    bot_y = 3 * app.height / 4
    right = app.width - 20
    countsList = [(score, app.counts[score]) for score in app.counts]
    for i in range(len(countsList)):
        score, count = countsList[i]
        y = top_y + (1 + 2 * i) * (bot_y - top_y) / (2 * len(countsList))
        canvas.create_text(right, y,
                        anchor='e',
                        font='Arial 16 bold',
                        text=f'{score}: {count}')

def resultsPage_redrawAll(app, canvas):
    drawGraph(app, canvas)
    drawTotals(app, canvas)
    drawButtons(app, canvas)
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
    app.arrowSpeed = 3
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