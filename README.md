# 🏠 Coliving - Backend Documentation

<p align="center">
  <img src="https://img.shields.io/static/v1?label=Python&message=3.10&color=blue&style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/static/v1?label=Flask&message=2.x&color=orange&style=for-the-badge&logo=flask"/>
  <img src="https://img.shields.io/static/v1?label=AWS&message=Lambda%20%2B%20API%20Gateway&color=ff9900&style=for-the-badge&logo=amazonaws"/>
  <img src="https://img.shields.io/static/v1?label=Terraform&message=IaC&color=5C4EE5&style=for-the-badge&logo=terraform"/>
  <img src="https://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=yellow&style=for-the-badge"/>
  <img src="https://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/>
</p>

> Status do Projeto: :heavy_check_mark: (concluído) | :warning: (em desenvolvimento) | :x: (não iniciado)

---

### Tópicos

:small_blue_diamond: [Descrição](#descrição-page_facing_up) :heavy_check_mark:

:small_blue_diamond: [Estrutura do Projeto](#estrutura-do-projeto-triangular_ruler-straight_ruler) :heavy_check_mark:

:small_blue_diamond: [Estrutura Detalhada](#estrutura-detalhada-package) :heavy_check_mark:

:small_blue_diamond: [Como Executar o Projeto Localmente](#como-executar-o-projeto-localmente-rocket) 

:small_blue_diamond: [Testes Locais](#testes-locais-test_tube) 

:small_blue_diamond: [Deploy na AWS (Lambda + API Gateway)](#deploy-na-aws-lambda--api-gateway-cloud) 

:small_blue_diamond: [Terraform – Provisionamento](#terraform--provisionamento-gear) 

:small_blue_diamond: [Contribuições](#contribuições-technologist) 

:small_blue_diamond: [Tecnologias Utilizadas](#tecnologias-utilizadas-wrench) 

---

## Descrição :page_facing_up:

Este é o **backend do sistema Coliving**, responsável por fornecer as APIs REST para gerenciamento de usuários em ambientes colaborativos de moradia. A arquitetura combina:

- **Microsserviços com AWS Lambda + API Gateway**
- **Aplicação Flask** para desenvolvimento e testes locais
- **Banco de dados PostgreSQL (RDS)**
- **Infraestrutura gerenciada com Terraform**
- **Automação de deploy com GitHub Actions**

---

## Estrutura do Projeto :triangular_ruler: :straight_ruler:

```plaintext
coliving-backend/
├── app/                       # Funções Lambda
├── terraform/                 # Infraestrutura como Código (IaC)
├── .github/                   # CI/CD com GitHub Actions
├── src/                       # Aplicação Flask
├── .env.example               # Variáveis de ambiente exemplo
├── requirements.txt           # Dependências do projeto
└── README.md
```

---

## Estrutura Detalhada :package:

### 1. `app/` – Funções AWS Lambda
- `handler.py`: Define handlers como `get_person`, `create_person`.
- `requirements.txt`: Dependências específicas para ambiente Lambda.
- `deploy.sh`: Script para empacotar e subir a função.
- `zipped_function.zip`: Arquivo gerado para upload manual (ou via script).

### 2. `terraform/` – Infraestrutura como Código
- `main.tf`: Define a infraestrutura principal (RDS, VPC, etc.).
- `lambda.tf`: Define funções Lambda e API Gateway.
- `variables.tf`: Variáveis reutilizáveis.
- `outputs.tf`: Saídas como URL da API.

### 3. `.github/workflows/` – CI/CD
- `deploy.yml`: Automatiza o deploy da função Lambda via GitHub Actions.

### 4. `src/` – Aplicação Flask

| Pasta/Arquivo     | Descrição                                               |
|-------------------|---------------------------------------------------------|
| `app.py`          | Ponto de entrada da API Flask                           |
| `config/`         | Conexões, configurações e variáveis                     |
| `controllers/`    | Lógica dos endpoints (`auth`, `person`)                 |
| `routes/`         | Define as rotas conectadas aos controladores            |
| `services/`       | Lógica de negócio                                       |
| `repositories/`   | Interações com o banco de dados                         |
| `models/`         | Representações das entidades no banco                   |
| `middleware/`     | Autenticação, CORS                                      |
| `errors/`         | Tratamento de exceções personalizadas                   |
| `utils/`          | JWT, criptografia e funções auxiliares                  |
| `validators/`     | Validação de entrada de dados                           |
| `migrations/`     | Scripts do Alembic para migrações de banco              |

---

## Como Executar o Projeto Localmente :rocket:

### 1. Clone o repositório:
```bash
git clone https://github.com/FrancisLauriano/coliving-backend.git
cd coliving-backend/src
```

### 2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scriptsctivate     # Windows
```

### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente:
Crie um arquivo `.env` com base no `.env.example`.

---

## Testes Locais :test_tube:

Com o ambiente ativado e dependências instaladas:

```bash
python app.py
```

A API estará disponível em: `http://localhost:5000/`

---

## Deploy na AWS (Lambda + API Gateway) :cloud:

Você pode implantar as funções Lambda:

- Manualmente via `deploy.sh` e `zipped_function.zip`
- Automaticamente via GitHub Actions (`.github/workflows/deploy.yml`)

---

## Terraform – Provisionamento :gear:

Para provisionar a infraestrutura na AWS:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

---

## Contribuições :technologist:

Contribuições são bem-vindas! Siga os passos:

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feat/minha-funcionalidade`)
3. Faça commit (`git commit -m 'Minha contribuição'`)
4. Push (`git push origin feat/minha-funcionalidade`)
5. Crie um Pull Request

---

## Tecnologias Utilizadas :wrench:

- Python 3.10+
- Flask
- AWS Lambda + API Gateway
- PostgreSQL (via RDS)
- Terraform
- GitHub Actions (CI/CD)
- JWT, criptografia, validação