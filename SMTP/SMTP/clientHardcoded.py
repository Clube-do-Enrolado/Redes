# ==============================CABEÇALHO=================================
# |                                                                      |
# | AUTORES: Andy Barbosa                                                |
# |          Rafael Palierini                                            |
# |          Rubens Mendes                                               |
# |          Vitor Acosta                                                |
# |                                                                      |
# | DISCPLINA Tóp. Avançados de Redes de Computadores                    |
# | TEMA: Protocolo SMTP                                                 |                  
# | TIPO: Cliente SMTP que se comunica sem nenhum protocolo de segurança |
# |       hardcoded.                                                     |
# |                                                                      |
# | ÚLTIMA MODIFICAÇÃO: 14/10/2020 04:24                                 |
# |                                                                      |
# ========================================================================

# =======================================================================
# |                                                                     |
# |                      BIIBLIOTECAS IMPORTADAS                        |
# |                                                                     |
# =======================================================================

import smtplib # Biblioteca do Cliente
import email.utils# Permite funcionalidades de utilidade para formatação/geração.
from email.mime.text import MIMEText # Classe de Texto.
from email.mime.multipart import MIMEMultipart # Classe de multiplas partes (Permite anexar arquivos).
from email.mime.image import MIMEImage # Classe de imagens.
from email.mime.base import MIMEBase # Base do MIME.
import time # Tempo do sistema operacional.

# =======================================================================
# |                                                                     |
# |                        CABEÇALHO DA MENSAGEM                        |
# |                                                                     |
# =======================================================================

#Cria uma mensagem que contêm multiplas partes do MIME anexadas.
#
#     |
#     V
msg = MIMEMultipart()

# Define o remetente na tupla ({nome}, {e-mail})
#
#             |
#             V                        {nome}          {e-mail}
msg["From"] = email.utils.formataddr(("Obiwan", "obiwan@jaku.com"))

#Define os destinatários na tupla ({nomes}, {e-mails})
#
#           |
#           V                              {nomes}                                   {e-mails}
msg["To"] = email.utils.formataddr(("Vader, Luke, Paimon", "vader@deathstar.com, luke@jaku.com, paimon@genshinimpact.com"))

# Define a data e hora de envio da mensagem através do tempo do sistema.
#
#             |
#             V
msg["Date"] = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

# Define o assunto do e-mail
#
#                 |
#                 V
msg["Subject"] = "You were my brother Anakin!"

# =======================================================================
# |                                                                     |
# |                              MENSAGEM                               |
# |                                                                     |
# =======================================================================

# msg.preamble é responsável por salvar a mensagem do e-mail.

msg.preamble = "This is my preamble, hope this works now.\nLet's see if it works with multiple lines correctly.\n"

# =======================================================================
# |                                                                     |
# |                              ARQUIVOS                               |
# |                                                                     |
# =======================================================================

# Aqui você poderá decidir os arquivos que deseja anexar.
#
# Só é possível anexar um arquivo de cada tipo. Caso deseje enviar mais
# de um arquivo do mesmo tipo, será necessário enviar duas mensagens.
#
# Algumas linhas de código estão comentadas pois não está sendo feito o
# envio de alguma arquivo daquele formato. Para utilizar, basta remover o
# comentário e informar qual o nome do arquivo que deseja enviar.
# 
# Para evitar problemas, por favor, coloque o arquivo na mesma pasta que
# o cliente está rodando.

textFilename = "texto.txt"
jpegFilename = "neymar.jpeg"
#jpgFilename = ""
#pngFilename = ""
gifFilename = "xandao.gif"

text = MIMEText(open(textFilename).read())
text.add_header('Content-Disposition', 'attachment', filename=textFilename)

jpeg = MIMEImage(open(jpegFilename, 'rb').read())
jpeg.add_header('Content-Disposition', 'attachment', filename=jpegFilename)

#jpg = MIMEImage(open(jpgFilename, 'rb').read())
#jpg.add_header('Content-Disposition', 'attachment', filename=jpgFilename)

#png = MIMEImage(open(pngFilename, 'rb').read())
#png.add_header('Content-Disposition', 'attachment', filename=pngFilename)

gif = MIMEImage(open(gifFilename, 'rb').read())
gif.add_header('Content-Disposition', 'attachment', filename=gifFilename)

# =======================================================================
# |                                                                     |
# |                               ANEXOS                                |
# |                                                                     |
# =======================================================================

# Aqui é onde de fato é realizado o anexo, para anexar o arquivo desejado
# acima, por favor, remova o comentário do arquivo correto.

msg.attach(text)
msg.attach(jpeg)
#msg.attach(jpg)
#msg.attach(png)
msg.attach(gif)

# =======================================================================
# |                                                                     |
# |                               CONEXÃO                               |
# |                                                                     |
# =======================================================================

# Define qual o servidor o cliente deve se conectar através do IP e da
# Porta do servidor.
#
#        |
#        V               {IP}     {Porta}
server = smtplib.SMTP("127.0.0.1", 1025)

# Caso deseje ver um debug do processo da mensagem, deixe em True, caso
# queira desativar, troque por False
#
#      |
#      V             {Bool}
server.set_debuglevel(True)

# =======================================================================
# |                                                                     |
# |                               ENVIO                                 |
# |                                                                     |
# =======================================================================

# Aqui é realizado o envio da mensagem ao servidor através do método: 
# sendmail({remetente}, {destinatários}, {mensagem}).
# 
#      |                                                  {Destinatários}
#      V           {Remetente}     [     {Destinatário}  ,  {Destinatário},       {Destinatário}   ...]     {Mensagem}
server.sendmail("obiwan@jaku.com", ["vader@deathstar.com", "luke@jaku.com", "paimon@genshinimpact.com"], msg.as_string())

# =======================================================================
# |                                                                     |
# |                             ENCERRANDO                              |
# |                                                                     |
# =======================================================================

# Aqui é encerrado a conexão com o servidor.
#
#      |
#      V
server.quit()
