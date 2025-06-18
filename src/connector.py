class Connector(): # Define uma nova classe chamada Connector. Diferente dos equipamentos, ela não herda da classe
# Equipment.

    def __init__(self, name):
        # O construtor da classe Connector.
        # 'name' é um atributo identificador para o conector (ex: "Corrente de Saída da Bomba", "Entrada do Aquecedor").

        self.name = name
        # Atribui o nome ao conector.

        self.property_in = None
        # Inicializa 'property_in' como None. Este atributo vai armazenar um objeto ThermoProperty que representa as propriedades da corrente que ENTRA no conector (ou seja, a que vem do equipamento 'equipment_in').

        self.property_out = None
        # Inicializa 'property_out' como None. Este atributo vai armazenar um objeto ThermoProperty que representa as propriedades da corrente que SAI do conector (ou seja, a que vai para o equipamento 'equipment_out'). Em um conector ideal, property_in e property_out deveriam ser idênticos, representando a mesma corrente que passa pelo conector.

        self.equipment_in = None
        # Inicializa 'equipment_in' como None. Este atributo vai armazenar uma instância da classe Equipment(ou uma de suas subclasses, como Pump, Heater, etc.) da qual a corrente está SAINDO.

        self.equipment_out = None
        # Inicializa 'equipment_out' como None. Este atributo vai armazenar uma instância da classe Equipment (ou uma de suas subclasses) para a qual a corrente está ENTRANDO.

    def add_equipment_in(self, equipment):
        # Adiciona o equipamento do qual a corrente *chega* (saiu de) a este conector.
        self.equipment_in = equipment

    def add_equipment_out(self, equipment):
        # Adiciona o equipamento para o qual a corrente *segue* (vai entrar em) a partir deste conector.
        self.equipment_out = equipment


    def set_properties_in(self, property):
        # Define o objeto ThermoProperty que descreve a corrente que entra no conector.
        self.property_in = property

    def set_properties_out(self, property):
        # Define o objeto ThermoProperty que descreve a corrente que sai do conector.
        self.property_out = property


    def calculate(self):
        # Este metodo é chamado para garantir que as propriedades das correntes associadas a este conector estejam calculadas.

        self.property_in.calculate()
        # Chama o metodo 'calculate()' do objeto ThermoProperty que representa a entrada.
        # Isso garante que todas as propriedades termodinâmicas da corrente de entrada sejam determinadas com base nas propriedades de estado fornecidas.

        self.property_out.calculate()
        # Chama o metodo 'calculate()' do objeto ThermoProperty que representa a saída.
        # Isso garante que todas as propriedades termodinâmicas da corrente de saída sejam determinadas.Idealmente, 'property_out' seria uma cópia ou referência de 'property_in' em um conector simples, ou haveria uma lógica para que 'property_out' refletisse as mesmas condições de 'property_in'.