import socket as socket
import os
from ProcessRequest import ProcessRequest

#x[i]: descrição
#x[0]: são os URI dos diretórios (\\pasta\subpasta\..)
#x[1]: são os nomes (pasta, outrapasta)
#x[2]: Todos arquivos alcançaveis a partir do diretório informado.
#print([x[2] for x in os.walk(".")])

class HTTPServer():
    def __init__(self):
        self.PORTA = 8080
        self.HOST = "127.0.0.1"
        self.main()

    def process_connection(self, sokt):
        """
        Processa conexões feitas pelo cliente, permitindo a correta obtenção
        e tratamento das requisições. Método que encaminha e recebe informações
        de classes auxiliares.

        Parameters:
        sokt (socket.socket): Objeto Socket gerado após especificar o
        endereço da familia (e.g. AF_INET,AF_INET6, AF_UNIX) e
        o tipo do socket (e.g. SOCK_DGRAM, SOCK_STREAM, SOCK_RAW).

        Returns:
        None
        """

        #Adquire o socket de conexão e o endereço de quem conectou ao servidor.
        conec, endr = sokt.accept()
        print("--> Conectado com o endereço: {}".format(endr))

        #Recebe a requisição do cliente em bits e transforma-a com o decode()
        #para string.
        request = conec.recv(2048).decode()
        print(request)

        #Divide e transforma a string de requisição em um vetor sempre que
        #encontrar espaços entre as palavras.
        splitted_request = request.split()
        
        #Instância da classe responsável por processar as requisições.
        pr = ProcessRequest()

        #Adquire as respostas do método response.
        responseHeader, responseBody = pr.response(splitted_request)

        #Envia o Header da resposta
        conec.sendall(bytes(responseHeader.encode("UTF-8")))

        #Verifica se o corpo da mensagem não é nulo
        if responseBody is not None:
            #E então o envia
            conec.sendall(bytes(responseBody.encode("UTF-8")))
    
    def main(self):
        """
        Método inicial do servidor. Responsável por criar o socket.

        Parameters:
        None

        Returns:
        None
        """
        #Define a família de endereços com a qual o socket irá se comunicar.
        #       endereços Internet Protocol v4 (IPV4) 
        #                            |     Protocolo baseado à conexão (TCP)
        #                            |              |
        #                            V              V
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sokt:
            #Conecta o socket com o HOST e PORTA especificados.
            sokt.bind((self.HOST, self.PORTA))
            print("--> Servidor Executando na porta %s"%(self.PORTA))
            while True:
                #Aceita 1 conexão de requests antes de recusar outras requests.
                sokt.listen(1)
                self.process_connection(sokt)

HTTPServer()