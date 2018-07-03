Linear-Pong

A game of pong designed to be playable on a linear strip of individually addressable RGB-LEDs.

The first, and current, version I have working is written in CircuitPython for the Adafruit Playground Express.
This is purely because I have a bunch of them lying around that I got for free with shipments, and they
are super easy to code for. The built-in LEDs and speaker are great bonuses too, meaning that all 
the external components needed for a basic game is a potentiometer!

Attach a 3.3V analog signal to A1 for control, otherwise all the files just need to be copied to the 
root directory of the Playground Express board running CircuitPython.

