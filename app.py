
import os
import pathlib
import shutil
import streamlit as st
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import mimetypes
from functools import wraps
import logging
from PIL import Image

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()

# Initialize Google GenAI client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Constants
MODEL_ID = "gemini-2.0-flash"
CAPTURE_FOLDER = "files"
IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]
NUTRITIONIST_PROMPT = """
Analyze the provided image of a meal and provide a comprehensive nutritional analysis.

Task Requirements:

1. Food Item Identification: Identify and list the individual food items present in the image.
2. Nutritional Breakdown: For each food item, provide the following nutritional information:
    - Calories
    - Fat (total, saturated, and unsaturated)
    - Energy
    - Carbohydrates (%)
    - Protein (%)
    - Other key ingredients (e.g., fiber, sugar, sodium) (%)
3. Total Calories and Macronutrient Analysis: Calculate and report the total calories and macronutrient breakdown (carbohydrates, protein, fat) for the entire meal.
4. Health Rating: Assign a health rating on a scale of 1-10, considering factors such as nutrient balance, calorie density, and presence of essential vitamins and minerals. Provide a justification for the assigned health rating.
5. Recommendations for Improvement: Suggest specific replacements or additions to the meal to improve its nutritional quality and health rating. Estimate the revised health rating if these recommendations are implemented.

Input Requirements:

- Image of a meal ( photograph or digital image)

Output Requirements:

- A comprehensive report including:
    - Food item identification and listing
    - Nutritional breakdown for each food item
    - Total calories and macronutrient analysis
    - Health rating and justification
    - Recommendations for improvement and revised health rating

Evaluation Metrics:

- Accuracy of food item identification
- Precision of nutritional breakdown and calculations
- Relevance and effectiveness of recommendations for improvement
- Clarity and coherence of the report

Please provide your analysis and report in a clear and concise format.
"""




def generate_response(
    client: genai.Client, model_id: str, contents: list
):
    try:
        response = client.models.generate_content(model=model_id, contents=contents)
        return response
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        st.error("Failed to generate response. Please try again.")
        return None


def detect_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def read_file(filepath: str) -> types.Part:
    try:
        data_bytes = types.Part.from_bytes(
            data=pathlib.Path(filepath).read_bytes(),
            mime_type=detect_mime_type(filepath),
        )
        return data_bytes
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        st.error("Failed to read file. Please try again.")
        return None


def clear_directory(folder_path: str = "files") -> None:
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")


def create_directory(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        st.write("Took: %2.4f sec" % (te - ts))
        return result

    return wrap



# Create a Streamlit interface
st.title("Nutritionist's Corner")

# Add a picture of a Nutritionist at the top
st.image("nutritionist.jpg", width=1000)

# Create a flag to indicate if the file uploads were successful
file_uploaded = False

# Clear the contents of the "files" directory
clear_directory(CAPTURE_FOLDER)

# Create a directory to store the uploaded files
create_directory(CAPTURE_FOLDER)

# Upload the file and read it
file_uploader = st.file_uploader("Upload images of food eaten during the day", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
if file_uploader:
    with st.spinner("Uploading files..."):
        for file in file_uploader:
            file_path = os.path.join(CAPTURE_FOLDER, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            time.sleep(0.1)  # Simulate a progress bar
        file_uploaded = True
        st.success("Files uploaded successfully!")

def display_uploaded_images():
    st.header("Uploaded Images:")
    for file in file_uploader:
        file_path = os.path.join(CAPTURE_FOLDER, file.name)
        image = Image.open(file_path)
        st.image(image, caption=file.name, width=200)

display_uploaded_images()
# Create a button to analyze the uploaded files
if st.button("Analyze"):
    # Call the LLM API to analyze the uploaded files
    # Replace this with your actual LLM API call
    ts = time.time()
    contents = [read_file(os.path.join(CAPTURE_FOLDER, file.name)) for file in file_uploader]
    print(f"Contents: {contents}")
    output = generate_response(
            client, MODEL_ID, [NUTRITIONIST_PROMPT] + contents
        )
    if output:
        st.markdown(f"{output.text}")
    te = time.time()
    st.write("Took: %2.4f sec" % (te - ts))
