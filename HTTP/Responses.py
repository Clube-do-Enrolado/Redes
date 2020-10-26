import datetime


class Responses:
    """
        Classe que constrói as respostas do servidor
        para o cliente.

        Methods:
        open_file: Método de utilidade para algumas respostas.
        OK: Formata a resposta para 200 OK, juntamente com o corpo.
        NotFound: Formata a resposta para 404 not Found, juntamente com o corpo.
    """

    def __init__(self, serverName):
        """
        Método de inicialização da classe, contém as principais
        variáveis e esquemas utilizados.

        Parameters:
        serverName (string): Nome da máquina servidor.

        Returns:
        None
        """

        self.SERVER_NAME = serverName

        #Modelo de header geral para qualquer resposta do servidor.
        #De acordo com a RFC2616[seção 4.2] - É uma boa prática enviar no
        #header primeiramente o general-header, depois response/request header
        #e por último o entity-header.
        self.response_general_header = ("HTTP/1.1 {} {}\r\n" #Status-Line
                             "Date: {}\r\n"                  #general-header
                             "Connection: keep-alive\r\n"    #general-header    
                             "Server: {}\r\n"                #response-header
                             "Content-Type: {}\r\n\r\n")         #entity-header

        self.DATE_SERVER = ( #Variável responsável por armazenar a data
        datetime.datetime.now(datetime.timezone.utc) #Adquire a data/hora atual
        .strftime("%a, %d %b %Y %H:%M:%S GMT")) #Formata segundo RFC2616[3.3.1]

        #Corpo de uma resposta (mais utilizado em erros)
        self.response_general_body = ("<!DOCTYPE html>\n"
            "<html>\n"
            "\t<head>\n"
            "\t\t<title>{}</title>\n"
            "\t</head>\n"
            "\t<body>\n"
            "\t\t<h1>{}</h1>\n"
            "\t\t<p>{}</p>\n"
            "\t</body>\n"
            "</html>\n")

    def open_file(self, filepath):
        """
        Método que lê um arquivo para construção da resposta.
        Antes de invocar o método, é certo que esse arquivo
        existe.

        Parameters:
        filepath (string): Diretório do arquivo desejado para abertura.

        Returns:
        (binary): Conteúdo do arquivo em binário.
        """
        try:
            with open(filepath,'rb') as archive:
                content = archive.read()
                archive.close()
            return content
        except:
            return self.NotFound()

    def OK(self, filepath):
        """
        Constrói a mensagem para um arquivo encontrado.

        Parameters:
        filepath (string): Caminho do arquivo que existe no diretório.

        Returns:
        (string, string): Header e corpo da resposta.
        """
        return (
            self.response_general_header.format(
                '200',
                'OK',
                self.DATE_SERVER,
                self.SERVER_NAME,
                'text/html'
                ),
            self.open_file(filepath)
        )

    def NotFound(self):
        """
        Constrói a mensagem para um arquivo não encontrado

        Returns:
        (string, string): Header e corpo da resposta.
        """
        return (
            self.response_general_header.format(
                '404',
                'Not Found',
                self.DATE_SERVER,
                self.SERVER_NAME,
                'text/html'
                ),
            bytes(self.response_general_body.format(
                "404 Not Found", "404 - Not Found",
                "O arquivo requisitado ao servidor nao existe :("
            ).encode("UTF-8")))

    def BadRequest(self):
        """
        Constrói a mensagem para um arquivo não encontrado

        Returns:
        (string, string): Header e corpo da resposta.
        """
        return (
            self.response_general_header.format(
                '400',
                'Bad Request',
                self.DATE_SERVER,
                self.SERVER_NAME,
                'text/html'
                ),
            bytes(self.response_general_body.format(
                "400 Bad Request", "400 - Bad Request",
                "A requisição enviada nao pode ser atendida pelo servidor."
            ).encode("UTF-8")))