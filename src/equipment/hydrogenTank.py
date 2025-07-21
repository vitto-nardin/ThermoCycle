from .equipment import Equipment
# Imports the 'Equipment' class from the 'equipment' module.
# This import is vital to establish the inheritance relationship,
# allowing Pump to use all functionalities of Equipment.


class HydrogenTank(Equipment):
    # Defines the Pump class as a subclass of Equipment.
    # This inheritance allows Pump to access and use methods and attributes of Equipment.

    def __init__(self, name):
        # The __init__ method is the constructor of the Pump class.
        # It is invoked when a new instance of Pump is created.
        # 'name' is an argument to identify the pump.

        super().__init__(name)
        # Calls the constructor of the parent class (Equipment) using 'super()'.
        # This ensures that the pump instance is correctly initialized with
        # all basic equipment attributes, such as name, connector lists
        # and properties, and the heat and work attributes.


        self.heat = 0.0
        # Overrides the 'heat' attribute (heat) inherited from Equipment, setting it to 0.0.
        # Pumps are typically modeled as adiabatic equipment, which means that
        # heat exchange with the environment is considered negligible.

    def calculate(self):
        # This method defines the specific calculation logic for a pump.
        # It will be responsible for determining the work associated with the pump's operation.

        self.work = - 250
        # Assigns the value of work ('self.work') to the negative of the enthalpy balance
        # ('self.enthalpy_balance').

        # 'self.enthalpy_balance' is calculated by the 'energy_balance' method (inherited from Equipment)
        # as (H_out - H_in).
        # For a pump, the First Law of Thermodynamics for a steady-state control volume,
        # with negligible heat and kinetic/potential energy changes, is:
        # Q - W = DeltaH
        # If Q = 0 (adiabatic pump), then -W = DeltaH, i.e., W = -DeltaH.
        # Here, 'W' represents the work done *by* the system.
        # In pumps, work is *supplied to* the system (e.g., by an electric motor),
        # which, by the convention of thermodynamics (positive work when done by the system),
        # means that the work 'W' would be negative.
        # Therefore, if DeltaH (H_out - H_in) is positive (the fluid's enthalpy increases in the pump),
        # then 'self.work' will be negative, indicating work received by the system.