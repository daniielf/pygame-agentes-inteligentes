## ARQUIVO DE CONFIGURACAO PARA OS AGENTES INTELIGENTES
# AQUI ESTAO AS VARIAIVES PARA SERVIREM DE CONFIGURACAO PARA OS AGENTES INTELIGENTES USAREM COMO PARAMETROS

##### LEVEL 1 - BALIZA

## TOLERANCIA - DADOS DE TOLERANCIA

_L1_tentativas = 3  # QUANTIDADE DE TENTATIVAS (DEFAULT = 3)
_L1_tempo_restante = 15   # TEMPO PARA ATIVAR AJUDA segundos (DEFAULT = 15)
_L1_batidas = 3     # QUANTIDADE DE BATIDAS (DEFAULT = 3)

## AJUSTES - DADOS DE AJUSTE PARA O JOGO

_L1_penalidade_tempo_facil = 1          # PENALIDADE DE TEMPO PARA CADA BATIDA (DEFAULT = 2.5)
_L1_penalidade_tempo_dificil = 2        # PENALIDADE DE TEMPO PARA CADA BATIDA (DEFAULT = 6)

_L1_tempo_jogo_dificil = 40             # TEMPO DE JOGO PARA O MODO DIFICIL (DEFAULT = 40)
_L1_tempo_jogo_facil = 60               # TEMPO DE JOGO PARA O MODO FACIL (DEFAULT = 60)


##### LEVEL 2 - BALIZA COM OBSTACULOS

## TOLERANCIA - DADOS DE TOLERANCIA

_L2_tentativas = 3  # QUANTIDADE DE TENTATIVAS (DEFAULT = 3)
_L2_tempo_restante = 40000   # TEMPO PARA ATIVAR AJUDA milisegundos (DEFAULT = 40000)
_L2_batidas = 2     # QUANTIDADE DE BATIDAS (DEFAULT = 2)

## AJUSTES - DADOS DE AJUSTE PARA O JOGO

_L2_tempo_jogo_dificil = 30            # TEMPO DE JOGO PARA O MODO DIFICIL (DEFAULT = 40)
_L2_tempo_jogo_facil = 45              # TEMPO DE JOGO PARA O MODO FACIL (DEFAULT = 60)
_L2_penalidade_tempo_facil = 2          # PENALIDADE DE TEMPO PARA CADA BATIDA (DEFAULT = 3)
_L2_penalidade_tempo_dificil = 4        # PENALIDADE DE TEMPO PARA CADA BATIDA (DEFAULT = 8)


##### LEVEL 3 - SIMULADOR DE TRANSITO

## TOLERANCIA - DADOS DE TOLERANCIA

_L3_batidas = 5         # BATIDAS DE CARRO (DEFAULT = 5)
_L3_falha_atender = 2   # NAO ATENDER O TELEFONE (DEFAULT = 2)

## AJUSTES - DADOS DE AJUSTE

_L3_tempo_jogo_dificil = 40            # TEMPO DE JOGO PARA O MODO DIFICIL (DEFAULT = 40)
_L3_tempo_jogo_facil = 60              # TEMPO DE JOGO PARA O MODO FACIL (DEFAULT = 60)

_L3_ponto_atender_facil = 200       # AJUSTE DE PONTOS AUMENTADO PARA ATENDER O CELULAR (DEFAULT = 200)
_L3_ponto_atender_dificil = 50      # AJUSTE DE PONTOS AUMENTADO PARA ATENDER O CELULAR (DEFAULT = 50)