# PRODUCAO DE HIDROGENIO EM ELETROLISADOR DE MEMBRANA DE TROCA DE PROTONS (PEM)
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

# --- Instanciação dos Equipamentos do Ciclo PEM ---
# Cria instâncias das subclasses de Equipment, cada uma representando um componente físico.
reservoir = Reservoir("reservoir")
pump = Pump("pump")
heater = Heater("heater")
pem_electrolyzer = pemElectrolyzer("pemElectrolyzer")
dehumidifier = Dehumidifier("dehumidifier")
hydrogenTank = HydrogenTank("hydrogenTank")
cooler = Cooler("cooler")

# # # CONDICOES OPERACIONAIS # # #
fluid = "Water" # Define o fluido de trabalho para o ciclo. Neste caso, é "Water".
fluid02 = "Hydrogen"
water_mass_flow_rate = 0.0025 # [kg/s] Agua de alimentacao. De 0.0025 (150 ml/min) a 0.0167 (1000 ml/min)

pem_electrolyzer.temperature = 353.15 # ºC Temperatura de operação do eletrolisador PEM
pem_electrolyzer.hydrogen_pressure = 3.5e7 # Pa pressão do hidrogenio produzido
pem_electrolyzer.current = 20000 # [A/m^{2}] Densidade de corrente no eletrolisador PEM
pem_electrolyzer.inlet_water = water_mass_flow_rate # [kg/s] Agua de alimentacao

#######################################################################################################
# # # MONTAGEM DO SISTEMA DE PRODUCAO # # #
prop_1 = ThermoProperty("point_1", fluid) # Estado da Água Deionizada no Reservatorio
prop_1.set_mass_flow_rate(water_mass_flow_rate) # Reservatorio Operando Vazao Constante
prop_1.set_pressure(101325) # Pressao atmosferica
prop_1.set_temperature(293.15) # Temperatura ambiente

pipe_1 = Connector("pipe_1", 1.0) # Conecta saída do reservatório à entrada da bomba
pipe_1.set_properties_in(prop_1) # Propriedade na entrada do pipe_1
pipe_1.pressureLoss() # Roda a perda de carga no trecho pipe_1

prop_1b = ThermoProperty("point_1b", fluid) # propriedade do fluido na saida do pipe_1
prop_1b.set_mass_flow_rate(water_mass_flow_rate)
prop_1b.set_pressure(prop_1.P - pipe_1.DeltaP) # Pressao na saida do pipe_1
prop_1b.set_temperature(prop_1.T) # pipe_1 adiabático

pipe_1.set_properties_out(prop_1b)
###################################################################################################

prop_2 = ThermoProperty("point_2", fluid) # Depois da bomba isotérmica
prop_2.set_mass_flow_rate(water_mass_flow_rate) # Regime permanente
prop_2.set_pressure(506625) # Pressao na bomba definida em 5 bar
prop_2.set_temperature(prop_1b.T) # Considerando bomba isotérmica

pipe_2 = Connector("pipe_2", 1.0) # Conecta saída da bomba à entrada do aquecedor
pipe_2.set_properties_in(prop_2)
pipe_2.pressureLoss() # Roda a perda de carga no trecho pipe_2

prop_2b = ThermoProperty("point_2b", fluid)
prop_2b.set_mass_flow_rate(water_mass_flow_rate) # regime permanente
prop_2b.set_pressure(prop_2.P - pipe_2.DeltaP) # define a pressao na saida do pipe_2
prop_2b.set_temperature(prop_2.T) # pipe_2 adiabático

pipe_2.set_properties_out(prop_2b)
#######################################################################################################

prop_3 = ThermoProperty("point_3", fluid) # Depois do aquecedor
prop_3.set_mass_flow_rate(water_mass_flow_rate)
prop_3.set_pressure(prop_2b.P) # Desconsiderando perda de carga no aquecedor
prop_3.set_temperature(pem_electrolyzer.temperature) # Temperatura definida na saída do aquecedor como sendo a mesma de operacao da PEM

pipe_3 = Connector("pipe_3", 1.0) # Conecta saída do aquecedor à entrada do eletrolisador PEM
pipe_3.set_properties_in(prop_3)
pipe_3.pressureLoss() # calcula a perda de carga no trecho pipe_3

prop_3b = ThermoProperty("point_3b", fluid)
prop_3b.set_mass_flow_rate(water_mass_flow_rate) # regime permanente
prop_3b.set_pressure(prop_3.P - pipe_3.DeltaP) # define a pressao na saida do pipe_3
prop_3b.set_temperature(prop_3.T) # pipe 3 adiabatico

pipe_3.set_properties_out(prop_3b)
#######################################################################################################

# Calcula os flow rates no eletrolisador PEM - Lei de Faraday Eletrolise
pem_electrolyzer.pemEfficiency()
pem_electrolyzer.flowRates()

