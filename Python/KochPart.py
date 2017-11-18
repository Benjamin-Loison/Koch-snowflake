#-------------------------------------------------------------------------------
# Name:        Koch
# Purpose:     Draw the Koch snowflake
#
# Author:      Benjamin Loison
#
# Created:     18/11/2017
# Copyright:   (c) Benjamin Loison 2017
# Licence:     No licence (quote the author)
#-------------------------------------------------------------------------------

## Load TKinter standard library which has graphical tools
from tkinter import *
## Load math standard module which has the sqrt (root) and trigonometric functions
from math import *

BLACK = "#000000"

## Use of lists [] and not tuples () because tuples are unchangeable
## Define a plot function to plot black dot by default
def plot(x, y, color = BLACK):
    global canvas
    ## Use a segment of one pixel to draw a point (no plot function in TKinter)
    ## Add 1 to all coordinates arguments because we don't see the point with
    ## coordinates [1, 1]
    ## Don't need to round (maybe done by TKinter)
    canvas.create_line(x + 1, y + 1, x + 2, y + 2, fill = color)

def segment(x0, y0, x1, y1, color = BLACK):
    global canvas
    canvas.create_line(x0 + 1, y0 + 1, x1 + 2, y1 + 2, fill = color)

## Argument: text to display to the user
def intInput(text):
    return int(input(text))

## Load TK Engine
tkengine = Tk()
## Load twindow
window = Frame(tkengine)
window.pack()
WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1500
## Background hexadecimal code: white
canvas = Canvas(window, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg = "#FFFFFF")
canvas.pack()

# Beginning of the code for Koch snowflake

## Input segment's extremities coordinates x and y (1 to WIDTH/HEIGHT (included))
x0, y0 = intInput("x0"), intInput("y0")
x1, y1 = intInput("x1"), intInput("y1")

## Number of iterations for the Koch snowflake (more than 1 (included))
## Add 1 to iterations because in range(1, 1) doesn't do anything
iterations = intInput("Iterations") + 1

## Change the angle of the global fractal
initializationAngle = float(input("Initialization angle"))

## Display with dots or segments
typeOfDisplay = intInput("Display with dots or segments (0 or 1)")

## Compute Un with U(n+1) = Un + 3 * 4 ^ (n - 1)
## Set U0 to nbCoupleCoordinates
nbCoupleCoordinates = 2
for n in range(1, iterations):
    nbCoupleCoordinates += 3 * 4 ** (n - 1)

## Set nbCoupleCoordinates to an int. It is no more a float otherwise we can't do some things
nbCoupleCoordinates = int(nbCoupleCoordinates)

## Define coordinates list with nbCoupleCoordinates lists with two elements (x and y)
coordinates = [[0, 0]] * nbCoupleCoordinates

## Fill with input values
coordinates[0] = [x0, y0]
## nbCoupleCoordinates - 1 because in Python we begin to count at 0 for lists
coordinates[nbCoupleCoordinates - 1] = [x1, y1]

