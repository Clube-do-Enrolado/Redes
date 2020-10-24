import datetime


class Responses:
    def __init__(self, serverName):
        self.SERVER_NAME = serverName
        self.response_general_header = ("HTTP/1.1 {} {}\r\n"   #Status-Line
                             "Date: {}\r\n"               #general-header
                             "Connection: keep-alive\r\n" #general-header    
                             "Server: {}\r\n"             #response-header
                             "Content-Type: {}\r\n\r\n")  #entity-header

        self.date_server = ( #Variável responsável por armazenar a data
        datetime.datetime.now(datetime.timezone.utc) #Adquire a data/hora atual
        .strftime("%a, %d %b %Y %H:%M:%S GMT")) #Formata segundo RFC2616[3.3.1]

        self.response_general_body = """
            <!DOCTYPE html>
            <html>
            <head>
            <title>{}</title>
            </head>
            <body>

            <h1>{}</h1>

            <p>{}</p>

            </body>
            </html>
            """
        
    def OK(self):
        return (
        self.response_general_header.format(
            '200',
            'OK',
            self.date_server,
            'Servidor',
            'text/html'
            ),
        self.response_general_body.format(
            "Home", "Bem-vindo ao clube",
            """
            Pagina com o melhor front-end de Sao Paulo
            """
        ))
    def NotFound(self):
        return (
        self.response_general_header.format(
            '404',
            'Not Found',
            self.date_server,
            'Servidor',
            'text/html'
            ),
        self.response_general_body.format(
            "404 Not Found", "404 - Not Found",
            """
            O arquivo requisitado ao servidor nao existe :(
            """
        ))
       
