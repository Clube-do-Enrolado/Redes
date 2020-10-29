import os
from itertools import chain


global serverUri, serverFolders, serverFiles

serverUri = [x[0] for x in os.walk(".")]
#Adquire o nome de todos diretórios
serverFolders = [x[1] for x in os.walk(".")]
#Adquire todos arquivos
serverFiles = [x[2] for x in os.walk(".")]

#Não utilizado.
def is_folder(requested_file):
    """
    Verifica se o arquivo solicitado é um diretório.

    Parameters:
    requested_file (string): Nome do arquivo desejado para a pesquisa.

    Returns:
    (bool): True (se o arquivo for diretório) ou False (caso não seja).
    """
    for key in range(len(serverFolders)):  
        if requested_file in serverFolders[key]:
            print("O %s É diretório"%requested_file)

def find_file(requested_file):
    """
    Verifica a existência do arquivo requisitado a partir do root do server.
    
    Parameters:
    requested_file (string): Nome do arquivo desejado para a pesquisa.

    Returns:
    (bool): True (caso arquivo encontrado) ou False (caso não encontre).
    """           
    return requested_file in chain(*serverFiles)

def get_file_path(filename):
    """
    Adquire o caminho absoluto do arquivo solicitado.

    Parameters:
    filename (string): Nome do arquivo.

    Returns:
    (string): Caminho absoluto do arquivo.
    """
    return "{}{}".format(os.getcwd(), filename.replace('/','\\'))

def open_file(filepath):
    """
    Método que lê um arquivo dado seu diretório.
    Antes de invocar o método, é certo que esse arquivo
    existe.

    Parameters:
    filepath (string): Diretório do arquivo desejado para abertura.

    Returns:
    (binary): Conteúdo do arquivo em binário.
    (int): 
    """
    try:
        with open(filepath,'rb') as archive:
            content = archive.read()
            content_size = archive.seek(0, os.SEEK_END)
            archive.close()
        return content, content_size
    except:
        return None, None

def createFile(file_to_create):
    pass