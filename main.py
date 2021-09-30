from gerador import*
import numpy as np

num_barras = 118
redun_min = .6
nome_top = 'A'+str(num_barras) + 'b.txt'


#LÊ topologia
with open(nome_top, 'r') as f:
    A = np.array([[int(num) for num in line.split(',')] for line in f])

#GERA esquema de medição
E,med_plan = gera_plano(A,redun_min)

#ESCREVE esquema de medição
num_medidas =  sum(med_plan[:,6])
with open(f'E{num_barras}b{num_medidas}m.txt','w') as f:
        np.savetxt(f, E) 
with open(f'med{num_barras}b{num_medidas}m.txt','w') as f:
        np.savetxt(f, med_plan,fmt='%i')  
