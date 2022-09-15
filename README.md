## Links úteis.

- [Como fazer requisições HTTP para a API.](#como-fazer-requisições-http-para-a-api-usando-curl)
- [Setup do ambiente de produção.](/src#setup-do-ambiente-de-debugdesenvolvimento)
- [Setup do ambiente de local de desenvolvimento.](/src#setup-do-ambiente-de-debugdesenvolvimento)
- [Como gerar migrations.](/src#como-gerar-migrations)
- [Como contribuir.](https://github.com/fga-eps-mds/2022-1-TiControla-Docs/blob/main/CONTRIBUTING.md)
- [Outros documentos.](https://github.com/fga-eps-mds/2022-1-TiControla-Docs)





## Como fazer requisições HTTP para a API usando cURL.
A biblioteca cURL não é necessária. Para converter um comando cURL para uma linguagem de programação (como javascript), use o site <https://curlconverter.com/#javascript>. Para fins de debugging, além do cURL, por exemplo, existem as ferramentas httpie e postman.


##### Como cadastrar um usuário. Observação: é impossível criar um superusuário por meio da API pública.

```
curl -H "Content-Type: application/json" \
     -X POST \
     --data '{"email":"SUBSTITUIR_PELO_SEU_EMAIL@gmail.com", "password":"pass"}' \
     "https://161.35.248.92.nip.io/register/"
```

##### Como fazer o login de um usuário. Atenção: como a nossa autenticação é baseada em sessões de uso, é necessário reutilizar dois outputs gerados pelo login a fim de acessar os dados do usuário. Esses outputs são o "csrftoken" e o "sessionid".

```
curl -H "Content-Type: application/json" \
     -X POST \
     --data '{"email":"SUBSTITUIR_PELO_SEU_EMAIL@gmail.com", "password":"pass"}' \
     "https://161.35.248.92.nip.io/login/"
```

##### Como fazer o logout do usuário. Lembre de reutilizar o "csrftoken" e o "sessionid".

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X POST \
     'https://161.35.248.92.nip.io/logout/'
```

##### Como requisitar dados pessoais do usuário logado (email, nome completo, data de criação do usuário). Essa requisição pode ser usada para mostrar uma tela com os dados pessoais que o usuário informou à API. Lembre de reutilizar o "sessionid".

```
curl -H "Cookie: sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -X GET \
     'https://161.35.248.92.nip.io/profile/'
```

##### Como atualizar o nome de um usuário logado. Observação: não é possível atualizar o email. Lembre de reutilizar o "csrftoken" e o "sessionid".

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X PATCH \
     --data 'full_name=Leonardo Miranda' \
     'https://161.35.248.92.nip.io/profile/'
```

##### Como requisitar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para mostrar o saldo do usuário, o limite disponível do cartão e o limite máximo do cartão. Para cada usuário, só há um valor de saldo, um único valor de limite disponível e um único valor de limite máximo. Lembre de reutilizar o "sessionid".

```
curl -H "Cookie: sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -X GET \
     'https://161.35.248.92.nip.io/profile/data/'
```

##### Como atualizar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para atualizar o saldo do usuário (saldo), o limite disponível do cartão (limite_disponivel) e o limite máximo do cartão (limite_maximo). É possível atualizar cada valor de forma separada (perceba que no exemplo abaixo o saldo não é atualizado). Lembre de reutilizar o "csrftoken" e o "sessionid".

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X PATCH \
     --data 'limite_maximo=7000&limite_disponivel=1500' \
     'https://161.35.248.92.nip.io/profile/data/'
```
