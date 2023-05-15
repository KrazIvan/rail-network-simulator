import trains as t
import unittest

class TestRailNetwork(unittest.TestCase):
    def test_load_stations(self):
        '''
        Function that tests load_stations().
        
        '''
        network = t.RailNetwork()
        file_name = "test_stations.txt"
        with open(file_name, "w") as f:
            f.write("Hej,0.666\nPå,0.9\nDig,0.05\n")
        network.load_stations(file_name)
        # Checks that the name matches
        self.assertEqual(network.stations["Hej"].name, "Hej")
        self.assertEqual(network.stations["På"].name, "På")
        self.assertEqual(network.stations["Dig"].name, "Dig")
        # Checks that delay_probability matches
        self.assertEqual(network.stations["Hej"].delay_probability, 0.666)
        self.assertEqual(network.stations["På"].delay_probability, 0.9)
        self.assertEqual(network.stations["Dig"].delay_probability, 0.05)
    

    def test_load_connections(self):
        '''
        Function that tests load_connections().
        
        '''
        network = t.RailNetwork()
        stations_file = "test_stations2.txt"
        with open(stations_file, "w") as f:
            f.write("A,0.666\nB,0.187\nC,0.05\nD,0.69\n")
        network.load_stations(stations_file)
        connections_name = "test_connections.txt"
        with open(connections_name, "w") as test:
            test.write("A,B,red,N\nB,C,red,E\nC,D,red,S\n")
        network.load_connections(connections_name)
        # Checks that the stations are on the red line.
        self.assertIn("A", network.lines["red"].stations)
        self.assertIn("B", network.lines["red"].stations)
        self.assertIn("C", network.lines["red"].stations)
        self.assertIn("D", network.lines["red"].stations)
        # Checks that the names of the stations in the red line match.
        self.assertEqual(network.lines["red"].stations["A"].name, "A")
        self.assertEqual(network.lines["red"].stations["B"].name, "B")
        self.assertEqual(network.lines["red"].stations["C"].name, "C")
        self.assertEqual(network.lines["red"].stations["D"].name, "D")
    

    def test_station_reachability_checker(self):
        '''
        Function that tests station_reachability_checker().
        
        '''
        network = t.RailNetwork()
        test_connections = [('A', 'B', 'blue', 'S'),
                            ('B', 'C', 'blue', 'S'), 
                            ('C', 'D', 'blue', 'S'), 
                            ('X', 'Y', 'green', 'S'), 
                            ('Y', 'C', 'green', 'S'), 
                            ('C', 'Z', 'green', 'S')] # Connections for "Map 1".
        
        # Test with neighboring stations.
        self.assertTrue(network.station_reachability_checker("A", "B", 1, test_connections))
        self.assertFalse(network.station_reachability_checker("A", "B", 0, test_connections))
        self.assertTrue(network.station_reachability_checker("B", "A", 1, test_connections))

        # Test with same station.
        self.assertTrue(network.station_reachability_checker("A", "A", 0, test_connections))
        self.assertTrue(network.station_reachability_checker("X", "X", 666, test_connections))

        # Test with example from the assignment instructions.
        self.assertFalse(network.station_reachability_checker("A", "X", 3, test_connections))
        self.assertTrue(network.station_reachability_checker("A", "Z", 3, test_connections))

        # Test with impossible-to-get-to station.
        self.assertFalse(network.station_reachability_checker("A", "Meme", 10000, test_connections))
        self.assertFalse(network.station_reachability_checker("Meme", "A", 10000, test_connections))

        # Test recognition of reachability despite no connection stated.
        self.assertTrue(network.station_reachability_checker("Meme", "Meme", 0, test_connections))
        self.assertTrue(network.station_reachability_checker("Meme", "Meme", 1, test_connections))

        # Miscellaneous tests.
        self.assertTrue(network.station_reachability_checker("A", "D", 3, test_connections))
        self.assertFalse(network.station_reachability_checker("A", "D", 2, test_connections))
        self.assertTrue(network.station_reachability_checker("X", "Z", 3, test_connections))
        self.assertFalse(network.station_reachability_checker("X", "Z", 2, test_connections))


if __name__ == "__main__":
    unittest.main()