import math
import pyaudio
import tkinter as tk
from cmu_112_graphics import *

###################################################
# Common Helpers
###################################################

def commonKeyPressed(app, event):
    if event.key == "M" or event.key == "m":
        app.mode = "menuMode"
    elif event.key == "T" or event.key == "t":
        app.mode = "tunerMode"
    elif event.key == "R" or event.key == "r":
        app.mode = "recordMode"
    elif event.key == "H" or event.key == "h":
        app.displayHelp = not app.displayHelp

def drawHelpText(app, canvas):
    canvas.create_text(app.width//2, app.height - 30, 
            text="Click 'H' to open help page.", font="Arial 10 bold")

def drawHelp(app, canvas):
    if app.displayHelp:
        canvas.create_rectangle(30, 30, app.width - 30, app.height - 30, fill="white")

def drawTitle(app, canvas, text):
    canvas.create_text(app.width/2, 30, text=text, font="Arial 30 bold")

###################################################
# Menu Mode 
###################################################

def getMenuButtonLocation(app, i):
    topY = app.height // 2
    height = 30
    width = 100
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
        app.mode = mode

def menuMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def drawMenuTitle(app, canvas):
    drawTitle(app, canvas, "PocketScore")

def drawMenuImage(app, canvas):
    pass

def drawMenuButtons(app, canvas):
    for i in range(len(app.menuButtons)):
        x1, y1, x2, y2 = getMenuButtonLocation(app, i)
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", width=2)
        canvas.create_text((x1 + x2)//2, (y1 + y2)//2, 
                text=app.menuButtons[i][0], font="Arial 15 bold")

def menuMode_redrawAll(app, canvas):
    drawMenuTitle(app, canvas)
    drawMenuImage(app, canvas)
    drawMenuButtons(app, canvas)
    drawHelpText(app, canvas)
    drawHelp(app, canvas)

###################################################
# Tuner Mode 
###################################################

def getPitchAndCents(freq, pitchChart):
    bestPitch = None
    bestError = None
    logFreq = math.log2(freq)
    for (pitch, pitchFreq) in pitchChart:
        logPitchFreq = math.log2(pitchFreq)
        error = logFreq - logPitchFreq
        if bestError == None or (abs(error) < abs(bestError)):
            bestPitch = pitch
            bestError = error
    return (bestPitch, bestError * 1200)

def updatePitchInfo(app):
    app.pitch, app.cents = getPitchAndCents(app.tunerFreq, app.pitchChart)
    app.flat = app.cents < -10
    app.sharp = app.cents > 10

def tunerMode_timerFired(app): #Test code to be replaced with mic input
    if app.currFreqI == 0:
        app.up = True
    if app.currFreqI == len(app.freqs) - 1:
        app.up = False
    app.tunerFreq = app.freqs[app.currFreqI]
    if app.up:
        app.currFreqI += 1
    else:
        app.currFreqI -= 1
    updatePitchInfo(app)

def tunerMode_mousePressed(app, event):
    pass

def tunerMode_keyPressed(app, event):
    commonKeyPressed(app, event)

def drawTunerTitle(app, canvas):
    drawTitle(app, canvas, "Tuner")

def getTunerCenter(app):
    x = app.width // 2
    y = app.height // 2
    return (x, y)

def drawTunerArc(app, canvas):
    (x, y) = getTunerCenter(app)
    r = 120
    canvas.create_arc(x - r, y - r, x + r, y + r, 
            width=2, extent=90, style=tk.ARC, start=45)

def drawTunerNeedle(app, canvas):
    (x, y) = getTunerCenter(app)
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
    theta = math.pi / 2 + math.pi / 2 * (-app.cents / 100)
    x2 = x + math.cos(theta) * 110
    y2 = y - math.sin(theta) * 110
    canvas.create_line(x, y, x2, y2, width=2)

def drawPitch(app, canvas):
    (x, y) = getTunerCenter(app)
    canvas.create_text(x, y + 40, text=app.pitch, font="Arial 15 bold")

def drawTendency(app, canvas):
    flatFill = "white"
    sharpFill = "white"
    if not app.flat and not app.sharp:
        flatFill = "green"
        sharpFill = "green"
    elif app.flat:
        flatFill = "red"
    elif app.sharp:
        sharpFill = "red"
    (x, y) = getTunerCenter(app)
    flatX1 = x - 50
    flatY1 = y - 10
    flatX2 = x - 30
    flatY2 = y + 10
    canvas.create_rectangle(flatX1, flatY1, flatX2, flatY2, fill=flatFill)
    sharpX1 = x + 30
    sharpY1 = y - 10
    sharpX2 = x + 50
    sharpY2 = y + 10
    canvas.create_rectangle(sharpX1, sharpY1, sharpX2, sharpY2, fill=sharpFill)

def drawTunerDisplay(app, canvas):
    drawTunerArc(app, canvas)
    drawTunerNeedle(app, canvas)
    drawPitch(app, canvas)
    drawTendency(app, canvas)

def drawDroneSection(app, canvas):
    pass

def tunerMode_redrawAll(app, canvas):
    drawTunerTitle(app, canvas)
    drawTunerDisplay(app, canvas)
    drawDroneSection(app, canvas)
    drawHelpText(app, canvas)
    drawHelp(app, canvas)

###################################################
# Record Mode 
###################################################




###################################################
# Main App 
###################################################

def appStarted(app):
    app.mode = "menuMode"
    createMenuButtons(app)
    app.displayHelp = False
    app.tunerFreq = 447
    app.tunerBaseFreq = 440
    app.pitch = "A4"
    app.cents = 0
    app.pitchChart = createPitchChart(app.tunerBaseFreq)
    app.freqs = [x for x in range(340, 540)]
    app.currFreqI = 0
    app.up = True
    app.flat = False
    app.sharp = False

def createMenuButtons(app):
    buttons = [("Tuner", "tunerMode"), ("Record", "recordMode")]
    app.menuButtons = buttons

def getFreqFromPitch(baseFreq, note, octave):
    result = baseFreq * 2**(octave - 4)
    if note == "C":
        result *= 2**(-9/12)
    elif note == "C#":
        result *= 2**(-8/12)
    elif note == "D":
        result *= 2**(-7/12)
    elif note == "D#":
        result *= 2**(-6/12)
    elif note == "E":
        result *= 2**(-5/12)
    elif note == "F":
        result *= 2**(-4/12)
    elif note == "F#":
        result *= 2**(-3/12)
    elif note == "G":
        result *= 2**(-2/12)
    elif note == "G#":
        result *= 2**(-1/12)
    elif note == "A": # Nothing happens, this is the base note.
        result *= 2**0
    elif note == "A#":
        result *= 2**(1/12)
    elif note == "B":
        result *= 2**(2/12)
    else:
        print("Unrecognized note.")
        assert(False)
    return result

def createPitchChart(baseFreq):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octaves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return [(f"{note}{octave}", getFreqFromPitch(baseFreq, note, octave)) for octave in octaves for note in notes]

runApp(width=500, height=500)