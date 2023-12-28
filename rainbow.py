#
# simple led strip example with button for changing
#
#

import sys
import neopixel
import random
import micropython # for interrupts

from machine import Pin
import time

# uncomment when debugging callback problems
#micropython.alloc_emergency_exception_buf(100)

# globals
int_flag = 0
int_time = 0
int_count = 0

# for pico w this is "LED" not 25
led = Pin("LED", Pin.OUT)


ws_pin = 0 # gpio pin
pixel_pin = 0
#led_num = 255
#num_pixels = 255
led_num = 216 # 256
num_pixels = 216 # 256
BRIGHTNESS = 0.1

'''
pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.3, auto_write=False)
'''

pixels = neopixel.NeoPixel(Pin(ws_pin), led_num)

def demo(np):
    global int_flag
    
    n = np.n

    # cycle
    for i in range(1 * n):
        for j in range(n):
            if (int_flag != 0): return
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
def bounce(np):
    global int_flag
    
    n = np.n
    
    for i in range(1 * n):
        for j in range(n):
            if (int_flag != 0): return
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
def fadein_out(np):
    global int_flag
    
    n = np.n
    
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (int_flag != 0): return
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write() 
    
def clear(np):
    n = np.n
    
    np.fill((0, 0, 0))
    '''
    for i in range(n):
        np[i] = (0, 0, 0)
    '''
    np.write()
# end clear()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    global int_flag
    
    for i in range(num_pixels):
        if (int_flag != 0): return
        pixels[i] = color
        #time.sleep(wait)
        pixels.write()
        time.sleep(0.5)

def twinkle(color, count, wait):
    global int_flag
    
    val = 200
    
    for x in range(count):
        if (int_flag != 0): return
        #print(random.randint(0, num_pixels-1))
        pixels[random.randint(0, num_pixels-1)] = (val, 0, 0)
        #setPixel(random(NUM_LEDS),red,green,blue);
        pixels.write() # showStrip();
        time.sleep(0.25) # delay(SpeedDelay);
        if ((x % 10) == 0):
            clear(pixels)
     #if(OnlyOne) {
       #setAll(0,0,0);
     #}
# end twinkle()


def rainbow_cycle(wait):
    global int_flag
    
    for j in range(255):
        for i in range(num_pixels):
            if (int_flag != 0): return
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()
        
