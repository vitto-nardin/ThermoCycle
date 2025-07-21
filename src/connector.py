class Connector(): # Defines a new class called Connector. Unlike equipment, it does not inherit from the
# Equipment class.

    def __init__(self, name, length):
        # The constructor of the Connector class.
        # 'name' is an identifier attribute for the connector (e.g., "Pump Outlet Stream", "Heater Inlet").

        self.name = name
        # Assigns the name to the connector.

        self.length = length

        self.DeltaP = None

        self.property_in = None
        # Initializes 'property_in' as None. This attribute will store a ThermoProperty object that represents the properties of the stream entering the connector (i.e., the one coming from the 'equipment_in' equipment).

        self.property_out = None
        # Initializes 'property_out' as None. This attribute will store a ThermoProperty object that represents the properties of the stream exiting the connector (i.e., the one going to the 'equipment_out' equipment). In an ideal connector, property_in and property_out should be identical, representing the same stream passing through the connector.

        self.equipment_in = None
        # Initializes 'equipment_in' as None. This attribute will store an instance of the Equipment class (or one of its subclasses, such as Pump, Heater, etc.) from which the stream is EXITING.

        self.equipment_out = None
        # Initializes 'equipment_out' as None. This attribute will store an instance of the Equipment class (or one of its subclasses) to which the stream is ENTERING.

    def add_equipment_in(self, equipment):
        # Adds the equipment from which the stream *arrives* (exited from) at this connector.
        self.equipment_in = equipment

    def add_equipment_out(self, equipment):
        # Adds the equipment to which the stream *goes* (will enter) from this connector.
        self.equipment_out = equipment


    def set_properties_in(self, property):
        # Defines the ThermoProperty object that describes the stream entering the connector.
        self.property_in = property

    def set_properties_out(self, property):
        # Defines the ThermoProperty object that describes the stream exiting the connector.
        self.property_out = property

    def pressureLoss(self):
        self.DeltaP = self.length*1000


    def calculate(self):
        # This method is called to ensure that the properties of the streams associated with this connector are calculated.

        self.property_in.calculate()
        # Calls the 'calculate()' method of the ThermoProperty object that represents the input.
        # This ensures that all thermodynamic properties of the inlet stream are determined based on the provided state properties.

        self.property_out.calculate()
        # Calls the 'calculate()' method of the ThermoProperty object that represents the output.
        # This ensures that all thermodynamic properties of the outlet stream are determined. Ideally, 'property_out' would be a copy or reference of 'property_in' in a simple connector, or there would be logic for 'property_out' to reflect the same conditions as 'property_in'.