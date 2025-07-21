# HYDROGEN PRODUCTION IN PROTON EXCHANGE MEMBRANE (PEM) ELECTROLYZER
# VITTORIO NARDIN, SINMEC, 2025.

from src.thermoProperty import ThermoProperty
from src.pemCycle import pemCycle

from src.connector import Connector
from src.equipment.heater import Heater
from src.equipment.pump import Pump
from src.equipment.pemElectrolyzer import pemElectrolyzer
from src.equipment.reservoir import Reservoir
from src.equipment.dehumidifier import Dehumidifier
from src.equipment.hydrogenTank import HydrogenTank
from src.equipment.cooler import Cooler

# --- Instantiation of PEM Cycle Equipment ---
# Creates instances of Equipment subclasses, each representing a physical component.
reservoir = Reservoir("reservoir")
pump = Pump("pump")
heater = Heater("heater")
pem_electrolyzer = pemElectrolyzer("pemElectrolyzer")
dehumidifier = Dehumidifier("dehumidifier")
hydrogenTank = HydrogenTank("hydrogenTank")
cooler = Cooler("cooler")

# # # OPERATIONAL CONDITIONS # # #
fluid = "Water" # Defines the working fluid for the cycle. In this case, it is "Water".
fluid02 = "Hydrogen"
water_mass_flow_rate = 0.0025 # [kg/s] Feed water. From 0.0025 (150 ml/min) to 0.0167 (1000 ml/min)

pem_electrolyzer.temperature = 353.15 # ºC PEM electrolyzer operating temperature
pem_electrolyzer.hydrogen_pressure = 3.5e7 # Pa pressure of produced hydrogen
pem_electrolyzer.current = 20000 # [A/m^{2}] Current density in the PEM electrolyzer
pem_electrolyzer.inlet_water = water_mass_flow_rate # [kg/s] Feed water

#######################################################################################################
# # # SYSTEM ASSEMBLY # # #
prop_1 = ThermoProperty("point_1", fluid) # State of Deionized Water in the Reservoir
prop_1.set_mass_flow_rate(water_mass_flow_rate) # Reservoir Operating at Constant Flow Rate
prop_1.set_pressure(101325) # Atmospheric pressure
prop_1.set_temperature(293.15) # Ambient temperature

pipe_1 = Connector("pipe_1", 1.0) # Connects reservoir outlet to pump inlet
pipe_1.set_properties_in(prop_1) # Property at pipe_1 inlet
pipe_1.pressureLoss() # Runs pressure loss in pipe_1 section

prop_1b = ThermoProperty("point_1b", fluid) # fluid property at pipe_1 outlet
prop_1b.set_mass_flow_rate(water_mass_flow_rate)
prop_1b.set_pressure(prop_1.P - pipe_1.DeltaP) # Pressure at pipe_1 outlet
prop_1b.set_temperature(prop_1.T) # adiabatic pipe_1

pipe_1.set_properties_out(prop_1b)
###################################################################################################

prop_2 = ThermoProperty("point_2", fluid) # After the isothermal pump
prop_2.set_mass_flow_rate(water_mass_flow_rate) # Steady state
prop_2.set_pressure(506625) # Pump pressure set at 5 bar
prop_2.set_temperature(prop_1b.T) # Considering isothermal pump

pipe_2 = Connector("pipe_2", 1.0) # Connects pump outlet to heater inlet
pipe_2.set_properties_in(prop_2)
pipe_2.pressureLoss() # Runs pressure loss in pipe_2 section

prop_2b = ThermoProperty("point_2b", fluid)
prop_2b.set_mass_flow_rate(water_mass_flow_rate) # steady state
prop_2b.set_pressure(prop_2.P - pipe_2.DeltaP) # defines pressure at pipe_2 outlet
prop_2b.set_temperature(prop_2.T) # adiabatic pipe_2

pipe_2.set_properties_out(prop_2b)
#######################################################################################################

prop_3 = ThermoProperty("point_3", fluid) # After the heater
prop_3.set_mass_flow_rate(water_mass_flow_rate)
prop_3.set_pressure(prop_2b.P) # Disregarding pressure loss in the heater
prop_3.set_temperature(pem_electrolyzer.temperature) # Temperature defined at heater outlet as the same as PEM operating temperature

pipe_3 = Connector("pipe_3", 1.0) # Connects heater outlet to PEM electrolyzer inlet
pipe_3.set_properties_in(prop_3)
pipe_3.pressureLoss() # calculates pressure loss in pipe_3 section

prop_3b = ThermoProperty("point_3b", fluid)
prop_3b.set_mass_flow_rate(water_mass_flow_rate) # steady state
prop_3b.set_pressure(prop_3.P - pipe_3.DeltaP) # defines pressure at pipe_3 outlet
prop_3b.set_temperature(prop_3.T) # adiabatic pipe 3

pipe_3.set_properties_out(prop_3b)
#######################################################################################################

# Calculates flow rates in the PEM electrolyzer - Faraday's Law of Electrolysis
pem_electrolyzer.pemEfficiency()
pem_electrolyzer.flowRates()

