Gemini Vision + OCR Tool
A powerful web-based tool that lets you analyze any image or PDF to extract text (OCR) and summarize the visual content using Google Gemini Vision. This app is built with Gradio for a simple, interactive UI. No machine learning experience required—just upload your file and receive instant results!

🚦 How it works
text
graph TD
    A[User Uploads Image or PDF] --> B{File Type?}
    B -- Image --> C[OCR via pytesseract]
    B -- PDF --> D[Convert each page to image]
    D --> C
    C --> E[Summarize with Gemini Vision API]
    E --> F[Show OCR Text & AI Summary in App]
Upload an image:

Extracts text using OCR (pytesseract).

Sends the image to Google Gemini Vision API for description/summary.

Upload a PDF:

Converts every page to an image.

Applies OCR and Gemini Vision to each page.

Displays results page-wise.

📦 Key Features
Image & Multi-page PDF support (auto-detection)

Accurate OCR (pytesseract)

Smart AI-powered summaries (Google Gemini Vision)

Fast, simple UI (Gradio)

Handles errors, provides clear feedback


