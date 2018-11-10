from __future__ import division

_id = '13766566717'

filename = str(_id) + '.txt'

l1_totalTries = 0
l2_totalTries = 0
l3_totalTries = 0

l1_temposVitoria = []
l2_temposVitoria = []
l3_pontosObtidos = []

l1_totalWin = 0
l2_totalWin = 0
l3_acoesPositivass = 0

l1_totalInfracoes = 0
l2_totalInfracoes = 0
l3_totalInfracoes = 0


_level_resumes = [] ## [level, infracoes, 'w/l' / '-' , tempo restante/ pontuacao, data ]


file = open(filename, 'r')

index = -1

file_line = file.readline()
while (file_line):
    infoArray = file_line.split(' ') ## [ 0: id , 1: level, 2: action, 3: value , 4: hour:minute , 5: dd-mm-yyyy , 6: '\n']

    ## ANALISE DO LEVEL 1
    if (infoArray[1] == '1'):
        if (infoArray[2] == 'NOVOJOGO'):
            index += 1
            l1_totalTries +=1
            _level_resumes.append([1,0,'-', 0, infoArray[4] + ' ' + infoArray[5]])


        if (infoArray[2] == 'VENCEU'):
            l1_totalWin += 1
            l1_temposVitoria.append(infoArray[3])

            _level_resumes[index][2] = 'w'
            _level_resumes[index][3] = infoArray[3]

        if (infoArray[2] == 'PERDEU'):
            _level_resumes[index][2] = 'l'
            _level_resumes[index][3] = infoArray[3]

        if (infoArray[2] == 'INFRACAO'):
            l1_totalInfracoes += 1

            _level_resumes[index][1] += 1

    if (infoArray[1] == '2'):
        if (infoArray[2] == 'NOVOJOGO'):
            index += 1

            l2_totalTries +=1
            _level_resumes.append([2,0,'-', 0, infoArray[4] + ' ' + infoArray[5]])

        if (infoArray[2] == 'VENCEU'):
            l2_totalWin += 1
            l2_temposVitoria.append(infoArray[3])

            _level_resumes[index][2] = 'w'
            _level_resumes[index][3] = infoArray[3]

        if (infoArray[2] == 'PERDEU'):
            _level_resumes[index][2] = 'l'
            _level_resumes[index][3] = infoArray[3]


        if (infoArray[2] == 'INFRACAO'):
            l2_totalInfracoes += 1
            _level_resumes[index][1] += 1


    if (infoArray[1] == '3'):
        if (infoArray[2] == 'TERMINOU'):
            index += 1
            l3_totalTries +=1
            l3_pontosObtidos.append(infoArray[3])

            _level_resumes.append([3,0,'-', 0, infoArray[4] + ' ' + infoArray[5]])
            _level_resumes[index][3] = infoArray[3]

        if (infoArray[2] == 'BATIDA' or infoArray[2] == 'NAOATENDEU' or infoArray[2] == 'ATENDEUERRADO'):
            l3_totalInfracoes += 1

            _level_resumes[index][1] += 1

        if (infoArray[2] == 'ATENDEU' or infoArray[2] == 'PAROU'):
            l3_acoesPositivass += 1


    file_line = file.readline()


def sortMode(list):
    return list[0]

_level_resumes.sort(key=sortMode)
#
# for game in _level_resumes:
#     print (game)


file.close()

_infracoesPorPartida = 0
if (l1_totalTries + l2_totalTries > 0):
    _infracoesPorPartida = (l1_totalInfracoes + l2_totalInfracoes) / (l1_totalTries + l2_totalTries)

_totalTentavias = (l1_totalTries) + (l2_totalTries)
_totalInfracoes = (l1_totalInfracoes) + (l2_totalInfracoes)

_3_infracoesPorPartida = 0
_3_pontosMedio = 0
if (l3_totalTries > 0):
    _3_infracoesPorPartida = (l3_totalInfracoes) / (l3_totalTries)

# print 'Total Vitorias Level 1:  ' + str(l1_totalWin)
# print 'Total Vitorias Level 2:  ' + str(l2_totalWin)
# print 'Total Acoes Positivas Level 3:  ' + str(l3_acoesPositivass)
#
# print '\nTotal Tentativas Level 1:  ' + str(l1_totalTries)
# print 'Total Tentativas Level 2:  ' + str(l2_totalTries)
# print 'Total Tentativas Level 3:  ' + str(l3_totalTries)
#
# print '\nTotal Infra. Level 1:  ' + str(l1_totalInfracoes)
# print 'Total Infra. Level 2:  ' + str(l2_totalInfracoes)
# print 'Total Infra. Level 3:  ' + str(l3_totalInfracoes)
#
# print '\n-- Level 1 e 2 -- :\n'
# print 'Total Tentativas:  ' + str(_totalTentavias)
# print 'Total Infracoes:  ' + str(_totalInfracoes)
# print 'Media infracao por partida ' + ("%.3f" % _infracoesPorPartida)
#
# print '\n-- Level 3 -- :\n'
# print 'Total Tentativas:  ' + str(l3_totalTries)
# print 'Total Infracoes:  ' + str(l3_totalInfracoes)
# print 'Media infracao por partida ' + ("%.3f" % _3_infracoesPorPartida)
#
#
# print '\n\n -- Win Level 1 --'

#
# for time in l1_temposVitoria:
#     print 'Tempo Restante: ' + str(time)

# print '\n\n -- Win Level 2 --'
# for time in l2_temposVitoria:
#     print 'Tempo Restante: ' + str(time)


_l3_totalPontos = 0
# print '\n\n -- Win Level 3 --'
for points in l3_pontosObtidos:
    # print 'Pontos Obtidos: ' + str(points)
    _l3_totalPontos += int(points)

_l3_pontosMedia = 0
if (l3_totalTries > 0):
    _l3_pontosMedia = _l3_totalPontos / l3_totalTries


##

## ARQUIVO DE RESUMO PESSOAL
personalResumeFile = open('resumos/' + _id + '_resumo.txt', 'w')
personalResumeFile.write('RESUMO DO JOGADOR : ' + _id + '\n')
personalResumeFile.write('LEVEL | INFRACOES | VIT/DER | TEMPO RES. / PONTOS | DATA \n')
for line in _level_resumes:
    personalResumeFile.write(str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3]) + ' ' + str(line[4]) + '\n')


## ARQUIVO GERAL DOS JOGADORES
# ID    L1-TRY   L1-INFRACOES   L1-WINS   L2-TRY  L2-INFRACOES  L2-WINS  (L1 + L2) INFRA/TRY  L3-TRY    L3-INFRACOES    L3-MEDIAPONTOS  L3 INFRA/TRY
generalFile = open('resumos/resumoGeral.txt', 'a')
generalFile.write(
    _id + ' ' + str(l1_totalTries) + ' ' + str(l1_totalInfracoes) + ' ' + str(l1_totalWin) + ' ' + str(l2_totalTries) + ' ' + str(l2_totalInfracoes) + ' ' + str(l2_totalWin) + ' ' + str(_infracoesPorPartida)
    + ' ' +str(l3_totalTries) + ' ' + str(l3_totalInfracoes) + ' ' + str(_l3_pontosMedia) + ' ' + str(_3_infracoesPorPartida) + '\n'
)