# rail-network-simulator by Ivan Shabalin

import random
import unittest
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

class Train:
    '''
    The Train class represents a train on the rail network.
    
    Attributes: 
    
    station: The station where the train is currently located.
    direction: The train's current direction (North or South).
    line: The line on which the train is running (blue, green, red, etc).
    train_id: Train's ID number.
    train_delayed: The train's delayed status (True or False).

    '''


    def __init__(self, station, direction, line, train_id, train_delayed):
        '''
        Function that initializes the Train object.
        
        Parameters: 

        station: The station where the train is currently located.
        direction: The train's current direction (North or South).
        line: The line on which the train is running (blue, green, red, etc).
        train_id: Train's ID number.
        train_delayed: The train's delayed status (True or False).

        '''
        self.station = station
        self.direction = direction
        self.line = line
        self.train_id = train_id
        self.train_delayed = train_delayed
    

    def __str__(self):
        '''
        Function that returns a string representation of the Train object, 
        with relevant information about the train to be used in the train info messages,
        including if the train got delayed.

        '''
        if self.train_delayed == True: # Displays "(DELAY)" on delayed trains.
            delay = " (DELAY)"
        else:
            delay = ""
        return f"\nTrain {self.train_id} on {self.line} line is at station {self.station.name} heading in {self.direction} direction{delay}\n"
    

class Station:
    '''
    The Station class represents a station on the rail network.
    
    '''
    def __init__(self, name, delay_probability):
        '''
        Function that initializes the Station object.
        
        Parameters: name: The station's name.
        delay_probability: The risk the station has of delaying a train on it.

        Stores trains in a list to add and remove from itself.

        '''
        self.name = name
        self.delay_probability = delay_probability
        self.trains = []
        
    
    def __str__(self):
        '''
        Function that returns a string representation of the Station object, 
        with relevant information about the station.

        '''
        return f"Station {self.name} with delay probability {self.delay_probability} and {len(self.trains)} trains"
    
    def add_train(self, train):
        '''
        Function to add a train to the station, in order to simulate the train entering the station.

        Parameter: A train.

        '''
        self.trains.append(train)
    
    def remove_train(self, train):
        '''
        Function to remove a train to the station, in order to simulate the train leaving the station.

        Parameter: A train.
        
        '''
        self.trains.remove(train)
    

class Line:
    '''
    The Line class represents a line on the rail network (such as for example a blue, green or red line).
    
    '''
    def __init__(self, name):
        '''
        Function that initializes the Station object.
        
        Parameters: name: The line's name/color (such as "blue", "green" or "red").

        Stores stations in a dictionary to add to lines and
        return station names.

        '''
        self.name = name
        self.stations = {}
    
    def __str__(self):
        '''
        Function that returns a string representation of the Line object, 
        with its name. Used to identify the line a train is on.

        '''
        return f"{self.name.upper()} line" # Uppercases the name.
    
    def add_station(self, station):
        '''
        Adds a station to the line.

        '''
        self.stations[station.name] = station
    
    def get_station(self, station_name):
        '''
        Returns a station from the line.

        '''
        return self.stations[station_name]
    

