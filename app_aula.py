# Este código é um exemplo prático de como as classes ThermoProperty, Conector, Equipment (e suas subclasses), e ThermoCycle são usadas em conjunto para simular um ciclo termodinâmico completo, especificamente um Ciclo Rankine. Ele demonstra a aplicação do framework que você desenvolveu, construindo e analisando um sistema real.

from src.thermoProperty import ThermoProperty
from src.connector import Connector
from src.equipment.turbine import Turbine
from src.equipment.heater import Heater
from src.equipment.condenser import Condenser
from src.equipment.heatExchanger import heatExchanger
from src.equipment.mixingChamber import mixingChamber
from src.equipment.pump import Pump
from src.thermoCycle import ThermoCycle
# Importa todas as classes necessárias do seu projeto. Isso centraliza os componentes que serão utilizados para construir o ciclo termodinâmico.

fluid = "Water" # Define o fluido de trabalho para o ciclo. Neste caso, é "Water".
water_mass_flow_rate = 1.0  # kg/s
# Define a vazão mássica do fluido que percorrerá o ciclo.


# --- Definição dos Pontos de Estado (ThermoProperty) ---
# Cada 'prop_X' representa um ponto de estado termodinâmico específico no ciclo.
# Os valores de pressão (P) e temperatura (T) são fornecidos para cada ponto,
# permitindo que a classe ThermoProperty calcule as demais propriedades
# (entalpia H, entropia S, etc.) usando CoolProp.
# Note que a temperatura é definida em Celsius e convertida para Kelvin internamente.
# A pressão é definida em Pascal.

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

# --- Definição dos Conectores (Tubulações) ---
# Cada 'pipe_X' representa uma tubulação ou fluxo que conecta os equipamentos.
# Aqui, a lógica é que 'property_in' e 'property_out' do conector são o MESMO objeto ThermoProperty,
# indicando que as propriedades da corrente não mudam significativamente ao passar pela tubulação.

pipe_1 = Connector("pipe_1") # Conecta saída do Heater à entrada da Turbine
pipe_1.set_properties_in(prop_3)
pipe_1.set_properties_out(prop_3)

pipe_2 = Connector("pipe_2") # Conecta saída da Turbine à entrada do Condenser
pipe_2.set_properties_in(prop_4)
pipe_2.set_properties_out(prop_4)

pipe_3 = Connector("pipe_3") # Conecta saída do Condenser à entrada da Pump
pipe_3.set_properties_in(prop_1)
pipe_3.set_properties_out(prop_1)

pipe_4 = Connector("pipe_4") # Conecta saída da Pump à entrada do Heater
pipe_4.set_properties_in(prop_2)
pipe_4.set_properties_out(prop_2)

pipe_5 = Connector("pipe_5")
pipe_5.set_properties_in(prop_5)
pipe_5.set_properties_out(prop_5)

pipe_6 = Connector("pipe_6")
pipe_6.set_properties_in(prop_6)
pipe_6.set_properties_out(prop_6)

pipe_7 = Connector("pipe_7")
pipe_7.set_properties_in(prop_7)
pipe_7.set_properties_out(prop_7)

pipe_8 = Connector("pipe_8")
pipe_8.set_properties_in(prop_8)
pipe_8.set_properties_out(prop_8)

pipe_9 = Connector("pipe_9")
pipe_9.set_properties_in(prop_9)
pipe_9.set_properties_out(prop_9)


# --- Instanciação dos Equipamentos do Ciclo ---
# Cria instâncias das subclasses de Equipment, cada uma representando um componente físico.
heater = Heater("heater")
turbine = Turbine("turbine")
condenser = Condenser("condenser")
pump = Pump("pump")
pumpAux = Pump("pumpAux")
heatExchanger = heatExchanger("heatExchanger")
mixingChamber = mixingChamber("mixingChamber")

# --- Conectando os Equipamentos com os Conectores ---
# Aqui, define-se quais conectores estão associados às entradas e saídas de cada equipamento.
# Esta é a etapa fundamental para montar a topologia do ciclo.
# Por exemplo, 'heater.add_connectors_in(pipe_4)' significa que 'pipe_4' alimenta o 'heater'.

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


# --- Construção e Simulação do Ciclo Termodinâmico ---
# Cria uma instância da classe ThermoCycle e adiciona todos os equipamentos a ela.
rankine_power_cycle = ThermoCycle()
rankine_power_cycle.add_equipment(pump)
rankine_power_cycle.add_equipment(turbine)
rankine_power_cycle.add_equipment(condenser)
rankine_power_cycle.add_equipment(heater)
rankine_power_cycle.add_equipment(heatExchanger)
rankine_power_cycle.add_equipment(pumpAux)
rankine_power_cycle.add_equipment(mixingChamber)

# --- Execução da Simulação ---
rankine_power_cycle.initialize()
# Chama o metodo 'initialize()' do ThermoCycle. Este metodo é crucial:
# Ele percorre os equipamentos e seus conectores, vinculando as propriedades termodinâmicas
# dos conectores às listas 'properties_in' e 'properties_out' dos equipamentos.
# Também garante que todos os conectores sejam adicionados à lista de conectores do ciclo.

rankine_power_cycle.calculate()
# Chama o metodo 'calculate()' do ThermoCycle. Isso executa a sequência de cálculos:
# 1. 'connector.calculate()' para todos os conectores (garante que as propriedades dos pontos sejam calculadas via CoolProp).
# 2. 'equipment.energy_balance()' para todos os equipamentos (calcula enthalpy_balance para cada um).
# 3. 'equipment.calculate()' para todos os equipamentos (calcula calor/trabalho específico de cada tipo de equipamento).

rankine_power_cycle.calculate_efficiency()
# Chama o metodo 'calculate_efficiency()' para determinar a eficiência térmica global do ciclo, com base nos valores de trabalho e calor calculados.

rankine_power_cycle.draw("app_aula.png")
# Gera um diagrama do ciclo e o salva como "app_aula.png" usando networkx e matplotlib. Este é um recurso visual excelente para verificar a topologia do ciclo.