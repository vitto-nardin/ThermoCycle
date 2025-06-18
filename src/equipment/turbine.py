from .equipment import Equipment
# Importa a classe 'Equipment' do módulo 'equipment'.
# Essa linha é crucial porque ela estabelece a relação de herança, permitindo que a classe Turbine
# estenda e utilize as funcionalidades já definidas em Equipment.


class Turbine(Equipment):
    # Define a classe Turbine como uma subclasse de Equipment.
    # A herança é indicada por '(Equipment)' após o nome da classe.

    def __init__(self, name):
        # Este é o construtor da classe Turbine. Ele é executado sempre que você cria uma nova turbina.
        # 'name' é o argumento que você usará para dar um nome a esta instância específica da turbina.

        super().__init__(name)
        # Chama o construtor da classe pai (Equipment) usando 'super()'.
        # Isso é fundamental para garantir que todos os atributos básicos de um equipamento,
        # como o nome, as listas de conectores de entrada e saída, e os atributos 'heat' e 'work',
        # sejam inicializados corretamente.

        self.heat = 0.0
        # Sobrescreve o atributo 'heat' (calor) que foi inicializado como None em Equipment,
        # definindo-o como 0.0. Turbinas são frequentemente modeladas como **adiabáticas**,
        # o que significa que a troca de calor com o ambiente é considerada desprezível durante a operação.

    def calculate(self):
        # Este metodo define a lógica de cálculo específica para uma turbina.
        # Ele será responsável por determinar o trabalho gerado pela turbina.

        self.work = - self.enthalpy_balance
        # Atribui o valor do trabalho ('self.work') ao negativo do balanço de entalpia
        # ('self.enthalpy_balance').

        # O 'self.enthalpy_balance' é calculado pelo metodo 'energy_balance' (herdado de Equipment)
        # como (H_out - H_in).
        # Para uma turbina, que expande um fluido e gera trabalho, a entalpia do fluido diminui,
        # ou seja, H_out < H_in. Isso resulta em um 'enthalpy_balance' negativo.

        # A Primeira Lei da Termodinâmica para um volume de controle em regime permanente,
        # com calor e variações de energia cinética/potencial desprezíveis, é:
        # Q - W = DeltaH
        # Se Q = 0 (turbina adiabática), então -W = DeltaH, o que implica W = -DeltaH.
        # Aqui, 'W' representa o trabalho realizado *pelo* sistema.
        # Como o 'enthalpy_balance' (DeltaH) é negativo para uma turbina,
        # 'self.work' (que é -DeltaH) será positivo, indicando trabalho realizado *pelo* sistema,
        # o que é consistente com a função de uma turbina.