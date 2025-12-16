import pandas as pd
from fastapi import FastAPI, HTTPException
from Schema.user_input import userinput
from Schema.prediction_response import Responses
from model.predict import MODEL_VERSION, model, model_predict

app = FastAPI()


@app.get('/')
def home():
    return {'message': 'Insurance Premium Prediction API'}


@app.get('/health')
def health_check():
    return {
        'status': 'ok',
        'VERSION': MODEL_VERSION,
        'model_load': model is not None
    }


@app.post('/predict', response_model=Responses)
def premium_input(data: userinput):
    user_input = {
        'Bmi': data.bmi_calculate,
        'age_group': data.age_group,
        'life_style_risk': data.life_risk,
        'city_tier': data.tier_city,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    try:
        prediction = model_predict(user_input)
        return prediction

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))