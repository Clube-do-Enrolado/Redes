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
# |       com input.                                                     |
# |                                                                      |
# | ÚLTIMA MODIFICAÇÃO: 14/10/2020 03:57                                 |
# |                                                                      |
# ========================================================================

# =======================================================================
# |                                                                     |
# |                      BIIBLIOTECAS IMPORTADAS                        |
# |                                                                     |
# =======================================================================

import smtplib #Biblioteca para SMTP implemetada para o cliente.
import email.utils #Provê funções utilitárias para formatação/geração do email.
from email.mime.text import MIMEText #Classe de mensagens do SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import time
from tkinter import filedialog #Classe que permite a abertura de arquivos via GUI.


class Mail():
    def __init__(self):
        self.data = {
            'titulo': '',
            'destinatario': [],
            'mensagem': '',
            'anexo': []
        }
        self.selectedFileName = ''
        self.askInput()

    '''
    Metódo que abre o filedialog do Tkinter (biblioteca padrão do Python para criação de GUIs)
    visando que o usuário escolha um arquivo de anexo.
    '''
    def openAttachment(self):
        print("--> Selecione o arquivo...")
        #Cria o Dialog
        self.selectedFileName = filedialog.askopenfilename(initialdir = '/', title = 'Selecione o arquivo',
                                    filetypes=(("Arquivos de Imagem", "*.jpeg *.jpg *.png *.gif"), ("Arquivos de texto", "*.txt")))

        #Se o usuário clicar no botão de cancelar, não será gerado o objeto self.selectedFileName
        #esse if verifica esse caso.
        if not self.selectedFileName:
            print("-->    Erro ao adquirir o arquivo.\n\tProcedendo sem anexos...")
        
        #Caso o usuário selecione um arquivo válido, será salvo o nome e a extensão do arquivo
        #no dicionário self.data na chave 'anexo'.
        else:
            splitedPath = self.selectedFileName.split('/')
            self.data['anexo'] = splitedPath[-1].split('.') 
    
    '''
    Método que pede e recebe os dados do usuário via console.
    '''
    def askInput(self):
        print('\n\tPara enviar o e-mail, insira os dados requeridos.\n')
        self.data['titulo'] = input("\n--> Título do Email: ")

        print("\n\tDestinatário (Nome): ")
        fromName = input("\n-->Nome: ")
        self.data['destinatario'].append(fromName)
        print("\n\tDestinatário (Email): ")
        fromEmail = input('\n-->Email: ')
        self.data['destinatario'].append(fromEmail)
        
        print("\n\t--- Conteúdo do Email --- ")
        self.data['mensagem'] = input("--> ")

        print('\n\t--- Deseja inserir um anexo? ---\n[S]im\t[N]ão\n')
        self.attachment = input("--> Resposta: ").upper()

        if self.attachment == "S":
            self.openAttachment()

        self.makeEmail()
    
    '''
    Método que monta a mensagem a ser enviada ao servidor SMTP.
    '''
    def makeEmail(self):
        print("--> Processando...")
        self.msg = MIMEMultipart()

        #Remetente da mensagem
        self.msg['From'] = email.utils.formataddr(("Vader", "vader@deathstar.com"))

        #Destinatário da mensagem
        self.msg['To'] = email.utils.formataddr(self.data['destinatario'])

        #Data de envio da mensagem
        self.msg['Date'] = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))


        #Assunto da mensagem
        self.msg['Subject'] = self.data['titulo']
        #Mensagem
        self.msg.preamble = self.data['mensagem']

        #O usuário selecionou previamente um anexo, portanto, deve-se inseri-lo no email.
        if self.selectedFileName:
            fileName = '.'.join(self.data['anexo'])

            #Caso o anexo seja do tipo jpeg, deve-se executar o MIMEImage
            if (self.data['anexo'][1] == 'jpeg' or self.data['anexo'][1] == 'jpg' or self.data['anexo'][1] == 'png' or self.data['anexo'][1] == 'gif'):
                msgAttachment = MIMEImage(open(self.selectedFileName, 'rb').read())
                msgAttachment.add_header('Content-Disposition', 'attachment', filename=fileName)

            #Caso contrário, o arquivo tem extensão .txt e é possível utilizar o MIMEText.
            else:
                msgAttachment = MIMEText(open(self.selectedFileName).read())
                msgAttachment.add_header('Content-Disposition', 'attachment', filename=fileName)

            #Salva o anexo do usuário na mensagem
            self.msg.attach(msgAttachment)  

        
        server = smtplib.SMTP("127.0.0.1", 1030)
        server.set_debuglevel(True) #Debug to see messages interaction 
        server.sendmail("vader@deathstar.com", [self.data['destinatario']], self.msg.as_string())     
        
        print("\n\tMensagem enviada com sucesso!\n\tEncerrando conexão..")
        server.quit()

Mail()