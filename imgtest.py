from cmu_112_graphics import *

def appStarted(app):
    app.image1 = app.loadImage('images/arrow_left.png').convert("RGBA")
    app.timerDelay = 33
    app.transparentImages = []
    for i in range(9):
        transparentImage = Image.new(mode="RGBA", size=app.image1.size)
        for x in range(transparentImage.width):
            for y in range(transparentImage.height):
                r, g, b, a = app.image1.getpixel((x, y))
                if a != 0:
                    transparentImage.putpixel((x, y), (r, g, b, 255 - 30 * i))
                else:
                    transparentImage.putpixel((x, y), (r, g, b, a))
        app.transparentImages.append(app.scaleImage(transparentImage, 1 + i/9))
    app.imageIndex = None

def timerFired(app):
    if app.imageIndex != None:
        app.imageIndex += 1
        if app.imageIndex >= len(app.transparentImages):
            app.imageIndex = None

def keyPressed(app, event):
    app.imageIndex = 0

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='red')
    if app.imageIndex != None:
        canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.transparentImages[app.imageIndex]))

runApp(width=1000, height=1000)

