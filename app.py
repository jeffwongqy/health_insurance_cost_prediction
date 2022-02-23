import streamlit as st
import numpy as np
import pickle
import time
import sklearn

# load the model
rfr_model = pickle.load(open(r"insurance_model.sav", "rb"))
# load the scaler 
scaler = pickle.load(open(r"standardscaler.sav", "rb"))


# create a function to predict the insurance cost
def insuranceCostPredict(age, sex, bmi, smoker, region, children):
    # encode the sex categorical type into numerical type 
    if sex == 'Female':
        sex = 0
    else:
        sex = 1
    
    # encode the smoker categorical type into numerical type
    if smoker == 'No':
        smoker = 0
    else:
        smoker = 1
    
    # encode the region ('Northwest', 'Northeast', 'Southwest', 'Southeast') categorical type into numerical type 
    if region == 'Northwest':
        region = 0
    elif region == 'Northeast':
        region = 1
    elif region == 'Southwest':
        region = 2
    else:
        region = 3
    
    # combine the input data into an array list
    input_data = np.array([age, sex, bmi, smoker, region, children]).reshape(1, -1)
    
    # scale the input data 
    input_data_scale = scaler.transform(input_data)
    
    # predict the medical insurance cost using the trained random forest regressor 
    medical_insurance_cost_predict = rfr_model.predict(input_data_scale)
    
    return medical_insurance_cost_predict



def main():
    
    ################################################################# Sidebar ##################################################################
    st.sidebar.header("**What is so unique about this health insurance app?**")
    st.sidebar.write("""
                     This web app integrated with a **Random Forest Regressor** algorithm to predict your medical insurance costs
                     based on the following attributes: 
                     - age
                     - sex 
                     - body mass index (BMI)
                     - number of children in the household
                     - smoking or not
                     - the demographic region
                     """)
    
    
    st.sidebar.header("**Body Mass Index (BMI) calculator**")
    weight = st.sidebar.number_input("Enter your weight in kg (e.g. 45.7 kg): ", min_value = 0.00, format = "%.2f")
    height = st.sidebar.number_input("Enter your height in m (e.g. 1.76 m): ", min_value = 0.00,  max_value = 2.50, format = "%.2f")
    
    button = st.sidebar.button("Calculate")
    
    if button == True: 
        if weight > 0.00 and height == 0.00:
            st.sidebar.error("Please enter a value for your height!")
        
        elif weight == 0.00 and height > 0.00:
            st.sidebar.error("Please enter a value for your weight!")
        
        elif weight == 0.00 and height == 0.00:
            st.sidebar.error("Please enter a value for your height and weight!")
        else:
            # calculate the bmi 
            bmi_value = weight/(height**2)
            st.sidebar.info("Your BMI is: " + str(round(bmi_value, 3)))
            
            
     ################################################################# Main ##################################################################
    st.title("Do you wish to predict your health insurance costs using data?")
    st.image("image/medical_insurance.jpg", width = 700)
            
    st.info("""
            **NOTE:**
            Please kindly fill up all the **required** fields in the form below and click on the 'Predict' button to predict
            your medical insurance costs. 
            """)
    
    with st.form('Form 1'):
        # prompt the user for age
        age = st.slider(label = "How old are you? ", min_value = 1, max_value = 100, help = "Use the mouse to render over the range slider to match your current age.")
        
        # prompt the user for gender
        sex = st.selectbox("What is your gender? ", ['', 'Male', 'Female'])
        
        # prompt the user for bmi 
        bmi = st.number_input("What is your BMI? ", min_value = 0.00, format = "%.2f", help = "BMI is a person's weight in kg divided by the squares of height in m. If you wish to know about your BMI, you may use the calculator on the sidebar.")
        
        # prompt the user for smoking status
        smoker = st.selectbox("Are you a smoker? ", ['', 'Yes', 'No'])
        
        # prompt the user for demographic living region 
        region = st.selectbox("What is your current demographic location? ",['', 'Northwest', 'Northeast', 'Southwest', 'Southeast'])
        
        # prompt the user for number of children living in the same household
        children = st.number_input("What is the total number of children living in the same household? ", min_value = 0, format = "%d")
       
        # prompt the user to click on the button to perform prediction 
        predict_button = st.form_submit_button("Predict")
        
        # only if the button is true, the perform the following task 
        if predict_button:
            if sex == '' or smoker == '' or region == '' or bmi < 1.00:
                st.error("**NOTE:** Please kindly fill up all the **required** fields before submitting it.")
            else:
                # call the function to predict the medical insurance cost 
                predict_medical_insurance_cost = insuranceCostPredict(age, sex, bmi, smoker, region, children)
                
                with st.spinner(text = "On its way..."):
                    time.sleep(6)
                
                # display the prediction medical insurance cost
                st.success("**Result:** Your predicted medical insurance cost is ${:.2f}".format(predict_medical_insurance_cost[0]))
                st.info("**NOTE:** The predicted medical insurance cost shown above is for your own reference. Your actual medical insurance cost may be varied due to certain factors. ")
                st.info("Thank you for using our app! ")
if __name__ == "__main__":
    main()
