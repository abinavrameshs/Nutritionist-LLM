# Nutritionist-LLM
Analyze the provided image of a meal and provide a comprehensive nutritional analysis.

## Overview
Nutritionist-LLM is a Streamlit application that leverages Google's GenAI to analyze images of meals and provide detailed nutritional information. The application identifies food items in the image, breaks down their nutritional content, and offers health ratings and recommendations for improvement.

## Features
- Food Item Identification: Detects and lists individual food items present in the image.
- Nutritional Breakdown: Provides detailed nutritional information for each food item, including calories, fat, energy, carbohydrates, protein, and other key ingredients.
- Total Calories and Macronutrient Analysis: Calculates and reports the total calories and macronutrient breakdown for the entire meal.
- Health Rating: Assigns a health rating on a scale of 1-10 based on nutrient balance, calorie density, and essential vitamins and minerals.
- Recommendations for Improvement: Suggests specific replacements or additions to improve the meal's nutritional quality and health rating.

## Setup

This project is initialized using `pdm`. To learn more about `pdm`, please refer to the [pdm documentation](https://pdm-project.org/en/latest/).

### Installation Steps

1. **Install `pdm`**:
    ```sh
    pip install pdm
    ```

2. **Initialize the project**:
    ```sh
    pdm init
    ```

3. **Install the required dependencies**:
    ```sh
    pdm install
    ```

4. **Create a [.env](http://_vscodecontentref_/2) file** in the root of your repository and include the following:
    ```env
    GOOGLE_API_KEY=<YOUR_API_KEY>
    ```
## Running the Application

To run the Streamlit application, use the following command:
```sh
pdm run streamlit run app.py
```

## References

- [Google API Docs](https://ai.google.dev/gemini-api/docs/document-processing?lang=python)
- [Streamlit Documentation](https://docs.streamlit.io/)
