class Equipment(): # Defines a new class called 'Equipment'
    def __init__(self, name):
        # The __init__ method is the class constructor.
        # It is called whenever a new instance of Equipment is created.
        # 'self' refers to the current instance of the class.
        # 'name' is an argument that must be provided when creating an equipment.

        self.name = name
        # Assigns the provided name to the 'name' attribute of the instance.

        self.connectors_in = []
        # Initializes an empty list to store input connectors (pipes).

        self.connectors_out = []
        # Initializes an empty list to store output connectors.

        self.properties_in = []
        # Initializes an empty list to store the properties (temperature, pressure...) of the input streams.

        self.properties_out = []
        # Initializes an empty list to store the properties of the output streams.

        self.heat = None
        # Initializes the 'heat' attribute as None. This attribute will represent the heat exchange of the equipment.

        self.work = None
        # Initializes the 'work' attribute as None. This attribute will represent the work of the equipment.

    def add_connectors_in(self, connector): # method to add connectors to the input connectors list.
        self.connectors_in.append(connector)

    def add_connectors_out(self, connector): # method to add connectors to the output connectors list
        self.connectors_out.append(connector)

    def set_heat(self, heat): # method that allows assigning a heat value to the equipment.
        self.heat = heat

    def set_work(self, work): # method that allows assigning a work value to the equipment.
        self.work = work

    def energy_balance(self):
        # method calculates the energy balance of the equipment.
        h_in = 0.0 # Initializes input enthalpy to zero.
        h_out = 0.0 # Initializes output enthalpy to zero.
        print(self.name) # Prints the equipment name for identification.
        for property in self.properties_in: # Loop through the properties_in list
            print('- IN:') # Adds the 'in' label for input properties.
            print(property.resume) # Prints the property summary implemented in thermoProperty.py
            h_in += property.H * property.mass_flow_rate # Calculates the enthalpy carried by the flow into the equipment.

        for property in self.properties_out: # Loop through the properties_out list
            print('- OUT:') # Adds the 'out' label for output properties.
            print(property.resume)
            h_out +=  property.H * property.mass_flow_rate # Calculates the enthalpy carried by the flow out of the equipment.

        self.enthalpy_balance = h_out - h_in # Calculates the enthalpy balance (Output - Input) and stores it in the 'enthalpy_balance' attribute of the instance.