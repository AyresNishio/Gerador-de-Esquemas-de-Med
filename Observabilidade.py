import numpy as np

#plano de medição
#Coluna - função
# 0 - de
# 1 - para
# 2 - Unidade de Medição
# 3 - Circuito
# 4 - Tipo
# 5 - de (redundante)
# 6 - ligado ou desligado

def Jacobiana(A,medidas,fasor):
    n_med=int(sum(medidas[:,6]))
    n=A.shape[0]
    H=np.zeros([n_med,n])#nao precisa de ref pois possui medida fasorial
    Haux= np.zeros([n_med,n-1])
    ind=0
    med=0
    while (med<n_med):

        if (medidas[ind,6]==1):#indica se a medida esta ligada ou desligada

            de=int(medidas[ind,1])-1
            para=int(medidas[ind,2])-1

            if (de!=para): #serve para medida de fluxo de potencia e de corrente
                H[med,de]=1
                H[med,para]=-1

            if (de==para)and(medidas[ind,4]==3):#medida de angulo
                 H[med,de]=1

            if (de==para)and(medidas[ind,4]==2):#medida de injecao de Potencia
                nbc=int(sum(A[de,:]))
                for l in range(n-1):
                    if (l==de):
                        H[med,l]=nbc
                    else:
                        H[med,l]=-1*(A[de,l])    
            med=med+1
        ind=ind+1


    if (fasor==0):
        return H
    else:
        Haux=H[:,1:n-1]
        return Haux

    #A = topologia

def Ganho(H):
    G=np.matmul(np.transpose(H),H)
    return G

def Covariância(G,H):
    I=np.eye(H.shape[0])
    if (teste_observabilidade(G,1.E-10)):
        aux = np.matmul(H,np.linalg.inv(G))
        E= I - np.matmul(aux,np.transpose(H))
    else :
        E=np.zeros(H.shape[0])
    return E  

def teste_observabilidade(G,tol):
    if(np.linalg.det(G)>=tol): 
        return True  
    if(np.linalg.det(G)<tol): 
        print('Não observável')
        return False 


# nbar =30
# nome_top = 'A' +str(nbar) + 'b.txt'
# with open(nome_top, 'r') as f:
#     A = np.array([[int(num) for num in line.split(',')] for line in f])
# nmed=43
# nome_med = "med_"+str(nbar)+"bus_"+str(nmed)+".txt"
# with open(nome_med, 'r') as f:
#     med_plan = np.array([[int(num) for num in line.split(',')] for line in f])

# fasor=0 #0 indica que há medida fasorial e 1 indica que não há medida fasorial
# n=A.shape[0]-fasor
# H = Jacobiana(A,med_plan,fasor)
# G = Ganho(H)
# E = Covariância(G,H)

# with open(f'E{nbar}m{nmed}b.txt','w') as f:
#     np.savetxt(f, E) 
