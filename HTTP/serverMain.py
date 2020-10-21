import socket as socket
import os


class HTTPServer():
    def __init__(self):
        self.PORTA = 8080
        self.HOST = "127.0.0.1"
        self.main()

    def serverProcess(self, sokt):
        #Adquire o socket de conexão e o endereço de quem conectou-se ao servidor.
        conec, endr = sokt.accept()
        print("--> Conectado com o endereço: {}".format(endr))

        #Recebe a requisição do cliente em bits e transforma-a com o decode() para string.
        request = conec.recv(1024).decode()
        split_request = request.split()
        if split_request[0] == "GET":
            print("-->GET {}".format(split_request[1]))
        else:
            conec.sendall('ok'.encode())
    
    def main(self):
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
                self.serverProcess(sokt)

HTTPServer()

