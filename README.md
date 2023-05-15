# rail-network-simulator #


<img src="https://github.com/KrazIvan/rail-network-simulator/blob/main/Some%20generated%20maps/RailNetworkMap6.PNG" alt= "A generated map of a rail network from this program." width="600" height="600">

This program is an interactive rail network simulator that features options to advance time, see 
information on trains, get route information, and generate maps of the entire current network.
The program also simulates train delays.

## How the program is started and used. ##
You start the program by simply running it, you will be prompted to input the name of a 
stations file and a connections file, which you will need in order to use the program. These are 
provided in the same folder as the program. It’s possible to skip the file inputs if they get too 
tedious by uncommenting two lines of commented code above them and simply writing the 
name of your files there. After inputting the file names, you will 
have to input the number of trains you want to simulate (note that you must have at least one 
train).

After inputting the files and the number of trains you want. You’ll be taken to an 
options menu, where you can advance time forward in the simulation, see the positions of 
trains by their ID numbers and what stations and lines they are on and if they got delayed. 
You can also check the route information, which will tell you if it’s possible to reach a 
specific station on the rail network from another station, in a given time frame. The can
also generate a map of the entire rail network, which will show you all of the stations, lines
and the trains.

You can quit the simulation at any moment at this point by inputting “*q*”, which will quit the simulation 
and run some unit tests.

## Which libraries/modules are used and how these are downloaded and installed if they are not part of Python’s standard distribution ##

The original *trains.py* (*originaltrains.py*) doesn’t use any libraries/modules that need to be manually installed or 
downloaded. The program uses the built-in random module (to create randomness) and the 
unittest module (to do unit tests). Both are part of Python’s standard distribution.

However the new *trains.py* (which can generate rail network maps) requires the *Matplotlib* and *NetworkX* libraries. 
You'll need to install these libraries as they aren't part of Python’s standard distribution.
The new *trains.py* also uses the *defaultdict* from *collections*, but *collections* is part of Python’s standard distribution.

## A description of how the program is structured (which files contain what, etc.) ##

The program starts by getting the information it needs from the stations file and the 
connections file in order to create the rail network and simulate it. 
The program gets the station names and their respective risks of delaying a 
train from the stations file, and the program gets the information on how stations are 
connected and which line/lines they belong to from the connections file. It also gets the 
number of trains to simulate from the user. The program separates this information into 
variables which it then uses to create the *Train*, *Station*, *Line* and *RailNetwork* classes and 
their attributes, these classes in turn have their own function/methods and perform different 
tasks in the simulation, such are moving trains to different stations, delaying trains, etc. 
Similarly to their real-life counterparts.

The *RailNetwork* class is the “main” class of the 
simulation though, as it is the one performing the simulation by using the Train, Station and 
Line objects.

## Code design ##
The code is designed in an object-oriented way, where each class represents a real-life train, 
station, and line in a rail network. The network itself is a class too. The code has extensive 
error handling and commented “Dev features” that a user can uncomment if they wish to use 
them, in order to make the program less tedious to use. The program input prompts are 
designed to be as liberal as possible (case insensitive, ignores accidental spaces and dots) in 
order to not annoy a user who accidentally inputs an otherwise coherent input by giving them 
an error or invalid input message. Every function/class also features a docstring and 
comments which explains how they are supposed to work.

## Which algorithms are used and why ##
The *station_reachability_checker()* function makes use of a breadth-first search algorithm in 
order to implement a route info option in the program that will determine if 
it’s possible to reach a target station within a given amount of time steps.

When generating the map, the placement of the stations is set using the Fruchterman-Reingold force-directed algorithm.
