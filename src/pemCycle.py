from .equipment.dehumidifier import Dehumidifier
from .equipment.hydrogenTank import HydrogenTank
from .equipment.turbine import Turbine
from .equipment.heater import Heater
from .equipment.cooler import Cooler
from .equipment.condenser import Condenser
from .equipment.pump import Pump
from .equipment.pemElectrolyzer import pemElectrolyzer
from .equipment.reservoir import Reservoir

# Importa as classes específicas de equipamento (Turbine, Heater, Condenser, Pump)
# do diretório 'equipment'. Isso permite que a classe pemCycle reconheça e interaja
# com esses tipos especializados de equipamentos.

import networkx as nx
import matplotlib.pyplot as plt
# Importa as bibliotecas 'networkx' e 'matplotlib.pyplot'.
# 'networkx' é uma biblioteca para criação e manipulação de graficos.
# 'matplotlib.pyplot' é usada para plotar e visualizar os graficos.
# Elas são utilizadas especificamente no metodo 'draw' para gerar um diagrama do ciclo.


class pemCycle(): # Define a classe pemCycle sem herdar nenhuma outra classe.
    def __init__(self): # Construtor da classe pemCycle sem nenhum argumento além do 'self'.

        self.equipments = [] # Inicializa uma lista vazia para os equipamentos do pemCycle
        self.connectors = [] # Inicializa uma lista vazia para os conectores do pemCycle
        self.efficiency = None # Inicializa o atributo efficiency como None.
        self.W_liq = None
        self.Q_in = None

    def add_equipment(self, equipment):
        # Este metodo permite adicionar uma instancia de Equipment (ou uma subclasse de Equipment) a lista de equipamentos do ciclo.
        self.equipments.append(equipment)

    def initialize(self):
        # Este metodo é crucial para configurar as conexoes entre os equipamentos e conectores.
        # Percorre todos os equipamentos adicionados e estabelece as referencias cruzadas.

        for equipment in self.equipments: # Itera sobre cada equipamento no ciclo.
            for connector in equipment.connectors_in: # Para cada conector de entrada do equipamento:
                connector.add_equipment_out(equipment) # Informa ao conector que este equipamento é o equipamento de SAÍDA para ele (destino da corrente).
                if connector not in self.connectors: # Se o conector ainda não foi adicionado à lista geral de conectores do ciclo:
                    self.connectors.append(connector) # Adiciona-o para que possa ser iterado e calculado.
                equipment.properties_in.append(connector.property_out) # Adiciona a 'property_out' do conector (que é a corrente que entra no equipamento) à lista 'properties_in' do equipamento.

            for connector in equipment.connectors_out: # Para cada conector de saída do equipamento:
                connector.add_equipment_in(equipment) # Informa ao conector que este equipamento é o equipamento de ENTRADA para ele (origem da corrente).
                if connector not in self.connectors: # Se o conector ainda não foi adicionado à lista geral de conectores do ciclo:
                    self.connectors.append(connector) # Adiciona-o.
                equipment.properties_out.append(connector.property_in) # Adiciona a 'property_in' do conector (que é a corrente que sai do equipamento) à lista 'properties_out' do equipamento.

                # Nota importante sobre 'properties_in/out' do equipment:
                # A lógica atual assume que a 'property_out' de um conector é a entrada de um equipamento e 'property_in' de um conector é a saída de um equipamento. Isso significa que, ao conectar A -> Conector -> B:
                # A.properties_out deve ser igual a Conector.property_in;
                # B.properties_in deve ser igual a Conector.property_out;
                # E, idealmente, Conector.property_in deve ser igual a Conector.property_out.
                # Essa configuração da 'initialize' é crítica para o fluxo de dados.


    def calculate(self): # Este metodo orquestra a sequência de cálculos para o ciclo.
        for connector in self.connectors: # Itera entre os elementos conectores.
            connector.calculate()  # Primeiro, calcula as propriedades das correntes em todos os conectores. Isso garante que todas as propriedades termodinâmicas (H, S, T, P) das correntes sejam determinadas pela biblioteca CoolProp antes de fazer os balanços dos equipamentos.

        for equipment in self.equipments: # Itera entre os equipamentos.
            equipment.energy_balance() # Em seguida, calcula o balanço de entalpia para cada equipamento. Este metodo (herdado da classe Equipment) calcula 'enthalpy_balance = H_out - H_in'.

        for equipment in self.equipments: # Novamente, itera entre os equipamentos.
            equipment.calculate() # Finalmente, calcula o calor ou trabalho específico de cada equipamento. Este metodo é polimórfico: cada subclasse (Condenser, Heater, Pump, Turbine) tem sua própria implementação de 'calculate' que usa 'enthalpy_balance' para determinar 'heat' ou 'work'.

    def calculate_efficiency(self): # Este metodo calcula a eficiência do ciclo termodinâmico. A eficiência é tipicamente definida como (Trabalho Líquido Gerado) / (Calor Adicionado).
        W_liq = 0.0 # Inicializa o trabalho liq. como zero.
        Q_in = 0.0 # Inicializa o calor total adicionado como zero.

        for equipment in self.equipments: # Itera sobre cada equipamento para somar o trabalho e o calor.
            if isinstance(equipment, pemElectrolyzer): # Se o equipamento é uma Turbina (que gera trabalho positivo):
                W_liq += equipment.work
                Q_in += equipment.heat
            #elif isinstance(equipment, Pump): # Se o equipamento é uma Bomba (que consome trabalho, então 'work' será negativo):
            elif isinstance(equipment, Pump):
                Q_in -= equipment.work

            elif isinstance(equipment, Heater): # Se o equipamento é um Aquecedor (que adiciona calor positivo):
                Q_in -= equipment.heat

            elif isinstance(equipment, Cooler):
                Q_in -= equipment.heat
                # Obs: Condensadores não são incluídos no Q_in porque removem calor (Q_out).

            elif isinstance(equipment,Reservoir):
                Q_in -= equipment.work

            elif isinstance(equipment, Dehumidifier):
                Q_in -= equipment.work

            elif isinstance(equipment,HydrogenTank):
                Q_in -= equipment.work

        self.W_liq = W_liq
        self.Q_in = Q_in
        #self.efficiency = pemElectrolyzer.flowRates(self.efficiency)
        self.efficiency = W_liq / Q_in # Calcula a eficiência dividindo o trabalho líquido pelo calor adicionado e armazena o resultado. É importante notar que 'W_liq' é a soma algébrica de trabalho positivo (turbina) e negativo (bomba).

        self.resume = (f"--- Cycle W_liq = {self.W_liq} \n"
                       f"--- Cycle W_in = {self.Q_in} \n"
                       f"--- Cycle Overall Efficiency = {self.efficiency}\n")

    def draw(self, output_file): # Este metodo gera um diagrama visual do ciclo usando networkx e matplotlib.
        G = nx.DiGraph() # Cria um novo grafo direcionado (DiGraph) do networkx.
        # Grafos direcionados são adequados para ciclos onde o fluxo tem uma direção.

        for connector in self.connectors: # Itera sobre cada conector para adicionar arestas (conexões) ao grafo.
            G.add_edge(connector.equipment_in.name,
                       connector.equipment_out.name,
                       label=connector.name)
            # Adiciona uma aresta do equipamento de entrada do conector para o equipamento de saída do conector. A 'label' da aresta será o nome do conector, facilitando a identificação no diagrama.

        plt.figure(figsize=(10, 8)) # Cria uma nova figura matplotlib com um tamanho específico.
        pos = nx.circular_layout(G) # Calcula as posições dos nós (equipamentos) em um layout circular para o grafo.

        nx.draw(G, pos, with_labels=True, node_size=6000, node_color='lightblue', arrows=True, font_size=10)
        # Desenha o grafo:
        # - G: o grafo a ser desenhado.
        # - pos: as posições calculadas dos nós.
        # - with_labels=True: exibe os nomes dos equipamentos nos nós.
        # - node_size: tamanho dos nós.
        # - node_color: cor de preenchimento dos nós.
        # - arrows=True: desenha setas para indicar a direção do fluxo.
        # - font_size: tamanho da fonte dos rótulos dos nós.

        edge_labels = nx.get_edge_attributes(G, 'label')  # Obtém os rótulos das arestas (que são os nomes dos conectores).
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red') # Desenha os rótulos nas arestas.

        plt.savefig(output_file, dpi=300) # Salva a figura gerada em um arquivo. 'dpi' (dots per inch) define a resolução.

        plt.show()
        # plt.close() # Fecha a figura para liberar memória.


