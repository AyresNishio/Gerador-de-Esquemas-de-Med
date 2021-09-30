import numpy as np
from random import seed
from random import sample

from Observabilidade import *

    #plano de medição
#Coluna - função
# 0 - numero da medida
# 1 - de
# 2 - para (igual a de em caso de injeção)
# 3 - Circuito (não utilizado)
# 4 - Tipo (1 fluxo, 2 injeção, 3 ângulo, 7 corrente)
# 5 - Unidade de Medição (de)
# 6 - ligado ou desligado

def gera_plano(A,redun_min):
    #Conta numero de ramos
    num_ramos = 0
    for line in A:
        for i in line:
            num_ramos += i
    num_ramos = int(num_ramos/2)
    #Conta numero de barras
    num_barras = A.shape[0]
    #maximo de medidas
    max_med = num_ramos*2 + num_barras
    #Plano vazio
    med_plan = gera_plano_vazio(A,num_ramos,num_barras,max_med)
    #Sorteia barra 
    barras_nao_alocadas = [i for i in range(1,num_barras+1)]
    #seed(5)
    barras_sorteadas = sample(barras_nao_alocadas, 1)
    barras_nao_alocadas = [x for x in barras_nao_alocadas if x not in barras_sorteadas]
    medidas_adicionadas = 0
    medidas_adicionadas += aloca_medidas(med_plan,barras_sorteadas)
    redun =  medidas_adicionadas/max_med
    #enquanto redun < redun_min e rede não observavel

    fasor=1 #0 indica que há medida fasorial e 1 indica que não há medida fasorial
    H = Jacobiana(A,med_plan,fasor)
    G = Ganho(H)
    while(not teste_observabilidade(G,1.E-10) or redun<redun_min):
        barras_sorteadas = sample(barras_nao_alocadas, 1)
        barras_nao_alocadas = [x for x in barras_nao_alocadas if x not in barras_sorteadas]
        medidas_adicionadas += aloca_medidas(med_plan,barras_sorteadas)
        redun =  medidas_adicionadas/max_med
        H = Jacobiana(A,med_plan,fasor)
        G = Ganho(H)
        print(teste_observabilidade(G,1.E-10), redun)
        
    E = Covariância(G,H)
       
    return E, med_plan

    print('')


def gera_plano_vazio(A,num_ramos, num_barras, max_med):
    med_plan = np.zeros([max_med,7],np.int32)
    medida = 0
    # #medidas de ângulo
    # for linha in range(num_barras):
    #     barra = linha+1
    #     med_plan[medida][0] = medida + 1
    #     med_plan[medida][1] = barra
    #     med_plan[medida][2] = barra
    #     med_plan[medida][3] = 1
    #     med_plan[medida][4] = 3
    #     med_plan[medida][5] = barra
    #     med_plan[medida][6] = 0
        
    #     medida = medida + 1

    #medidas de ângulo
    for linha in range(num_barras):
        for col in range(num_barras):
            if(A[linha][col] == 1):
                de = linha+1
                para = col+1
                med_plan[medida][0] = medida
                med_plan[medida][1] = de
                med_plan[medida][2] = para
                med_plan[medida][3] = 1
                med_plan[medida][4] = 1
                med_plan[medida][5] = de
                med_plan[medida][6] = 0
                
                medida = medida + 1

    #medidas de fluxo
    for linha in range(num_barras):
        barra = linha+1
        med_plan[medida][0] = medida
        med_plan[medida][1] = barra
        med_plan[medida][2] = barra
        med_plan[medida][3] = 1
        med_plan[medida][4] = 2
        med_plan[medida][5] = barra
        med_plan[medida][6] = 0
        
        medida = medida + 1

    return med_plan

def aloca_medidas(med_plan, num_barr):
    medidas_adicionadas = 0
    for linha in med_plan:
        if(linha[1] ==num_barr or linha[2] == num_barr): 
            if linha[6] == 0 : 
                medidas_adicionadas=medidas_adicionadas + 1
                linha[6] = 1 
    return medidas_adicionadas