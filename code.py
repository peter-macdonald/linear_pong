import time
import array
import math
import random
import board
import neopixel
import audioio
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

sound = True

FREQUENCY = 440  # 440 Hz middle 'A'
SAMPLERATE = 8000  # 8000 samples/second, recommended!

# Button
button = DigitalInOut(board.BUTTON_A)
button.direction = Direction.INPUT
button.pull = Pull.DOWN

# Generate one period of sine wav.
length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)
 
# enable the speaker
spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = Direction.OUTPUT
spkrenable.value = True

sample = audioio.AudioOut(board.SPEAKER, sine_wave)
sample.frequency = SAMPLERATE

# Setup the pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()

# Setup the controller
controller = AnalogIn(board.A1)

while True:

    dir_x = 1
    dir_y = 1
    speed_x = 5
    speed_y = 10
    min_x = 1
    max_x = len(pixels) - 1
    min_y = 0
    max_y = 200
    inc_x = 0.3
    inc_y = 30
    max_speed_x = 20
    max_speed_y = 255

    position_x = min_x
    position_y = 0

    paddle_x = 0
    paddle_y = 0
    paddle_width = 100

    def getVoltage(pin):  # helper
        return (pin.value * 3.3) / 65536

    def gaussian(x, a, b, c):
        ''' a is the height, b is the center, c is the shape'''
        return a * (3 ** (-((x-b)**2)/(2*c**2)))

    def y2Color(y):
        col = (0, 0, 0)
        if y < 85:
            col = (y * 3, 255 - y * 3, 0)
        elif y < 170:
            y -= 85
            col = (255 - y * 3, 0, y * 3)
        else:
            y -= 170
            col = (0, y * 3, 255 - y * 3)
        return col

    def drawPaddle():
        pixels[0] = y2Color(paddle_y)

    def drawBall():
        for i in range(0,len(pixels)):
            dist = i - position_x
            brightness = gaussian(dist, 1, 0, 0.3)
            pixels[i] = tuple(int(brightness * col) for col in y2Color(position_y))

    def isColliding(pos, lim_min, lim_max):
        if pos < lim_min or pos >= lim_max:
            return True
        return False

    def getTime():
        return time.monotonic()

    def playTone():
        if sound:
            sample.play(loop=True)  # keep playing the sample over and over
            time.sleep(0.01)  # until...
            sample.stop()  # we tell the board to stop

    def gameOver():
        global dir_x
        global dir_y
        print('GAME OVER')
        dir_x = 0
        dir_y = 0

        while not button.value:
            pass

    t = getTime()
    while True:
        dt = getTime() - t
        t = getTime()

        paddle_y = int((controller.value / 65535) * max_y)

        disp_x = speed_x * dt * dir_x
        position_x += disp_x
        if isColliding(position_x, min_x, max_x):
            if position_x >= max_x: # wall colliding
                pass
            else: # paddle colliding
                if not isColliding(position_y, paddle_y - paddle_width/2, paddle_y + paddle_width/2):
                    print('hit!')
                else:
                    print('miss!')
                    gameOver()
                    break

            print('bump', position_x)
            playTone()
            dir_x *= -1
            speed_x += inc_x
            speed_y += random.random() * inc_y - inc_y/2
            if speed_x > max_speed_x:
                speed_x = max_speed_x
            position_x = min(max_x, position_x)
            position_x = max(min_x, position_x)

        disp_y = speed_y * dt * dir_y
        position_y += disp_y
        if isColliding(position_y, min_y, max_y):
            playTone()
            dir_y *= -1
            speed_y += inc_y
            if speed_y > max_speed_y:
                speed_y = max_speed_y
            position_y = min(max_y, position_y)
            position_y = max(min_y, position_y)
        
        pixels.fill((0, 0, 0))
        drawBall()
        drawPaddle()
        pixels.show()