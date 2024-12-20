import streamlit as st

from vertexai.preview.generative_models import GenerativeModel, Image  # Importing GenerativeModel and Image classes
import vertexai  # Importing Vertex AI SDK
import tempfile  # For creating temporary files and directories
import os  # For interacting with the operating system

PROJECT_ID = "xxxxxxx"  # Your Vertex AI project ID
REGION = "us-central1"  # Region where your Vertex AI resources are located

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=REGION)

def generate_response(prompt, image_file):
    """
    Function to generate response based on a prompt and an image.

    Parameters:
    - prompt: The text prompt for generating the response.
    - image_file: The image file to be used in generating the response.

    Returns:
    - The generated response.
    """
    # Load the image from file
    image = Image.load_from_file(image_file)



    # Initialize the GenerativeModel with a specific model
    model = GenerativeModel("gemini-1.0-pro-vision")

    # Generate content based on the prompt and image
    response = model.generate_content([prompt, image])

    # Return the generated response
    return response.candidates[0].content.text

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
