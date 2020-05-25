# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
import random

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
 
# Configure the count of pixels:
PIXEL_COUNT = 48
PIXEL_CLOCK = 11
PIXEL_DOUT  = 10
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=PIXEL_CLOCK, do=PIXEL_DOUT)

#new functions
#colour lists and functions
coloor = {
    'r': 255,
    'g': 0,
    'b': 0
}

#define pallette to be used
#palette = 'xmascolours'

#create a list of tuples, each one defining two shades of base colours: red, orange, yellow, green purple and blue, we then randomly select from this to produce a random
#colour palette that is also distinctive
listcolours = [
        (178, 31, 53),
        (216, 39, 53),
        (255, 116, 53),
        (255, 203, 53),
	(255, 249, 53),
	(0, 117, 58),
	(0, 158, 71),
	(22, 221, 53),
	(0, 82, 165),
	(0, 121, 231),
	(0, 169, 252),
	(104, 30, 126),
	(125, 60, 181),
	(189, 122, 246),
	]

#define a festive themed colour pallette
xmascolours = [
        (255, 255, 255),
	(255, 0, 0),
	(0, 255, 0),
	(0, 0, 255),
        (30, 124, 32),
        (0, 55, 251),
        (223, 101, 0),
        (129, 0, 219)
	]

#define a halloween themed colour pallette
halloweencolours = [
        (21, 24, 24),
        (49, 49, 49),
        (242, 143, 28),
        (110, 58, 158),
        (243, 106, 31),
        (243, 134, 31),
        (192, 60, 9),
        (235, 97, 35),
        (245, 205, 8),
        (103, 160, 50),
        (95, 43, 147),
        ]


#the below produces truly random colours, but often they are variations on white and pink
def get_random_color():
        """Gets a random color - RGB values"""
        coloor = {
            'r': random.randint(0, 255),
            'g': random.randint(0, 255),
            'b': random.randint(0, 255)
        }
        return coloor

def get_random_themed_color():
        """Gets a random themed color - RGB values"""
        coloor = random.choice(xmascolours)
        color = {
            'r': coloor[0],
            'g': coloor[1],
            'b': coloor[2]
        }
        return color



# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)
 
# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)

