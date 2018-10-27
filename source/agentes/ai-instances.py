import datetime
### TIPOS DE AGENTES DO SISTEMA

## PADROES DE COMPARACAO
# 'eq' : IGUAL
# 'gte' : MAIOR QUE
# 'gt' : MAIOR
# 'lte' : MENOR QUE
# 'lt' : MENOR

def comparaValoresPadronizado(comparacao, valor_parametro, valor_entrada):
    if (comparacao == "eq"):
        return (valor_entrada == valor_parametro)
    if (comparacao == "gte"):
        return (valor_entrada >= valor_parametro)
    if (comparacao == "gt"):
        return (valor_entrada > valor_parametro)
    if (comparacao == "lte"):
        return (valor_entrada <= valor_parametro)
    if (comparacao == "lt"):
        return (valor_entrada < valor_parametro)



## AGENTE DE ACAO
class Agente_Interativo():
    def __init__(self, valor_parametro, callback, comparacao):
        self.parametro = valor_parametro    # PARAMETRO DE COMPORTAMENTO (DEFINIDO NO ai-config.py)
        self.acao = callback                # METODO DE CALLBACK PARA ATIVAR A FUNCIONALIDADE DO AGENTE
        self.comparacao = comparacao        # TIPO DE COMPARACAO (IGUAL, MAIOR, MENOR, MAIOR-IGUAL, MENOR-IGUAL)

    # Metodo que analisa a entrada e interage de acordo com os padroes de comparacao e parametro do agente
    def analizaEntrada(self, valor_entrada):
        if comparaValoresPadronizado(self.comparacao, self.parametro, valor_entrada):
            self.acao()



## AGENTE DE LOG
class Agente_de_Escrita():
    def __init__(self, caminho_de_escrita = '../logs/log.txt', idJogador = 'N/I', atividade = ''):
        self.caminhoArquivo = caminho_de_escrita    # CAMINHO DO ARQUIVO DE OUTPUT DO AGENTE
        self.id = idJogador                         # IDENTFICADOR DO JOGADOR
        self.atividade = atividade                  # NUMERO OU NOME DA ATIVIDADE (FASE)

    # Metodo para escrever no arquivo de saida dado os valores de entrada
    # Formato:  ID      ATIVIDADE       << VALORES DE ENTRADA >>    DATA
    def escreveLog(self, dadosEntrada=[]):
        dadosSaida = [self.id, self.atividade]
        dadosSaida = dadosSaida + dadosEntrada
        dadosSaida.append(datetime.datetime.now())  # insere o tempo do registro como ultimo parametro

        for elem in dadosEntrada:
            print(elem)
            # ESCREVE NO ARQUIVO


