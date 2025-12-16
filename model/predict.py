import pickle
import pandas as pd
with open("model/model.pkl","rb") as f:
    model = pickle.load(f)


MODEL_VERSION = '1.0.0.2'

class_labels = model.classes_.tolist()

def model_predict(user_input : dict):
    df = pd.DataFrame([user_input])
    predicted_class = model.predict(df)[0]
    probablities = model.predict_proba(df)[0]
    confidence = max(probablities)
    
    class_proba = dict(zip(class_labels,map(lambda p : round(p,4),probablities))) 
    
    return {
        'predicted_category' : predicted_class,
        'confidence' : round(confidence,4),
        'class_prob' : class_proba
    }
    # input_df = pd.DataFrame([user_input])
    
    
    # output  = model.predict(input_df)[0]
    
    # return output