from CoolProp.CoolProp import PropsSI, PhaseSI # Usage of the CoolProp library

class ThermoProperty(): # Defines a new class called 'ThermoProperty'
    def __init__(self, name, fluid): # Class constructor:
        # 'self' refers to the current instance of the class.
        # 'name' is an identifier for this set of properties.
        # 'fluid' is the string representing the fluid name (e.g., "Water")
        self.name = name # assigns the provided name to the name attribute
        self.fluid = fluid # assigns the provided fluid to the fluid attribute.

        self.mass_flow_rate = None # initializes mass_flow_rate as None.

        self.T = None # Initializes Temperature as None.
        self.P = None # Initializes Pressure as None.
        self.H = None # Initializes Enthalpy as None.
        self.S = None # Initializes Entropy as None.
        self.Q = None # Initializes Quality (vapor fraction) as None.

        self.resume = None # Initializes 'resume' as None.

    def set_mass_flow_rate(self, mass_flow_rate): # Defines the mass flow rate for this stream.
        self.mass_flow_rate = mass_flow_rate

    def set_temperature(self, T): # Defines the temperature.
        self.T = T + 273.15 # The input value 'T' is in Celsius and is converted to Kelvin (by adding 273.15)
        # for use with CoolProp.

    def set_pressure(self, P): # Defines the pressure.
        self.P = P

    def set_enthalpy(self, H): # Defines the specific enthalpy.
        self.H = H

    def set_entropy(self, S): # Defines the specific entropy.
        self.S = S

    def set_quality(self, Q): # Defines the quality (0 for saturated liquid, 1 for saturated vapor).
        self.Q = Q

    def calculate(self):  # This method attempts to calculate missing thermodynamic properties
        # using known properties and the CoolProp library.

        # Flags to check which properties have been defined.
        T_flag = self.T is not None
        P_flag = self.P is not None
        H_flag = self.H is not None
        S_flag = self.S is not None
        Q_flag = self.Q is not None

        # Calculation condition: If Pressure (P) and Temperature (T) are known.
        # CoolProp can calculate other properties from P and T.
        if P_flag and T_flag:
            # Calculates enthalpy (H) using PropsSI, passing 'P' and 'T' as inputs.
            self.H = PropsSI('H', 'P', self.P, 'T', self.T, self.fluid)
            # Calculates entropy (S) using PropsSI, similarly.
            self.S = PropsSI('S', 'P', self.P, 'T', self.T, self.fluid)
            # Calculates density (rho) [kg/m^{3}]
            self.rho = PropsSI('D', 'T', self.T, 'P', self.P, self.fluid)
            # Calculates specific heat (cp) at constant pressure [J/(kg*K)]
            self.cp = PropsSI('CPMASS', 'T', self.T, 'P', self.P, self.fluid)
            # Calculates dynamic viscosity (mu) [Pa*s]
            self.mu = PropsSI('V', 'T', self.T, 'P', self.P, self.fluid)
            # Calculates thermal conductivity (alpha) [W/(m*K)]
            self.alpha = PropsSI('L', 'T', self.T, 'P', self.P, self.fluid)
            # Calculates the fluid's Prandtl number (Pr)
            self.Pr = PropsSI('PRANDTL', 'T', self.T, 'P', self.P, self.fluid)

            # Formats a summary string with the calculated (and input) properties.
            # Converts back to more common units (kPa, C, kJ/kg, kJ/kgK) for the summary.
            self.resume = (f"--- Fluid = {self.fluid}\n"
                           f"--- P = {self.P / 1e3} kPa\n"
                           f"--- T = {self.T - 273.15} C\n")