# coliving-backend

```plaintext
coliving-backend/
├── app/                       # Código relacionado às funções Lambda
│   ├── handler.py             # Lambda Handlers para microsserviços
│   ├── requirements.txt       # Dependências do Lambda
│   ├── deploy.sh              # Script para empacotar e subir as funções Lambda
│   └── zipped_function.zip    # Arquivo gerado para upload no Lambda
├── terraform/                 # Configurações de infraestrutura com Terraform
│   ├── main.tf                # Configuração principal (RDS, Lambda, API Gateway)
│   ├── lambda.tf              # Configuração específica para Lambda
│   ├── variables.tf           # Variáveis reutilizáveis
│   ├── outputs.tf             # Saídas da infraestrutura
├── .github/                   # Configurações de CI/CD para GitHub Actions
│   └── workflows/
│       └── deploy.yml         # Automação de deploy no Lambda
├── src/                       # Código principal da aplicação Flask
│   ├── app.py                 # Ponto de entrada principal
│   ├── .env                   # Variáveis de ambiente (exemplo no .env.example)
│   ├── requirements.txt       # Dependências da aplicação Flask
│   ├── config/                # Configurações da aplicação
│   │   ├── database.py        # Configuração do banco de dados
│   │   └── settings.py        # Configurações gerais (chaves, conexões)
│   ├── controllers/           # Controladores para lógica de API
│   │   ├── person_controller.py
│   │   └── auth_controller.py
│   ├── errors/                # Tratamento de erros personalizados
│   │   ├── custom_exceptions.py
│   │   └── error_handlers.py
│   ├── middleware/            # Middlewares para autenticação, CORS, etc.
│   │   ├── auth_middleware.py
│   │   └── cors.py
│   ├── migrations/            # Arquivos gerados pelo Alembic
│   │   └── [arquivos de migração]
│   ├── models/                # Modelos para o banco de dados
│   │   └── person_model.py
│   ├── repositories/          # Camada de persistência
│   │   └── person_repository.py
│   ├── routes/                # Rotas da aplicação Flask
│   │   ├── person_routes.py
│   │   └── auth_routes.py
│   ├── services/              # Lógica de negócio
│   │   ├── person_service.py
│   │   ├── auth_service.py
│   │   └── import_service.py
│   ├── utils/                 # Funções utilitárias
│   │   ├── jwt_utils.py
│   │   └── encryption_utils.py
│   ├── validators/            # Validações de entrada de dados
│   │   └── person_validator.py
├── .env.example               # Exemplo das variáveis de ambiente
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências gerais do projeto
└── .gitignore                 # Arquivos e pastas a serem ignorados pelo Git
```



Explicação de Cada Parte
1. app/
Contém o código relacionado às funções Lambda:

handler.py: Funções que conectam Lambda ao banco de dados RDS e respondem às solicitações da API Gateway.
requirements.txt: Dependências necessárias para o ambiente Lambda.
deploy.sh: Script para criar e enviar o arquivo compactado para o Lambda.
zipped_function.zip: Arquivo gerado pelo script deploy.sh para deploy no Lambda.
2. terraform/
Configura a infraestrutura AWS:

main.tf: Configuração principal (VPC, RDS, etc.).
lambda.tf: Configuração específica para as funções Lambda e API Gateway.
variables.tf: Variáveis reutilizáveis para o Terraform.
outputs.tf: Outputs como endpoints da API.
3. .github/
Automação de deploy:

workflows/deploy.yml: Workflow do GitHub Actions para empacotar e enviar o código Lambda.
4. src/
Código principal da aplicação Flask:

app.py: Ponto de entrada principal da API.
config/: Configurações da aplicação.
database.py: Configuração de conexão ao RDS.
settings.py: Configurações gerais (chaves secretas, URL do banco).
controllers/: Controladores para as APIs (definem o que cada endpoint faz).
errors/: Definem erros e como eles são tratados.
middleware/: Funções intermediárias para autenticação e CORS.
models/: Modelos que representam as tabelas no banco.
repositories/: Interações com o banco de dados.
routes/: Define as rotas e conecta aos controladores.
services/: Contém a lógica de negócio.
utils/: Utilitários como geração de tokens JWT e criptografia.
validators/: Validações para os dados de entrada.
5. Outros Arquivos
.env: Variáveis de ambiente específicas do projeto.
.env.example: Exemplo de configuração para outros desenvolvedores.
README.md: Documentação do projeto, incluindo instruções de configuração e deploy.
.gitignore: Arquivos/pastas a serem ignorados pelo Git.
Como Funciona
Lambda Functions e API Gateway:

Código em app/ define os microsserviços, como get_person e create_person.
API Gateway conecta os endpoints às funções Lambda.
Banco de Dados RDS:

Configurado com Terraform (main.tf e lambda.tf).
Acessado tanto pelas funções Lambda quanto pela aplicação Flask.
CI/CD:

Deploy automatizado via GitHub Actions (.github/workflows/deploy.yml).
Aplicação Flask:

Utilizada para desenvolvimento local ou caso queira migrar para uma aplicação baseada em contêiner no futuro.
Com essa estrutura, você pode gerenciar o projeto de forma clara, além de possibilitar uma fácil transição entre desenvolvimento local e deploy na AWS.
