import xlsxwriter as excelWriter

### INDIVIDUAL
# id = '15875841745'
# filename =  id + '_resumo.txt'
# file = open(filename, 'r')
#
# file_line = file.readline() ## useless line
# file_line = file.readline() ## useless line
# file_line = file.readline()
#
#
# row = 0
# col = 0
#
# excelFile = excelWriter.Workbook(id + '_excel.xlsx')
# _worksheet = excelFile.add_worksheet()
#
# _worksheet.write(row,col, id)
#
# row += 1
# _worksheet.write(row, 0, 'FASE')
# _worksheet.write(row, 1, 'INFRACOES')
# _worksheet.write(row, 2, 'VITORIA (w)/ DERROTA (l)')
# _worksheet.write(row, 3, 'TEMPO RESTANTE / PONTOS ADQUIRIDOS')
# _worksheet.write(row, 4, 'HORA')
# _worksheet.write(row, 5, 'DATA')
#
# row += 1
# while (file_line):
#     infoArray = file_line.split(' ') ## [ LEVEL | INFRACOES | VIT/DE R | TEMPO RES. / PONTOS | DATA ]
#     col = 0
#
#     for value in infoArray:
#         _worksheet.write(row, col, value)
#         col += 1
#
#     row += 1
#     file_line = file.readline()


## GERAL

filename = 'resumoGeral.txt'
file = open(filename, 'r')


row = 0
col = 0

excelFile = excelWriter.Workbook('resumoGeral_excel.xlsx')
_worksheet = excelFile.add_worksheet()

_worksheet.write(row,col, 'Relatorio dos Jogadores')

row += 1
_worksheet.write(row, 0, 'ID')
_worksheet.write(row, 1, 'TENTATIVAS LEVEL 1')
_worksheet.write(row, 2, 'INFRAC. LEVEL 1')
_worksheet.write(row, 3, 'VITORIAS LEVEL 1')
_worksheet.write(row, 4, 'TENTATIVAS LEVEL 2')
_worksheet.write(row, 5, 'INFRAC. LEVEL 2')
_worksheet.write(row, 6, 'VITORIAS LEVEL 2')
_worksheet.write(row, 7, 'INFRAC. P/ TENTATIVA LEVEL 1 E 2')
_worksheet.write(row, 8, 'TENTATIVAS LEVEL 3')
_worksheet.write(row, 9, 'INFRAC. LEVEL 3')
_worksheet.write(row, 10, 'MEDIA PTS LEVEL 3')
_worksheet.write(row, 11, 'INFRAC. P/ TENTATIVA LEVEL 3')

file_line = file.readline() ## useless line
file_line = file.readline()

excelFile.close()
