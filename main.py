from gerador import*
import numpy as np

num_barras = 6
redun_min = .6
nome_top = 'A'+str(num_barras) + 'b.txt'


#LÊ topologia
with open(nome_top, 'r') as f:
    A = np.array([[int(num) for num in line.split(',')] for line in f])

#GERA esquema de medição
gera_plano(A,redun_min)

#ESCREVE esquema de medição
