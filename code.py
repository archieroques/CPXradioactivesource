import math, time, neopixel, random, board
from digitalio import DigitalInOut, Direction, Pull

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2) #sets up neopixels
pixels.fill((0,0,0))#turns them off
pixels.show()#shows new colours

anought = 100000 #activity at t=0, for calculations and stuff

halflife = 7 #starting halflife - this is not really needed any more
decayconst = math.log(2, math.e)/halflife #calculates the decay constant, lambda

nuclei = 100000 #no. of starting nuclei
timeinterval = 1 #how much to change time by

buttonA = DigitalInOut(board.BUTTON_A) #this all sets up button A
buttonA.direction = Direction.INPUT
buttonA.pull = Pull.DOWN

buttonB = DigitalInOut(board.BUTTON_B) #this all sets up button B
buttonB.direction = Direction.INPUT
buttonB.pull = Pull.DOWN

isotopes = ["O-22", "N-16", "Be-11", "C-10", "Db-261", "Sb-266", "Rf-261", "N-12", "C-14", "Nb-253"] #list of isotopes, only used for humans to pick an isotope
halflives = [2.25, 7.13, 13.81, 19.29, 27, 30, 81, 597.9, 181000000000.0, 97.0] #halflives corresponding to list above

isotope = 0 #initialises variable

def cycle(isotope): #this function moves the isotope on by 1
    if isotope < 10: #if it isn't at max
        isotope = isotope + 1 #add 1 to it
        pixels[isotope - 1] = ((50, 0, 50)) #light that LED as an indicator
        pixels.show()
    else: #if it is at max
        isotope = 0 #set it to 0 again
        pixels.fill((0,0,0)) #turn off the pixels so we can start lighting them again
        pixels.show()
    time.sleep(0.3) #wait a bit between button presses
    return isotope #return what the new isotope is so we can update the var
    

def decay(anought, halflife, timeinterval): #this is what runs when we press a&b
    decayconst = (math.log(2, math.e))/halflife #cauculates the decay constant lambda from the halflife given for the relevant isotope
    t = 1 #this is just a counter variable used to represent time
    while True: #run forever
        activity = anought * (math.e ** (-1 * decayconst * t)) #calculate the activity level for the current time (based on exponential decay function)
        sleeptime = (1/activity) #activity is decays per second, so time = 1 / decays per second = seconds per decay
        for i in range(10): #runs 10 times to get an element of randomness
            if random.randrange(0, 10, 1) == 5:  #if a random number between 0 and 10 is 5 (which happens 1/10th of the time)
                r = random.randrange(0, 255, 1) #set R, G and B to random colours (no reason for this, my physics teacher just liked the idea of it being colourful
                g = random.randrange(0, 255, 1)
                b = random.randrange(0, 255, 1)
                pixels.fill((r, g, b)) #fill pixels as such
                pixels.show()#show pixels
                time.sleep(0.01)#wait for a tiny tiny bit so it's a flash
                pixels.fill((0,0,0))#blank pixels
                pixels.show()#show pixels
            time.sleep(sleeptime/10)#sleep for a tenth of the time, as it runs 10 times per decay
        t = t + timeinterval#move on one time interval
while True: #always run the menu
    if buttonA.value == True and buttonB.value == True:#if they are both pressed
        decay(anought, halflives[isotope - 1], timeinterval)#run the decay function with selected isotope halflife
    elif buttonA.value == True and buttonB.value == False:#if that isn't happening, see if A is pressed
        isotope = cycle(isotope)#do an isotope selection cycle if it is
    