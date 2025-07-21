# ThermoCycle and PemCycle Simulator
The Thermodynamic and PEM Hydrogen Production Simulator is a Python-based tool designed for modeling and analyzing various thermodynamic cycles, built upon Object-Oriented Programming (OOP) principles.

The present code was developed by me, M.Sc. Vittorio Nardin, in 2025 for the Scientific Programming for Thermal Sciences lecture administered by Professor P.h.D. Rafael F.L. de Cerqueira at the Mechanical Engineering Post-Graduate Program of the Universidade Federal de Santa Catarina (UFSC), Florianópolis, Santa Catarina, Brasil.

Its core capabilities include:

### General Thermodynamic Cycle Simulation
* **Fundamental Component Modeling:** Utilizes base classes such as `ThermoProperty` for defining fluid states and calculating properties (like enthalpy and entropy) using the CoolProp library. `Connector` classes model the flows linking different equipment, and a general `Equipment` base class allows for the creation of various thermodynamic components.
* **Support for Standard Equipment:** Includes specific subclasses for common thermodynamic equipment, such as `Turbine`, `Heater`, `Condenser`, and `Pump`.
* **Comprehensive Cycle Analysis:**
    * Determines thermodynamic properties at various state points within the cycle.
    * Performs energy balances for individual pieces of equipment.
    * Calculates specific heat and work for each component.
    * Determines the overall thermal efficiency of the simulated cycle.
* **Visual Representation:** Generates schematic diagrams of the cycle's topology using the `networkx` and `matplotlib` libraries, providing an excellent visual resource for verifying the system's layout.

### PEM Hydrogen Production Cycle Simulation
* **Specialized Application:** Specifically adapted to simulate the green hydrogen production process using Proton Exchange Membrane (PEM) electrolyzers.
* **Dedicated Equipment:** Incorporates specialized equipment vital for hydrogen production, including `pemElectrolyzer`, `Reservoir`, `Dehumidifier`, `HydrogenTank`, and `Cooler`.
* **Operational Parameter Control:** Allows users to define key operational conditions for the PEM electrolyzer, such as operating temperature, produced hydrogen pressure, current density, and inlet water mass flow rate.
* **Production Rate Calculations:** Calculates hydrogen and oxygen production rates based on Faraday's Law of Electrolysis and the electrolyzer's efficiency.
* **Performance Reporting:** Provides detailed performance summaries for both the PEM electrolyzer itself and the entire hydrogen production cycle.

The simulator demonstrates the practical application of the developed framework for building and analyzing real-world thermodynamic systems.




Updates:

14/06/2025 - Original code development for Rankine Cycle (Rafael F.L. de Cerqueira).

18/06/2025 - Added comments to the original code (Vittorio Nardin).

20/06/2025 - Added additional equipment and generated the schematic drawing of the regenerative Rankine cycle (Vittorio Nardin).

26/06/2025 - Added the pemElectrolyzer class that inherits attributes from the parent class Equipment to start the final project of the discipline (Vittorio Nardin).

17/07/2025 - Completion of implementations for the final project of the Scientific Programming for Engineering and Thermal Sciences discipline (Vittorio Nardin).

21/07/2025 - Translation to English (Vittorio Nardin).