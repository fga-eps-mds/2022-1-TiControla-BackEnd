# Por enquanto, quando acontece um erro relacionado ao servidor,
# o output fica beeem feio e fica bem nítido que ocorreu um erro.
# Porém, quando acontece um erro nos cálculos que são feitos
# sobre os dados do usuário, nada explícito acontece. Logo é necessário
# escrever testes melhores.
# USAGE: python3 testes_nao_automatizados.py > tests_output.txt
from subprocess import check_output


# variáveis globais
EMAIL = 'SUBSTITUIR_PELO_SEU_EMAIL_DE_VERDADE@gmail.com'
SENHA = 'ESCOLHA_UMA_SENHA_SEGURA'
URL = "http://localhost:8000"
# URL = "https://161.35.248.92.nip.io"

##### Como cadastrar um usuário. Observação: é impossível criar um superusuário por meio da API pública.
COMANDO_CADASTRAR_USUARIO = '''
curl -H "Content-Type: application/json" \
     -X POST \
     --data '{"email":"''' + EMAIL + '''", "password":"''' + SENHA + '''"}' \
     "''' + URL + '''/register/"
'''

##### Como fazer o login de um usuário. Atenção: como a nossa autenticação é baseada em sessões de uso, é necessário reutilizar dois outputs gerados pelo login a fim de acessar os dados do usuário. Esses outputs são o 'csrftoken' e o 'sessionid'.
COMANDO_FAZER_LOGIN = '''
curl -H "Content-Type: application/json" \
     -X POST \
     --data '{"email":"''' + EMAIL + '''", "password":"''' + SENHA + '''"}' \
     "''' + URL + '''/login/"
'''


def rodar_comando(comando):
    output = check_output(comando, shell=True).decode('utf-8').rstrip()
    return output


