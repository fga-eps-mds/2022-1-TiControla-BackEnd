## Setup do ambiente de produção
A API que está rodando na produção já é atualizada automaticamente por meio de GitHub Actions. Esta seção serve para caso seja necessário refazer a infraestrutura e configurar as GitHub Actions. É necessário instalar kubectl, openssl e terraform na sua máquina.

##### Como criar o servidor usando DigitalOcean e Terraform
A DigitalOcean oferece 100 USD de crédito para estudantes por meio do GitHub Student Developer Pack (estudantes da UnB tem acesso ao pack). Independente do GitHub Education, é necessário ter um cartão de crédito internacional para liberar o crédito de 100 USD.

```
# clonar o repositório
git clone https://github.com/leomichalski/2022-1-TiControla-IaC

# mudar o diretório atual para "2022-1-TiControla-IaC"
cd 2022-1-TiControla-IaC

# criar um arquivo "terraform.tfvars"
touch terraform.tfvars

# botar o seguinte conteúdo no arquivo "terraform.tfvars" substituindo os valores adequadamente
do_token = "SUBSTITUIR_PELO_SEU_TOKEN_DA_DIGITAL_OCEAN"
k8s_name = "k8s-name"
region   = "nyc1"

# inicializar o terraform
terraform init

# ver as ações a serem realizadas antes de realizar
terraform plan

# criar servidor ou executar alterações no servidor (é necessário escrever "yes" ou usar a flag -auto-approve)
terraform apply

# após criar o servidor e o cluster kubernetes, vai ser gerado um arquivo "kube_config.yaml" que será necessário para as próximas etapas
```

##### Como criar um certificado tls para poder usar HTTPS
Mais detalhes em: https://kubernetes.github.io/ingress-nginx/user-guide/tls/

```
# substituir a string "161.35.248.92.nip.io" pelo domínio da aplicação e "ticontrola-api" por um nome adequado para a aplicação
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ticontrola-api.key -out ticontrola-api.crt -subj "/CN=161.35.248.92.nip.io/O=161.35.248.92.nip.io"
```

##### Como subir certificado tls para o cluster k8s

```
# substituir a string "ticontrola-api" por um nome adequado para a aplicação
# substituir o caminho para o "kube_config.yaml"
kubectl create secret tls ticontrola-api-tls --key ticontrola-api.key --cert ticontrola-api.crt --kubeconfig=/my/path/to/kube_config.yaml
```

##### Como instalar o cert-manager no cluster (sem helm)

Mais detalhes em: <https://cert-manager.io/docs/installation/>

```
# instalar (lembrar de talvez atualizar a versão do cert-manager, a versão usada neste comando é a v1.9.1)
# substituir o caminho para o "kube_config.yaml"
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.9.1/cert-manager.yaml --kubeconfig=/my/path/to/kube_config.yaml
```

##### Como instalar o ingress controller da nginx no cluster (sem helm)

Mais detalhes em: <https://kubernetes.github.io/ingress-nginx/deploy/>

```
# instalar (lembrar de talvez atualizar a versão do nginx ingress controller, a versão usada neste comando é a v1.3.0)
# substituir o caminho para o kubeconfig
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml --kubeconfig=/my/path/to/kube_config.yaml
```

##### Criar GitHub Secrets

DOCKERHUB_USER
```
Substituir por nome de usuario do dockerhub.
```

DOCKERHUB_PWD
```
Substituir por senha do dockerhub.
```

K8S_CONFIG
```
Substituir pelo conteudo do arquivo "kube_config.yaml".
```

API_SECRET
```
{
    "DJANGO_SUPERUSER_EMAIL": "SUBSTITUIR",
    "DJANGO_SUPERUSER_PASSWORD": "SUBSTITUIR",
    "SECRET_KEY": "SUBSTITUIR_POR_UMA_SECRET_KEY_DO_DJANGO",
    "EMAIL_HOST_USER": "SUBSTITUIR_POR_UM_GMAIL@gmail.com",
    "DEFAULT_FROM_EMAIL": "SUBSTITUIR_POR_UM_GMAIL@gmail.com",
    "EMAIL_HOST_PASSWORD": "SUBSTITUIR_PELA_APP_SPECIFIC_PASSWORD"
}
```

DB_SECRET
```
{
    "MYSQL_USER": "SUBSTITUIR",
    "MYSQL_PASSWORD": "SUBSTITUIR",
    "MYSQL_ROOT_PASSWORD": "SUBSTITUIR"
}
```

## Setup do ambiente de debug/desenvolvimento

### Usando Docker

##### Mudar o diretório atual para "2022-1-TiControla-BackEnd/src"
```
cd 2022-1-TiControla-BackEnd/src
```

##### Criar um arquivo ".env" na pasta "src"
```
touch .env
```

##### Botar o seguinte conteúdo no arquivo ".env". Lembre de substituir o valor das variáveis de ambiente por valores adequados.
```
EMAIL_HOST_USER=SUBSTITUIR_POR_UM_GMAIL@gmail.com
DEFAULT_FROM_EMAIL=SUBSTITUIR_POR_UM_GMAIL@gmail.com
EMAIL_HOST_PASSWORD=SUBSTITUIR_PELA_APP_SPECIFIC_PASSWORD
```

##### Rodar o container da API usando o docker-compose
```
sudo docker-compose up --build
```

## Como gerar migrations.
Este processo não é automático e nem deve ser automatizado: "Once the migration is applied, commit the migration and the models change to your version control system as a single commit - that way, when other developers (or your production servers) check out the code, they’ll get both the changes to your models and the accompanying migration at the same time." [fonte](https://docs.djangoproject.com/en/4.1/topics/migrations/#workflow)

### Usando Docker

##### Baixar a imagem docker a partir do Docker Hub
```
docker pull leommiranda/ti-controla-django-api
```

##### Navegar até o diretório "src"

```
cd src
```

##### Rodar um terminal dentro da imagem docker usando o seguinte comando
```
docker run --rm -it -v $(pwd):/current_dir -w /current_dir --user "$(id -u):$(id -g)" leommiranda/ti-controla-django-api bash
```

##### Criar as migrations
```
python3 manage.py makemigrations
python3 manage.py makemigrations user
python3 manage.py makemigrations user_data
```
