
class Equipment(): # Define uma nova classe chamada 'Equipment'
    def __init__(self, name):
        # O metodo __init__ e o construtor da classe.
        # Ele e chamado sempre que uma nova instancia de Equipment é criada.
        # 'self' refere-se a instancia atual da classe.
        # 'name' é um argumento que deve ser fornecido ao criar um equipamento.

        self.name = name
        # Atribui o nome fornecido ao atributo 'name' da instancia.

        self.connectors_in = []
        # Inicializa uma lista vazia para armazenar conectores de entrada (tubulações).

        self.connectors_out = []
        # Inicializa uma lista vazia para armazenar os conectores de saída.

        self.properties_in = []
        # Inicializa uma lista vazia para armazenar as propriedades (temperatura, pressão...) das correntes de entrada.

        self.properties_out = []
        # Inicializa uma lista vazia para armazenar as propriedades das correntes na saída.

        self.heat = None
        # Inicializa o atributo 'heat' como None. Este atributo representará a troca de calor do equipamento.

        self.work = None
        # Inicializa o atributo 'work' como None. Este atributo representará o trabalho do equipamento.

    def add_connectors_in(self, connector): # metodo para adicionar os conectores a lista de conectores de entrada.
        self.connectors_in.append(connector)

    def add_connectors_out(self, connector): # metodo para adicionar os conectores a lista de conectores de saída
        self.connectors_out.append(connector)

    def set_heat(self, heat): # metodo que permite atribuir um valor de calor ao equipamento.
        self.heat = heat

    def set_work(self, work): # metodo que permite atribuir um valor de trabalho ao equipamento.
        self.work = work

    def energy_balance(self):
        # metodo calcula o balanço de energia do equipamento.
        h_in = 0.0 # Inicializa entalpia entrada igual a zero.
        h_out = 0.0 # Inicializa entalpia saida igual a zero.
        print(self.name) # Imprime o nome do equipamento para identificacao.
        for property in self.properties_in: # Loop na lista properties_in
            print('- IN:') # Adiciona o rotulo 'in' para as prop. de entrada.
            print(property.resume) # Imprime o resumo da prop. implementado em thermoProperty.py
            h_in += property.H * property.mass_flow_rate # Calcula a entalpia carregada pelo escoamento para dentro do equipamento.

        for property in self.properties_out: # Loop na lista properties_out
            print('- OUT:') # Adiciona o rotulo 'out' para as prop. de saida.
            print(property.resume)
            h_out +=  property.H * property.mass_flow_rate # Calcula a entalpia carregada pelo escoamento para fora do equipamento.

        self.enthalpy_balance = h_out - h_in # Calcula o balanço de entalpia (Saída - Entrada) e armazena no atributo 'enthalpy_balance' da instância.

