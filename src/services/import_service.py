# services/import_service.py:
import json
import requests
import logging
from repositories.person_repository import PersonRepository
from utils.encryption_utils import EncryptionUtils
from config.settings import Config
from errors.custom_errors import ExternalAPIError, InternalServerError

logger = logging.getLogger(__name__)

class ImportService:
    """
    Serviço para importar pessoas de uma API REST externa.
    """
    @staticmethod
    def import_people():
        """
        Faz uma requisição GET para a API REST configurada, obtém os dados e os salva no banco de dados.

        Returns:
            dict: Resumo da operação de importação.

        Raises:
            ExternalAPIError: Caso ocorra um erro ao consumir a API externa.
            InternalServerError: Caso ocorra um erro inesperado ao salvar os dados no banco.
        """
        url = Config.EXTERNAL_API_URL  # Carrega a URL da API externa a partir da configuração
        logger.info(f"Iniciando importação de pessoas da API externa: {url}")

        try:
            # Realiza a chamada GET na API externa
            response = requests.get(url)
            response.raise_for_status()  # Lança uma exceção para erros HTTP

            # Extrai o campo "body" e faz o parsing do JSON contido nele
            raw_body = response.json().get("body")
            if not raw_body:
                logger.error("Resposta da API externa não contém o campo 'body'.")
                raise ExternalAPIError(service="API Externa", message="Campo 'body' ausente na resposta.")
            
            data = json.loads(raw_body).get("clientes", [])
            logger.info(f"{len(data)} pessoas encontradas na API externa.")

            # Inicializa o utilitário de criptografia
            encryption = EncryptionUtils()

            imported_count = 0
            skipped_count = 0

            for person in data:
                try:
                    # Verificar se o e-mail já está cadastrado
                    if PersonRepository.get_by_email(person["E-mail"]):
                        logger.info(f"E-mail já cadastrado: {person['E-mail']} - Ignorando.")
                        skipped_count += 1
                        continue

                    # Insere no banco de dados com valores obrigatórios
                    PersonRepository.create({
                        "name": person["Nome"],
                        "phone": person["Telefone"],
                        "email": person["E-mail"],
                        "person_type": person["Tipo"],
                        "registration_date": person["Data de Cadastro"], 
                        "password": encryption.encrypt(Config.DEFAULT_PASSWORD)  # Senha padrão criptografada
                    })
                    imported_count += 1
                except Exception as e:
                    # Continua importando os demais registros em caso de erro individual
                    logger.warning(f"Erro ao salvar a pessoa {person.get('Nome')}: {e}")

            logger.info(f"Importação concluída: {imported_count} pessoas importadas, {skipped_count} ignoradas.")
            return {
                "message": f"Importação finalizada: {imported_count} pessoas importadas, {skipped_count} ignoradas."
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao consumir a API externa: {e}")
            raise ExternalAPIError(service="API Externa", message=str(e))

        except Exception as e:
            logger.error(f"Erro inesperado durante a importação: {e}")
            raise InternalServerError("Erro inesperado durante a importação de pessoas.")