prop_4 = ThermoProperty("point_4", fluid) # After the PEM electrolyzer
prop_4.set_mass_flow_rate(pem_electrolyzer.outlet_water)
prop_4.set_pressure(prop_3b.P) # Disregarding pressure loss in the PEM electrolyzer
prop_4.set_temperature(pem_electrolyzer.temperature) # Considering that the electrolyzer operates isothermally

pipe_4 = Connector("pipe_4", 1.0) # Connects PEM electrolyzer outlet to reservoir inlet
pipe_4.set_properties_in(prop_4)
pipe_4.pressureLoss() # calculates pressure loss in pipe_4 section

prop_4b = ThermoProperty("point_4b", fluid)
prop_4b.set_mass_flow_rate(pem_electrolyzer.outlet_water + pem_electrolyzer.outlet_oxygen) # considers the two-phase flow of recirculating water and oxygen
prop_4b.set_pressure(prop_4.P - pipe_4.DeltaP) # defines pressure at pipe_4 outlet
prop_4b.set_temperature(prop_4.T) # adiabatic pipe_4

pipe_4.set_properties_out(prop_4b)
#######################################################################################################

prop_5 = ThermoProperty("point_5", fluid02) # After the PEM electrolyzer - cathode
#prop_5.set_mass_flow_rate(water_mass_flow_rate)
prop_5.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_5.set_pressure(pem_electrolyzer.hydrogen_pressure)
prop_5.set_temperature(pem_electrolyzer.temperature) # Considering that the electrolyzer operates isothermally

pipe_5 = Connector("pipe_5", 1.0) # Connects PEM electrolyzer outlet to dehumidifier inlet
pipe_5.set_properties_in(prop_5)
pipe_5.set_properties_out(prop_5)
#######################################################################################################

prop_6 = ThermoProperty("point_6", fluid02) # After the dehumidifier
#prop_6.set_mass_flow_rate(water_mass_flow_rate)
prop_6.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_6.set_pressure(pem_electrolyzer.hydrogen_pressure) # Disregarding pressure loss in the dehumidifier
prop_6.set_temperature(pem_electrolyzer.temperature) # Considering isothermal dehumidifier

pipe_6 = Connector("pipe_6", 1.0) # Connects dehumidifier outlet to cooler inlet
pipe_6.set_properties_in(prop_6)
pipe_6.set_properties_out(prop_6)

prop_7 = ThermoProperty("point_7", fluid02)
prop_7.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_7.set_pressure(pem_electrolyzer.hydrogen_pressure)
prop_7.set_temperature(293.15) # H2 storage at ambient temperature and 350 bar

pipe_7 = Connector("pipe_7", 1.0) # Connects cooler outlet to H2 reservoir inlet
pipe_7.set_properties_in(prop_7)
pipe_7.set_properties_out(prop_7)

# --- Connecting Equipment with Connectors ---
reservoir.add_connectors_in(pipe_4)
reservoir.add_connectors_out(pipe_1)

pump.add_connectors_in(pipe_1)
pump.add_connectors_out(pipe_2)

heater.add_connectors_in(pipe_2)
heater.add_connectors_out(pipe_3)

pem_electrolyzer.add_connectors_in(pipe_3)
pem_electrolyzer.add_connectors_out(pipe_4)
pem_electrolyzer.add_connectors_out(pipe_5)

dehumidifier.add_connectors_in(pipe_5)
dehumidifier.add_connectors_out(pipe_6)

cooler.add_connectors_in(pipe_6)
cooler.add_connectors_out(pipe_7)

hydrogenTank.add_connectors_in(pipe_7)


# --- Construction and Simulation of the Thermodynamic Cycle ---
# Creates an instance of the pemCycle class and adds all equipment to it.
pem_cycle = pemCycle()
pem_cycle.add_equipment(reservoir)
pem_cycle.add_equipment(pump)
pem_cycle.add_equipment(heater)
pem_cycle.add_equipment(pem_electrolyzer)
pem_cycle.add_equipment(dehumidifier)
pem_cycle.add_equipment(cooler)
pem_cycle.add_equipment(hydrogenTank)


# --- Simulation Execution ---
pem_cycle.initialize()
# Calls the 'initialize()' method of pemCycle. This method is crucial:
# It iterates through the equipment and its connectors, linking the thermodynamic properties
# of the connectors to the 'properties_in' and 'properties_out' lists of the equipment.
# Also ensures that all connectors are added to the cycle's connector list.

pem_cycle.calculate()
# Calls the 'calculate()' method of pemCycle. This executes the calculation sequence:
# 1. 'connector.calculate()' for all connectors (ensures that point properties are calculated via CoolProp).
# 2. 'equipment.energy_balance()' for all equipment (calculates enthalpy_balance for each).
# 3. 'equipment.calculate()' for all equipment (calculates specific heat/work for each equipment type).

pem_cycle.calculate_efficiency()
# Calls the 'calculate_efficiency()' method to determine the overall thermal efficiency of the cycle, based on the calculated work and heat values.

pem_cycle.draw("app_PEM.png")
# Generates a cycle diagram and saves it as "app_aula.png" using networkx and matplotlib. This is an excellent visual resource for verifying the cycle topology.

# Add this to see the results
print("\nPerformance of PEM Electrolyzer:")
print(pem_electrolyzer.resume)

print("\nPEM H2 Green Cycle Results:")
print(pem_cycle.resume)