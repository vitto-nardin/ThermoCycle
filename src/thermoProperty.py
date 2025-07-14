from CoolProp.CoolProp import PropsSI, PhaseSI # Utilizacao da biblioteca CoolProp

class ThermoProperty(): # Define uma nova classe chamada 'ThermoProperty'
    def __init__(self, name, fluid): # Construtor da classe:
        # 'self' refere-se à instancia atual da classe.
        # 'name' é um identificador para este conjunto de propriedades.
        # 'fluid' é a string que representa o nome do fluido (ex: "Water")
        self.name = name # atribui o nome fornecido ao atributo name
        self.fluid = fluid # atribui o fluid fornecido ao atributo fluid.

        self.mass_flow_rate = None # inicializa mass_flow_rate como None.

        self.T = None # Inicializa a Temperatura como None.
        self.P = None # Inicializa a Pressão como None.
        self.H = None # Inicializa a Entalpia como None.
        self.S = None # Inicializa a Entropia como None.
        self.Q = None # Inicializa a Qualidade (fração de vapor) como None.

        self.resume = None # Inicializa 'resume' como None.

    def set_mass_flow_rate(self, mass_flow_rate): # Define a vazão mássica para esta corrente.
        self.mass_flow_rate = mass_flow_rate

    def set_temperature(self, T): # Define a temperatura.
        self.T = T + 273.15 # O valor de entrada 'T' é em Celsius e é convertido para Kelvin (adicionando 273.15)
        # para uso com CoolProp.

    def set_pressure(self, P): #  Define a pressão.
        self.P = P

    def set_enthalpy(self, H): # Define a entalpia específica.
        self.H = H

    def set_entropy(self, S): # Define a entropia específica.
        self.S = S

    def set_quality(self, Q): # Define a qualidade (0 para líquido saturado, 1 para vapor saturado).
        self.Q = Q

    def calculate(self):  # Este metodo tenta calcular as propriedades termodinâmicas faltantes
        # usando as propriedades conhecidas e a biblioteca CoolProp.

        # Flags para verificar quais propriedades foram definidas.
        T_flag = self.T is not None
        P_flag = self.P is not None
        H_flag = self.H is not None
        S_flag = self.S is not None
        Q_flag = self.Q is not None

        # Condição de cálculo: Se Pressão (P) e Temperatura (T) são conhecidas.
        # CoolProp pode calcular outras propriedades a partir de P e T.
        if P_flag and T_flag:
            # Calcula a entalpia (H) usando PropsSI, passando 'P' e 'T' como entradas.
            self.H = PropsSI('H', 'P', self.P, 'T', self.T, self.fluid)
            # Calcula a entropia (S) usando PropsSI, de forma similar.
            self.S = PropsSI('S', 'P', self.P, 'T', self.T, self.fluid)
            # Calcula a densidade (rho) [kg/m^{3}]
            self.rho = PropsSI('D', 'T', self.T, 'P', self.P, self.fluid)
            # Calcula o calor especifico (cp) a pressao constante [J/(kg*K)]
            self.cp = PropsSI('CPMASS', 'T', self.T, 'P', self.P, self.fluid)
            # Calcula a viscosidade dinamica (mu) [Pa*s]
            self.mu = PropsSI('V', 'T', self.T, 'P', self.P, self.fluid)
            # Calcula a condutividade térmica (alpha) [W/(m*K)]
            self.alpha = PropsSI('L', 'T', self.T, 'P', self.P, self.fluid)
            # Calcula o Prandtl do fluido (Pr)
            self.Pr = PropsSI('PRANDTL', 'T', self.T, 'P', self.P, self.fluid)

            # Formata uma string de resumo com as propriedades calculadas (e de entrada).
            # Converte de volta para unidades mais comuns (kPa, C, kJ/kg, kJ/kgK) para o resumo.
            self.resume = (f"--- Fluid = {self.fluid}\n"
                           f"--- P = {self.P / 1e3} kPa\n"
                           f"--- T = {self.T - 273.15} C\n"
                           f"--- H = {self.H / 1e3} kJ/kg\n"
                           f"--- S = {self.S / 1e3} kJ/kgK\n"
                           f"--- rho = {self.rho} kg/m^{3}\n"
                           f"--- cp = {self.cp / 1e3} kJ/kgK\n"
                           f"--- mu = {self.mu} Pa*s\n"
                           f"--- alpha = {self.alpha / 1e3} kW/mK\n"
                           f"--- Pr = {self.Pr}")