RED = (255, 0, 0)
HALFRED = (128, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
HALFGREEN = (0, 128, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

def rainbow():
    pixels.fill(RED)
    #pixels.write()
    # Increase or decrease to change the speed of the solid color change.
    #time.sleep(1)
    pixels.fill(GREEN)
    #pixels.write()
    #time.sleep(1)
    pixels.fill(BLUE)
    #pixels.write()
    #time.sleep(1)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow
# end rainbbow()

def neo_chase(np, color, width, duration):
    n = np.n
    clear(np)
    
    # fill the array with the colour scheme - GREEN/RED/BLUE
    for i in range (n // (3 * width)):
        for j in range (width):
            np[(i) * (3 * width) + j] = GREEN
            np[(i) * (3 * width) + (width) + j] = RED
            np[(i) * (3 * width) + (2 * width) + j] = BLUE
    np.write()

    #print(np[0]) # colour?
    px = 0
    idx = 0
    colour = 0
    for c in range(20 * width): # while true?
        for i in range (n):
            if (int_flag != 0): return
            # move the pixels along one
            if ((n - 1) - i > 0):
                np[(n - 1) - i] = np[(n - 1) - (i + 1)]
            
        x = c // width
        # every 'width' pixels we change the colour
        if (x != px):
            px = x
            idx = 0
            colour += 1
            colour = colour % 3 # reset?
            #if (colour == 3):
                #colour = 0
            
        if (colour == 0):
            np[0] = BLUE
        elif (colour == 1 ):
            np[0] = RED
        elif (colour == 2):
            np[0] = GREEN
            
        np.write()
 
    #time.sleep(duration)
# end neo_chase

def cylon(np, eyesize):
    n = np.n
    
    clear(np)
    colour = (255, 10, 10)
    
    for i in range (n - eyesize - 2):
        if int_flag != 0: return
        clear(np)
        np[i] = colour
        for j in range (eyesize):
            np[i+j] = colour
        np[i + eyesize + 1] = colour
        np.write()
    time.sleep(0.25)
    max = n - eyesize - 2
    for i in range (n - eyesize - 2):
        if int_flag != 0: return
        c = max - i
        clear(np)
        np[c] = colour
        for j in range (eyesize):
            np[c+j] = colour
        np[c + eyesize + 1] = colour
        np.write()
    time.sleep(0.25)
# end cylon()

xmasMod = 0
# xmas lights
def xmaslights(np):
    global xmasMod
    
    n = np.n
    clear(np)
    
    for i in range (n):
        if (i % 2  == xmasMod):
            np[i] = RED
        else:
            np[i] = HALFGREEN
            
    if (xmasMod == 0):
        xmasMod = 1
    else:
        xmasMod = 0
    np.write()
    time.sleep(1.0)
    
    '''
   for( int i = 0; i < numPixels; i++ ) {
     if( i % 2 == xmasMod )
        strip.setPixelColor(i, 255,0,0);
     else
        strip.setPixelColor(i, 0,255,0); 
   }
   
   if( xmasMod == 0 )
     xmasMod = 1;
   else
     xmasMod = 0;
     
  strip.show();
}
'''


def neo_sweep(np, color, width, duration):
    global int_flag
    
    bkgnd = []
    num_pixels = np.n
    
    clear(np)
    
    for i in range(num_pixels + width):
        if (int_flag != 0): return
        erase = i - width
        if erase >= 0:
            np[erase] = bkgnd.pop()

        if i < num_pixels:
            bkgnd.insert(0, np[i])
            np[i] = color

        np.write() # np.show()
        time.sleep(duration)

# function to test number of pixels
def test (np):
    clear(np)
    
    np[0] = GREEN
    np[np.n - 1] = GREEN
    np.write()
    time.sleep(2)

    np[0] = RED
    np[np.n - 1] = RED
    np.write()
    time.sleep(2)

    np[0] = BLUE
    np[np.n - 1] = BLUE

    np.write()
    time.sleep(2)
# end test()

def int_handler(pin):
    global int_flag, int_count, int_time
    
    #int_count += 1
    #print(f'Interrupt from pin {pin} {int_count}')
    #print(f'flags {pin.irq().flags()} {pin.value()}')
    # we only trigger on the fall and 'wait' for 300msec
    if ((pin.value() == 0) and ((time.ticks_ms() - int_time) > 300)):
        #print("Falling")
        int_flag = 1
        int_count += 1
        int_time = time.ticks_ms()


# pull button pin up and set trigger on falling
pin_button = Pin(1, mode=Pin.IN, pull=Pin.PULL_UP)
pin_button.irq(trigger=Pin.IRQ_FALLING, handler=int_handler)

# main loop
seq = 0
no_seqs = 9

color = RED # (255,0,0)
width = 8
duration = 0.025

animations = {
        neo_sweep(pixels, PURPLE, width, duration),
        xmaslights(pixels),
        cylon(pixels, 5),
        neo_chase(pixels, PURPLE, 6, 1),
        rainbow(),
        twinkle(10, 20, 0)
    }
try:

    
    while True:
        led.toggle()
        #if (seq == 0):
            #test(pixels)
        animations[5]
        
        if (seq == 0):
            neo_sweep(pixels, PURPLE, width, duration)
        elif (seq == 1):
            xmaslights(pixels)
        elif(seq == 2):
            cylon(pixels, 5)
        elif (seq == 3):
            neo_chase(pixels, PURPLE, 6, 1)
        elif (seq == 4):
            rainbow()
        elif (seq == 5):
            fadein_out(pixels)
        elif (seq == 6):
            bounce(pixels)
        elif (seq == 7):
            demo(pixels)
        elif (seq == 8):
            twinkle(10, 20, 0)
            
        if (int_flag != 0): # we had an interrupt
            int_flag = 0
            seq += 1
            if (seq == no_seqs): seq = 0

except KeyboardInterrupt:
    # if running from boot.py - need to do this twice
    #print("Keyboard interrupted")
    clear(pixels)
    print("Exiting ...")
    #raise SystemExit(0)
    sys.exit(0)
# end of file