from .equipment.dehumidifier import Dehumidifier
from .equipment.hydrogenTank import HydrogenTank
from .equipment.turbine import Turbine
from .equipment.heater import Heater
from .equipment.cooler import Cooler
from .equipment.condenser import Condenser
from .equipment.pump import Pump
from .equipment.pemElectrolyzer import pemElectrolyzer
from .equipment.reservoir import Reservoir

# Imports the specific equipment classes (Turbine, Heater, Condenser, Pump)
# from the 'equipment' directory. This allows the pemCycle class to recognize and interact
# with these specialized types of equipment.

import networkx as nx
import matplotlib.pyplot as plt
# Imports the 'networkx' and 'matplotlib.pyplot' libraries.
# 'networkx' is a library for creating and manipulating graphs.
# 'matplotlib.pyplot' is used to plot and visualize the graphs.
# They are specifically used in the 'draw' method to generate a cycle diagram.


class pemCycle(): # Defines the pemCycle class without inheriting any other class.
    def __init__(self): # Constructor of the pemCycle class without any arguments other than 'self'.

        self.equipments = [] # Initializes an empty list for the equipments of the pemCycle
        self.connectors = [] # Initializes an empty list for the connectors of the pemCycle
        self.efficiency = None # Initializes the efficiency attribute as None.
        self.W_liq = None
        self.Q_in = None

    def add_equipment(self, equipment):
        # This method allows adding an instance of Equipment (or a subclass of Equipment) to the cycle's equipment list.
        self.equipments.append(equipment)

    def initialize(self):
        # This method is crucial for configuring the connections between equipment and connectors.
        # Iterates through all added equipment and establishes cross-references.

        for equipment in self.equipments: # Iterates over each equipment in the cycle.
            for connector in equipment.connectors_in: # For each input connector of the equipment:
                connector.add_equipment_out(equipment) # Informs the connector that this equipment is the OUTPUT equipment for it (destination of the stream).
                if connector not in self.connectors: # If the connector has not yet been added to the general list of cycle connectors:
                    self.connectors.append(connector) # Adds it so it can be iterated and calculated.
                equipment.properties_in.append(connector.property_out) # Adds the 'property_out' of the connector (which is the stream entering the equipment) to the 'properties_in' list of the equipment.

            for connector in equipment.connectors_out: # For each output connector of the equipment:
                connector.add_equipment_in(equipment) # Informs the connector that this equipment is the INPUT equipment for it (origin of the stream).
                if connector not in self.connectors: # If the connector has not yet been added to the general list of cycle connectors:
                    self.connectors.append(connector) # Adds it.
                equipment.properties_out.append(connector.property_in) # Adds the 'property_in' of the connector (which is the stream exiting the equipment) to the 'properties_out' list of the equipment.

                # Important note about 'properties_in/out' of the equipment:
                # The current logic assumes that the 'property_out' of a connector is the input of an equipment and 'property_in' of a connector is the output of an equipment. This means that, when connecting A -> Connector -> B:
                # A.properties_out must be equal to Connector.property_in;
                # B.properties_in must be equal to Connector.property_out;
                # And, ideally, Connector.property_in must be equal to Connector.property_out.
                # This configuration of 'initialize' is critical for data flow.


    def calculate(self): # This method orchestrates the sequence of calculations for the cycle.
        for connector in self.connectors: # Iterates between the connector elements.
            connector.calculate()  # First, calculates the properties of the streams in all connectors. This ensures that all thermodynamic properties (H, S, T, P) of the streams are determined by the CoolProp library before making the equipment balances.

        for equipment in self.equipments: # Iterates between the equipment.
            equipment.energy_balance() # Next, calculates the enthalpy balance for each equipment. This method (inherited from the Equipment class) calculates 'enthalpy_balance = H_out - H_in'.

        for equipment in self.equipments: # Again, iterates between the equipment.
            equipment.calculate() # Finally, calculates the specific heat or work of each equipment. This method is polymorphic: each subclass (Condenser, Heater, Pump, Turbine) has its own implementation of 'calculate' that uses 'enthalpy_balance' to determine 'heat' or 'work'.

    def calculate_efficiency(self): # This method calculates the efficiency of the thermodynamic cycle. Efficiency is typically defined as (Net Work Generated) / (Heat Added).
        W_liq = 0.0 # Initializes the net work as zero.
        Q_in = 0.0 # Initializes the total heat added as zero.

        for equipment in self.equipments: # Iterates over each equipment to sum the work and heat.
            if isinstance(equipment, pemElectrolyzer): # If the equipment is a Turbine (which generates positive work):
                W_liq += equipment.work
                Q_in += equipment.heat
            #elif isinstance(equipment, Pump): # If the equipment is a Pump (which consumes work, so 'work' will be negative):
            elif isinstance(equipment, Pump):
                Q_in -= equipment.work

            elif isinstance(equipment, Heater): # If the equipment is a Heater (which adds positive heat):
                Q_in -= equipment.heat

            elif isinstance(equipment, Cooler):
                Q_in -= equipment.heat
                # Note: Condensers are not included in Q_in because they remove heat (Q_out).

            elif isinstance(equipment,Reservoir):
                Q_in -= equipment.work

            elif isinstance(equipment, Dehumidifier):
                Q_in -= equipment.work

            elif isinstance(equipment,HydrogenTank):
                Q_in -= equipment.work

        self.W_liq = W_liq
        self.Q_in = Q_in
        #self.efficiency = pemElectrolyzer.flowRates(self.efficiency)
        self.efficiency = W_liq / Q_in # Calculates the efficiency by dividing the net work by the heat added and stores the result. It is important to note that 'W_liq' is the algebraic sum of positive work (turbine) and negative work (pump).

        self.resume = (f"--- Cycle W_liq = {self.W_liq} \n"
                       f"--- Cycle W_in = {self.Q_in} \n"
                       f"--- Cycle Overall Efficiency = {self.efficiency}\n")

    def draw(self, output_file): # This method generates a visual diagram of the cycle using networkx and matplotlib.
        G = nx.DiGraph() # Creates a new directed graph (DiGraph) from networkx.
        # Directed graphs are suitable for cycles where the flow has a direction.

        for connector in self.connectors: # Iterates over each connector to add edges (connections) to the graph.
            G.add_edge(connector.equipment_in.name,
                       connector.equipment_out.name,
                       label=connector.name)
            # Adds an edge from the connector's input equipment to the connector's output equipment. The edge's 'label' will be the connector's name, facilitating identification in the diagram.

        plt.figure(figsize=(10, 8)) # Creates a new matplotlib figure with a specific size.
        pos = nx.circular_layout(G) # Calculates the positions of the nodes (equipment) in a circular layout for the graph.

        nx.draw(G, pos, with_labels=True, node_size=6000, node_color='lightblue', arrows=True, font_size=10)
        # Draws the graph:
        # - G: the graph to be drawn.
        # - pos: the calculated positions of the nodes.
        # - with_labels=True: displays the names of the equipment on the nodes.
        # - node_size: size of the nodes.
        # - node_color: fill color of the nodes.
        # - arrows=True: draws arrows to indicate the flow direction.
        # - font_size: font size of the node labels.

        edge_labels = nx.get_edge_attributes(G, 'label')  # Gets the edge labels (which are the connector names).
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red') # Draws the labels on the edges.

        plt.savefig(output_file, dpi=300) # Saves the generated figure to a file. 'dpi' (dots per inch) defines the resolution.

        plt.show()
        # plt.close() # Closes the figure to release memory.