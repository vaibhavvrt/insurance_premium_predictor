import streamlit as st
import pandas as pd
from model.predict import MODEL_VERSION, model_predict
from config.city_tier import tier_1_cities, tier_2_cities

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Title and header
st.markdown('<h1 class="main-header">🏥 Insurance Premium Predictor</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for information
with st.sidebar:
    st.header("ℹ️ About")
    st.info(f"**Model Version:** {MODEL_VERSION}")
    st.markdown("""
    This application predicts insurance premium categories based on:
    - Personal demographics (age, BMI)
    - Lifestyle factors (smoking status)
    - Location (city tier)
    - Income level
    - Occupation
    """)
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Fill in all the required fields")
    st.markdown("2. Click 'Predict Premium' button")
    st.markdown("3. View your predicted premium category")

# Main form
st.header("📋 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        help="Enter your age (must be 18 or above)"
    )
    
    weight = st.number_input(
        "Weight (kg)",
        min_value=10.0,
        max_value=300.0,
        value=70.0,
        step=0.1,
        help="Enter your weight in kilograms"
    )
    
    height = st.number_input(
        "Height (feet)",
        min_value=3.0,
        max_value=8.0,
        value=5.6,
        step=0.1,
        help="Enter your height in feet (e.g., 5.6 for 5 feet 6 inches)"
    )
    
    income_lpa = st.number_input(
        "Annual Income (LPA)",
        min_value=0.1,
        max_value=1000.0,
        value=10.0,
        step=0.1,
        help="Enter your annual income in Lakhs Per Annum"
    )

with col2:
    smoker = st.radio(
        "Smoking Status",
        options=[False, True],
        format_func=lambda x: "Non-Smoker" if not x else "Smoker",
        help="Select your smoking status"
    )
    
    # Combine all cities for dropdown
    all_cities = sorted(tier_1_cities + tier_2_cities)
    city = st.selectbox(
        "City",
        options=all_cities + ["Other"],
        help="Select your city or 'Other' if not listed"
    )
    
    # If "Other" is selected, allow text input
    if city == "Other":
        city = st.text_input(
            "Enter your city name",
            value="",
            help="Enter your city name (will be classified as Tier 3)"
        )
    
    occupation = st.selectbox(
        "Occupation",
        options=['retired', 'freelancer', 'student', 'government_job', 
                 'business_owner', 'unemployed', 'private_job'],
        help="Select your occupation"
    )

# Calculate BMI and other derived fields
if st.button("🔮 Predict Premium", type="primary", use_container_width=True):
    if city == "" and city == "Other":
        st.error("Please enter your city name or select a city from the list.")
    else:
        try:
            # Calculate BMI
            bmi = round(weight / (height**2), 2)
            
            # Determine age group
            if age < 25:
                age_group = 'young'
            elif age < 45:
                age_group = 'adult'
            elif age < 60:
                age_group = 'middle_aged'
            else:
                age_group = 'senior'
            
            # Determine life risk
            if smoker and bmi > 30:
                life_risk = 'high'
            elif smoker or bmi > 27:
                life_risk = 'medium'
            else:
                life_risk = 'low'
            
            # Determine city tier
            city_normalized = city.strip().title()
            if city_normalized in tier_1_cities:
                tier_city = 1
            elif city_normalized in tier_2_cities:
                tier_city = 2
            else:
                tier_city = 3
            
            # Prepare input for prediction
            user_input = {
                'Bmi': bmi,
                'age_group': age_group,
                'life_style_risk': life_risk,
                'city_tier': tier_city,
                'income_lpa': income_lpa,
                'occupation': occupation
            }
            
            # Make prediction
            with st.spinner("Analyzing your data..."):
                prediction = model_predict(user_input)
            
            # Display results
            st.markdown("---")
            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
            st.header("📊 Prediction Results")
            
            # Main prediction
            pred_category = prediction['predicted_category']
            confidence = prediction['confidence']
            
            # Color coding for categories
            category_colors = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🔴'
            }
            emoji = category_colors.get(pred_category.lower(), '📌')
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Predicted Category",
                    value=f"{emoji} {pred_category.upper()}"
                )
            
            with col2:
                st.metric(
                    label="Confidence Score",
                    value=f"{confidence:.2%}"
                )
            
            with col3:
                st.metric(
                    label="BMI",
                    value=f"{bmi}"
                )
            
            # Probability distribution
            st.subheader("📈 Probability Distribution")
            prob_df = pd.DataFrame(
                list(prediction['class_prob'].items()),
                columns=['Category', 'Probability']
            )
            prob_df['Probability'] = prob_df['Probability'].apply(lambda x: f"{x:.2%}")
            prob_df['Category'] = prob_df['Category'].str.upper()
            
            # Display as columns
            prob_cols = st.columns(len(prob_df))
            for idx, row in prob_df.iterrows():
                with prob_cols[idx]:
                    st.metric(
                        label=row['Category'],
                        value=row['Probability']
                    )
            
            # Additional information
            st.markdown("---")
            st.subheader("ℹ️ Your Profile Summary")
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.write(f"**Age Group:** {age_group.replace('_', ' ').title()}")
                st.write(f"**Life Style Risk:** {life_risk.upper()}")
                st.write(f"**City Tier:** {tier_city}")
            
            with info_col2:
                st.write(f"**Occupation:** {occupation.replace('_', ' ').title()}")
                st.write(f"**Annual Income:** ₹{income_lpa:.1f} LPA")
                st.write(f"**Smoking Status:** {'Yes' if smoker else 'No'}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Insurance Premium Predictor | Model Version " + MODEL_VERSION +
    "</div>",
    unsafe_allow_html=True
)

