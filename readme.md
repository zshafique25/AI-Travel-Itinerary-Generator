# AI Travel Itinerary Generator

This project is a travel itinerary generator specifically designed for creating detailed travel plans for trips in Pakistan. The generator uses Cohere's AI model to craft itineraries based on user input, considering travel times, routes, local events, national holidays, and other essential factors.

## Features

- Create realistic and well-organized itineraries.
- Calculate travel times and suggest feasible routes.
- Provide detailed daily activities and sightseeing spots.
- Include accommodation details for each night.
- Highlight local events and festivals.
- Recommend local cuisine and dining options.
- Consider road conditions and possible delays.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/zshafique25/AI-Travel-Itinerary-Generator.git
    cd AI-Travel-Itinerary-Generator
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your Cohere API key:
    ```bash
    export COHERE_API_KEY='your_cohere_api_key'  # On Windows, use set COHERE_API_KEY=your_cohere_api_key
    ```

5. Set up your Gemini API key:
    ```bash
    export GEMINI_API_KEY='your_gemini_api_key'  # On Windows, use set GEMINI_API_KEY=your_gemini_api_key
    ```

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run MusafirAI.py
    ```

2. Open your browser and go to `http://localhost:8501` to use the travel itinerary generator.

## File Structure

- **MusafiirAI.py**: Contains the Streamlit app code for the user interface.
- **cohere_model.py**: Contains the code for interacting with the Cohere AI model to generate itineraries.

## Roadmap for the Travel Itinerary Generator App

### Current Features

**User Interface:**
- Step-by-step form to gather trip details:
  - Travel locations
  - Starting location
  - Starting date
  - Number of nights
  - Accommodation type
  - Trip type (Adventure or Laid-back)
  - Group size
- Custom CSS for styling:
  - Background color
  - Text color
  - Font size
  - Button styling
  - Footer design

**Backend:**
- **CohereModel** class for interacting with Cohere API:
  - Initializing Cohere client
  - Creating prompts for itinerary generation
  - Generating itineraries using Cohere AI

**PDF Generation:**
- Functionality to generate a PDF of the itinerary:
  - Custom header with a logo
  - Itinerary content with a disclaimer note
  - Download button for the PDF

**Session Management:**
- Handling user responses and session state:
  - Storing responses for each question
  - Navigating between questions
  - Generating and displaying the final itinerary

## Demo

[Watch the demo video](https://drive.google.com/file/d/117h3zaSv9ILCyDr5XDRpLRNV3FBUKzIw/view?usp=sharing)
