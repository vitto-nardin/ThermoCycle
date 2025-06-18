from .equipment import Equipment
# Importa a classe 'Equipment' do módulo 'equipment' (o ponto '.' indica que
# é um módulo dentro do mesmo pacote ou diretório).
# Isso é essencial para que Condenser possa herdar de Equipment.


class Condenser(Equipment):
    # Define a classe Condenser que herda de Equipment.
    # A herança é indicada por '(Equipment)' após o nome da classe.

    def __init__(self, name):
        # O método __init__ é o construtor da classe Condenser.
        # Ele é chamado quando uma nova instância de Condenser é criada.
        # 'name' é o argumento para nomear o condensador.

        super().__init__(name)
        # Chama o construtor da classe pai (Equipment) usando 'super()'.
        # Isso garante que todos os atributos de Equipment (name, connectors_in,
        # properties_in, heat, work, etc.) sejam inicializados corretamente.

        self.work = 0.0
        # Sobrescreve o valor padrão de 'work' (inicializado como None em Equipment)
        # para 0.0. Isso é uma premissa comum para condensadores, que geralmente não
        # realizam nem recebem trabalho significativo (não são bombas, turbinas, etc.).

    def calculate(self):
        # Este metodo define o comportamento de cálculo específico para um condensador.
        # Ele é uma implementação específica de um metodo que poderia ser genérico ou abstrato
        # na classe base Equipment, ou simplesmente um novo metodo próprio do Condenser.

        self.heat = self.enthalpy_balance
        # Define o calor trocado (self.heat) como sendo igual ao balanço de entalpia
        # (self.enthalpy_balance).
        # Lembrando que 'self.enthalpy_balance' é calculado no metodo 'energy_balance'
        # da classe pai 'Equipment' (h_out - h_in).

        # Para um condensador, o calor é tipicamente removido do sistema,
        # ou seja, Q < 0. No balanço de energia Q - W = DeltaH, se W=0,
        # então Q = DeltaH. Como condensadores removem calor, o DeltaH (H_out - H_in)
        # será negativo. Portanto, self.heat será negativo, indicando calor saindo.