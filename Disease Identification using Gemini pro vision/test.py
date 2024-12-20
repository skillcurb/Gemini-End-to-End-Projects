import streamlit as st
import tempfile  # For creating temporary files and directories
import os  # For interacting with the operating system
from pathlib import Path
import google.generativeai as genai

genai.configure(api_key="AIzaSyAqrgSAAPBvmVXsSTJdrTDO-ZEppyY-IeA")
def generate_response(prompt, image_file):
   # Set up the model
    generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    
    image_parts = [
  {
    "mime_type": "image/jpeg",
    "data": image_file.read_bytes()
  },
]
    prompt_parts = [
    image_parts[0],
    "Identify the disease this person might have based on the provided image. Also provide details of the disease",
    ]

    response = model.generate_content(prompt_parts)
    return(response.text)

def main():
 st.title('Disease Identification')

 

 img = st.file_uploader("Choose an image...", type=["png","jpg","jpeg"])

 # If an image is uploaded
 if img: 
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp() 
    # Define the path to save the uploaded image
    path = os.path.join(temp_dir, img.name) 
    # Write the uploaded image to the specified path
    with open(path, "wb") as f:
        f.write(img.getvalue())

 # Input area for user's question
 st.header(":violet[Question]")
 question = st.text_area(label="Enter your question")
 submit = st.button("Submit")
    
 # If a question is entered and submitted
 if question and submit:
    # Generate a response based on the question and uploaded image
    response = generate_response(question, path)
    # Display the generated response
    st.header("Answer")
    st.write(response)

# Entry point of the script
if __name__ == "__main__":
    main()
