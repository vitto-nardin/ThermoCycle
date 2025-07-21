from .equipment import Equipment
# Imports the 'Equipment' class from the 'equipment' module.
# This import is fundamental for the Heater class to extend the functionality of Equipment.

class pemElectrolyzer(Equipment):
    # Defines the Heater class, indicating that it is a subclass of Equipment
    # through the syntax '(Equipment)'.

    def __init__(self, name):
        # The __init__ method is the constructor of the Heater class.
        # It is executed whenever a new instance of Heater is created.
        # 'name' is an argument that allows giving a descriptive name to the heater.

        super().__init__(name)
        # Calls the constructor of the parent class (Equipment) using 'super()'.
        # This is crucial for initializing all attributes defined in Equipment,
        # such as 'name', 'connectors_in', 'properties_in', 'heat', 'work', etc.

        self.heat = None
        self.work = None
        # Overrides the 'work' attribute (work) which was initialized as None in the Equipment class,
        # setting it to 0.0. Heaters are typically heat exchange devices
        # that do not perform or consume significant work, similar to condensers.

        self.current = None
        self.voltage = None
        self.temperature = None
        self.efficiency = None
        self.hydrogen_pressure = None

        self.inlet_water = None
        self.outlet_hydrogen = None
        self.outlet_water = None
        self.outlet_oxygen = None


    def calculate(self):
        # This method defines the specific calculation logic for a heater.
        # It will be called to determine the heat involved in the heater's process.

        self.heat = self.current*self.voltage
        self.work = (self.outlet_hydrogen/0.00201568)*285830
        # Assigns the value of 'self.enthalpy_balance' to 'self.heat'.
        # 'self.enthalpy_balance' is calculated by the 'energy_balance' method (inherited from Equipment),
        # which represents the difference between the total outlet enthalpy and the total inlet enthalpy
        # (H_out - H_in).

        # In a heater, heat is typically added to the system (Q > 0).
        # According to the First Law of Thermodynamics for a steady-state control volume and
        # with negligible work and kinetic/potential energy changes:
        # Q - W = DeltaH.
        # If W = 0, then Q = DeltaH.
        # Since heat is added, DeltaH (H_out - H_in) will be positive,
        # which also makes self.heat positive, indicating heat entering the system.

    def pemEfficiency(self):
        self.voltage = 0.0381*((self.current/1e4)**2) + 0.1221*(self.current/1e4) + 1.6797
        self.efficiency = 1.481/self.voltage


    def flowRates(self):
        faraday_constant = 96485.3 # [C/mol e^{-}]
        molar_mass_h2 = 0.002016 # [kg/mol]
        molar_mass_h2o = 0.01801528 # [kg/mol]
        molar_mass_o2 = 0.0160 # [kg/mol]

        # Flow rates
        self.outlet_hydrogen = self.efficiency*self.current*molar_mass_h2/(2*faraday_constant)
        self.outlet_water = self.inlet_water - self.efficiency*self.current*molar_mass_h2o/(2*faraday_constant)
        self.outlet_oxygen = self.efficiency*self.current*molar_mass_o2/(4*faraday_constant)



        self.resume = (f"--- Hydrogen Mass Flow Rate = {self.outlet_hydrogen} [kg/s]\n"
                       f"--- Recirculation Water Flow Rate = {self.outlet_water} [kg/s]\n"
                       f"--- Produced Oxygen = {self.outlet_oxygen} [kg/s]\n"
                       f"--- PEM Electrolyzer Efficiency = {self.efficiency}\n")