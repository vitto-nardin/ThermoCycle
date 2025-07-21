from .equipment import Equipment
# Imports the 'Equipment' class from the 'equipment' module (the dot '.' indicates that
# it is a module within the same package or directory).
# This is essential for Condenser to inherit from Equipment.


class Condenser(Equipment):
    # Defines the Condenser class which inherits from Equipment.
    # Inheritance is indicated by '(Equipment)' after the class name.

    def __init__(self, name):
        # The __init__ method is the constructor of the Condenser class.
        # It is called when a new instance of Condenser is created.
        # 'name' is the argument to name the condenser.

        super().__init__(name)
        # Calls the constructor of the parent class (Equipment) using 'super()'.
        # This ensures that all attributes of Equipment (name, connectors_in,
        # properties_in, heat, work, etc.) are correctly initialized.

        self.work = 0.0
        # Overrides the default 'work' value (initialized as None in Equipment)
        # to 0.0. This is a common assumption for condensers, which generally do not
        # perform or receive significant work (they are not pumps, turbines, etc.).

    def calculate(self):
        # This method defines the specific calculation behavior for a condenser.
        # It is a specific implementation of a method that could be generic or abstract
        # in the base Equipment class, or simply a new method specific to the Condenser.

        self.heat = self.enthalpy_balance
        # Defines the heat exchanged (self.heat) as being equal to the enthalpy balance
        # (self.enthalpy_balance).
        # Recall that 'self.enthalpy_balance' is calculated in the 'energy_balance' method
        # of the parent class 'Equipment' (h_out - h_in).

        # For a condenser, heat is typically removed from the system,
        # i.e., Q < 0. In the energy balance Q - W = DeltaH, if W=0,
        # then Q = DeltaH. Since condensers remove heat, DeltaH (H_out - H_in)
        # will be negative. Therefore, self.heat will be negative, indicating heat leaving.