def main():
    # output = rodar_comando(COMANDO_CADASTRAR_USUARIO)
    # print(output)

    output = rodar_comando(COMANDO_FAZER_LOGIN)
    print(output)

    sessionid = output.split('{"sessionid":"')[1].split('"')[0]
    csrftoken = output.split('csrftoken":"')[1].split('"')[0]
    print('sessionid:', sessionid)
    print('csrftoken:', sessionid)

    lista_de_testes = []
    lista_de_mensagens_de_teste = []

    lista_de_mensagens_de_teste.append(" Como requisitar dados pessoais do usuário logado (email, nome completo, data de criação do usuário). Essa requisição pode ser usada para mostrar uma tela com os dados pessoais que o usuário informou à API. Lembre de reutilizar o 'sessionid'.")
    lista_de_testes.append(f'''
    curl -H "Cookie: sessionid={sessionid};" \
        -X GET \
        '{URL}/profile/'
    ''')

    lista_de_mensagens_de_teste.append(" Como atualizar o nome de um usuário logado. Observação: não é possível atualizar o email. Lembre de reutilizar o 'csrftoken' e o 'sessionid'.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X PATCH \
        --data 'full_name=Leonardo Miranda' \
        '{URL}/profile/'
    ''')

    lista_de_mensagens_de_teste.append(" Como requisitar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para mostrar o saldo do usuário, o limite disponível do cartão e o limite máximo do cartão. Para cada usuário, só há um valor de saldo, um único valor de limite disponível e um único valor de limite máximo. Lembre de reutilizar o 'sessionid'.")
    lista_de_testes.append(f'''
    curl -H "Cookie: sessionid={sessionid};" \
        -X GET \
        '{URL}/profile/data/'
    ''')

    lista_de_mensagens_de_teste.append(" Como atualizar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para atualizar o saldo do usuário (saldo) e o limite máximo do cartão (limite_maximo). É possível atualizar cada valor de forma separada (perceba que no exemplo abaixo o saldo não é atualizado). Lembre de reutilizar o 'csrftoken' e o 'sessionid'.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X PATCH \
        --data 'limite_maximo=7000' \
        '{URL}/profile/data/'
    ''')

    lista_de_mensagens_de_teste.append(" Criar cartão. O campo 'apelido_cartao' é obrigatório.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'apelido_cartao=nubank&limite_credito=7000' \
        '{URL}/profile/cartao/'
    ''')

    lista_de_mensagens_de_teste.append(" Criar cartão. O campo 'apelido_cartao' é obrigatório.")

    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'apelido_cartao=digimon&limite_credito=7000' \
        '{URL}/profile/cartao/'
    ''')


    lista_de_mensagens_de_teste.append(" Listar cartões do usuário logado.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X GET \
        '{URL}/profile/cartao/'
    ''')


    lista_de_mensagens_de_teste.append(" Alterar cartão do usuário por id. Cada id de cartão é único, e não se repete entre usuários.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X PATCH \
        --data 'id=1&apelido_cartao=digio&limite_credito=2000' \
        '{URL}/profile/cartao/'
    ''')


    lista_de_mensagens_de_teste.append(" Deletar cartao do usuário por id. O id é do cartão.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X DELETE \
        --data 'id=2' \
        '{URL}/profile/cartao/'
    ''')

    lista_de_mensagens_de_teste.append(" Criar gasto do cartão de crédito. Os campos 'id_cartao' e 'date' (data de pagar a conta) são obrigatórios.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'id_cartao=1&date=2020-01-01' \
        '{URL}/profile/gastos/credito/'

    ''')

    lista_de_mensagens_de_teste.append(" Criar gasto do cartão de crédito. Os campos 'id_cartao' e 'date' (data de pagar a conta) são obrigatórios.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'id_cartao=1&date=2020-02-01' \
        '{URL}/profile/gastos/credito/'

    ''')


    lista_de_mensagens_de_teste.append(" Listar gastos do cartão de crédito do usuário logado")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X GET \
        '{URL}/profile/gastos/credito/'
    ''')


    lista_de_mensagens_de_teste.append(" Alterar gasto do cartão de crédito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X PATCH \
        --data 'id=1&quantidade_parcelas=12' \
        '{URL}/profile/gastos/credito/'

    ''')


    lista_de_mensagens_de_teste.append(" Deletar gasto do cartão de crédito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X DELETE \
        --data 'id=2' \
        '{URL}/profile/gastos/credito/'
    ''')

    lista_de_mensagens_de_teste.append(" Criar gasto do cartão de débito. Não há campo 'id_cartao' e nem 'quantidade_parcelas' aqui. O campo 'date' (data de pagar a conta) é obrigatório.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'date=2020-01-01' \
        '{URL}/profile/gastos/debito/'

    ''')

    lista_de_mensagens_de_teste.append(" Criar gasto do cartão de débito. Não há campo 'id_cartao' e nem 'quantidade_parcelas' aqui. O campo 'date' (data de pagar a conta) é obrigatório.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'date=2020-02-01' \
        '{URL}/profile/gastos/debito/'

    ''')


    lista_de_mensagens_de_teste.append(" Listar gastos do cartão de débito do usuário logado")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X GET \
        '{URL}/profile/gastos/debito/'

    ''')


    lista_de_mensagens_de_teste.append(" Alterar gasto do cartão de débito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X PATCH \
        --data 'id=1&tipo=alimentacao&valor=100' \
        '{URL}/profile/gastos/debito/'

    ''')


    lista_de_mensagens_de_teste.append(" Deletar gasto do cartão de débito por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X DELETE \
        --data 'id=2' \
        '{URL}/profile/gastos/debito/'
    ''')

    lista_de_mensagens_de_teste.append(" Criar gasto fixo. Não há campo 'id_cartao' e nem 'quantidade_parcelas' aqui. O campo 'date' (data de pagar a conta) é obrigatório.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'date=2020-01-01' \
        '{URL}/profile/gastos/fixo/'

    ''')

    lista_de_mensagens_de_teste.append(" Criar gasto fixo. Não há campo 'id_cartao' e nem 'quantidade_parcelas' aqui. O campo 'date' (data de pagar a conta) é obrigatório.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        --data 'date=2020-02-03' \
        '{URL}/profile/gastos/fixo/'

    ''')


    lista_de_mensagens_de_teste.append(" Listar gastos fixos do usuário logado")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X GET \
        '{URL}/profile/gastos/fixo/'

    ''')


    lista_de_mensagens_de_teste.append(" Alterar gasto fixo por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X PATCH \
        --data 'id=1&tipo=alimentacao&valor=100' \
        '{URL}/profile/gastos/fixo/'

    ''')


    lista_de_mensagens_de_teste.append(" Deletar gasto fixo por id. Cada id de gasto é único, e não se repete jamais (exceto em caso de inconsistência no banco).")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X DELETE \
        --data 'id=2' \
        '{URL}/profile/gastos/fixo/'
    ''')



    lista_de_mensagens_de_teste.append(" Limites disponíveis agrupados por mês.")
    lista_de_testes.append(f'''
        curl -H "referer: {URL}/" \
            -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
            -H "X-CSRFToken: {csrftoken}" \
            -X GET \
            '{URL}/profile/limite-disponivel/mensal/'
    ''')

    lista_de_mensagens_de_teste.append(" Saldos disponíveis agrupados por mês.")
    lista_de_testes.append(f'''
        curl -H "referer: {URL}/" \
            -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
            -H "X-CSRFToken: {csrftoken}" \
            -X GET \
            '{URL}/profile/saldo-disponivel/mensal/'
    ''')

    lista_de_mensagens_de_teste.append(" Total gasto por cartão de crédito e por mês.")
    lista_de_testes.append(f'''
        curl -H "referer: {URL}/" \
            -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
            -H "X-CSRFToken: {csrftoken}" \
            -X GET \
            '{URL}/profile/cartao/total/mensal/'
    ''')

    lista_de_mensagens_de_teste.append(" Gastos do cartão de débito agrupados por mês e por dia.")
    lista_de_testes.append(f'''
        curl -H "referer: {URL}/" \
            -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
            -H "X-CSRFToken: {csrftoken}" \
            -X GET \
            '{URL}/profile/gastos/debito/diario/'
    ''')

    lista_de_mensagens_de_teste.append(" Gastos do cartão de crédito agrupados por mês e por dia.")
    lista_de_testes.append(f'''
        curl -H "referer: {URL}/" \
            -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
            -H "X-CSRFToken: {csrftoken}" \
            -X GET \
            '{URL}/profile/gastos/credito/diario/'
    ''')

    lista_de_mensagens_de_teste.append(" Como fazer o logout do usuário. Lembre de reutilizar o 'csrftoken' e o 'sessionid'.")
    lista_de_testes.append(f'''
    curl -H "referer: {URL}/" \
        -H "Cookie: csrftoken={csrftoken};sessionid={sessionid};" \
        -H "X-CSRFToken: {csrftoken}" \
        -X POST \
        '{URL}/logout/'
    ''')
