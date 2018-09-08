# Inteligencia artificial, Python, para o jogo MS. HACK-MAN (https://booking.riddles.io/competitions/ms.-hack-man)
# Matheus Alves de Andrade

# Versão 1.0
# Desenvolvimento iniciado em 20/08/2018
# Versão finalizada em 29/08/2018

class Campo:
	'''
		Esta classe abstrai o campo de jogo
	'''

	def __init__(self, largura, altura):
		self.campo = None
		self.largura = largura
		self.altura = altura

	def set(self, listaCelulas):
		'''
		    Este método atualiza o estado do campo
		'''
		self.campo = self.formatarCampo(listaCelulas)
		self.aplicarCheiros()
		#self.debugPrintCampo()

	def debugPrintCampo(self):
		'''
			Este método serve para mostrar o campo armazenado em um arquivo
			C:\\Users\\[USUÁRIO]\\AppData\\Local\\Programs\\ai-bot-workspace
		'''
		arquivo = open("logCampo.txt","w+")
		for i in range(0, self.altura):
			arquivo.write("\r\n")
			for j in range(0, self.largura):
				if(not self.campo[i][j]['acessivel']):
					arquivo.write("|#.#|")
				else:
					arquivo.write("|"+str(self.campo[i][j]['cheiroBom'])+"|")
				
		arquivo.close()


	def formatarCampo(self, bruto):
		processado = []
		splitted = bruto.split(',')
		for i in range(0, self.altura):
			processado.append([])
			for j in range(0, self.largura):
				if(splitted[ i*self.largura + j ] == 'x'):
					processado[i].append( {'acessivel': False} )
				else:
					processado[i].append( {'acessivel': True, 'conteudo': splitted[ i*self.largura + j ], 'cheiroBom': 0.0, 'cheiroRuim': 0.0} )

		return processado

	def aplicarCheiros(self):
		for i in range(0, self.altura):
			for j in range(0, self.largura):
				if(self.campo[i][j]['acessivel']): # Está acessível
					if('C' in self.campo[i][j]['conteudo'].split(";")): # É um código
						self.aplicarCheiroBom(10.0, i, j)
					if('E' in [x[0] for x in self.campo[i][j]['conteudo'].split(";")]): # É um bug
						self.aplicarCheiroRuim(5.0, i, j)

	def aplicarCheiroBom(self, cheiro, x, y, vizitados = None):
		if(vizitados == None):
			vizitados = [False for x in range(self.altura*self.largura)]

		if(cheiro > 0): # Se o cheiro ainda pode ser aplicado
			vizitados[x*self.largura+y] = True
			if(self.campo[x][y]['cheiroBom'] < cheiro):
				self.campo[x][y]['cheiroBom'] = cheiro # aplicando cheiro

			if((x-1 >= 0 and self.campo[x-1][y]['acessivel']) and not (vizitados[(x-1)*self.largura+y])):
				self.aplicarCheiroBom(cheiro-0.5, x-1, y, vizitados) # Va para cima

			if(x+1 < self.altura and self.campo[x+1][y]['acessivel'] and not (vizitados[(x+1)*self.largura+y])):
				self.aplicarCheiroBom(cheiro-0.5, x+1, y, vizitados) # Va para baixo

			if(y-1 >= 0 and self.campo[x][y-1]['acessivel'] and not (vizitados[x*self.largura+(y-1)])):
				self.aplicarCheiroBom(cheiro-0.5, x, y-1, vizitados) # Va para esquerda

			if(y+1 < self.largura and self.campo[x][y+1]['acessivel'] and not (vizitados[x*self.largura+(y+1)])):
				self.aplicarCheiroBom(cheiro-0.5, x, y+1, vizitados) # Va para direita

	def aplicarCheiroRuim(self, cheiro, x, y, vizitados = None):
		if(vizitados == None):
			vizitados = [False for x in range(self.altura*self.largura)]

		if(cheiro > 0): # Se o cheiro ainda pode ser aplicado
			vizitados[x*self.largura+y] = True
			if(self.campo[x][y]['cheiroRuim'] < cheiro):
				self.campo[x][y]['cheiroRuim'] = cheiro # aplicando cheiro

			if((x-1 >= 0 and self.campo[x-1][y]['acessivel']) and not (vizitados[(x-1)*self.largura+y])):
				self.aplicarCheiroRuim(cheiro-0.5, x-1, y, vizitados) # Va para cima

			if(x+1 < self.altura and self.campo[x+1][y]['acessivel'] and not (vizitados[(x+1)*self.largura+y])):
				self.aplicarCheiroRuim(cheiro-0.5, x+1, y, vizitados) # Va para baixo

			if(y-1 >= 0 and self.campo[x][y-1]['acessivel'] and not (vizitados[x*self.largura+(y-1)])):
				self.aplicarCheiroRuim(cheiro-0.5, x, y-1, vizitados) # Va para esquerda

			if(y+1 < self.largura and self.campo[x][y+1]['acessivel'] and not (vizitados[x*self.largura+(y+1)])):
				self.aplicarCheiroRuim(cheiro-0.5, x, y+1, vizitados) # Va para direita

