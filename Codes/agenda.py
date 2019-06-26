import sys
from datetime import datetime

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

# não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False

  ################ COMPLETAR
  novaAtividade = descricao
  for i in extras:
    novaAtividade += i + ' '
  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  aux=True
  ################ COMPLETAR
  if len(pri)!=3 or pri[0]!='(' or pri[2]!=')' or not (ord(pri[1])>64 and ord(pri[1])<91) and not (ord(pri[1])>96 and ord(pri[1])<123):
    aux=False
    
  return aux
  
# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin):
  aux = True
  if len(horaMin) != 4 or not soDigitos(horaMin):
    aux = False
  else:
    ################ COMPLETAR
    hora = int(horaMin[:2])
    minu = int(horaMin[2:])
    if hora < 0 or hora > 23 or minu > 59 or minu < 0:
      aux = False
  return aux

# Valida se foi colocado dias maiores no meses com 30 e 29 dias
def diaValido(dia,mes):
  aux = True
  mes30=[4,6,9,11]
  if mes == 2 and (dia > 29 or dia < 1):
    aux = False
  for i in mes30:
    if i==mes and dia>30:
      aux=False
  return aux
      
  
  
  
# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  aux = True
  if len(data) != 8 or not soDigitos(data):
    aux = False
  else:
    dia=int(data[:2])
    mes=int(data[2:4])
    ano=int(data[4:])
    if dia<1 or dia>31 or mes>12 or mes<1 or ano>9999 or ano<1000 or not diaValido(int(dia),int(mes)):
      aux=False
  return aux

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  aux = True

  ################ COMPLETAR
  if proj[0] != '+' or len(proj)<2:
    aux = False
  
  return aux
# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  aux = True
  ################ COMPLETAR
  if cont[0] != '@' or len(cont)<2:
    aux = False
  return aux
# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  aux = True
  if type(numero) != str :
    aux = False
  for x in numero :
    if x < '0' or x > '9' :
      aux = False
  return aux 


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []
  for l in linhas:
    data=''
    hora=''
    pri=''
    contexto=''
    projeto=''
    desc=''

    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    for p in tokens:
      if dataValida(p):
        data = p
      elif horaValida(p):
        hora = p
      elif prioridadeValida(p):
        pri = p
      elif contextoValido(p):
        contexto = p
      elif projetoValido(p):
        projeto = p
      else:
        desc += p + " "
    
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    ################ COMPLETAR
    if desc!='':
      itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens

def filtrar(listas, comandos):
  resultado=[]
  aux=0
  if comandos[0] == 'pri':
    comandos.pop(0)
    aux=2
    
  elif comandos[0] == 'c':
    comandos.pop(0)
    aux=3
   
  elif comandos[0] == 'pro':
    comandos.pop(0)
    aux=4
    
  else:
    return listas
  
  for i in listas:
    if i[1][aux]==comandos[0]:
      resultado.append(i)
  return resultado
        
# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar(comandos):
  linhas=[]
  arquivoLido = ""
  backUp= ""
  try: 
    fp = open(TODO_FILE, 'r')
    arquivoLido = fp.read()
    backUp=fp.read()
    fp.close()
  except IOError as err:
    print("Não foi possível ler para o arquivo " + TODO_FILE)
    print(err)
    return ''
  ################ COMPLETAR
 
  
  aux = ''
  count=1
  for i in arquivoLido:
    if i == "\n":
      linhas.append(str(count)+'- '+aux)
      aux = ''
      count+=1
    else:
      aux+=i

  linhas=organizar(linhas)
  if len(comandos)>0:
    if comandos[0] == 'f':
      comandos.pop(0)
      linhas = filtrar(linhas, comandos)
  #print(linhas)
  linhas=ordenarPorPrioridade(linhas)
  #linhas = ordenarPorDataHora(linhas)  
  #linhas=ordenarPorPrioridade(linhas)
  #linhas = ordenarPorDataHora(linhas)
  for i in linhas:
    aux=''
    if i[1][2]!='':
      aux+= i[1][2] + ' '
    if i[1][0]!='':
      aux+= i[1][0][:2]+"/"+i[1][0][2:4]+"/"+i[1][0][4:]+' '
    if i[1][1]!='':
      aux+=i[1][1][:2]+'h'+i[1][1][2:]+'m'+' '
  
    print(i[0][:2] + aux + i[0][2:] + i[1][3] + ' ' + i[1][4])
  #return linhas

def bubbleSort(numeros,aux):
  for i in range(0,len(numeros)-1):
    for j in range(0, len(numeros)-1-i):     
      if numeros[j][aux]>numeros[j+1][aux]:
        numeros[j],numeros[j+1]=numeros[j+1],numeros[j]
      elif numeros[j][aux]==numeros[j+1][aux] and aux<4:
        bubbleSort([numeros[j],numeros[j+1]],aux+1)
        

