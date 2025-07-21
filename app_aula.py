# This code is a practical example of how the ThermoProperty, Connector, Equipment (and its subclasses), and ThermoCycle classes are used together to simulate a complete thermodynamic cycle, specifically a Rankine Cycle. It demonstrates the application of the framework you developed, building and analyzing a real system.

from src.thermoProperty import ThermoProperty
from src.connector import Connector
from src.equipment.turbine import Turbine
from src.equipment.heater import Heater
from src.equipment.condenser import Condenser
from src.equipment.heatExchanger import heatExchanger
from src.equipment.mixingChamber import mixingChamber
from src.equipment.pump import Pump
from src.thermoCycle import ThermoCycle
# Imports all necessary classes from your project. This centralizes the components that will be used to build the thermodynamic cycle.

fluid = "Water" # Defines the working fluid for the cycle. In this case, it is "Water".
water_mass_flow_rate = 1.0  # kg/s
# Defines the mass flow rate of the fluid that will flow through the cycle.


# --- Definition of State Points (ThermoProperty) ---
# Each 'prop_X' represents a specific thermodynamic state point in the cycle.
# The pressure (P) and temperature (T) values are provided for each point,
# allowing the ThermoProperty class to calculate the other properties
# (enthalpy H, entropy S, etc.) using CoolProp.
# Note that the temperature is defined in Celsius and converted to Kelvin internally.
# Pressure is defined in Pascal.

prop_1 = ThermoProperty("point_1", fluid)
prop_1.set_mass_flow_rate(water_mass_flow_rate)
prop_1.set_pressure(17e3)
prop_1.set_temperature(30)

prop_2 = ThermoProperty("point_2", fluid)
prop_2.set_mass_flow_rate(water_mass_flow_rate)
prop_2.set_pressure(3e6)
prop_2.set_temperature(30)

prop_3 = ThermoProperty("point_3", fluid)
prop_3.set_mass_flow_rate(water_mass_flow_rate)
prop_3.set_pressure(3e6)
prop_3.set_temperature(350)

prop_4 = ThermoProperty("point_4", fluid)
prop_4.set_mass_flow_rate(water_mass_flow_rate)
prop_4.set_pressure(20e3)
prop_4.set_temperature(65)

prop_5 = ThermoProperty("point_5", fluid)
prop_5.set_mass_flow_rate(water_mass_flow_rate/2)
prop_5.set_pressure(1.5e6)
prop_5.set_temperature(142.5)

prop_6 = ThermoProperty("point_6", fluid)
prop_6.set_mass_flow_rate(water_mass_flow_rate/2)
prop_6.set_pressure(1.5e6)
prop_6.set_temperature(80)

prop_7 = ThermoProperty("point_7", fluid)
prop_7.set_mass_flow_rate(water_mass_flow_rate/2)
prop_7.set_pressure(3e6)
prop_7.set_temperature(80)

prop_8 = ThermoProperty("point_8", fluid)
prop_8.set_mass_flow_rate(water_mass_flow_rate/2)
prop_8.set_pressure(3e6)
prop_8.set_temperature(80)

prop_9 = ThermoProperty("point_9", fluid)
prop_9.set_mass_flow_rate(water_mass_flow_rate)
prop_9.set_pressure(3e6)
prop_9.set_temperature(80)

# --- Definition of Connectors (Pipes) ---
# Each 'pipe_X' represents a pipe or flow that connects the equipment.
# Here, the logic is that 'property_in' and 'property_out' of the connector are the SAME ThermoProperty object,
# indicating that the stream properties do not change significantly when passing through the pipe.

pipe_1 = Connector("pipe_1", 1.0) # Connects Heater outlet to Turbine inlet
pipe_1.set_properties_in(prop_3)
pipe_1.set_properties_out(prop_3)

pipe_2 = Connector("pipe_2", 1.0) # Connects Turbine outlet to Condenser inlet
pipe_2.set_properties_in(prop_4)
pipe_2.set_properties_out(prop_4)

pipe_3 = Connector("pipe_3", 1.0) # Connects Condenser outlet to Pump inlet
pipe_3.set_properties_in(prop_1)
pipe_3.set_properties_out(prop_1)

