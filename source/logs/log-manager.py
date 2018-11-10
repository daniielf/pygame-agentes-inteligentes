from __future__ import division

_id = '13291895746'

filename = str(_id) + '.txt'

l1_totalTries = 0
l2_totalTries = 0

l1_temposVitoria = []
l2_temposVitoria = []

l1_totalWin = 0
l2_totalWin = 0

l1_totalInfracoes = 0
l2_totalInfracoes = 0

file = open(filename, 'r')

file_line = file.readline()
while (file_line):
    infoArray = file_line.split(' ') ## [ 0: id , 1: level, 2: action, 3: value , 4: hour:minute , 5: dd-mm-yyyy , 6: '\n']

    ## ANALISE DO LEVEL 1
    if (infoArray[1] == '1'):
        if (infoArray[2] == 'NOVOJOGO'):
            l1_totalTries +=1
        if (infoArray[2] == 'VENCEU'):
            l1_totalWin += 1
            l1_temposVitoria.append(infoArray[3])
        if (infoArray[2] == 'INFRACAO'):
            l1_totalInfracoes += 1

    if (infoArray[1] == '2'):
        if (infoArray[2] == 'NOVOJOGO'):
            l2_totalTries +=1
        if (infoArray[2] == 'VENCEU'):
            l2_totalWin += 1
            l2_temposVitoria.append(infoArray[3])
        if (infoArray[2] == 'INFRACAO'):
            l2_totalInfracoes += 1


    file_line = file.readline()

file.close()

_infracoesPorPartida = 0.0
_infracoesPorPartida += (l1_totalInfracoes + l2_totalInfracoes) / (l1_totalTries + l2_totalTries)
_totalTentavias = (l1_totalTries) + (l2_totalTries)
_totalInfracoes = (l1_totalInfracoes) + (l2_totalInfracoes)


print 'Total Vitorias Level 1:  ' + str(l1_totalWin)
print 'Total Vitorias Level 2:  ' + str(l2_totalWin)

print 'Total Tentativas Level 1:  ' + str(l1_totalTries)
print 'Total Tentativas Level 2:  ' + str(l2_totalTries)

print 'Total Infra. Level 1:  ' + str(l1_totalInfracoes)
print 'Total Infra. Level 2:  ' + str(l2_totalInfracoes)

print 'Total Tentativas:  ' + str(_totalTentavias)
print 'Total Infracoes:  ' + str(_totalInfracoes)
print 'Media infracao por partida ' + ("%.3f" % _infracoesPorPartida)

print '\n\n -- Win Level 1 --'
for time in l1_temposVitoria:
    print 'Tempo Restante: ' + str(time)

print '\n\n -- Win Level 2 --'
for time in l2_temposVitoria:
    print 'Tempo Restante: ' + str(time)
# for line in file.readline():

