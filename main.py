import pandas as pd
import os

class BancoDados:
    def __init__(self, arquivo='dados.csv'):
        self.arquivo = arquivo
        if os.path.exists(arquivo):
            self.carregar_dados()
        else:
            self.inicializar_dados()

    def inicializar_dados(self):
        self.dados = pd.DataFrame(columns=['Modelo da bateria', 'Tensão da bateria (V)', 'Resistência interna (Ohms)', 'Taxa de descarga (C)', 'Tamanho da bateria (mm)', 'Peso da bateria (g)', 'Capacidade da bateria (mAh)', 'Modelo do motor', 'Pico de corrente do motor (A)', 'Estimativa de tempo de voo', 'Recomendação'])
        self.dados.to_csv(self.arquivo, index=False)

    def carregar_dados(self):
        self.dados = pd.read_csv(self.arquivo)
        self.dados['Estimativa de tempo de voo'] = pd.to_numeric(self.dados['Estimativa de tempo de voo'], errors='coerce')

    def calcular_estimativa_tempo_voo(self, capacidade_bateria, pico_corrente_motor):
        return ((((capacidade_bateria) / 1000) * 60) / pico_corrente_motor)

    def adicionar_dados(self):
        if not hasattr(self, 'dados'):
            self.carregar_dados()

        while True:
            modelo_bateria = input("Digite o modelo da bateria (Obrigatorio): ")
            tensao_bateria = input("Digite a tensão da bateria (V) (Obrigatorio): ")
            resistencia_interna = input("Digite a resistência interna (Ohms): ")
            taxa_descarga = input("Digite a taxa de descarga (C) (Obrigatorio): ")
            tamanho_bateria = input("Digite o tamanho da bateria (mm): ")
            peso_bateria = input("Digite o peso da bateria (g): ")
            capacidade_bateria = input("Digite a capacidade da bateria (mAh) (Obrigatorio): ")
            modelo_motor = input("Digite o modelo do motor (Obrigatorio): ")
            pico_corrente_motor = input("Digite o pico de corrente do motor (A) (Obrigatorio): ")

            # Verifica se os dados obrigatórios foram fornecidos
            if not all([modelo_bateria, tensao_bateria, taxa_descarga, capacidade_bateria, modelo_motor, pico_corrente_motor]):
                print("Erro: Todos os dados obrigatórios devem ser fornecidos.")
                continue

            if resistencia_interna.strip() != '':
                resistencia_interna = float(resistencia_interna)
            if tamanho_bateria.strip() == '':
                tamanho_bateria = 'Não Informado'
            if peso_bateria.strip() == '':
                peso_bateria = 'Não Informado'
            else:
                peso_bateria = float(peso_bateria)

            # Converte dados numéricos para float
            tensao_bateria = float(tensao_bateria)
            taxa_descarga = float(taxa_descarga)
            capacidade_bateria = float(capacidade_bateria)
            pico_corrente_motor = float(pico_corrente_motor)

            # Calcula a estimativa de tempo de voo usando o método
            estimativa_tempo_voo = self.calcular_estimativa_tempo_voo(capacidade_bateria, pico_corrente_motor)

            # Determina a recomendação da bateria
            recomendacao = 'Bateria Recomendada' if taxa_descarga > pico_corrente_motor else 'Bateria Não Recomendada'

            # Verifica se já existe uma entrada com os mesmos dados
            if not self.dados[
                (self.dados['Modelo da bateria'] == modelo_bateria) &
                (self.dados['Tensão da bateria (V)'] == tensao_bateria) &
                (self.dados['Resistência interna (Ohms)'] == resistencia_interna) &
                (self.dados['Taxa de descarga (C)'] == taxa_descarga) &
                (self.dados['Tamanho da bateria (mm)'] == tamanho_bateria) &
                (self.dados['Peso da bateria (g)'] == peso_bateria) &
                (self.dados['Capacidade da bateria (mAh)'] == capacidade_bateria) &
                (self.dados['Modelo do motor'] == modelo_motor) &
                (self.dados['Pico de corrente do motor (A)'] == pico_corrente_motor) &
                (self.dados['Estimativa de tempo de voo'] == estimativa_tempo_voo)
            ].empty:
                print("Já existe uma entrada com os mesmos dados. Os dados não serão adicionados novamente.")
            else:
                # Adiciona os novos dados ao DataFrame
                novos_dados = {
                    'Modelo da bateria': [modelo_bateria],
                    'Tensão da bateria (V)': [tensao_bateria],
                    'Resistência interna (Ohms)': [resistencia_interna],
                    'Taxa de descarga (C)': [taxa_descarga],
                    'Tamanho da bateria (mm)': [tamanho_bateria],
                    'Peso da bateria (g)': [peso_bateria],
                    'Capacidade da bateria (mAh)': [capacidade_bateria],  
                    'Modelo do motor': [modelo_motor],
                    'Pico de corrente do motor (A)': [pico_corrente_motor],
                    'Estimativa de tempo de voo': [estimativa_tempo_voo],
                    'Recomendação': [recomendacao]
                }
                self.dados = pd.concat([self.dados, pd.DataFrame(novos_dados)], ignore_index=True)

                # Reorganiza o DataFrame pelo tempo de voo em ordem decrescente
                self.dados = self.dados.sort_values(by='Estimativa de tempo de voo', ascending=False).reset_index(drop=True)
                

                # Salva o DataFrame atualizado no arquivo
                self.dados.to_csv(self.arquivo, index=False)

                print("Dados adicionados com sucesso!")

            continuar = input("Deseja adicionar mais dados? (s/n): ")
            if continuar.lower() != 's':
                break

# Utilização da classe
banco_dados = BancoDados()
banco_dados.adicionar_dados()
