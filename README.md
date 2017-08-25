# trackerProgram version 1.2
A tool to track any object of a certain color with a camera, displaying a square on aimed object.

It was designed to be a tool to configure any program which needs to track an specified object with a camera.

Our project is to use it for creating a 'numeric theremin' (search www.google.com to learn what's a theremin) : theremin's player will wear gloves of a certain color and be allowed to play music, moving his hands in front of his camera.
Before, he will have to use this program to set the instrument.
That's why this program save user's setting in a file which will be used by theremin's program.

This version implements a startup widget which allows the user to choose which camera he wants to use.
Thus, no or several cameras can be pluggeg without bug.

The code also has a new structure : it is more divided in order to provide a good flexibility.
The old structure involved a fat main class (which was WorkingSetting). Now the main class
(DisplayFrames) is no more a subclass and is as big as the others. That reduces the number of self attributes
and makes the code more flexible.

This program is achieved with Python 2.7.13, using OpenCV 3.2.0 and PyQt 4.8.7.

We are Vanessa Dan, Eve Machefert and Alix Plamont, french students working on this school project.