class Player:
	def __init__(self, nome):
		self.nome = nome
		self.snippets = 0
		self.mines = 0

	def set(self, attr_name, value):
		if attr_name == "snippets":
			self.snippets = int(value)
		elif attr_name == "mines":
			self.mines = int(value)

class Bot:
	def __init__(self):
		self.data = {}
		self.field = None
		self.me = None
		self.round = 0
		self.posAnterior = None

	def settings(self, args):
		'''
		args - list(str). Uma lista que contém a configuração a ser setada

		Todos os dados que entram como configuração são salvos em self.data
		'''
		self.data[args[0]] = args[1]
		if args[0] == "your_bot":
			self.players = dict(map( lambda x: (x, Player(x)), self.data["player_names"].split(",") ))
			self.me = self.players[args[1]]
		elif args[0] == "field_height":
			self.field = Campo(int(self.data["field_width"]), int(self.data['field_height']))

	def minhaPosicao(self):
		for i in range(0, self.field.altura):
			for j in range(0, self.field.largura):
				if(self.field.campo[i][j]['acessivel']):
					itens = self.field.campo[i][j]['conteudo'].split(";")
					for item in itens:
						if(item == "P"+self.me.nome[-1]):
							return (i, j)
		return (-1,-1) # Não deu certo

	def update(self, args):
		'''
			args - list(str). O comando na forma de lista
		'''
		if args[0] == "game":
			if args[1] == "field":
				# A engine sinalizou que esta é uma atualizadação do campo de jogo
				self.field.set(args[2])
			else:
				# De acordo com a documentação as unicas atualizações de game possíveis são do campo e do round atual
				self.round = int(args[2])
		else:
			# Etualizando informações sobre um player
			# Selecionando o player dos que já temos salvos e executando a atualização
			self.players[args[0]].set(args[1], args[2])

	def action(self, args):
		'''
			args - list(str). O comando na forma de lista
		'''
		if args[0] == "move": # A Engine solicitou um movimento
			x, y = self.minhaPosicao()
			print ( self.decidirDirecao(self.field.campo, x, y) )
		else: # A engine está solicitando que caractere pretendemos jogar
			print("bixiette") # Selecionando

	def decidirDirecao(self, campo, x, y):
		movimentos = []
		if(x-1 >= 0 and campo[x-1][y]['acessivel']):
			movimentos.append(("up", campo[x-1][y]['cheiroBom']-3*campo[x-1][y]['cheiroRuim']))

		if(x+1 < self.field.altura and campo[x+1][y]['acessivel']):
			movimentos.append(("down", campo[x+1][y]['cheiroBom']-3*campo[x+1][y]['cheiroRuim']))

		if(y-1 >= 0 and campo[x][y-1]['acessivel']):
			movimentos.append(("left", campo[x][y-1]['cheiroBom']-3*campo[x][y-1]['cheiroRuim']))

		if(y+1 < self.field.largura and campo[x][y+1]['acessivel']):
			movimentos.append(("right", campo[x][y+1]['cheiroBom']-3*campo[x][y+1]['cheiroRuim']))

		movimentos = sorted(movimentos, key=lambda x: x[1])
		if(len(movimentos) == 1):
			self.setPosAnterior(movimentos[0][0])
			return movimentos[0][0]

		primeiro = movimentos[-1]
		segundo = movimentos[-2]

		if(primeiro[1] == segundo[1] and primeiro[0] == self.posAnterior): # Não volte pra posição anterior
			primeiro, segundo = segundo, primeiro

		self.setPosAnterior(primeiro[0])

		return primeiro[0]

	def setPosAnterior(self, moveAtual):
		if(moveAtual == 'up'):
			self.posAnterior = 'down'
		if(moveAtual == 'down'):
			self.posAnterior = 'up'
		if(moveAtual == 'left'):
			self.posAnterior = 'right'
		if(moveAtual == 'right'):
			self.posAnterior = 'left'

	def run(self):

		while 1:
			line = input()
			if len(line) == 0:
				continue
			parts = line.split(" ")
			controller = {
				"settings": self.settings,
				"update": self.update,
				"action": self.action
			}
			controller[parts[0]](parts[1:])


if __name__ == "__main__":
	bot = Bot()
	bot.run()