def colorWipe(pixels, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(pixels.count()):
        pixels.set_pixel(i, color)
        pixels.show()
        time.sleep(wait_ms/1000.0)



def rainbow_cycle(pixels, wait=0):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
# strip.numPixels() = pixels.count()
# strip = pixels
# strip.setPixelColor( =  pixels.set_pixel(
# strip.show() = pixels.show()

##new ones
def Color(red, green, blue):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return ((red & 0xFF) << 16) | ((green & 0xFF) << 8) | (blue & 0xFF)

def theaterChase(pixels, color, wait_ms=50, iterations=10):
    """Movie theater marquee style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, pixels.count(), 3):
                pixels.set_pixel(i+q, color)
            pixels.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, pixels.count(), 3):
                pixels.set_pixel(i+q, 0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater marquee style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, pixels.count(), 3):
                pixels.set_pixel(i+q, wheel((i+j) % 255))
            pixels.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, pixels.count(), 3):
                pixels.set_pixel(i+q, 0)

#newer ones from led lights
# list of the lights to use in patterns
pattern_lights = range(0, PIXEL_COUNT)

class LightsController(object):
    """Contains functions for controlling the lights"""
    @staticmethod
    def off(lights=None):
        if lights is None:
            pixels.clear()
        else:
            for i in lights:
                pixels.set_pixel_rgb(i, 0, 0, 0)
        pixels.show()

    @staticmethod
    def on(lights=None):
        if lights is None:
            LightsController.set_color()
        else:
            for i in lights:
                pixels.set_pixel_rgb(i, color['r'], color['g'], color['b'])
            pixels.show() 

    @staticmethod
    def set_color(light=None, show=True):
        """Set a specific led or all leds to the current color
           Set show to False to skip calling pixels.show()
        """
        if light is None:
            pixels.set_pixels_rgb(color['r'], color['g'], color['b'])
        else:
            pixels.set_pixel_rgb(light, color['r'], color['g'], color['b'])
        if show:
            pixels.show()

    @staticmethod
    def get_random_color():
        """Gets a random color - RGB values"""
        color = {
            'r': random.randint(0, 255),
            'g': random.randint(0, 255),
            'b': random.randint(0, 255)
        }
        return color

    @staticmethod
    def brightness_decrease(wait=0, step=1):
        """Decrease the brightness until black"""
        for j in range(int(256 // step)):
            for i in range(pixels.count()):
                r, g, b = pixels.get_pixel_rgb(i)
                r = int(max(0, r - step))
                g = int(max(0, g - step))
                b = int(max(0, b - step))
                # we don't need to check the is_rbg flag here because this decreases from the current values
                pixels.set_pixel_rgb(i, r, g, b)
            pixels.show()
            # if we have reached black, then we are done
            if r == 0 and g == 0 and b == 0:
                break
            if wait > 0:
                time.sleep(wait)

    @staticmethod
    def brightness_increase(wait=0, step=1):
        """Increase the brightness until full"""
        for j in range(int(256 // step)):
            for i in range(pixels.count()):
                r = int(min(j, color['r']))
                g = int(min(j, color['g']))
                b = int(min(j, color['b']))
                pixels.set_pixel_rgb(i, r, g, b)
            pixels.show()
            # if we have reached the full color, then we are done
            if r == color['r'] and g == color['g'] and b == color['b']:
                break
            if wait > 0:
                time.sleep(wait)

    @staticmethod
    def wheel(pos):
        """The wheel function to interpolate between different hues"""
        if pos < 85:
            return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)
#end of the controller classes

#new defs from led lights

def chase_up(delay=0.05, pause=0.1, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light])
            time.sleep(delay)
            LightsController.off([light])
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True
 
def chase_down(delay=0.05, pause=0.1, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights[::-1]:
            LightsController.on([light])
            time.sleep(delay)
            LightsController.off([light])
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fill_up(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light])
            time.sleep(delay)
        time.sleep(pause)
        LightsController.off()
        time.sleep(delay)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fill_down(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights[::-1]:
            LightsController.on([light])
            time.sleep(delay)
        time.sleep(pause)
        LightsController.off()
        time.sleep(delay)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fill_up_and_down(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light])
            time.sleep(delay)
        time.sleep(pause)
        for light in pattern_lights[::-1]:
            LightsController.off([light])
            time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fill_up_chase_up(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light])
            time.sleep(delay)
        for light in pattern_lights:
            LightsController.off([light])
            time.sleep(delay)
        time.sleep(pause)
        LightsController.off()
        time.sleep(delay)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def alternating(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    group1 = [i for i in pattern_lights if i % 2]
    group2 = [i for i in pattern_lights if i % 2 == 0]
    while not done:
        LightsController.off(group2)
        time.sleep(delay)
        LightsController.on(group1)
        time.sleep(pause)
        LightsController.on(group2)
        time.sleep(delay)
        LightsController.off(group1)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def random_sets(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        # get a random half from the available lights
        lights = random.sample(pattern_lights, PIXEL_COUNT // 2)
        LightsController.on(lights)
        time.sleep(pause)
        LightsController.off(lights)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def random_on_off(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    lights = list(pattern_lights)
    while not done:
        random.shuffle(lights)
        for light in lights:
            LightsController.on([light])
            time.sleep(delay)
        time.sleep(pause)
        random.shuffle(lights)
        for light in lights:
            LightsController.off([light])
            time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def appear_from_back_again(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        # in order to speed up this pattern in goes in "blocks" of 10
        for i in range(0, PIXEL_COUNT, 10):
            for j in reversed(range(i, PIXEL_COUNT)):
                pixels.clear()
                # first set all pixels at the beginning
                for k in range(i):
                    LightsController.set_color(k, show=False)
                # set the pixel at position j and the 9 preceeding pixels
                for m in range(max(j-9, 0), j+1):
                    LightsController.set_color(m, show=False)
                pixels.show()
                time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fade_in_out(delay=0.1, pause=0.5, rounds=0):
    LightsController.off()
    done = False
    current_round = rounds
    while not done:
        LightsController.brightness_increase(wait=delay)
        time.sleep(pause)
        LightsController.brightness_decrease(wait=delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

# old ones
def rainbow_colors(pixels, wait=0):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness_decrease(pixels, wait=0, step=1):
    for j in range(int(256 // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def blink_color(pixels, blink_times=5, wait=0, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)


def appear_from_back(pixels, color=(255, 0, 0)):
    pos = 0
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0)





if __name__ == "__main__":
    while True:
        pixels.clear()
        pixels.show()
        ## time.sleep(1)
        ## Clear all the pixels to turn them off.
        ## pixels.clear()
        ## pixels.show()  # Make sure to call show() after changing any pixels!
        ##random colour range list of contrasting colours
        for x in range(0, 5):
            #color = get_random_color()
            #chase_up(delay=0.05, pause=0, rounds=1)
            #chase_down(delay=0.05, pause=0, rounds=1)
            color = get_random_color()
            fill_up(delay=0.05, pause=0, rounds=1)
            fill_down(delay=0.05, pause=0, rounds=1)
            color = get_random_color()
            #fill_up_chase_up(delay=0.05, pause=0, rounds=1)
        for x in range(0, 5):
            #color = LightsController.get_random_color()
            #alternating(delay=0.05, pause=0, rounds=1)
            #color = LightsController.get_random_color()
            #random_sets(delay=0.05, pause=0, rounds=1)
            #random_on_off(delay=0.05, pause=0, rounds=1)
            color = get_random_color()
            appear_from_back_again(delay=0.05, pause=0, rounds=1)
            fade_in_out(delay=0.05, pause=0, rounds=1)
	for x in range(0, 5):
            coloor = []
            coloor = random.choice(listcolours)
	    appear_from_back(pixels, color=(coloor[0], coloor[1], coloor[2]))
        #brightness_decrease(pixels)
	for x in range(0, 10):
	    coloor = []
	    coloor = random.choice(listcolours)
	    colorWipe(pixels, Color(coloor[0], coloor[1], coloor[2]))
  	    #truly random colours, actually not as good
	    coloor = get_random_color()
            colorWipe(pixels, Color(coloor['r'], coloor['g'], coloor['b']))
        #brightness_decrease(pixels)
        #for x in range(0, 5):
            #coloor = []
            #coloor = random.choice(listcolours)
	    #theaterChase(pixels, Color(coloor[0], coloor[1], coloor[2]))
        #brightness_decrease(pixels)
        rainbow_cycle_successive(pixels, wait=0)
        rainbow_cycle(pixels, wait=0)
        #brightness_decrease(pixels)
        #for x in range(0, 5):
            #coloor = []
            #coloor = random.choice(listcolours)
            #blink_color(pixels, blink_times = 1, color=(coloor[0], 0, 0))
            #blink_color(pixels, blink_times = 1, color=(0, coloor[1], 0))
            #blink_color(pixels, blink_times = 1, color=(0, 0, coloor[2]))
            #blink_color(pixels, blink_times = 1, color=(coloor[0], coloor[1], coloor[2]))
        rainbow_colors(pixels)
        #theaterChaseRainbow(pixels)
        rainbow_cycle_successive(pixels, wait=0)
        rainbow_cycle(pixels, wait=0)
        #brightness_decrease(pixels)

        
