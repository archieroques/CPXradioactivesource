import math, time, neopixel, random, board
from digitalio import DigitalInOut, Direction, Pull

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0,0,0))
pixels.show()

anought = 100000

halflife = 7
decayconst = math.log(2, math.e)/halflife

nuclei = 100000
timeinterval = 1

buttonA = DigitalInOut(board.BUTTON_A)
buttonA.direction = Direction.INPUT
buttonA.pull = Pull.DOWN

buttonB = DigitalInOut(board.BUTTON_B)
buttonB.direction = Direction.INPUT
buttonB.pull = Pull.DOWN

isotopes = ["O-22", "N-16", "Be-11", "C-10", "Db-261", "Sb-266", "Rf-261", "N-12", "C-14", "Nb-253"]
halflives = [2.25, 7.13, 13.81, 19.29, 27, 30, 81, 597.9, 181000000000.0, 97.0]

isotope = 0

def cycle(isotope):
    if isotope < 10:
        isotope = isotope + 1
        pixels[isotope - 1] = ((50, 0, 50))
        pixels.show()
    else:
        isotope = 0
        pixels.fill((0,0,0))
        pixels.show()
    time.sleep(0.3)
    return isotope
    

def decay(anought, halflife):
    decayconst = (math.log(2, math.e))/halflife
    t = 1
    while True:
        activity = anought * (math.e ** (-1 * decayconst * t))
        sleeptime = (1/activity)
        for i in range(10):
            if random.randrange(0, 10, 1) == 5:  
                r = random.randrange(0, 255, 1)
                g = random.randrange(0, 255, 1)
                b = random.randrange(0, 255, 1)
                pixels.fill((r, g, b))
                pixels.show()
                time.sleep(0.01)
                pixels.fill((0,0,0))
                pixels.show()
            time.sleep(sleeptime/10)
        t = t + 1
while True:
    if buttonA.value == True and buttonB.value == True:
        decay(anought, halflives[isotope - 1])
    elif buttonA.value == True and buttonB.value == False:
        isotope = cycle(isotope)
    