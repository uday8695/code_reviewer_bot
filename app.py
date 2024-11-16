import google.generativeai as genai
import streamlit as st

# Set up Google Generative AI (GenAI) API key
f = open("keys/gemini.txt")
key = f.read()

# configure the generative ai api keys
genai.configure(api_key=key)

# Title of the app
st.title("GenAI App - AI Code Reviewer")

# subtitle of the app
st.subheader("Please submit your code for expert review and get instant, helpful feedback!")

# Input area for Python code
user_prompt = st.text_area("Enter your Python code here:", placeholder="Paste your code here.....", height = 150)

# Button to generate review when clicked
if st.button("Generate Review"):
    if user_prompt is not None:
            try:
                # initialize the model genai
                model = genai.GenerativeModel("models/gemini-1.5-flash")

                # send the code to the model generator
                ai_assistant = model.start_chat(history = [])

                # generate the chat response
                response = ai_assistant.send_message(f"Please review the following Python code for errors or improvements:\n\n{user_prompt}\n\nProvide feedback and suggest fixes if necessary."
                    )
                
                # Display the subheader in green color
                st.markdown("<h2 style='color: green;'>Corrected Code and Review:</h2>", unsafe_allow_html=True)
                
                # display the chat response
                st.write(response.text)

            except Exception as e:
                 st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter your Python code.")