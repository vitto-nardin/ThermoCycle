from .equipment import Equipment
# Importa a classe 'Equipment' do módulo 'equipment'.
# Essa importação é vital para estabelecer a relação de herança,
# permitindo que Pump utilize todas as funcionalidades de Equipment.


class HydrogenTank(Equipment):
    # Define a classe Pump como uma subclasse de Equipment.
    # Essa herança permite que Pump acesse e utilize métodos e atributos de Equipment.

    def __init__(self, name):
        # O metodo __init__ é o construtor da classe Pump.
        # Ele é invocado quando uma nova instância de Pump é criada.
        # 'name' é um argumento para identificar a bomba.

        super().__init__(name)
        # Chama o construtor da classe pai (Equipment) usando 'super()'.
        # Isso garante que a instância da bomba seja inicializada corretamente com
        # todos os atributos básicos de um equipamento, como nome, listas de conectores
        # e propriedades, e os atributos heat e work.


        self.heat = 0.0
        # Sobrescreve o atributo 'heat' (calor) herdado de Equipment, definindo-o como 0.0.
        # Bombas são tipicamente modeladas como equipamentos adiabáticos, o que significa que
        # a troca de calor com o ambiente é considerada desprezível.

    def calculate(self):
        # Este metodo define a lógica de cálculo específica para uma bomba.
        # Ele será responsável por determinar o trabalho associado à operação da bomba.

        self.work = - 250
        # Atribui o valor do trabalho ('self.work') ao negativo do balanço de entalpia
        # ('self.enthalpy_balance').

        # O 'self.enthalpy_balance' é calculado pelo metodo 'energy_balance' (herdado de Equipment)
        # como (H_out - H_in).
        # Para uma bomba, a Primeira Lei da Termodinâmica para um volume de controle em regime permanente,
        # com calor e variações de energia cinética/potencial desprezíveis, é:
        # Q - W = DeltaH
        # Se Q = 0 (bomba adiabática), então -W = DeltaH, ou seja, W = -DeltaH.
        # Aqui, 'W' representa o trabalho realizado *pelo* sistema.
        # Em bombas, o trabalho é *fornecido ao* sistema (por exemplo, por um motor elétrico),
        # o que, pela convenção da termodinâmica (trabalho positivo quando realizado pelo sistema),
        # significa que o trabalho 'W' seria negativo.
        # Portanto, se DeltaH (H_out - H_in) é positivo (a entalpia do fluido aumenta na bomba),
        # então 'self.work' será negativo, indicando trabalho recebido pelo sistema.

