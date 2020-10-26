import os
from itertools import chain
from Responses import Responses


class ProcessRequest:
    def __init__(self, serverName):

        #Salva o nome do host do objeto socket.
        self.SERVER_NAME = serverName

        #Adquire todos arquivos
        self.serverFiles = [x[2] for x in os.walk(".")]

        #Adquire o nome de todos diretórios
        self.serverFolders = [x[1] for x in os.walk(".")]

        #Cria instância da classe de respostas
        # para uso no método de processamento
        self.response = Responses(self.SERVER_NAME)

        self.extensoes_suportadas = ['html','ico']

    def find_file(self, requested_file):
        """
        Verifica a existência do arquivo requisitado a partir do root do server.
        
        Parameters:
        requested_file (string): Nome do arquivo desejado para a pesquisa.

        Returns:
        (bool): True (caso arquivo encontrado) ou False (caso não encontre).
        """

        #Simples for para verificação se o requested_file é diretório ou não
        #ainda resta implementação para o directory-listing.
        for key in range(len(self.serverFolders)):
            #print(self.serverFolders[key])            
            if requested_file in self.serverFolders[key]:
                print("O %s É diretório"%requested_file)
                
        return requested_file in chain(*self.serverFiles)


    def process(self, request):
        """
        Cria a resposta apropriada para uma dada requisição.

        Parameters:
        request (list): Requisição feita pelo cliente ao servidor, uma lista
        contendo todos os dados indexados. Dados relevantes são:
        request[0] -> método da requisição (e.g GET, POST, PUT).
        request[1] -> request-URI.
        request[2] -> HTTP-Version.

        Returns:
        (string,string): A resposta do servidor para uma dada requisição.
                         Sendo o primeiro o Header e o segundo o Body.
        
        """     
        if not request:
            self.responseHeader, self.responseBody = self.response.BadRequest()

        elif request[0]=="GET":
            #Adquire somente o request-uri após o /.
            requested_file = request[1].split('/')[-1]
            '''
            A partir do os.walk, é possível verificar se o arquivo procurado pelo usuário
            na request é válido, não sendo necessário o if \\/
            if request[1]=="/":
            
            Envolvendo tudo em um try/catch, se o arquivo existir, continua com a operação.
            Caso contrário retorna 404.

            Caso encontre o log, porém o arquivo está em uma pasta diferente, 
            o retorno do walk será [[index.html.log],[index.html]]
            o que mostra que o index.html mudou de diretório.
            O que retorna 301 - Moved permanently.
            '''
            print("DEBUG: ",request[1])
            print("DEBUG: ",request[1].replace('/','\\'))
            print("DEBUG: ",os.getcwd()+request[1].replace('/','\\'))
            print("DEBUG: ",os.getcwd())
            #Se o arquivo desejado na requisição for o root "/"
            #De acordo com a RFC, essa requisição deve carregar a página base.
            if(request[1] == "/"):
                self.responseHeader, self.responseBody = self.response.OK('home.html')

            #Se o arquivo existir nos diretórios do servidor, entra na condição.
            elif (self.find_file(requested_file)):

                #Se o arquivo desejado possui sua extensão suportada pelo
                #servidor (isso é, arquivos que o método OK da classe Responses
                #consegue ler e retornar).
                if(requested_file.split('.')[-1] in self.extensoes_suportadas):
                    self.responseHeader, self.responseBody = self.response.OK(os.getcwd()+request[1].replace('/','\\'))

                #Se não é uma extensão suportada, retorne Not Found.
                else:
                    self.responseHeader, self.responseBody = self.response.NotFound()

            else:
                self.responseHeader, self.responseBody = self.response.NotFound()
        
        print(self.responseHeader, self.responseBody)
        return self.responseHeader, self.responseBody