def ordenarPorDataHora(itens):
  dataHora=[]
  for i in range(len(itens)):
    #aux=[itens[i][1][0][4:],itens[i][1][0][2:4],itens[i][1][0][:2],itens[i][1][1][:2],itens[i][1][1][2:],i]
    aux=[itens[i][1][0][4:],itens[i][1][0][2:4],itens[i][1][0][:2],itens[i][1][1][:2],itens[i][1][1][2:]]
    if aux[0]!="":
      dataHora.append(aux)

  bubbleSort(dataHora,0)
  aux=[]
  for i in dataHora:
    for w in itens:
      if i[2]+i[1]+i[0]+i[3]+i[4] == w[1][0]+w[1][1]:
        aux.insert(0,w)
        itens.remove(w)
        
        
  aux=aux+itens
      
  #for i in aux:
  #  print(i)
  ################
  return aux

def ordenarNumeros(lista):
  for i in range(0,len(lista)-1):
    for j in range(0,len(lista)-1):
      Ilist= ord(lista[j][1][2][1]) if lista[j][1][2] != '' else 255
      Jlist= ord(lista[j+1][1][2][1]) if lista[j+1][1][2] != '' else 255
      if Ilist>Jlist:
        lista[j],lista[j+1] = lista[j+1],lista[j]
      elif Ilist==Jlist:
        aux = ordenarPorDataHora([lista[j],lista[j+1]])
        lista[j],lista[j+1] = aux[0],aux[1] 

def ordenarPorPrioridade(itens):
  #i=0
  #prioridades=[]
  #aux=itens[:]
  #for a in itens:
  #  if a[1][2]!='':
  #   prioridades.append(a)

  
  ordenarNumeros(itens)
  #for i in itens:
  # print(i)
   
  #for i in itens:
   # print(i)
  #i=0
  #for a in range(len(itens)):
  #  if itens[a][1][2]!='':
  #    itens.pop(a)
  #    itens.insert(0,prioridades[i])
  #    i+=1
  #print(prioridades+itens)
  #print(itens[0][1][2][1])
  #print(prioridades)
  return itens
    

def fazer(num):

  linhas=[]
  fp = open(TODO_FILE, 'r')
  arquivoLido = fp.read()
  fp.close()
  aux=''
  for i in arquivoLido:
    if i == "\n":
      linhas.append(aux+'\n')
      aux = ''
    else:
      aux+=i
  fp=open(ARCHIVE_FILE,'a')
  #Abertura dos arquivos
  done=linhas[num-1]
  print(linhas[num-1],'\nAtividade Concluida!')
  linhas.pop(num-1)
  #Operações de alteração
  fp.writelines(done)
  #Alterações implementadas
  fp.close()
  #Fechamento dos arquivos
  fp=open(TODO_FILE, 'w')
  fp.writelines(linhas)
  fp.close
  return 

 
def remover(num):

  linhas=[]
  fp = open(TODO_FILE, 'r')
  arquivoLido = fp.read()
  fp.close()
  aux=''
  for i in arquivoLido:
    if i == "\n":
      linhas.append(aux+'\n')
      aux = ''
    else:
      aux+=i
  print(linhas[num-1],'\nAtividade removida')
  linhas.pop(num-1)
  fp=open(TODO_FILE, 'w')
  fp.writelines(linhas)
  fp.close

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  alvo=[]
  i=0
  aux=''
  while i<26:
    alvo.append('('+chr(65+i)+')')
    i+=1


  fp = open(TODO_FILE, 'r')
  atividades= fp.readlines()
  fp.close()
  print(atividades[int(num)-1])
  aux=str(atividades[int(num)-1])
  local=-1
  for a in alvo:
    if atividades[int(num)-1].find(a)!=-1:
      local=atividades[int(num)-1].find(a)
    
  if local==-1:
    atividades[int(num)-1]='('+prioridade+') '+atividades[int(num)-1]
  else:
    aux=aux[:local+1]+aux[local+2:]
    atividades[int(num)-1]='('+prioridade+') '+aux[:local+1]+aux[local+2:]
  fp=open(TODO_FILE, 'w')
  fp.writelines(atividades)
  fp.close()
  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  comandos.pop(0) # remove 'agenda.py'
  
  #Adicionar uma tarefa
  if comandos[0] == ADICIONAR:
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    print(itemParaAdicionar)
##    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    result = adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    if result:
      print('Ação adicionada com sucesso! ')
  elif comandos[0] == LISTAR:
    comandos.pop(0) # remove 'listar'
    listar(comandos)
##    return    
##    ################ COMPLETAR
##
  elif comandos[0] == REMOVER:
    comandos.pop(0) # remove 'remover'
    remover(int(comandos[0]))
    comandos.pop(0)
##    return    
##
##    ################ COMPLETAR    
##
  elif comandos[0] == FAZER:
    comandos.pop(0)
    fazer(int(comandos[0]))
    comandos.pop(0)
##    return    
##
##    ################ COMPLETAR
##
  elif comandos[0] == PRIORIZAR:
    comandos.pop(0)
    priorizar(comandos[0],comandos[1])
    comandos.pop(0)
    comandos.pop(0)
    # remove 'prioridade'
##    return    
##    ################ COMPLETAR
##
  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
