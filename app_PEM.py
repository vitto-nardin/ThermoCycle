# Este código é um exemplo prático de como as classes ThermoProperty, Conector, Equipment (e suas subclasses), e pemCycle são usadas em conjunto para simular um ciclo termodinâmico completo, especificamente um Ciclo Rankine. Ele demonstra a aplicação do framework que você desenvolveu, construindo e analisando um sistema real.

from src.thermoProperty import ThermoProperty
from src.pemCycle import pemCycle

from src.connector import Connector
from src.equipment.heater import Heater
from src.equipment.pump import Pump
from src.equipment.pemElectrolyzer import pemElectrolyzer
from src.equipment.reservoir import Reservoir
from src.equipment.dehumidifier import Dehumidifier
from src.equipment.hydrogenTank import HydrogenTank

# --- Instanciação dos Equipamentos do Ciclo PEM ---
# Cria instâncias das subclasses de Equipment, cada uma representando um componente físico.
reservoir = Reservoir("reservoir")
pump = Pump("pump")
heater = Heater("heater")
pem_electrolyzer = pemElectrolyzer("pemElectrolyzer")
dehumidifier = Dehumidifier("dehumidifier")
hydrogenTank = HydrogenTank("hydrogenTank")

fluid = "Water" # Define o fluido de trabalho para o ciclo. Neste caso, é "Water".
fluid02 = "Hydrogen"
water_mass_flow_rate = 1.0  # [kg/s] Agua de alimentacao

pem_electrolyzer.current = 50000 # [A/m^{2}] Densidade de corrente
pem_electrolyzer.inlet_water = water_mass_flow_rate # [kg/s] Agua de alimentacao

# --- Definição dos Pontos de Estado (ThermoProperty) ---
# Cada 'prop_X' representa um ponto de estado termodinâmico específico no ciclo.
# Os valores de pressão (P) e temperatura (T) são fornecidos para cada ponto,
# permitindo que a classe ThermoProperty calcule as demais propriedades
# (entalpia H, entropia S, etc.) usando CoolProp.
# Note que a temperatura é definida em Celsius e convertida para Kelvin internamente.
# A pressão é definida em Pascal.

prop_1 = ThermoProperty("point_1", fluid) # No reservatório
prop_1.set_mass_flow_rate(water_mass_flow_rate)
prop_1.set_pressure(101325)
prop_1.set_temperature(25)

prop_2 = ThermoProperty("point_2", fluid) # Depois da bomba isotérmica
prop_2.set_mass_flow_rate(water_mass_flow_rate)
prop_2.set_pressure(506625)
prop_2.set_temperature(25) # Considerando bomba isotérmica

prop_3 = ThermoProperty("point_3", fluid) # Depois do aquecedor
prop_3.set_mass_flow_rate(water_mass_flow_rate)
prop_3.set_pressure(506625) # Desconsiderando perda de carga no aquecedor
prop_3.set_temperature(80)

# Calcular os flow rates no eletrolisador PEM
pem_electrolyzer.flowRates()

prop_4 = ThermoProperty("point_4", fluid) # Depois do eletrolisador PEM
#prop_4.set_mass_flow_rate(water_mass_flow_rate)
prop_4.set_mass_flow_rate(pem_electrolyzer.outlet_water)
prop_4.set_pressure(506625) # Desconsiderando perda de carga no eletrolisador PEM
prop_4.set_temperature(80) # Considerando que o eletrolisador opera de maneira isotérmica

prop_5 = ThermoProperty("point_5", fluid02) # Depois do eletrolisador PEM - catodo
#prop_5.set_mass_flow_rate(water_mass_flow_rate)
prop_5.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_5.set_pressure(3.5e7)
prop_5.set_temperature(80) # Considerando que o eletrolisador opera de maneira isotérmica

prop_6 = ThermoProperty("point_6", fluid02) # Depois do desumidificador
#prop_6.set_mass_flow_rate(water_mass_flow_rate)
prop_6.set_mass_flow_rate(pem_electrolyzer.outlet_hydrogen)
prop_6.set_pressure(3.5e7) # Desconsiderando perda de carga no desumidificador
prop_6.set_temperature(80) # Considerando desumidificador isotérmico

