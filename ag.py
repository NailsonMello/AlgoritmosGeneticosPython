from flask import Flask, render_template, request
from random import random
import matplotlib.pyplot as plt
import pymysql

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/resultado', methods = ['POST', 'GET'])
def send_data():
    rugtt = []
	#p1 = Produto("Iphone 6", 0.0000899, 2199.12)
    lista_produtos = []
    conexao = pymysql.connect(host='localhost', user='root', passwd='123456', db='produtos')#fazendo a conexão com a base de dados para recuperar os produtos cadastrados
    cursor = conexao.cursor()
    cursor.execute('select nome, espaco, valor, quantidade from produtos')
    for produto in cursor:
        #print(produto[3])
        for i in range(produto[3]):
            lista_produtos.append(Produto(produto[0], produto[1], produto[2]))
    
    cursor.close()
    conexao.close()
     
    espacos = []
    valores = []
    nomes = []
	
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 10
    ind = 1
    tamanho_populacao = 20
    taxa_mutacao = 0.01
    numero_geracoes = 100
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            item = str(ind)+" -- Produto: "+lista_produtos[i].nome + " - Valor: R$ "+str(lista_produtos[i].valor)
            rugtt.append(item)
            ind = ind+1
    gerr = ger
    vr = valor
    ep = espaco
    cr = croo
    grafico = ag.lista_solucoes
    return render_template('home.html',rugtt = rugtt,gerr = gerr, vr=vr, ep=ep, cr=cr, grafico=grafico)
	
# classe que armazena os produtos 
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome #criando um atributo que recebe o parametro nome
        self.espaco = espaco
        self.valor = valor
 #       
class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos #cria o atributo que recebe o parametro
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = []
        
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
                
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
           if self.cromossomo[i] == '1':
               nota += self.valores[i]
               soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
        
    def crossover(self, outro_individuo):
        corte = round(random()  * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
    
    def mutacao(self, taxa_mutacao):
        #print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        #print("Depois %s " % self.cromossomo)
        return self
        
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    #aqui mostra a geracao
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        global ger
        global valor
        global espaco
        global croo
        self.inicializa_populacao(espacos, valores, limite_espacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
        ger = str(self.melhor_solucao.geracao)
        valor = str("{:10.2f}".format(self.melhor_solucao.nota_avaliacao))	
        espaco = str("{:10.3f}".format(self.melhor_solucao.espaco_usado))
        croo = str(self.melhor_solucao.cromossomo)		
               
        return self.melhor_solucao.cromossomo
                   
if __name__ == '__main__':
	app.run(debug=True)

    
   