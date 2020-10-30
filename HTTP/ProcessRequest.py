import os
from Responses import Responses
import NetUtils as NetUtils


class ProcessRequest:
    def __init__(self, serverName):

        #Salva o nome do host do objeto socket.
        self.SERVER_NAME = serverName

        #Cria instância da classe de respostas
        # para uso no método de processamento
        self.response = Responses(self.SERVER_NAME)

        #Extensões suportadas pelo servidor.
        self.extensoes_suportadas = ['html','txt','md','jpeg','png','jpg','gif']

    def process(self, request, body):
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
        
        elif request[2] != "HTTP/1.1":
            self.responseHeader, self.responseBody = self.response.HTTPVersionNotSupported()

        elif request[0]=="GET":
            #Adquire somente o request-uri após o /.
            requested_file = request[1].split('/')[-1]

            #Adquire a extensão do arquivo solicitado
            requested_extension = request[1].split('.')[-1]

            #Se o arquivo desejado na requisição for o root "/"
            #De acordo com a RFC, essa requisição deve carregar a página base.
            if(request[1] == "/"):
                self.responseHeader, self.responseBody = (
                    self.response.OK('home.html',requested_extension))

            #Se o arquivo existir nos diretórios do servidor, entra na condição.
            elif (NetUtils.find_file(requested_file)):

                #Se o arquivo desejado possui sua extensão suportada pelo
                #servidor (isso é, arquivos que o método OK da classe Responses
                #consegue ler e retornar).
                if(requested_extension in self.extensoes_suportadas):
                    self.responseHeader, self.responseBody = (
                        self.response.OK(NetUtils.get_file_path(request[1]), requested_extension))

                #Se não é uma extensão suportada, retorne Not Found.
                else:
                    self.responseHeader, self.responseBody = self.response.NotFound()

            #O arquivo requisitado não existe de fato no servidor.
            else:
                self.responseHeader, self.responseBody = self.response.NotFound()

        elif request[0]=="PUT":
            #Adquire somente o request-uri após o /.
            requested_file = request[1].split('/')[-1]

            #Adquire a extensão do arquivo solicitado
            requested_extension = request[1].split('.')[-1]

            #Verifica se o arquivo foi criado corretamente no diretório,
            #isso é, a requisição foi feita para o diretório correto "userdata"

            if NetUtils.createFile(request[1], body):
                #Se existe o arquivo dado na requisição nos diretórios do servidor
                #E um corpo do arquivo para escrita
                print("Req: ", NetUtils.find_file(requested_file))
                if NetUtils.find_file(requested_file) and body:
                    #Deve-se retornar o código 200 OK para a alteração do arquivo
                    #com um novo conteúdo.
                    self.responseHeader, self.responseBody = (
                        self.response.OK(NetUtils.get_file_path(request[1]),requested_extension)
                    )
                    

                #Caso o arquivo exista nos diretórios do servidor, mas não foi informado
                #um corpo na requisição
                elif NetUtils.find_file(requested_file):

                    #Deve-se retornar o código 204 No Content para a alteração do arquivo
                    #com um conteúdo vazio.
                    self.responseHeader, self.responseBody = self.response.NoContent(requested_extension)
                    
                
                #Caso não exista o arquivo, cria-se um novo.
                else:

                    #Retornando o 201 Created com o conteúdo dado (vazio ou não).
                    self.responseHeader, self.responseBody = self.response.Created(requested_extension)
                    
                    
            #Caso a requisição foi destinada à outro diretório,
            #o arquivo será criado de qualquer forma no diretório "userdata"
            #e a resposta 301 Moved Permanently será exibida com o diretório
            #correto para o arquivo.
            else:
                self.responseHeader, self.responseBody = self.response.MovedPermanently(requested_file)
            NetUtils.refresh_known_files()
        else:
            self.responseHeader, self.responseBody = self.response.BadRequest()
        
        print("ResponseHeader:\n ",self.responseHeader)
        return self.responseHeader, self.responseBody
