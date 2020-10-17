# ==============================CABEÇALHO=================================
# |                                                                      |
# | AUTORES: Andy Barbosa                                                |
# |          Rafael Palierini                                            |
# |          Rubens Mendes                                               |
# |          Vitor Acosta                                                |
# |                                                                      |
# | DISCPLINA Tóp. Avançados de Redes de Computadores                    |
# | TEMA: Protocolo SMTP                                                 |                  
# | TIPO: Servidor SMTP smtp.jaku.com                                    |
# |                                                                      |
# | ÚLTIMA MODIFICAÇÃO: 14/10/2020 04:41                                 |
# |                                                                      |
# ========================================================================

# =======================================================================
# |                                                                     |
# |                      BIIBLIOTECAS IMPORTADAS                        |
# |                                                                     |
# =======================================================================

import smtpd # Biblioteca do Servidor SMTP.
import smtplib # Biblioteca do Cliente SMTP.
import asyncore # Biblioteca que permite um serviço de socket assíncrono.
import base64 # Biblioteca que permite o uso de decode para base 64.

# =======================================================================
# |                                                                     |
# |                       CLASSE SMTP CUSTOMIZADA                       |
# |                                                                     |
# =======================================================================

# Classe personalizada do servidor SMTP
#
# Está classe é responsável por estruturar e definir como o servidor se
# comporta ao receber uma mensagem.
class CustomSMTPServer(smtpd.SMTPServer):

    # =======================================================================
    # |                                                                     |
    # |                     FUNÇÃO PARA SALVAR ARQUIVOS                     |
    # |                                                                     |
    # =======================================================================

    def writeInServer(self, fileType):
        # Essa função recebe um parâmetro fileType (Tipo String). É verifica-
        # do qual o tipo do arquivo anexado. Após a vereficação é feito um
        # tratamento para cada arquivo ser salvo da maneira correta.
        #
        # =======================================================================
        # |                                                                     |
        # |                               IMAGEM                                |
        # |                                                                     |
        # =======================================================================
        #
        #           |
        #           V
        #
        #                 {Tipo}
        if fileType.find("image") > -1:

            #           |
            #           V
            # {fileType}   {Tipo do arquivo}
            if fileType == "image jpg":
                # ImageIndex é a variavel que salva o índice do tipo da imagem 
                # encontrado no corpo da mensagem no cabeçalho do anexo, garan-
                # tindo assim a leitura de todos os dados corretamente.
                imageIndex = self.emailData.index("Content-Type: image/jpeg") + 4

            #           |
            #           V
            # {fileType}   {Tipo do arquivo}
            if fileType == "image jpeg":
                imageIndex = self.emailData.index("Content-Type: image/jpeg") + 4

            #           |
            #           V
            # {fileType}   {Tipo do arquivo}
            if fileType == "image png":
                imageIndex = self.emailData.index("Content-Type: image/png") + 4

            #           |
            #           V
            # {fileType}   {Tipo do arquivo}
            if fileType == "image gif":
                imageIndex = self.emailData.index("Content-Type: image/gif") + 4

            # Abre um arquivo com o nome e a extensão do arquivo encontrado e o 
            # escreve em binário.
            file = open(self.foundFileName, "wb")

            # Essa variável salvará todo o código da imagem do corpo da mensagem.
            imageCode = ""

            # Esse laço percorre todo o código da imagem para salvar o código que
            # deverá ser decodificado para então ser escrito no arquivo. Dessa 
            # forma será possível reescrever a imagem e visualizar a mesma de ma-
            # neira correta.
            for j in range(len(self.emailData)):
                if j >= imageIndex:
                    if self.emailData[j] == self.delimitador:
                        break
                    imageCode += (self.emailData[j]) + "\n"

            # Escreve a imagem no arquivo decodificada da base64 em binário. 
            file.write(base64.b64decode(imageCode))

            # Fecha o arquivo para salvar o que foi escrito.
            file.close()
        
        # =======================================================================
        # |                                                                     |
        # |                                TEXTO                                |
        # |                                                                     |
        # =======================================================================
        #
        #           |
        #           V
        #
        # {fileType}   {Tipo do arquivo}
        if fileType == "text base64":
            # textArchiveIndex é a variável que salva o índice do tipo do texto 
            # encontrado no corpo da mensagem no cabeçalho do anexo, garantindo 
            # assim a leitura de todos os dados corretamente.
            textArchiveIndex = self.emailData.index('Content-Type: text/plain; charset="utf-8"') + 4

            # Abre um arquivo com o nome e a extensão do arquivo encontrado e o 
            # escreve em binário.
            file = open(self.foundFileName, "wb")

            # Essa variável salvará todo o código do texto do corpo da mensagem.
            textData = ""

            # Esse laço percorre todo o código da texto para salvar o código que
            # deverá ser decodificado para então ser escrito no arquivo. Dessa 
            # forma será possível reescrever a texto e visualizar a mesma de ma-
            # neira correta.
            for j in range(len(self.emailData)):
                if j >= textArchiveIndex:
                    if self.emailData[j] == self.delimitador:
                        break
                    textData += (self.emailData[j]) + '\n'

            # Escreve o texto no arquivo decodificada da base64 em binário.
            file.write(base64.b64decode(textData))
            # Fecha o arquivo para salvar o que foi escrito.
            file.close()
        #
        #           |
        #           V
        #
        # {fileType}   {Tipo do arquivo}
        if fileType == "text us-ascii":
            # textArchiveIndex é a variável que salva o índice do tipo do texto 
            # encontrado no corpo da mensagem no cabeçalho do anexo, garantindo 
            # assim a leitura de todos os dados corretamente.
            textArchiveIndex = self.emailData.index('Content-Type: text/plain; charset="us-ascii"') + 5

            # Abre um arquivo com o nome e a extensão do arquivo encontrado em
            # formato de escrita.
            file = open(self.foundFileName, "w")

            # Essa variável salvará todo o código do texto do corpo da mensagem.
            textData = ''

            # Esse laço percorre todo o código da texto para salvar o código que
            # deverá ser decodificado para então ser escrito no arquivo. Dessa 
            # forma será possível reescrever a texto e visualizar a mesma de ma-
            # neira correta.
            for j in range(len(self.emailData)):
                if j >= textArchiveIndex:
                    if self.emailData[j] == self.delimitador:
                        break
                    textData += (self.emailData[j]) + '\n'

            # Escreve o texto no arquivo.
            file.write(textData)

            # Fecha o arquivo para salvar o que foi escrito.
            file.close()

        return

    # =======================================================================
    # |                                                                     |
    # |                  FUNÇÃO PARA PROCESSAR A MENSAGEM                   |
    # |                                                                     |
    # =======================================================================

    # Função process_message que está sendo sobrescrita
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        # Separa a mensagem pelo \n em uma lista para poder trabalhar melhor 
        # com a mesma.
        self.emailData = data.decode().split("\n")

        # Separador para ficar melhor a legibilidade no terminal.
        print("\n============================================================================\n")

        
        # Explicação do self.delimitador:
        #   O delimitador é uma variável importante que mostra onde começa os
        #   dados de um anexo e onde eles terminam. Esse valor previne o sal-
        #   vamento de dados em arquivos errados quando mais de um anexo é 
        #   enviado. Sem ele, um arquivo de texto poderia ter dados de um ar-
        #   quivo de imagem, ou vice-e-versa.
        #   Esse delimitador é o primeiro dado encontrado no corpo da mensa-
        #   gem (utilizando o self.emailData). Logo é possível acessá-lo a-
        #   través de self.emailData[0], o que retorna toda a linha de cabe-
        #   çalho.
        #   Ao utilizar o split(';')[-1] alcança-se a variavel "boundary", 
        #   que nos mostra o delimitador.
        #   Por fim, utiliza-se um segundo split('"')[1], o que nos retorna o
        #   código que delimita cada anexo.
        #
        self.delimitador = '--'+self.emailData[0].split(';')[-1].split('"')[1]

        # Aqui é percorrido todos os destinatários um a um, para enviar o a
        # mensagem para o servidor correto.
        for i in rcpttos:

            # Aqui é verificado se o destinatário é pertencente ao domínio
            # jaku.com para salvar a mensagem no servidor.
            if(i.find("@jaku.com") > -1):
                
                # Verifica se existe arquivos anexados, se existir algum ane-
                # xo, será feito um tratamento na mensagem para adquirir o
                # nome original do arquivo com a extensão e então será chama-
                # da a função writeInServer() de maneira apropriada para tra-
                # tar e reescrever o arquivo da maneira correta.
                if (data.decode().find("Content-Type: image/jpeg") > -1):
                    attachmentInfo = self.emailData.index("Content-Type: image/jpeg") + 3
                    self.foundFileName = self.emailData[attachmentInfo].split("=")[-1].replace('"',"")
                    self.writeInServer("image jpeg")

                if (data.decode().find("Content-Type: image/jpg") > -1):
                    attachmentInfo = self.emailData.index("Content-Type: image/jpg") + 3
                    self.foundFileName = self.emailData[attachmentInfo].split("=")[-1].replace('"',"")
                    self.writeInServer("image jpg")

                if(data.decode().find("Content-Type: image/png") > -1):
                    attachmentInfo = self.emailData.index("Content-Type: image/png") + 3
                    self.foundFileName = self.emailData[attachmentInfo].split("=")[-1].replace('"',"")
                    self.writeInServer("image png")

                if(data.decode().find("Content-Type: image/gif") > -1):
                    attachmentInfo = self.emailData.index("Content-Type: image/gif") + 3
                    self.foundFileName = self.emailData[attachmentInfo].split("=")[-1].replace('"',"")
                    self.writeInServer("image gif")
                
                if (data.decode().find('Content-Type: text/plain; charset="utf-8"') > -1):
                    attachmentInfo = self.emailData.index('Content-Type: text/plain; charset="utf-8"') + 3
                    self.foundFileName = self.emailData[attachmentInfo].split("=")[-1].replace('"',"")
                    self.writeInServer("text base64")

                if (data.decode().find('Content-Type: text/plain; charset="us-ascii"') > -1):
                    attachmentInfo = self.emailData.index('Content-Type: text/plain; charset="us-ascii"') + 3
                    self.foundFileName = self.emailData[attachmentInfo].split("=")[-1].replace('"',"")
                    self.writeInServer("text us-ascii")

                # Caso não exista um anexo na mensagem.
                else:
                    pass

                # Abre o arquivo de mensagem do servidor (ou cria um caso não
                # tenha) e se prepara para adicionar uma nova mensagem.
                serverMessage = open("ServerMSG.txt", "a")
                serverMessage.write("\n\n\n=========================================================================================\n\n\n")

                # Imprime e salva no arquivo de mensagens recebidas do servi-
                # dor o IP de quem enviou a mensagem.
                print("\nMensagem enviada pelo IP {}" .format(peer))
                serverMessage.write("\nMensagem enviada pelo IP {}\n" .format(peer))

                # Imprime e salva no arquivo de mensagens recebidas do servi-
                # dor o e-mail de quem enviou a mensagem.
                print("Mensagem enviada pelo e-mail {}" .format(mailfrom))
                serverMessage.write("Mensagem enviada pelo e-mail {}\n" .format(mailfrom))

                # Imprime e salva no arquivo de mensagens recebidas do servi-
                # dor a mensagem do destinatário.
                print("Mensagem destinada ao e-mail {}" .format(i))
                serverMessage.write("Mensagem destinada ao e-mail {}\n" .format(i))

                # Imprime e salva no arquivo de mensagens recebidas do servi-
                # dor o tamanho da mensagem.
                print("Tamanho da mensagem: {}\n" .format(len(data)))
                serverMessage.write("Tamanho da mensagem: {}\n" .format(len(data)))

                # Imprime e salva no arquivo de mensagens recebidas do servi-
                # dor a mensagem completa.
                print("\nMensagem:\n")
                print(data.decode())
                serverMessage.write("\nMensagem:\n\n")
                serverMessage.write(data.decode())

                # Fecha o separador da mensagem.
                serverMessage.write("\n\n\n=========================================================================================\n\n\n")

                # Fecha o arquivo para salvar o que foi escrito.
                serverMessage.close()

            # Se o domínio do destinatario for @deathstar.com, o servidor de-
            # verá encaminhar o e-mail para outro endereço.
            elif(i.find("@deathstar.com") > -1):

                # Tenta se conectar ao servidor deathstar.com
                try:
                    # Anúncia que está se conectando ao deathstar.com para o
                    # servidor.
                    print("Contatando domínio deathstar.com")

                    # Cria a conexão com o servidor do respectivo domínio.
                    #         |
                    #         V              {IP}    {Porta}
                    server = smtplib.SMTP("127.0.0.1", 1030)

                    # Encaminha o e-mail para o servidor.
                    server.sendmail(mailfrom, i, data)

                    # Fecha o contato com o servidor.
                    server.quit()

                # Trata a exceção caso não seja possível se conectar.
                except:
                    print("Não foi possível se conectar ao deathstar.com")

            # Se o domínio do destinatario não for reconhecido pelo servidor,
            # o servidor irá dizer que não encontrou o domínio, consequente-
            # mente, não enviará a mensagem.
            else:
                continue

        print("\n============================================================================\n")

# =======================================================================
# |                                                                     |
# |                           CRIA O SERVIDOR                           |
# |                                                                     |
# =======================================================================

# Cria um servidor SMTP no endereço e porta solicitado.
#
#        |
#        V                    {IP}    {Porta}
server = CustomSMTPServer(("127.0.0.1", 1025), None)

# Notifica que o servidor está em execução
print("Servidor smtp.jaku.com em execucao")

# Faz o servidor escutar de forma assíncrona.
#
#        |
#        V
asyncore.loop()