# Inteligencia artificial, Python, para o jogo MS. HACK-MAN (https://booking.riddles.io/competitions/ms.-hack-man)
# Matheus Alves de Andrade

# Versão 0.0.1
# Desenvolvimento iniciado em 20/08/2018
# Versão finalizada em 20/08/2018

class Campo:
    '''
    	Esta classe abstrai o campo de jogo
    '''

    def __init__(self, largura, altura):
        self.campo = None
        self.inicializado = False
        self.largura = largura
        self.altura = altura

    def set(self, listaCelulas):
        '''
            Este método atualiza o estado do campo
        '''
        if self.inicializado:
            pass
        else:
            self.inicializado = True
            self.campo = self.formatarCampo(listaCelulas)

    def formatarCampo(self, bruto):
    	processado = []
    	splitted = bruto.split(',')

    	for i in range(0, self.altura):
    		processado.append([])
    		for j in range(0, self.largura):
    			processado[i].append( splitted[ (i+1)*j ] )

    	return processado


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
            self.field = Campo(int(self.data["field_width"]),
                               int(self.data['field_height']))

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
            print("up")  # TODO
        else: # A engine está solicitando que caractere pretendemos jogar
            print("bixiette") # Selecionando

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
