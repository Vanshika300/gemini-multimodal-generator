🤖 Gemini Multimodal Content Generator
A Streamlit web application that leverages the Google Gemini API to generate various forms of content, including natural language text, optimized prompts for AI image generators, and text-to-speech audio. This tool simplifies the content creation process by harnessing advanced generative AI capabilities.

✨ Features
Text Generation: Generate creative and informative text based on user prompts using different Gemini models (Flash, Pro).

Image Prompt Optimization: Transform simple ideas into detailed, high-quality prompts optimized for popular AI image generators (e.g., DALL-E, Midjourney, Stable Diffusion).

Audio Generation (Text-to-Speech): Convert written text into natural-sounding audio in multiple languages using gTTS.

Multi-Modal Generation: Generate text, image prompts, and audio all at once from a single comprehensive prompt.

Interactive UI: User-friendly and responsive interface built with Streamlit.

API Key Management: Securely handles API keys using environment variables.

🚀 Technologies Used
Python

Streamlit: For building the interactive web application.

Google Generative AI (Gemini API - gemini-1.5-flash, gemini-1.5-pro, gemini-1.0-pro): The core LLM for text and prompt generation.

gTTS (Google Text-to-Speech): For converting text into audio.

tempfile & os: For managing temporary audio files.

python-dotenv: For loading environment variables securely.

📸 Screenshots
(Note: Replace these placeholders with actual screenshots of your running application. If you place them in a screenshots folder, update the paths like screenshots/your_screenshot_name.png)

Main Interface:
A screenshot showing the main tabs for content generation.

Text Generation Example:
A screenshot of the text generation tab with generated content.

Image Prompt Generation Example:
A screenshot of the image prompt generation tab with an optimized prompt.

Audio Generation Example:
A screenshot of the audio generation tab with the audio player.

⚙️ How to Run Locally
Follow these steps to set up and run the Gemini Multimodal Content Generator on your local machine.

1. Prerequisites
   Python 3.8+: Ensure you have Python installed.

Google Gemini API Key: Obtain an API key from Google AI Studio.

2. Clone the Repository
   git clone https://github.com/your-username/gemini-multimodal-generator.git
   cd gemini-multimodal-generator

(Replace your-username with your actual GitHub username.)

3. Configure API Key
   Create a file named .env in the root directory of your project (the same directory as gemini_multimodal_app.py). Add your Google Gemini API key to it:

GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY"

Important: Replace "YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY" with your real key. This file is ignored by Git and will not be uploaded to GitHub, keeping your key secure.

4. Install Dependencies
   It's highly recommended to use a virtual environment:

# Create a virtual environment

python -m venv venv

# Activate the virtual environment

# On Windows:

.\venv\Scripts\activate

# On macOS/Linux:

source venv/bin/activate

# Install required Python packages

pip install -r requirements.txt

5. Run the Application
   Once all dependencies are installed and your .env file is configured, run the Streamlit application from your terminal:

streamlit run gemini_multimodal_app.py

This command will open the application in your web browser, usually at http://localhost:8501.

📧 Contact
Feel free to reach out if you have any questions or feedback!

Email: vanshikashukla065@gmail.com

LinkedIn: linkedin.com/in/vanshika-shukla30
