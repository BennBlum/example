import os
from mainapp.services.passport_extraction_service import PassportExtractionService
from mainapp.services.auth_service import AuthService

class Factory:  
    def create_auth_service(self) -> AuthService:
        return AuthService()
            
    def create_passport_service(self) -> PassportExtractionService:
       return PassportExtractionService(os.getenv("MODEL_PATH"))
        


