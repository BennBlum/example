"""
Schema definition for api extraction response. 

Example json output:

{
    "details": {
        "date_of_birth": "19 Aug 1990",
        "document_no": "123456789",
        "expiry_date": "04 Jul 2028",
        "last_name": "ANGELA",
        "names": "SMITH",
    },
    "mr_details": {
        "date_of_birth_mr": "900819",
        "expiry_mr": "280704",
        "last_name_mr": "ANGELA",
        "names_mr": "SMITH",
    },
}


"""
from typing import Optional
from pydantic import BaseModel

class PersonDetails(BaseModel):
    date_of_birth: Optional[str]
    document_no: Optional[str]
    expiry_date: Optional[str]
    last_name: Optional[str]
    names: Optional[str]

class MRDetails(BaseModel):
    date_of_birth_mr: Optional[str]
    expiry_mr: Optional[str]
    last_name_mr: Optional[str]
    names_mr: Optional[str]

class ExtractionResponse(BaseModel):
    details: Optional[PersonDetails]
    mr_details: Optional[MRDetails]
    
    