class RailNetwork:
    '''
    The RailNetwork class is the main class the whole simulation takes place in.
    It represents the entire network.
    
    '''
    def __init__(self):
        '''
        Function that initializes the RailStation object.
        Stores a dictionary of lines, with the line names as keys;
        a dictionary of stations, with the station names as keys;
        and a dictionary of trains, with the their ID numbers as keys.

        '''
        self.lines = {}
        self.stations = {}
        self.trains = {}
    
    def __str__(self):
        '''
        Function that returns a string representation of the RailNetwork object, 
        with relevant information about the rail network, such as amount of lines,
        amount of stations, and amount of trains in it.

        '''
        return f"Rail network with {len(self.lines)} lines, {len(self.stations)} stations, and {len(self.trains)} trains"
    
    def add_line(self, line):
        '''
        Function that adds a line to the network.
        
        Parameter: a line.

        '''
        self.lines[line.name] = line
    
    def add_station(self, station):
        '''
        Function that adds a station to the network.
        
        Parameter: a station.
        
        '''
        self.stations[station.name] = station
    
    def add_train(self, train, train_id):
        '''
        Function that adds a train to the network.
        
        Parameters: a train and its ID number.
        
        '''
        self.trains[train_id] = train
    

    def load_stations(self, filename):
        '''
        Function that loads and interpretes a stations file and adds its information into the Station object.
        
        Important for it to work: The txt file has to have a line for each station 
        with its risk of causing a delay (written in decimal form) separated by a comma,
        with no additional information or empty lines.
        
        Parameter: The file name of the stations file as a string.
        
        '''
        with open(filename, "r") as f:
            for line in f:
                name, delay_probability = line.strip().split(",") # Seperates information into variables.
                delay_probability = float(delay_probability) # Converts delay risk to a float
                station = Station(name, delay_probability)
                self.add_station(station) # Adds information to the Station object.
    

    def load_connections(self, filename):
        '''
        Function that loads and interpretes a connections file and adds its information into the Line object.
        
        Important for it to work: The txt file has to have a line for each connection 
        with all of its information written in order (source station, target station, line name, direction) 
        and separated by a comma,
        with no additional information or empty lines.
        
        Parameter: The file name of the connection file as a string.
        
        '''
        with open(filename, "r") as f:
            for line in f:
                # Seperates information into variables
                source, target, line_name, direction = line.strip().split(",")

                # Assign the source station and target station.
                source_station = self.stations[source]
                target_station = self.stations[target]

                # Creates new Line objects for new lines found
                # And adds them to the RailNetwork
                if line_name not in self.lines:
                    line = Line(line_name)
                    self.add_line(line)
                else:
                    line = self.lines[line_name]
                # Adds the source station and target station 
                line.add_station(source_station) 
                line.add_station(target_station) 
    

    def station_reachability_checker_file_opener(self, file_name):
        '''
        Function for opening a connections file 
        and returning a list of information (a list of tuples containing the pairs of station names)
        for station_reachability_checker() to interprete.

        Parameter: A connections file name as a string.
        '''
        with open(file_name, "r") as f:
            return [tuple(line.strip().split(",")) for line in f]
    

    def station_reachability_checker(self, start, target, time_limit, connections):
        '''
        Function for determining if it's possible to reach a station from 
        another station within a given time frame/movement limit.

        Parameters: The start station's name as a string; the target station's name as a string;
        the maximum amount of timesteps allowed, as an int; 
        and a list of tuples that all contain a pair of connected stations.
        
        Returns: True if it's possible, otherwise False.
        '''
        # Creates a queue to store the stations to visit
        queue = [(start, 1)] # Updates the time to 1
        visited = set()
        # While stations in queue
        while queue:
            # Gets next station and the time it took to reach it.
            station, time = queue.pop(0)
            # If target station is reached, return True.
            if station == target:
                return True
            # If failed to reach target before time limit, continue.
            if time > time_limit:
                continue
            # Adds station to visited list.
            visited.add(station)
            # Counts all non-visited connections of the current station to the queue.
            for connection in connections:
                if connection[0] == station and connection[1] not in visited:
                    queue.append((connection[1], time + 1)) # Updates time by 1
                elif connection[1] == station and connection[0] not in visited:
                    queue.append((connection[0], time + 1)) # Updates time by 1
        # Returns False if all possible stations have been visited without reaching target.
        return False

    
    def get_start_line(self, station):
        '''
        Function for finding and returning a line/lines from a station.

        Parameters: A Station object.
        
        Returns: A (randomly choosen) line.

        The function randomly chooses a line in case a station exists
        on more than one line (such as the case for station C in Map 1),
        so that you don't get multiple lines from the same station.

        Warning: Needs the random module to work.

        '''
        matching_lines = []

        for line in self.lines.values():
            for s in line.stations:
                if s == station.name:
                    matching_lines.append(line)

        return random.choice(matching_lines)

    
    def generate_train_map(self, connections_file):
        '''
        Function for creating a map of rail network by plotting the trains, stations and lines.

        Parameters: A connections file.
        
        Output: Displays a map of the rail network.

        Warning: Needs matplotlib.pyplot, networkx modules and the defaultdict to work.

        '''
        # Collects all the Train ojects in a list.
        all_trains = [train_obj for train_obj in self.trains.values()]

        # Reads the connections file.
        with open(connections_file, "r") as f:
            connections = f.readlines()

        # Creates the graph.
        G = nx.MultiDiGraph()

        for line in connections:
            source, target, line_name, direction = line.strip().split(',')
            G.add_edge(source, target, line=line_name, direction=direction)

        # Sets the positions of the nodes using the Fruchterman-Reingold algorithm.
        position = nx.spring_layout(G, k=1, seed=666)

        # Draws the nodes.
        nx.draw_networkx_nodes(G, position, node_size=300, node_color="w")

        # Draws the edges.
        edge_colors = []
        for _, _, attrs in G.edges(data=True):
            if "line" in attrs:
                edge_colors.append(attrs["line"])
            else:
                edge_colors.append("black") # Makes black the default color of the lines if the station's name isn't a color.
        nx.draw_networkx_edges(G, position, edge_color=edge_colors, width=2, arrowsize=20, arrowstyle="-")

        # Adds labels to the nodes.
        nx.draw_networkx_labels(G, position, font_size=10, font_family="sans-serif")

        # Gets the trains on each station.
        station_trains = defaultdict(list)
        for train in all_trains:
            station_trains[train.station].append(train)

        # Adds the trains' IDs to the map.
        for station, all_trains in station_trains.items():
            train_labels = [train.train_id for train in all_trains]
            x, y = position[station.name]
            plt.text(x, y - 0.03, "\n".join(str(train_label) for train_label in train_labels), fontsize=8, ha="center", va="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7))

        # Sets the axis limits and removes them.
        plt.axis("off")
        plt.xlim(-1.2, 1.2)
        plt.ylim(-1.2, 1.2)
        plt.title("Rail Network Map")

        # Shows the plot.
        plt.show()


    def simulate(self):
        '''
        Function that initiates the train simulation. 

        Continue simulation [1]: Simulates one time unit in the simulation.
        Trains move from one station to the next according to their direction (unless delayed), 
        when they reach an end of a line, they switch direction.
        
        Train info [2]: Shows information about each train in the simulation.

        Route info [3]: Determines if it's possible to reach a station from another station 
        within the given time frame.

        Show rail network map [4]: Shows a map of the entire network, along with all the trains and what station they're on.

        '''
        input_prompt = "Continue simulation [1], train info [2], route info [3], show rail network map [4], exit [q].\nSelect an option: "
        # Main simulation loop.
        while True:
            # Makes input case insensitive, and allows spaces and dots, for less strict inputs.
            choice = input(input_prompt).lower().replace(" ","").replace(".","")
            # Input checkpoint
            while not choice == "1" and choice != "2" and not choice == "3" and choice != "4" and not choice == "q":
                print("\nInvalid input.\n")
                choice = input(input_prompt).lower().replace(" ","").replace(".","") # New input if invalid
            if choice == "1": # Continue simulation [1]
                self.advance_time()
                print("\n", end="")
            elif choice == "2": # Train info [2]
                train_id = (input("Which train [1 - {}]: ".format(num_trains)))
                while True:
                    # Input checkpoint
                    if not int_check(train_id): # Not an int.
                        print("\nInvalid input. Don't input nonsense.\n")
                        train_id = (input("Which train [1 - {}]: ".format(num_trains)))
                        continue
                    elif not (int(train_id) >= 1 and int(train_id) <= num_trains): # Int not a train ID number.
                        print("\nInvalid input. Input the ID number of a train that exists.\n")
                        train_id = (input("Which train [1 - {}]: ".format(num_trains)))
                        continue
                    else:
                        break # Input checkpoint clear
                train_id = int(train_id)
                train = self.trains[train_id]
                print(train)
            elif choice == "3": # Route info [3]
                start_station_for_info = input("Select a start station: ")
                end_station_for_info = input("Select an end station: ")
                timesteps_for_info = input("Select timesteps: ")
                # Input checkpoint
                while not int_check(timesteps_for_info): # Not an int
                    print("\nInvalid input. Input a valid integer.\n")
                    timesteps_for_info = input("Select timesteps: ")
                timesteps_for_info = int(timesteps_for_info) # Input checkpoint clear
                connections = self.station_reachability_checker_file_opener(connections_file) # Opens the connections file.
                # Checks and prints if the stations can be reached in time.
                if self.station_reachability_checker(start_station_for_info, end_station_for_info, timesteps_for_info, connections) == True:
                    print(f"\nStation {end_station_for_info} is reachable from station {start_station_for_info} within {timesteps_for_info} timesteps.\n")
                if self.station_reachability_checker(start_station_for_info, end_station_for_info, timesteps_for_info, connections) == False:
                    print(f"\nStation {end_station_for_info} is not reachable from station {start_station_for_info} within {timesteps_for_info} timesteps.\n")
            elif choice == "4":
                #print(f"Stations: {self.stations}")
                #print(f"Lines: {self.lines}")
                #print(f"Trains: {self.trains}")
                self.generate_train_map(connections_file)
            elif choice == "q": # Exits the program [q]
                print("Thank you and goodbye!")
                break
    
    
    def advance_time(self):
        '''
        Function that simulates the passage of time in the simulation. 

        Trains move from one station to the next according to their direction (unless delayed), 
        when they reach an end of a line, they switch direction.
        
        If a train gets delayed, it will stay in its station, and will gain a delay status of True,
        which is visible on the train information for the train.

        True delay statuses get reset when time advances again, 
        but will be regained if the train gets delayed again.

        Features two Dev features which can be uncommented for those that want them.

        '''
        for train_id, train in self.trains.items():
            train.train_delayed = False # Resets delay status to False
            current_station = train.station
            current_line = train.line
            current_index = list(current_line.stations.keys()).index(current_station.name)

            # Switches direction if an end station is reached.
            if current_index == 0:
                    train.direction = "South"
            if current_index == len(list(current_line.stations.keys())) - 1:
                    train.direction = "North"

            if random.uniform(0, 1) < current_station.delay_probability: # Simulates delay at current station
                # (Dev feature) Uncomment below to see delays as they happen.
                #print(f"Train {train_id} is delayed at station {current_station.name}")
                train.train_delayed = True
            else:
                # Find next station for the train.
                if train.direction == "North":  
                    next_index = current_index - 1
                else:
                    next_index = current_index + 1
                
                # Gets name of the next station and assigns it.
                next_station_name = list(current_line.stations.keys())[next_index]
                next_station = current_line.get_station(next_station_name)

                # Moves the train by removing it from current station
                # and placing it on the next station.
                train.station.remove_train(train)
                next_station.add_train(train)
                train.station = next_station
                # (Dev feature) Uncomment below to simultaneously see where each train went.
                #print(f"Train {train_id} arrived at station {next_station.name}")


def file_existance_checker(filename):
    '''
    Function for making sure a file exists.

    Parameter: File name for a file.

    Returns False if the file doesn't exist, otherwise returns True.

    '''
    try: 
        with open(filename, "r") as test:
            return True
    except FileNotFoundError:
        return False


def int_check(user_input):
    '''
    Function for making sure the an input from the user can be converted to an integer.

    Parameter: User input.

    Returns False if the input can't be converted to an integer, otherwise True.

    '''
    try: 
        int(user_input)
    except ValueError:
        return False
    return True


def string_and_lessthanone_check(user_input):
    '''
    Function for detecting 4 seperate issues with the user input in order to create
    custom messages related to each issue.

    Parameter: User input.

    Returns "Infraction 1" if the user puts infinity.
    Returns "Infraction 2" if the user puts negative infinity.
    Returns "Infraction 3" if the input can't be converted to an int (by using int_check()).
    Returns "Infraction 4" if the input can be converted to an int, but is less than 1.
    Returns "You're clear, you can go." if these issues aren't present.

    Warning: Needs int_check() to work.

    '''
    if user_input == "infinity" or user_input == "inf" or user_input == "infinite":
        return "Infraction 1"
    elif user_input == "-infinity" or user_input == "-inf" or user_input == "-infinite":
        return "Infraction 2"
    elif not int_check(user_input):
        return "Infraction 3"
    elif int(user_input) < 1:
        return "Infraction 4"
    else:
        return "You're clear, you can go."


def stations_file_check(filename):
    '''
    Function for checking if a stations file that be interpreted.

    Parameter: A stations name.

    Returns False if the file can't be interpreted by the stations loader, 
    otherwise returns True.

    '''
    try:
        with open(filename, "r") as f:
            for line in f:
                name, delay_probability = line.strip().split(",")
                delay_probability = float(delay_probability)
                return True
    except UnicodeDecodeError:
        return False
    except ValueError:
        return False
    except KeyError:
        return False


def connections_file_check(filename):
    '''
    Function for checking if a connections file that be interpreted.

    Parameter: A connections name.

    Returns False if the file can't be interpreted by the connections loader, 
    otherwise returns True.

    '''
    try:
        with open(filename, "r") as f:
            for line in f:
                source, target, line_name, direction = line.strip().split(",")
                return True
    except UnicodeDecodeError:
        return False
    except ValueError:
        return False
    except KeyError:
        return False


# The program initiates here.
if  __name__ == "__main__":
    network = RailNetwork()
    # (Dev feature) Uncomment the 2 below/comment the other 2 file inputs to skip file names inputs. Note that this would mean that the files won't be checked for errors.
    #stations_file = ("stations.txt")
    #connections_file = ("connections.txt")
    stations_file = (input("Enter name of stations file: "))
    # Valid file checkpoint for the stations file.
    while not file_existance_checker(stations_file) or not stations_file_check(stations_file):
        if not file_existance_checker(stations_file): # Checks if the station file exists.
            print("This file does not exist.")
            stations_file = input("Enter name of stations file: ")
            continue
        if not stations_file_check(stations_file): # Checks if the station file can be interpreted.
            print("This file cannot be interpreted.")
            stations_file = input("Enter name of stations file: ")
            continue
    connections_file = (input("Enter name of connections file: "))
    # Valid file checkpoint for the connections file.
    while not file_existance_checker(connections_file) or not connections_file_check(connections_file):
        if not file_existance_checker(connections_file): # Checks if the connections file exists.
            print("This file does not exist.")
            connections_file = input("Enter name of connections file: ")
            continue
        if not connections_file_check(connections_file): # Checks if the connections file can be interpreted.
            print("This file cannot be interpreted.")
            connections_file = input("Enter name of connections file: ")
            continue
    network.load_stations(stations_file) # Loads information from the stations file into RailNetwork
    network.load_connections(connections_file) # Loads info from connections file into RailNetwork
    num_trains = (input("Enter number of trains: ")).lower().replace(" ","")
    # Train number input checkpoint
    while True:
        # New input if requested an infinite amount of trains (Easter egg message)
        if string_and_lessthanone_check(num_trains) == "Infraction 1":
            print("We don't have the processing power to simulate an infinite number of trains, sorry. But we're getting there.")
            num_trains = (input("Enter number of trains: ")).lower().replace(" ","")
            continue
        # New input if requested an amount of trains less than 1
        if string_and_lessthanone_check(num_trains) == "Infraction 2" or string_and_lessthanone_check(num_trains) == "Infraction 4":
            print("You need to have at least one train.")
            num_trains = (input("Enter number of trains: ")).lower().replace(" ","")
            continue
        # New input if requested a non-integer
        if string_and_lessthanone_check(num_trains) == "Infraction 3":
            print("Input a valid integer (no decimal numbers or any other nonsense).")
            num_trains = (input("Enter number of trains: ")).lower().replace(" ","")
            continue
        # Checkpoint cleared if no input issues.
        if string_and_lessthanone_check(num_trains) == "You're clear, you can go.":
            num_trains = int(num_trains)
            break
    print("\n", end="")
    # Populates the rail network with trains 
    for i in range(num_trains):
        # Assigns a station for each train by random.
        station_name = random.choice([key for key in network.stations.keys()])
        # Assigns a direction for each train by random.
        direction = random.choice(["North","South"])

        station = network.stations[station_name]
        # Finds a line to assign to each train
        # This is to prevent issues with stations that exist on more than 1 line
        line = network.get_start_line(station)

        # Creates the Train object
        train = Train(station, direction, line, i+1, False)

        # Adds the train and its ID to the network. 
        network.add_train(train, i+1)
        station.add_train(train)

    network.simulate()