# --- Definição dos Conectores (Tubulações) ---
# Cada 'pipe_X' representa uma tubulação ou fluxo que conecta os equipamentos.
# Aqui, a lógica é que 'property_in' e 'property_out' do conector são o MESMO objeto ThermoProperty,
# indicando que as propriedades da corrente não mudam significativamente ao passar pela tubulação.

pipe_1 = Connector("pipe_1") # Conecta saída do reservatório à entrada da bomba
pipe_1.set_properties_in(prop_1)
pipe_1.set_properties_out(prop_1)

pipe_2 = Connector("pipe_2") # Conecta saída da bomba à entrada do aquecedor
pipe_2.set_properties_in(prop_2)
pipe_2.set_properties_out(prop_2)

pipe_3 = Connector("pipe_3") # Conecta saída do aquecedor à entrada do eletrolisador PEM
pipe_3.set_properties_in(prop_3)
pipe_3.set_properties_out(prop_3)

pipe_4 = Connector("pipe_4") # Conecta saída do eletrolisador PEM à entrada do reservatório
pipe_4.set_properties_in(prop_4)
pipe_4.set_properties_out(prop_4)

pipe_5 = Connector("pipe_5") # Conecta saída do eletrolisador PEM à entrado do desumidificador
pipe_5.set_properties_in(prop_5)
pipe_5.set_properties_out(prop_5)

pipe_6 = Connector("pipe_6") # Conecta saída do desumidificador à entrada do tanque de h2
pipe_6.set_properties_in(prop_6)
pipe_6.set_properties_out(prop_6)



# --- Conectando os Equipamentos com os Conectores ---
# Aqui, define-se quais conectores estão associados às entradas e saídas de cada equipamento.
# Esta é a etapa fundamental para montar a topologia do ciclo.
# Por exemplo, 'heater.add_connectors_in(pipe_4)' significa que 'pipe_4' alimenta o 'heater'.

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

hydrogenTank.add_connectors_in(pipe_6)


# --- Construção e Simulação do Ciclo Termodinâmico ---
# Cria uma instância da classe pemCycle e adiciona todos os equipamentos a ela.
rankine_power_cycle = pemCycle()
rankine_power_cycle.add_equipment(reservoir)
rankine_power_cycle.add_equipment(pump)
rankine_power_cycle.add_equipment(heater)
rankine_power_cycle.add_equipment(pem_electrolyzer)
rankine_power_cycle.add_equipment(dehumidifier)
rankine_power_cycle.add_equipment(hydrogenTank)

# --- Execução da Simulação ---
rankine_power_cycle.initialize()
# Chama o metodo 'initialize()' do pemCycle. Este metodo é crucial:
# Ele percorre os equipamentos e seus conectores, vinculando as propriedades termodinâmicas
# dos conectores às listas 'properties_in' e 'properties_out' dos equipamentos.
# Também garante que todos os conectores sejam adicionados à lista de conectores do ciclo.

rankine_power_cycle.calculate()
# Chama o metodo 'calculate()' do pemCycle. Isso executa a sequência de cálculos:
# 1. 'connector.calculate()' para todos os conectores (garante que as propriedades dos pontos sejam calculadas via CoolProp).
# 2. 'equipment.energy_balance()' para todos os equipamentos (calcula enthalpy_balance para cada um).
# 3. 'equipment.calculate()' para todos os equipamentos (calcula calor/trabalho específico de cada tipo de equipamento).

rankine_power_cycle.calculate_efficiency()
# Chama o metodo 'calculate_efficiency()' para determinar a eficiência térmica global do ciclo, com base nos valores de trabalho e calor calculados.

rankine_power_cycle.draw("app_aula.png")
# Gera um diagrama do ciclo e o salva como "app_aula.png" usando networkx e matplotlib. Este é um recurso visual excelente para verificar a topologia do ciclo.

# Adicione isto para ver os resultados
print("\nResultados do Eletrolisador PEM:")
print(pem_electrolyzer.resume)