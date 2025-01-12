# app/deploy.sh:
#!/bin/bash

FUNCTION_NAME="coliving-backend-person-service"
ZIP_FILE="zipped_function.zip"

echo "Instalando dependências..."
pip install -r requirements.txt --target ./package

echo "Empacotando a função Lambda..."
cd package
zip -r "../$ZIP_FILE" .
cd ..
zip -g "$ZIP_FILE" handler.py

echo "Fazendo upload da função para o Lambda..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE

echo "Deploy concluído."