pipe_4 = Connector("pipe_4", 1.0) # Connects Pump outlet to Heater inlet
pipe_4.set_properties_in(prop_2)
pipe_4.set_properties_out(prop_2)

pipe_5 = Connector("pipe_5", 1.0)
pipe_5.set_properties_in(prop_5)
pipe_5.set_properties_out(prop_5)

pipe_6 = Connector("pipe_6", 1.0)
pipe_6.set_properties_in(prop_6)
pipe_6.set_properties_out(prop_6)

pipe_7 = Connector("pipe_7", 1.0)
pipe_7.set_properties_in(prop_7)
pipe_7.set_properties_out(prop_7)

pipe_8 = Connector("pipe_8", 1.0)
pipe_8.set_properties_in(prop_8)
pipe_8.set_properties_out(prop_8)

pipe_9 = Connector("pipe_9", 1.0)
pipe_9.set_properties_in(prop_9)
pipe_9.set_properties_out(prop_9)


# --- Instantiation of Cycle Equipment ---
# Creates instances of Equipment subclasses, each representing a physical component.
heater = Heater("heater")
turbine = Turbine("turbine")
condenser = Condenser("condenser")
pump = Pump("pump")
pumpAux = Pump("pumpAux")
heatExchanger = heatExchanger("heatExchanger")
mixingChamber = mixingChamber("mixingChamber")

# --- Connecting Equipment with Connectors ---
# Here, it is defined which connectors are associated with the inputs and outputs of each equipment.
# This is the fundamental step to assemble the cycle topology.
# For example, 'heater.add_connectors_in(pipe_4)' means that 'pipe_4' feeds the 'heater'.

heater.add_connectors_in(pipe_9)
heater.add_connectors_out(pipe_1)

turbine.add_connectors_in(pipe_1)
turbine.add_connectors_out(pipe_2)
turbine.add_connectors_out(pipe_5)

condenser.add_connectors_in(pipe_2)
condenser.add_connectors_out(pipe_3)

pump.add_connectors_in(pipe_3)
pump.add_connectors_out(pipe_4)

heatExchanger.add_connectors_in(pipe_4)
heatExchanger.add_connectors_in(pipe_5)
heatExchanger.add_connectors_out(pipe_6)
heatExchanger.add_connectors_out(pipe_8)

pumpAux.add_connectors_in(pipe_6)
pumpAux.add_connectors_out(pipe_7)

mixingChamber.add_connectors_in(pipe_7)
mixingChamber.add_connectors_in(pipe_8)
mixingChamber.add_connectors_out(pipe_9)


# --- Construction and Simulation of the Thermodynamic Cycle ---
# Creates an instance of the ThermoCycle class and adds all equipment to it.
rankine_power_cycle = ThermoCycle()
rankine_power_cycle.add_equipment(pump)
rankine_power_cycle.add_equipment(turbine)
rankine_power_cycle.add_equipment(condenser)
rankine_power_cycle.add_equipment(heater)
rankine_power_cycle.add_equipment(heatExchanger)
rankine_power_cycle.add_equipment(pumpAux)
rankine_power_cycle.add_equipment(mixingChamber)

# --- Simulation Execution ---
rankine_power_cycle.initialize()
# Calls the 'initialize()' method of ThermoCycle. This method is crucial:
# It iterates through the equipment and its connectors, linking the thermodynamic properties
# of the connectors to the 'properties_in' and 'properties_out' lists of the equipment.
# Also ensures that all connectors are added to the cycle's connector list.

rankine_power_cycle.calculate()
# Calls the 'calculate()' method of ThermoCycle. This executes the calculation sequence:
# 1. 'connector.calculate()' for all connectors (ensures that point properties are calculated via CoolProp).
# 2. 'equipment.energy_balance()' for all equipment (calculates enthalpy_balance for each).
# 3. 'equipment.calculate()' for all equipment (calculates specific heat/work for each equipment type).

rankine_power_cycle.calculate_efficiency()
# Calls the 'calculate_efficiency()' method to determine the overall thermal efficiency of the cycle, based on the calculated work and heat values.

rankine_power_cycle.draw("app_aula.png")
# Generates a cycle diagram and saves it as "app_aula.png" using networkx and matplotlib. This is an excellent visual resource for verifying the cycle topology.