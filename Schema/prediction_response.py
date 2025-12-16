from pydantic import BaseModel,Field
from typing import Dict

class Responses(BaseModel):
    predicted_category : str = Field(
        ...,
        description = "The Predicted Insurance Premium Category",
        example = "High"
    )
    confidence : float = Field(
        ...,
        description = "model confidence score",
        example = 10.8
    )
    class_prob : Dict [str,float] = Field(
        ...,
        description = "Probablities distribution across all classes",
        example = {"low" : 0.01,"medium" : 0.15,"high" : 2}
    )