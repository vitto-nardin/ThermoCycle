from .equipment import Equipment
# Imports the 'Equipment' class from the 'equipment' module.
# This import is fundamental for the Heater class to extend the functionality of Equipment.

class Cooler(Equipment):
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

        self.work = 0.0
        # Overrides the 'work' attribute (work) which was initialized as None in the Equipment class,
        # setting it to 0.0. Heaters are typically heat exchange devices
        # that do not perform or consume significant work, similar to condensers.

    def calculate(self):
        # This method defines the specific calculation logic for a heater.
        # It will be called to determine the heat involved in the heater's process.

        self.heat = -self.enthalpy_balance
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

        self.resume = (f"--- Cooler Self.Heat = {self.heat} [J]\n")