## At each iteration of the Koch snowflake
for iteration in range(1, iterations):

    ## At each iteration we reset the selectors at the beginning
    firstSelector, secondSelector = 0, 1

    ## While secondSelector is in the coordinates list
    while secondSelector <= nbCoupleCoordinates - 1:

        ## If there is coordinates at the secondSelector we generate an equilateral
        ## triangle (at the middle of the three times divided segment) to the left
        ## to the segment defined with the coordinates of the selectors
        if coordinates[secondSelector][0] != 0:

            ## Set variables for the selectors' coordinates
            xFirstSelector, yFirstSelector = coordinates[firstSelector]
            xSecondSelector, ySecondSelector = coordinates[secondSelector]

            ## Define a function which prepares the vector computings
            ## To go further: Access to variables could be done with pointers or
            ## introspection too
            def loadDirection(coord0, coord1):
                ## Put in coord0 the smallest coordinate and in coord1 the relative
                ## coordinates of the biggest coordinate to coord0
                firstCoord = min(coord0, coord1)
                secondCoordRelativeToFirstCoord = max(coord0, coord1) - firstCoord
                ## Check of the direction of vectors
                if firstCoord == coord0:
                    cfVector0, cfVector1 = 1, 2
                else:
                    cfVector0, cfVector1 = 2, 1
                ## Vector computings to determine the coordinates of the first and second
                ## third of the segment define with the coordinates of selectors
                coord0 = firstCoord + cfVector0 * secondCoordRelativeToFirstCoord / 3
                coord1 = firstCoord + cfVector1 * secondCoordRelativeToFirstCoord / 3
                return coord0, coord1

            ## Call loadDirection function for x and y
            xFirstSelector, xSecondSelector = loadDirection(xFirstSelector, xSecondSelector)
            yFirstSelector, ySecondSelector = loadDirection(yFirstSelector, ySecondSelector)

            secondSelectorMinusFirstSelector = secondSelector - firstSelector

            ## Compute first and third quarter list selectors
            ## Need an integer for list indice and not float
            firstQuarterListSelector = int(secondSelectorMinusFirstSelector * 1 / 4 + firstSelector)
            thirdQuarterListSelector = int(secondSelectorMinusFirstSelector * 3 / 4 + firstSelector)

            ## Fill coordinates list with computed values (first and third quarter)
            coordinates[firstQuarterListSelector] = [xFirstSelector, yFirstSelector]
            coordinates[thirdQuarterListSelector] = [xSecondSelector, ySecondSelector]

            ## Computing the coordinates of the extremity of the triangle
            ## Compute the coordinates of the middle of the segment defined with the first and
            ## second selectors, we simply use: (xA + xB) / 2 and the same for ordinates
            xCenter = (xFirstSelector + xSecondSelector) / 2
            yCenter = (yFirstSelector + ySecondSelector) / 2

            xFirstSelectorLessXCenter = xFirstSelector - xCenter
            yFirstSelectorLessYCenter = yFirstSelector - yCenter

            ## Compute the distance between the computed center and the extremities of the segment
            ## We simply use: root((xA - xI)² + (yA - yI)²) (I is the center of the segment)
            distanceCenterExtrimity = sqrt(xFirstSelectorLessXCenter ** 2 +
                                                yFirstSelectorLessYCenter ** 2)

            ## Compute the angle of the segement in the trigonometric circle
            ## We use polar coordinates: x = r cos a; y = r sin a; or: acos x / r = a (rad)
            segmentAngle = acos(xFirstSelectorLessXCenter / distanceCenterExtrimity)
            ## To compute the right angle, we verify the coordinates for the specified angle
            yCoordToConfirmSegmentAngle = yCenter + distanceCenterExtrimity * sin(segmentAngle)
            ## If it is not, set - segmentAngle to segmentAngle because -sin x = sin -x
            if yCoordToConfirmSegmentAngle != yFirstSelector:
                segmentAngle *= -1

            ## Add pi / 2 to segmentAngle because we want the right angle for the extrimity of
            ## the triangle and positive value because we were working on the point to the right
            ## of the center, likewise we are in the trigonometric direction
            segmentAngle += pi / 2

            ## We simply use the Theorem of Pythagore to compute the height of the triangle
            ## because we are in a equilateral triangle
            heightTriangle = sqrt(3 / 4 * (2 * distanceCenterExtrimity) ** 2)

            ## Use of polar coordinates to compute extremity coordinates of the triangle
            xExtremity = xCenter + heightTriangle * cos(segmentAngle)
            yExtremity = yCenter + heightTriangle * sin(segmentAngle)

            ## Fill the coordinates list with the coordinates of the extrimity of the triangle
            halfListSelector = int(secondSelectorMinusFirstSelector * 2 / 4 + firstSelector)
            coordinates[halfListSelector] = [xExtremity, yExtremity]

            firstSelector = secondSelector

        secondSelector += 1

if typeOfDisplay == 0:

    for selector in range(0, nbCoupleCoordinates):

        coordinatesCouple = coordinates[selector]
        plot(coordinatesCouple[0], coordinatesCouple[1])

else:

        for selector in range(0, nbCoupleCoordinates - 1):

            coordinatesCouple0, coordinatesCouple1 = coordinates[selector], coordinates[selector + 1]
            segment(coordinatesCouple0[0], coordinatesCouple0[1], coordinatesCouple1[0],
                                                                        coordinatesCouple1[1])

# End of the code for Koch snowflake

## Infinite loop to always display the window
tkengine.mainloop()