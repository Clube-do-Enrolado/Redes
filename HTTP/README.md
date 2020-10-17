# Implementação do protocolo HTTP 1.1

## Funcionalidades do servidor
O servidor deve ser capaz de responder corretamente à diferentes tipos de requisições feitas pelo cliente. Como:
- [ ] Responder enviando um arquivo (como por exemplo uma página).<br/>
&nbsp;&nbsp;&nbsp;&nbsp;Caso o cliente faça uma requisição do tipo [GET](https://tools.ietf.org/html/rfc7231#section-4.3.1). 
- [ ] Armazenar novos objetos enviados pelo cliente. <br/>
&nbsp;&nbsp;&nbsp;&nbsp;Caso o cliente faça uma requisição do tipo [PUT](https://tools.ietf.org/html/rfc2616#section-9.6).
- [ ] Responder caso o objeto solicitado não existir no servidor.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;Nesse caso, verificar as respostas do [servidor](https://tools.ietf.org/html/rfc2616#section-10).
- [ ] Responder caso o objeto foi movido para outro diretório do servidor. <br/>
&nbsp;&nbsp;&nbsp;&nbsp;Geralmente, o código de resposta será dado por [301](https://tools.ietf.org/html/rfc2616#page-62).