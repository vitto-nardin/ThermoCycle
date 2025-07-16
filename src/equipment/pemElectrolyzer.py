from .equipment import Equipment
# Importa a classe 'Equipment' do módulo 'equipment'.
# Essa importação é fundamental para que a classe Heater possa estender a funcionalidade de Equipment.

class pemElectrolyzer(Equipment):
    # Define a classe Heater, indicando que ela é uma subclasse de Equipment
    # através da sintaxe '(Equipment)'.

    def __init__(self, name):
        # O metodo __init__ é o construtor da classe Heater.
        # Ele é executado sempre que uma nova instância de Heater é criada.
        # 'name' é um argumento que permite dar um nome descritivo ao aquecedor.

        super().__init__(name)
        # Chama o construtor da classe pai (Equipment) usando 'super()'.
        # Isso é crucial para inicializar todos os atributos definidos em Equipment,
        # como 'name', 'connectors_in', 'properties_in', 'heat', 'work', etc.

        self.work = 0.0
        # Sobrescreve o atributo 'work' (trabalho) que foi inicializado como None na classe Equipment,
        # definindo-o como 0.0. Aquecedores são tipicamente dispositivos de troca de calor
        # que não realizam nem consomem trabalho significativo, de forma análoga aos condensadores.

        self.current = None
        self.temperature = None
        self.efficiency = None
        self.hydrogen_pressure = None

        self.inlet_water = None
        self.outlet_hydrogen = None
        self.outlet_water = None
        self.outlet_oxygen = None


    def calculate(self):
        # Este metodo define a lógica de cálculo específica para um aquecedor.
        # Ele será chamado para determinar o calor envolvido no processo do aquecedor.

        self.heat = self.enthalpy_balance
        # Atribui o valor do 'self.enthalpy_balance' ao 'self.heat'.
        # O 'self.enthalpy_balance' é calculado pelo metodo 'energy_balance' (herdado de Equipment),
        # que representa a diferença entre a entalpia total de saída e a entalpia total de entrada
        # (H_out - H_in).

        # Em um aquecedor, o calor é tipicamente adicionado ao sistema (Q > 0).
        # Pela Primeira Lei da Termodinâmica para um volume de controle em regime permanente e
        # com trabalho e variações de energia cinética/potencial desprezíveis:
        # Q - W = DeltaH.
        # Se W = 0, então Q = DeltaH.
        # Como o calor é adicionado, DeltaH (H_out - H_in) será positivo,
        # o que faz com que self.heat também seja positivo, indicando calor entrando no sistema.


    def flowRates(self):
        faraday_constant = 96485.3 # [C/mol e^{-}]
        molar_mass_h2 = 0.002016 # [kg/mol]
        molar_mass_h2o = 0.01801528 # [kg/mol]
        molar_mass_o2 = 0.0160 # [kg/mol]

        # Vazões
        self.outlet_hydrogen = self.efficiency*self.current*molar_mass_h2/(2*faraday_constant)
        self.outlet_water = self.inlet_water - self.efficiency*self.current*molar_mass_h2o/(2*faraday_constant)
        self.outlet_oxygen = self.efficiency*self.current*molar_mass_o2/(4*faraday_constant)

        self.resume = (f"--- Hydrogen Mass Flow Rate = {self.outlet_hydrogen} [kg/s]\n"
                       f"--- Recirculation Water Flow Rate = {self.outlet_water} [kg/s]\n"
                       f"--- Produced Oxygen = {self.outlet_oxygen} [kg/s]\n")