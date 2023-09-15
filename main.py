import csv

class Bateria:
    def __init__(self, modelo, taxa_descarga, tensao, peso_gramas, capacidade):
        self.modelo = modelo
        self.taxa_descarga = taxa_descarga
        self.tensao = tensao
        self.peso_gramas = peso_gramas
        self.capacidade = capacidade

    def __str__(self):
        return f"{self.modelo} ({self.capacidade}mAh, {self.tensao}V)"

    def atualizar(self, capacidade):
        self.capacidade = capacidade

class Motor:
    def __init__(self, modelo, capacidade_pico_corrente):
        self.modelo = modelo
        self.capacidade_pico_corrente = capacidade_pico_corrente

    def __str__(self):
        return f"{self.modelo} ({self.capacidade_pico_corrente}A)"

class BancoDadosVoo:
    def __init__(self):
        self.baterias = []
        self.motores = []
        self.melhor_combinacao = None
        self.nome_arquivo = 'dados_voo.csv'
        self.atualizar_banco_dados()

    def adicionar_bateria(self, bateria):
        self.baterias.append(bateria)
        self.atualizar_banco_dados()

    def adicionar_motor(self, motor):
        self.motores.append(motor)
        self.atualizar_banco_dados()

    def atualizar_banco_dados(self):
        self.baterias.sort(key=lambda bateria: -bateria.capacidade)
        self.motores.sort(key=lambda motor: -motor.capacidade_pico_corrente)

        ultima_melhor_combinacao = self.melhor_combinacao

        if self.baterias and self.motores:
            melhor_bateria = self.baterias[0]
            melhor_motor = self.motores[0]
            tempo_voo = self.calcular_tempo_voo(melhor_bateria, melhor_motor)
            self.melhor_combinacao = (tempo_voo)
        else:
            self.melhor_combinacao = None

        with open(self.nome_arquivo, 'w', newline='') as csvfile:
            nomes_campos = ['Modelo Bateria', 'Tensao', 'Peso (g)', 'Capacidade Bateria', 'Modelo Motor', 'Capacidade em Pico de Corrente do Motor', 'Tempo de Voo Estimado', 'Taxa descarga da bateria']
            escritor = csv.DictWriter(csvfile, fieldnames=nomes_campos)
            escritor.writeheader()

            for bateria in self.baterias:
                motor = self.motores[0] if self.motores else None
                tempo_voo = self.calcular_tempo_voo(bateria, motor)
                peso_gramas = bateria.peso_gramas
                taxadescarga = bateria.taxa_descarga
                escritor.writerow({
                    'Modelo Bateria': bateria.modelo,
                    'Tensao': bateria.tensao,
                    'Peso (g)': peso_gramas,
                    'Capacidade Bateria': bateria.capacidade,
                    'Modelo Motor': motor.modelo if motor else None,
                    'Capacidade em Pico de Corrente do Motor': motor.capacidade_pico_corrente if motor else None,
                    'Tempo de Voo Estimado': tempo_voo,
                    'Taxa descarga da bateria':  taxadescarga
                })

    def calcular_tempo_voo(self, bateria, motor):
        if bateria and motor:
            return float((((bateria.capacidade * 0.925)/1000) * (bateria.taxa_descarga))/motor.capacidade_pico_corrente)
        else:
            return None

    def obter_melhor_combinacao(self):
        return self.melhor_combinacao

if __name__ == "__main__":
    banco_dados_voo = BancoDadosVoo()

    while True:
        # Solicita ao usuário que insira os dados da bateria
        modelo_bateria = input("Digite o modelo da bateria (ou pressione Enter para sair): ")
        if not modelo_bateria:
            break
        taxa_descarga = float(input("Digite a taxa de descarga da bateria: "))
        tensao_bateria = float(input("Digite a tensão da bateria: "))
        peso_gramas_bateria = float(input("Digite o peso da bateria em gramas: "))
        capacidade_bateria = float(input("Digite a capacidade da bateria em mAh: "))

        # Cria uma instância de Bateria com os dados inseridos pelo usuário
        bateria_usuario = Bateria(modelo_bateria, taxa_descarga, tensao_bateria, peso_gramas_bateria, capacidade_bateria)

        # Adiciona a bateria ao banco de dados
        banco_dados_voo.adicionar_bateria(bateria_usuario)

        # Solicita ao usuário que insira os dados do motor
        modelo_motor = input("Digite o modelo do motor: ")
        capacidade_pico_corrente_motor = float(input("Digite a capacidade em pico de corrente do motor: "))

        # Cria uma instância de Motor com os dados inseridos pelo usuário
        motor_usuario = Motor(modelo_motor, capacidade_pico_corrente_motor)

        # Adiciona o motor ao banco de dados
        banco_dados_voo.adicionar_motor(motor_usuario)

        print('Informações Coletadas... \n Adicionar novas informações: ')

    banco_dados_voo.atualizar_banco_dados()

    melhor_combinacao = banco_dados_voo.obter_melhor_combinacao()

    if melhor_combinacao:
        melhor_bateria, melhor_motor, tempo_voo = melhor_combinacao
        print(f"Melhor Combinacao: \n"
              f"Melhor Bateria: {melhor_bateria}\n"
              f"Melhor Motor: {melhor_motor}\n"
              f"Tempo de Voo Estimado da Melhor Combinação: {tempo_voo:.2f} minutos\n")

