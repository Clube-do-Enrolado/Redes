import datetime
import NetUtils as NetUtils


class Responses:
    """
        Classe que constrói as respostas do servidor
        para o cliente.

        Methods:
        OK: Formata a resposta para 200 OK.
        Created: Formata a resposta para 201 Created.
        NoContent: Formata a resposta para 204 No Content.
        BadRequest: Formata a resposta para 400 Bad Request.
        NotFound: Formata a resposta para 404 not Found.
        HTTPVersionNotSupported: Formata a resposta para 505 HTTP Version Not Supported.
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
                             "Content-Type: {}\r\n"          #entity-header
                             "Content-Length: {}\r\n")       #entity-header         

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

        self.imageExtensions = ['jpeg','jpg','png','gif']


    #+---------------------------------------------------------+
    #|              Successful 2xx Messages Methods            |
    #+---------------------------------------------------------+


    def OK(self, filepath, ext):
        """
        Constrói a mensagem para um arquivo encontrado no servidor.
        Esse método, diferentemente das outras respostas, envia um
        arquivo que realmente existe no servidor.

        Parameters:
        filepath (string): Caminho do arquivo que existe no diretório.
        ext (string): Extensão do arquivo procurado.

        Returns:
        (string, string): Header e corpo da resposta.
        """
        content, size = NetUtils.open_file(filepath)

        if content is not None:
            return (
                self.response_general_header.format(
                    '200',
                    'OK',
                    self.DATE_SERVER,
                    self.SERVER_NAME,
                    '{}/{}'.format('image',ext) if ext in self.imageExtensions else 'text/html',
                    size
                    )+"\r\n",
                content
            )
        else:
            return self.NotFound()
    
    def Created(self, ext):
        """
        Constrói a mensagem informando ao cliente que o arquivo
        foi criado com sucesso.

        Parameters:
        ext (string): Extensão do arquivo criado.

        Returns:
        (string, string): Header e corpo da resposta.
        """
        content = bytes(self.response_general_body.format(
                "201 Created", "201 - Created",
                "O arquivo foi criado no servidor com sucesso :)"
                ).encode("UTF-8"))
        return (
            self.response_general_header.format(
                '201',
                'Created',
                self.DATE_SERVER,
                self.SERVER_NAME,
                '{}/{}'.format('image',ext) if ext in self.imageExtensions else 'text/html',
                len(content)
                )+"\r\n",
            content
            )
    
    def NoContent(self, ext):
        """
        Mensagem caso o arquivo seja criado, porém sem nenhum conteúdo.

        Parameters:
        ext (string): Extensão do arquivo criado.

        Returns:
        (string, string): Header e corpo da resposta.
        """        
        content = bytes("".encode("UTF-8"))
        return (
            self.response_general_header.format(
                '204',
                'No Content',
                self.DATE_SERVER,
                self.SERVER_NAME,
                '{}/{}'.format('image',ext) if ext in self.imageExtensions else 'text/html',
                len(content)
                )+"\r\n",
            content
        )

    def MovedPermanently(self, file):
        """
        Constrói a mensagem para um arquivo não encontrado

        Returns:
        (string, string): Header e corpo da resposta.
        """
        content =  ("127.0.0.1:8080/userdata/{}\r\n".format(file)
                .encode("UTF-8"))
        return (
            self.response_general_header.format(
                '301',
                'Moved Permanently',
                self.DATE_SERVER,
                self.SERVER_NAME,
                'text/html',
                len(content)
                )+"Location: 127.0.0.1:8080/userdata/{}\r\n".format(file),
            content
           )


    #+---------------------------------------------------------+
    #|            Client Error 4xx Messages Methods            |
    #+---------------------------------------------------------+

    def NotFound(self):
        """
        Constrói a mensagem para um arquivo não encontrado

        Returns:
        (string, string): Header e corpo da resposta.
        """
        content =  bytes(self.response_general_body.format(
                "404 Not Found", "404 - Not Found",
                "O arquivo requisitado ao servidor nao existe :("
                ).encode("UTF-8"))
        return (
            self.response_general_header.format(
                '404',
                'Not Found',
                self.DATE_SERVER,
                self.SERVER_NAME,
                'text/html',
                len(content)
                )+"\r\n",
            content
           )

    def BadRequest(self):
        """
        Constrói a mensagem para uma requisição feita incorretamente.

        Returns:
        (string, string): Header e corpo da resposta.
        """
        content = bytes(self.response_general_body.format(
                "400 Bad Request", "400 - Bad Request",
                "A requisicao enviada nao pode ser atendida pelo servidor."
                ).encode("UTF-8"))
        return (
            self.response_general_header.format(
                '400',
                'Bad Request',
                self.DATE_SERVER,
                self.SERVER_NAME,
                'text/html',
                len(content)
                )+"\r\n",
            content
            )




    #+---------------------------------------------------------+
    #|            Server Errors 5xx Messages Methods           |
    #+---------------------------------------------------------+
    def HTTPVersionNotSupported(self):
        """
        Constrói a mensagem para erro de versão do HTTP.

        Returns:
        (string, string): Header e corpo da resposta.
        """
        content = bytes(self.response_general_body.format(
                "505 HTTP Version Not Supported", "505 HTTP - Version Not Supported",
                "A versão especificada no método não é compatível com o servidor."
                ).encode("UTF-8"))
        return (
            self.response_general_header.format(
                '505',
                'HTTP Version Not Supported',
                self.DATE_SERVER,
                self.SERVER_NAME,
                'text/html',
                len(content)
                )+"\r\n",
            content
            )
