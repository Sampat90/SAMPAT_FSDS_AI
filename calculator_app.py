import streamlit as st

st.title("Simple Calculator")

# Input fields for numbers
num1 = st.number_input("Enter first number", value=0.0, format="%.2f")
num2 = st.number_input("Enter second number", value=0.0, format="%.2f")

# Select operation
operation = st.selectbox("Select operation", ("Add", "Subtract", "Multiply", "Divide"))

result = None
error = None

if st.button("Calculate"):
    try:
        if operation == "Add":
            result = num1 + num2
        elif operation == "Subtract":
            result = num1 - num2
        elif operation == "Multiply":
            result = num1 * num2
        elif operation == "Divide":
            if num2 == 0:
                error = "Error: Division by zero!"
            else:
                result = num1 / num2
    except Exception as e:
        error = f"An error occurred: {e}"

    if error:
        st.error(error)
    else:
        st.success(f"Result: {result}")

st.markdown("---")
st.caption("Made with Streamlit") 