import gradio as gr
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_bytes
import pytesseract
import google.generativeai as genai
import io

# === Gemini API Key ===
genai.configure(api_key="AIzaSyBdXC98bPh_t8ZpvyOZzsX-hXaEQykodX8")
vision_model = genai.GenerativeModel("gemini-1.5-flash")

# === OCR Helper ===
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# === Gemini Vision Summary ===
def gemini_understand_image(image):
    try:
        response = vision_model.generate_content([
            "Describe or summarize the contents of this image clearly.",
            image
        ])
        return response.text.strip()
    except Exception as e:
        return f"⚠ Gemini Vision Error: {e}"

# === Main Processor ===
def process_file(file_bytes):
    try:
        # Wrap bytes into a stream
        byte_stream = io.BytesIO(file_bytes)

        # Try to open as image
        try:
            image = Image.open(byte_stream)
            ocr_text = extract_text_from_image(image).strip()
            gemini_summary = gemini_understand_image(image)

            return f"""🖼 Image Analysis:
🔹 OCR Text:
{ocr_text or '[No text found]'}

🔹 Gemini Vision:
{gemini_summary or '[No output]'}"""

        except UnidentifiedImageError:
            # Not image → treat as PDF
            pages = convert_from_bytes(file_bytes, dpi=300)
            result = ""
            for i, page in enumerate(pages):
                ocr_text = extract_text_from_image(page).strip()
                gemini_summary = gemini_understand_image(page)
                result += f"""\n📄 Page {i+1}:
🔹 OCR Text:
{ocr_text or '[No text found]'}

🔹 Gemini Vision:
{gemini_summary or '[No output]'}\n"""
            return result.strip()

    except Exception as e:
        return f"❌ Error while processing: {str(e)}"

# === Gradio UI ===
with gr.Blocks() as demo:
    gr.Markdown("## 🔍 Gemini Vision + OCR Tool\nUpload a PDF or Image")
    with gr.Row():
        file_input = gr.File(label="Upload File", type="binary")
        output = gr.Textbox(label="Output", lines=30)
    btn = gr.Button("Analyze")

    btn.click(fn=process_file, inputs=file_input, outputs=output)

demo.launch(share=True)