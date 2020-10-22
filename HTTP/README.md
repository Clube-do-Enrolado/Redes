# Implementação do protocolo HTTP 1.1

## Funcionalidades do servidor

O servidor deve ser capaz de responder corretamente à diferentes tipos de requisições feitas pelo cliente. Como:

- [ ] Responder enviando um arquivo (como por exemplo uma página).

  - Caso o cliente faça uma requisição do tipo [GET](https://tools.ietf.org/html/rfc7231#section-4.3.1).

- [ ] Armazenar novos objetos enviados pelo cliente.

  - Caso o cliente faça uma requisição do tipo [PUT](https://tools.ietf.org/html/rfc2616#section-9.6).

- [ ] Responder caso o objeto solicitado não existir no servidor.

  - Nesse caso, verificar as respostas do [servidor](https://tools.ietf.org/html/rfc2616#section-10).

- [ ] Responder caso o objeto foi movido para outro diretório do servidor.
  
  - Geralmente, o código de resposta será dado por [301](https://tools.ietf.org/html/rfc2616#page-62).

## Algumas informações úteis sobre o protocolo

### Requests

A mensagem de requisição feita pelo cliente ao servidor inclui: o método para aplicar sobre um recurso, um identificador do recurso e a versão do protocolo usada.
A requisição segue o modelo:
**Método** SP **Request-URI** SP **HTTP-VERSION** CRLF.
Onde:

- Método: Trata-se do método que será aplicado sobre uma Request-URI.

  - Os métodos podem ser: GET, POST, PUT, DELETE etc. [Mais informação](https://tools.ietf.org/html/rfc2616#section-5.1.1).

- Request-URI: Os Universal Resource Identifiers são strings que identificam - via nome, localização, e qualquer outra característica - um recurso. Ou seja, o Request-URI é o endereço IP, o nome de domínio, ou qualquer outra string que permita alcançar um recurso.

- HTTP-VESION: Como o nome diz, é a versão do protocolo, para o presente projeto, a única versão suportada é "HTTP/1.1". Caso contrário, o servidor deve retornar um erro.

- SP: O espaço entre as palavras.

- CRLF: CR+LF - Carriage Return + Line Feed, ambos combinados preparam uma nova linha (LF) iniciando no lado esquerdo (CR).

Portanto, ao combinar todos conhecimentos, temos uma requisição de exemplo dada por:
GET 127.0.0.1/principal.html HTTP/1.1

**Se nenhum *target* for especificado após o Request-URI, obrigatoriamente, deve ser o *server root*, dado por "Request-URI/"**

### Responses

Após receber uma requisição, o servidor envia uma resposta.

A primeira linha da resposta consiste na *status_line*, ela segue o modelo: Status-Line = **HTTP-VERSION** SP **Status-Code** SP **Reason-Phrase** CRLF.
Onde:

- HTTP-VERSION: É a versão do HTTP, no presente projeto é apenas utilizado o HTTP/1.1, caso contrário é retornado erro.

- Status-Code: É um código de três dígitos resultante da tentativa de responder à uma requisição, esses códigos já existem para diversas funcionalidade e podem ser encontrados [aqui](https://tools.ietf.org/html/rfc2616#section-10).
  - De forma geral, o primeiro dígito faz referência a classe da resposta:
    - 1xx - Informações
    - 2xx - Sucesso
    - 3xx - Redirecionamento
    - 4xx - Erro de cliente
    - 5xx - Erro do servidor

- Reason-Phrase: É uma contextualização CURTA do código gerado pelo status-code.

## Considerações feitas em código

Para que o código fique legível para quem quiser trabalhar, foi adotado alguns
padrões do [PEP-8](https://www.python.org/dev/peps/pep-0008/).
Esses padrões garantem a correta documentação e entendimento do código.
A principal alteração considerada é em relação aos comentários.

- Para documentar um método/função em Python, utiliza-se o padrão:

``` python
def minha_funcao(parametros):
  """
  Uma breve descrição da finalidade da função.

  Parameters:
  nome_do_parametro(tipo): Descrição

  Returns:
  Descrição do retorno explicitando, se possível,
  o tipo.
  """  
  pass
```

- Além disso, foi adotado o padrão de nomes:
  
  - Classe: Primeira letra maíuscula, sem espaço ou hífen.
    - Ex: MinhaClasse, Classe
  - Métodos e funções: tudo minúsculo, podendo utilizar o hífen.
    - Ex: funcao_teste, funcao

- E por último, foi adotado a utilização de 79 caracteres por linha. O que
garante que o leitor visualize o código sem a necessidade de realizar o
scroll horizontal.
