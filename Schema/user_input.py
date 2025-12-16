from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Literal,Annotated
from config.city_tier import tier_1_cities,tier_2_cities

# create pydantic object
class userinput(BaseModel):
    age : Annotated[int,Field(...,description = 'enter the age ',example = '20',gt = 18)]
    weight : Annotated[float,Field(...,description = 'enter the weight',example = "56.32",gt = 10)]
    height : Annotated[float,Field(...,description = "enter the height ", example = '4.6',gt = 0)]
    income_lpa : Annotated[float,Field(...,description = "annual income ",example = '13',gt = 0)]
    smoker : Annotated[bool,Field(...,description = 'is user a smoker')]
    city : Annotated[str,Field(...,description = "city of ")]
    occupation : Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...)]
    
    @computed_field
    @property
    def bmi_calculate(self)-> float:
        bmi =  round(self.weight / (self.height**2),2)
        return bmi
    
    
    
    @computed_field
    @property
    def age_group(self)-> str:
        if self.age<25:
            return 'young'
        elif self.age < 45 :
            return 'adult'
        elif self.age < 60:
            return 'middle_aged'
        else:
            return 'senior'
        
    @computed_field
    @property
    def life_risk(self)-> str:
        if self.smoker and self.bmi_calculate > 30:
            return 'high'
        elif self.smoker or self.bmi_calculate > 27:
            return 'medium'
        else:
            return 'low'
    
    @computed_field
    @property
    def tier_city(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
    @field_validator('city')
    @classmethod
    def normalise_city(cls,v:str)->str:
        v = v.strip().title()
        return v