import streamlit as st

# App title
st.title("💪 Advanced BMI & Health Suggestion Calculator")
st.write("Track your health and get **personalized health suggestions** based on your BMI, age, and activity level.")

# Session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Inputs in columns
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("⚖️ Enter your weight (kg)", min_value=0.0)
with col2:
    age = st.number_input("🎂 Enter your age", min_value=0, max_value=120)

gender = st.radio('🚻 Select your gender', ('Male', 'Female', 'Prefer not to say'))

# Height input
status = st.radio('📏 Select your height format:', ('cms', 'meters', 'feet'))
if status == 'cms':
    height = st.number_input('Centimeters', min_value=0.0)
    height_m = height / 100
elif status == 'meters':
    height = st.number_input('Meters', min_value=0.0)
    height_m = height
else:
    height = st.number_input('Feet', min_value=0.0)
    height_m = height / 3.28

# Activity level input
activity_level = st.selectbox(
    '🏃‍♂️ Select your activity level:',
    ('Sedentary (little/no exercise)',
     'Lightly active (light exercise/sports 1-3 days/week)',
     'Moderately active (moderate exercise/sports 3-5 days/week)',
     'Very active (hard exercise/sports 6-7 days a week)',
     'Super active (twice/day training or physical job)')
)

# Calculate Button
if st.button('✅ Calculate BMI & Suggestions'):
    try:
        bmi = round(weight / (height_m ** 2), 2)
        st.session_state.history.append(
            {'BMI': bmi, 'Weight': weight, 'Height': height, 'Age': age, 'Gender': gender, 'Activity': activity_level})

        st.subheader(f"🔍 Your BMI is **{bmi}**")

        # BMI Interpretation
        if bmi < 16:
            st.error("You are **Extremely Underweight**. Immediate attention needed.")
            suggestion = "Increase your calorie intake with protein-rich food. Consult a doctor."
        elif 16 <= bmi < 18.5:
            st.warning("You are **Underweight**.")
            suggestion = "Add more healthy calories, carbs, and proteins to your diet."
        elif 18.5 <= bmi < 25:
            st.success("You are **Healthy**. Keep it up!")
            suggestion = "Maintain your diet and regular physical activity."
        elif 25 <= bmi < 30:
            st.warning("You are **Overweight**.")
            suggestion = "Reduce sugar & fats, increase cardio workouts."
        else:
            st.error("You are **Extremely Overweight**. Seek professional help.")
            suggestion = "Start with walking, reduce fast food, and consult a nutritionist."

        st.info(f"💡 **Health Tip:** {suggestion}")

        # Calculate Basal Metabolic Rate (BMR)
        if gender == 'Male':
            bmr = 10 * weight + 6.25 * height_m * 100 - 5 * age + 5
        elif gender == 'Female':
            bmr = 10 * weight + 6.25 * height_m * 100 - 5 * age - 161
        else:
            bmr = 10 * weight + 6.25 * height_m * 100 - 5 * age

        # Estimate daily calories based on activity
        activity_multipliers = {
            'Sedentary (little/no exercise)': 1.2,
            'Lightly active (light exercise/sports 1-3 days/week)': 1.375,
            'Moderately active (moderate exercise/sports 3-5 days/week)': 1.55,
            'Very active (hard exercise/sports 6-7 days a week)': 1.725,
            'Super active (twice/day training or physical job)': 1.9
        }
        calorie_needs = round(bmr * activity_multipliers[activity_level])

        with st.expander("📊 Calorie & Diet Recommendations"):
            st.write(f"**Estimated daily calorie needs:** {calorie_needs} kcal/day")
            if bmi < 18.5:
                st.write("➡️ Suggested Calorie Surplus: +500 kcal/day")
            elif bmi > 25:
                st.write("➡️ Suggested Calorie Deficit: -500 kcal/day")
            else:
                st.write("➡️ Maintain current calorie intake.")

            st.write("🍎 Recommended Foods:")
            st.write("- Fresh fruits & vegetables")
            st.write("- Whole grains & lean proteins")
            st.write("- Stay hydrated 💧")

            st.write("🚫 Foods to avoid:")
            st.write("- Sugary drinks")
            st.write("- Processed foods")
            st.write("- Excessive fast food")

        with st.expander("💪 Personalized Exercise Suggestions"):
            if bmi < 18.5:
                st.write("- Strength training 3-4 days a week")
                st.write("- Light cardio")
            elif bmi < 25:
                st.write("- Maintain current routine")
                st.write("- Yoga, jogging, swimming recommended")
            elif bmi >= 25:
                st.write("- Brisk walking, cycling, or HIIT workouts")
                st.write("- Start slow and increase gradually")

    except ZeroDivisionError:
        st.error("⚠️ Invalid height entered. Please enter a valid height.")

# Show history of all calculations
if st.checkbox("🕒 Show Previous Calculations"):
    for idx, record in enumerate(st.session_state.history[::-1], start=1):
        st.write(
            f"{idx}. BMI: **{record['BMI']}**, Weight: {record['Weight']} kg, Height: {record['Height']} {status}, Age: {record['Age']}, Gender: {record['Gender']}, Activity: {record['Activity']}")

# BMI Category Chart
with st.expander("📉 BMI Category Reference Chart"):
    st.markdown("""
    - < 16 : **Extremely Underweight**
    - 16 - 18.4 : **Underweight**
    - 18.5 - 24.9 : **Healthy**
    - 25 - 29.9 : **Overweight**
    - ≥ 30 : **Extremely Overweight**
    """)

# Reset button
if st.button("🔄 Reset Data"):
    st.session_state.history.clear()
    st.success("✅ All data has been reset.")
