# app/handler.py:
import psycopg2
import json

def get_person(event, context):
    # Conexão com o banco de dados
    connection = psycopg2.connect(
        dbname="colivingdb",
        user="user",
        password="password",
        host="rds-endpoint.us-east-1.rds.amazonaws.com",
        port=5432
    )
    cursor = connection.cursor()

    # Obtém o ID da pessoa da requisição
    person_id = event["queryStringParameters"]["id"]
    cursor.execute("SELECT * FROM persons WHERE id = %s", (person_id,))
    person = cursor.fetchone()

    if person:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "id": person[0],
                "name": person[1],
                "email": person[2],
                "phone": person[3]
            })
        }
    else:
        response = {
            "statusCode": 404,
            "body": json.dumps({"message": "Person not found"})
        }

    # Fecha conexão
    cursor.close()
    connection.close()
    return response