prop_4 = ThermoProperty("point_4", fluid) # Depois do eletrolisador PEM
prop_4.set_mass_flow_rate(pem_electrolyzer.outlet_water)
prop_4.set_pressure(prop_3b.P) # Desconsiderando perda de carga no eletrolisador PEM
prop_4.set_temperature(pem_electrolyzer.temperature) # Considerando que o eletrolisador opera de maneira isotérmica

pipe_4 = Connector("pipe_4", 1.0) # Conecta saída do eletrolisador PEM à entrada do reservatório
pipe_4.set_properties_in(prop_4)
pipe_4.pressureLoss() # calcula a perda de carga no trecho pipe_4

prop_4b = ThermoProperty("point_4b", fluid)
prop_4b.set_mass_flow_rate(pem_electrolyzer.outlet_water + pem_electrolyzer.outlet_oxygen) # considera o escoamento bifásico de água de recirculacao e oxigenio
prop_4b.set_pressure(prop_4.P - pipe_4.DeltaP) # define a pressao na saida do pipe_4
prop_4b.set_temperature(prop_4.T) # pipe_4 adiabatico

pipe_4.set_properties_out(prop_4b)
#######################################################################################################

prop_5 = ThermoProperty("point_5", fluid02) # Depois do eletrolisador PEM - catodo
#prop_5.set_mass_flow_rate(water_mass_flow_rate)
prop_5.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_5.set_pressure(pem_electrolyzer.hydrogen_pressure)
prop_5.set_temperature(pem_electrolyzer.temperature) # Considerando que o eletrolisador opera de maneira isotérmica

pipe_5 = Connector("pipe_5", 1.0) # Conecta saída do eletrolisador PEM à entrado do desumidificador
pipe_5.set_properties_in(prop_5)
pipe_5.set_properties_out(prop_5)
#######################################################################################################

prop_6 = ThermoProperty("point_6", fluid02) # Depois do desumidificador
#prop_6.set_mass_flow_rate(water_mass_flow_rate)
prop_6.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_6.set_pressure(pem_electrolyzer.hydrogen_pressure) # Desconsiderando perda de carga no desumidificador
prop_6.set_temperature(pem_electrolyzer.temperature) # Considerando desumidificador isotérmico

pipe_6 = Connector("pipe_6", 1.0) # Conecta saída do desumidificador à entrada do cooler
pipe_6.set_properties_in(prop_6)
pipe_6.set_properties_out(prop_6)

prop_7 = ThermoProperty("point_7", fluid02)
prop_7.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_7.set_pressure(pem_electrolyzer.hydrogen_pressure)
prop_7.set_temperature(293.15) # armazenamento de h2 a temperatura ambiente e 350 bar

pipe_7 = Connector("pipe_7", 1.0) # Conecta saída do cooler à entrada do reservatório de h2
pipe_7.set_properties_in(prop_7)
pipe_7.set_properties_out(prop_7)

# --- Conectando os Equipamentos com os Conectores ---
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


# --- Construção e Simulação do Ciclo Termodinâmico ---
# Cria uma instância da classe pemCycle e adiciona todos os equipamentos a ela.
pem_cycle = pemCycle()
pem_cycle.add_equipment(reservoir)
pem_cycle.add_equipment(pump)
pem_cycle.add_equipment(heater)
pem_cycle.add_equipment(pem_electrolyzer)
pem_cycle.add_equipment(dehumidifier)
pem_cycle.add_equipment(cooler)
pem_cycle.add_equipment(hydrogenTank)


# --- Execução da Simulação ---
pem_cycle.initialize()
# Chama o metodo 'initialize()' do pemCycle. Este metodo é crucial:
# Ele percorre os equipamentos e seus conectores, vinculando as propriedades termodinâmicas
# dos conectores às listas 'properties_in' e 'properties_out' dos equipamentos.
# Também garante que todos os conectores sejam adicionados à lista de conectores do ciclo.

pem_cycle.calculate()
# Chama o metodo 'calculate()' do pemCycle. Isso executa a sequência de cálculos:
# 1. 'connector.calculate()' para todos os conectores (garante que as propriedades dos pontos sejam calculadas via CoolProp).
# 2. 'equipment.energy_balance()' para todos os equipamentos (calcula enthalpy_balance para cada um).
# 3. 'equipment.calculate()' para todos os equipamentos (calcula calor/trabalho específico de cada tipo de equipamento).

pem_cycle.calculate_efficiency()
# Chama o metodo 'calculate_efficiency()' para determinar a eficiência térmica global do ciclo, com base nos valores de trabalho e calor calculados.

pem_cycle.draw("app_PEM.png")
# Gera um diagrama do ciclo e o salva como "app_aula.png" usando networkx e matplotlib. Este é um recurso visual excelente para verificar a topologia do ciclo.

# Adicione isto para ver os resultados
print("\nPerformance do Eletrolisador PEM:")
print(pem_electrolyzer.resume)

print("\nResultados Ciclo PEM de H2 Verde:")
print(pem_cycle.resume)