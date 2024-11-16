import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Google Generative AI (GenAI) API key
f = open("D:/23A55A4405/innomatics/code_reviewer_bot/keys/gemini.txt")
key = f.read()

# Configure the generative AI API keys
genai.configure(api_key=key)

# Title of the app with a clean background and more attractive typography
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #3E7F70;
        text-align: center;
    }
    .subheader {
        font-size: 20px;
        font-weight: 400;
        color: #6C757D;
        text-align: center;
    }
    .body-text {
        font-size: 18px;
        color: #495057;
        text-align: center;
    }
    .input-area {
        margin-bottom: 20px;
    }
    .button {
        background-color: #5F6368;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
    }
    .button:hover {
        background-color: #4C5258;
    }
    .review-output {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e1e1e1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-family: "Courier New", Courier, monospace;
        color: #333;
        font-size: 16px;
        line-height: 1.6;
    }
    .review-output pre {
        background-color: #f1f1f1;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
        font-size: 14px;
    }
    .warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffeeba;
        margin-top: 20px;
    }
    .review-title {
        font-size: 22px;
        font-weight: bold;
        color: #495057;
        margin-bottom: 15px;
    }
    .spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle with Emojis
st.markdown('<div class="title">🤖 AI-Code Reviewer 🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Submit your code for expert review and get instant, helpful feedback! 💻✨</div>', unsafe_allow_html=True)

# Row with Image and Text Side by Side
col1, col2 = st.columns([1, 2])  # Creating two columns
with col1:
    # Adding an Image related to AI/Tech and reducing the size
    image = Image.open("D:/23A55A4405/innomatics/code_reviewer_bot/image.png")  # Replace with your image path
    st.image(image, width=200)  # Reduce image size to 200px width

with col2:
    st.markdown("### 👨‍💻 Select your programming language:")
    languages = ["Python", "JavaScript", "Java", "C++", "Ruby", "Go", "HTML", "CSS", "PHP", "Swift", "Kotlin", "Other"]
    selected_language = st.selectbox("Programming Language:", languages, key="language")

# Row 2: Input area for code with better UI
st.markdown("### 🔧 Enter your code here:")
user_prompt = st.text_area("Paste your code below:", placeholder="Paste your code here.....", height=300, key="code", label_visibility="collapsed")

# Limit the number of characters in the input code to optimize performance
MAX_CODE_LENGTH = 1000  # Set a maximum number of characters
if len(user_prompt) > MAX_CODE_LENGTH:
    user_prompt = user_prompt[:MAX_CODE_LENGTH]  # Truncate the code if it's too long

# Function to detect language based on code
def detect_language_from_code(code):
    if "def " in code or "import " in code:
        return "Python"
    elif "console.log(" in code:
        return "JavaScript"
    elif "public class " in code:
        return "Java"
    elif "#include" in code:
        return "C++"
    elif "puts" in code:
        return "Ruby"
    elif "func " in code:
        return "Go"
    elif "<html>" in code or "<body>" in code:
        return "HTML"
    elif "div" in code:
        return "CSS"
    elif "$" in code:
        return "PHP"
    elif "struct " in code:
        return "Swift"
    elif "fun " in code:
        return "Kotlin"
    else:
        return "Unknown"

# Row 3: Button to generate review with enhanced styling
st.markdown("### ⚡ Click to review your code:")
if st.button("Generate Review ✨", key="generate_review", help="Click to analyze and improve your code!", use_container_width=True):
    if user_prompt and selected_language:
        detected_language = detect_language_from_code(user_prompt)

        # Check if the selected language matches the detected language
        if selected_language != detected_language:
            st.markdown('<div class="warning">⚠️ The selected language (%s) doesn\'t match the code language (%s). Please double-check your code.</div>' % (selected_language, detected_language), unsafe_allow_html=True)

        with st.spinner('Analyzing your code... Please wait. ⏳'):
            try:
                # Initialize the model genai
                model = genai.GenerativeModel("models/gemini-1.5-flash")

                # Send the code to the model generator
                ai_assistant = model.start_chat(history=[])

                # Adjusting the prompt to review code based on the selected language
                review_prompt = f"Please review the following {selected_language} code for errors, improvements, and suggestions. If necessary, provide corrected code and explain the changes:\n\n{user_prompt}\n"

                # Generate the chat response
                response = ai_assistant.send_message(review_prompt)

                # Display the subheader for the review
                st.markdown('<div class="review-title">✅ Corrected Code and Review:</div>', unsafe_allow_html=True)

                # Display the chat response with styled output
                st.markdown(f'<div class="review-output"><pre>{response.text}</pre></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please select a programming language and enter your code.")
