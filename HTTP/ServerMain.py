import socket as socket
from ProcessRequest import ProcessRequest

class HTTPServer():
    def __init__(self):
        self.PORTA = 8080
        self.HOST = "127.0.0.1"
        self.SERVER_NAME = socket.gethostname()
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
        request = conec.recv(4096).decode()
        
        print("DEBUG:",request)

        #Verifica se existe um corpo para receber na mensagem
        #(Geralmente em método PUT)
        if request.find('Content-Length') > -1:
            body = bytes("".encode("UTF-8"))
            body_splitted = request.split()
            index_length = body_splitted.index("Content-Length:")+1
            body_length = int(body_splitted[index_length])

            while body_length > 0:
                body += conec.recv(2048)
                body_length -= 2048


        #Divide e transforma a string de requisição em um vetor sempre que
        #encontrar espaços entre as palavras.
        splitted_request = request.split()
        
        #Instância da classe responsável por processar as requisições.
        pr = ProcessRequest(self.SERVER_NAME)

        #Adquire as respostas do método response.
        responseHeader, responseBody = pr.process(splitted_request, body)

        #Envia o Header da resposta
        conec.sendall(bytes(responseHeader.encode("UTF-8")))

        #Verifica se o corpo da mensagem não é nulo
        if responseBody is not None:
            #E então o envia
            conec.sendall(responseBody)
        
    
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
