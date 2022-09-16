![Logo TiControla](https://user-images.githubusercontent.com/102192917/184401954-7b7c706b-c287-4c22-83b0-a3039213c627.jpg)

## Repositórios do projeto
- [Docs](https://github.com/fga-eps-mds/2022-1-TiControla-Docs): documentos exceto os de instalação e de execução.
- [FrontEnd](https://github.com/fga-eps-mds/2022-1-TiControla-FrontEnd): aplicativo mobile.
- [BackEnd](https://github.com/fga-eps-mds/2022-1-TiControla-BackEnd): REST API.
- [IaC](https://github.com/fga-eps-mds/2022-1-TiControla-IaC): infraestrutura como código.

## Links úteis
- [Como fazer requisições HTTP para a API.](#como-fazer-requisições-http-para-a-api-usando-curl)
- [Setup do ambiente de produção.](/src#setup-do-ambiente-de-produção)
- [Setup do ambiente de local de desenvolvimento.](/src#setup-do-ambiente-de-debugdesenvolvimento)
- [Como gerar migrations.](/src#como-gerar-migrations)
- [Como contribuir.](https://github.com/fga-eps-mds/2022-1-TiControla-Docs/blob/main/CONTRIBUTING.md)
- [Outros documentos.](https://github.com/fga-eps-mds/2022-1-TiControla-Docs)



## Como fazer requisições HTTP para a API usando cURL
A biblioteca cURL não é necessária. Para converter um comando cURL para uma linguagem de programação (como javascript), use o site <https://curlconverter.com/#javascript>. Para fins de debugging, além do cURL, por exemplo, existem as ferramentas httpie e postman.

### Usuário

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

### Alguns dados financeiros do usuário (saldo mensal e limite mensal)

##### Como requisitar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para mostrar o saldo do usuário, o limite disponível do cartão e o limite máximo do cartão. Para cada usuário, só há um valor de saldo, um único valor de limite disponível e um único valor de limite máximo. Lembre de reutilizar o "sessionid".

```
curl -H "Cookie: sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -X GET \
     'https://161.35.248.92.nip.io/profile/data/'
```

##### Como atualizar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para atualizar o saldo do usuário (saldo) e o limite máximo do cartão (limite_maximo). É possível atualizar cada valor de forma separada (perceba que no exemplo abaixo o saldo não é atualizado). Lembre de reutilizar o "csrftoken" e o "sessionid".

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X PATCH \
     --data 'limite_maximo=7000' \
     'https://161.35.248.92.nip.io/profile/data/'
```

### Cartões do usuário

##### Criar cartão. O campo "apelido_cartao" é obrigatório.

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X POST \
     --data 'apelido_cartao=nubank&limite_credito=7000' \
     'https://161.35.248.92.nip.io/profile/cartao/'
```


##### Listar cartões do usuário logado.

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X GET \
     'https://161.35.248.92.nip.io/profile/cartao/'
```


##### Alterar cartão do usuário por id. Cada id de cartão é único, e não se repete entre usuários.

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X PATCH \
     --data 'id=1&apelido_cartao=digio&limite_credito=2000' \
     'https://161.35.248.92.nip.io/profile/cartao/'
```


##### Deletar cartao do usuário por id. O id é do cartão.

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X DELETE \
     --data 'id=1' \
     'https://161.35.248.92.nip.io/profile/cartao/'
```

### Gastos dos cartões de crédito do usuário


##### Criar gasto do cartão de crédito. Os campos "id_cartao" e "date" (data de pagar a conta) são obrigatórios.

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X POST \
     --data 'id_cartao=1&date=2020-01-01' \
     'https://161.35.248.92.nip.io/profile/gastos/credito/'

Atributos: id_cartao, quantidade_parcelas, date, tipo, nome, descricao, valor.
```


##### Listar gastos do cartão de crédito do usuário logado

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X GET \
     'https://161.35.248.92.nip.io/profile/gastos/credito/'
```


##### Alterar gasto do cartão de crédito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X PATCH \
     --data 'id=1&quantidade_parcelas=12' \
     'https://161.35.248.92.nip.io/profile/gastos/credito/'

Atributos: id_cartao, quantidade_parcelas, date, tipo, nome, descricao, valor.
```


##### Deletar gasto do cartão de crédito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X DELETE \
     --data 'id=1' \
     'https://161.35.248.92.nip.io/profile/gastos/credito/'
```

### Gastos dos cartões de débito do usuário

##### Criar gasto do cartão de débito. Não há campo "id_cartao" e nem "quantidade_parcelas" aqui. O campo "date" (data de pagar a conta) é obrigatório.

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X POST \
     --data 'date=2020-01-01' \
     'https://161.35.248.92.nip.io/profile/gastos/debito/'

Atributos: date, tipo, nome, descricao, valor.
```


##### Listar gastos do cartão de débito do usuário logado

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X GET \
     'https://161.35.248.92.nip.io/profile/gastos/debito/'

```


##### Alterar gasto do cartão de débito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X PATCH \
     --data 'id=1&tipo=alimentacao&valor=100' \
     'https://161.35.248.92.nip.io/profile/gastos/debito/'

Atributos: date, tipo, nome, descricao, valor.
```


##### Deletar gasto do cartão de débito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X DELETE \
     --data 'id=1' \
     'https://161.35.248.92.nip.io/profile/gastos/debito/'
```

### Gastos fixos (indiferente em relação ao cartão)

##### Criar gasto fixo. Não há campo "id_cartao" e nem "quantidade_parcelas" aqui. O campo "date" (data de pagar a conta) é obrigatório.

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X POST \
     --data 'date=2020-01-01' \
     'https://161.35.248.92.nip.io/profile/gastos/fixo/'

Atributos: date, tipo, nome, descricao, valor.
```


##### Listar gastos fixos do usuário logado

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X GET \
     'https://161.35.248.92.nip.io/profile/gastos/fixo/'

```


##### Alterar gasto fixo por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X PATCH \
     --data 'id=1&tipo=alimentacao&valor=100' \
     'https://161.35.248.92.nip.io/profile/gastos/fixo/'

Atributos: date, tipo, nome, descricao, valor.
```


##### Deletar gasto fixo por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).

```
curl -H "referer: https://161.35.248.92.nip.io/" \
     -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
     -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
     -X DELETE \
     --data 'id=1' \
     'https://161.35.248.92.nip.io/profile/gastos/fixo/'
```



### Outros

##### Limites disponíveis agrupados por mês.

```
    curl -H "referer: https://161.35.248.92.nip.io/" \
        -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
        -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
        -X GET \
        'https://161.35.248.92.nip.io/profile/limite-disponivel/mensal/'
```

##### Saldos disponíveis agrupados por mês.

```
    curl -H "referer: https://161.35.248.92.nip.io/" \
        -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
        -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
        -X GET \
        'https://161.35.248.92.nip.io/profile/saldo-disponivel/mensal/'
```

##### Total gasto por cartão de crédito e por mês.

```
    curl -H "referer: https://161.35.248.92.nip.io/" \
        -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
        -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
        -X GET \
        'https://161.35.248.92.nip.io/profile/cartao/total/mensal/'
```

##### Gastos do cartão de débito agrupados por mês e por dia.

```
    curl -H "referer: https://161.35.248.92.nip.io/" \
        -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
        -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
        -X GET \
        'https://161.35.248.92.nip.io/profile/gastos/debito/diario/'
```

##### Gastos do cartão de crédito agrupados por mês e por dia.

```
    curl -H "referer: https://161.35.248.92.nip.io/" \
        -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" \
        -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" \
        -X GET \
        'https://161.35.248.92.nip.io/profile/gastos/credito/diario/'
```
