import os
import datetime
from itertools import chain
from Responses import Responses


class ProcessRequest:
    def __init__(self, serverName):
        #Modelo de header geral para qualquer resposta do servidor.
        #De acordo com a RFC2616[seção 4.2] - É uma boa prática enviar no
        #header primeiramente o general-header, depois response/request header
        #e por último o entity-header.
        self.responseHeader = ("HTTP/1.1 {} {}\r\n"       #Status-Line
                             "Date: {}\r\n"               #general-header
                             "Connection: keep-alive\r\n" #general-header    
                             "Server: {}\r\n"             #response-header
                             "Content-Type: {}\r\n\r\n")  #entity-header
        
        #Salva o nome do host do objeto socket.
        self.SERVER_NAME = serverName

        #Adquire todos arquivos
        self.serverFiles = [x[2] for x in os.walk(".")]

        #Adquire o nome de todos diretórios
        self.serverFolders = [x[1] for x in os.walk(".")]



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
            print(self.serverFolders[key])            
            if requested_file in self.serverFolders[key]:
                print("O %s É diretório"%requested_file)
                
        return requested_file in chain(*self.serverFiles)


    def response(self, request):
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
        
        
        date_server = ( #Variável responsável por armazenar a data
        datetime.datetime.now(datetime.timezone.utc) #Adquire a data/hora atual
        .strftime("%a, %d %b %Y %H:%M:%S GMT")) #Formata segundo RFC2616[3.3.1]
        
        
        if request[0]=="GET":
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

            if self.find_file(request[1].split('/')[-1]):
                self.responseHeader, self.responseBody = Responses(self.SERVER_NAME).OK()
                
            else:
                self.responseHeader, self.responseBody = Responses(self.SERVER_NAME).NotFound()
            
            
        return self.responseHeader, self.responseBody
