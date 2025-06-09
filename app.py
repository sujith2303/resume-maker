import gradio as gr
import os
import fitz  # PyMuPDF for PDF text extraction
import pytesseract
from PIL import Image, UnidentifiedImageError # Added UnidentifiedImageError
from resume_maker import server
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def extract_text_from_file(file_obj):
    if file_obj is None:
        logging.info("extract_text_from_file called with no file_obj.")
        return ""

    name = file_obj.name # This is actually the temp file path in Gradio
    logging.info(f"Attempting to extract text from file: {name}")

    # It's better to use file_obj.name directly as Gradio provides a usable path
    # For file operations. The 'name' attribute of the tempfile object is its path.

    ext = os.path.splitext(name)[-1].lower()
    logging.info(f"File extension identified as: {ext}")

    # PDF
    if ext == ".pdf":
        logging.info(f"Processing as PDF: {name}")
        try:
            text = ""
            with fitz.open(name) as doc: # Use 'name' which is the file path
                for page in doc:
                    text += page.get_text()
            if not text.strip():
                message = "Successfully opened PDF, but no text could be extracted. The PDF might be image-based or empty."
                logging.warning(f"PDF processing for {name}: {message}")
                return message
            logging.info(f"Successfully extracted text from PDF: {name}")
            return text
        except fitz.fitz.FZ_ERROR_GENERIC as e: # More specific fitz error
            message = f"Error processing PDF (FZ_ERROR_GENERIC): {e}. The file might be corrupted or not a valid PDF."
            logging.error(f"PDF extraction error for {name}: {message}", exc_info=True)
            return message
        except RuntimeError as e: # fitz can also raise generic RuntimeError for various issues
            message = f"Error processing PDF (RuntimeError): {e}. The file might be corrupted or not a valid PDF."
            logging.error(f"PDF extraction error for {name}: {message}", exc_info=True)
            return message
        except Exception as e:
            message = f"An unexpected error occurred while extracting text from PDF: {e}"
            logging.error(f"PDF extraction error for {name}: {message}", exc_info=True)
            return message
    # Image
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        logging.info(f"Processing as Image: {name}")
        try:
            image = Image.open(name) # Use 'name'
            text = pytesseract.image_to_string(image)
            if not text.strip():
                message = "Successfully opened image, but Tesseract extracted no text. The image might not contain discernible text."
                logging.warning(f"Image processing for {name}: {message}")
                return message
            logging.info(f"Successfully extracted text from Image: {name}")
            return text
        except UnidentifiedImageError:
            message = f"Error processing image: Cannot identify image file. The file at '{name}' might be corrupted or not a supported image format."
            logging.error(f"Image extraction error for {name}: {message}", exc_info=True)
            return message
        except pytesseract.TesseractNotFoundError:
            message = "Error processing image: Tesseract is not installed or not found in your PATH."
            logging.error(f"Image extraction error for {name}: {message}", exc_info=True)
            return message
        except pytesseract.TesseractError as e: # More specific Tesseract error
            message = f"Error processing image with Tesseract: {e}"
            logging.error(f"Image extraction error for {name}: {message}", exc_info=True)
            return message
        except Exception as e:
            message = f"An unexpected error occurred while processing image: {e}"
            logging.error(f"Image extraction error for {name}: {message}", exc_info=True)
            return message
    # Text
    elif ext in [".txt"]:
        logging.info(f"Processing as Text: {name}")
        try:
            with open(name, "r", encoding="utf-8") as f: # Use 'name'
                text = f.read()
            if not text.strip():
                message = "Successfully opened text file, but it appears to be empty."
                logging.warning(f"Text file processing for {name}: {message}")
                return message
            logging.info(f"Successfully extracted text from Text file: {name}")
            return text
        except IOError as e:
            message = f"Error reading text file: {e}"
            logging.error(f"Text file read error for {name}: {message}", exc_info=True)
            return message
        except Exception as e:
            message = f"An unexpected error occurred while reading text file: {e}"
            logging.error(f"Text file read error for {name}: {message}", exc_info=True)
            return message
    else:
        message = f"Unsupported file type: '{ext}'. Please upload a PDF, text file, or image (PNG, JPG, BMP, TIFF)."
        logging.warning(f"Unsupported file type for {name}: {ext}")
        return message

def summarizer_tool(raw_resume_text, job_description, custom_instructions):
    """
    This function represents the summary/refinement step.
    It takes the raw resume text, job description, and custom instructions,
    and returns a refined/structured summary of the user's skills, experience, etc.
    In a real implementation, this would use an LLM or a custom parser.
    Here, we simulate it.
    """
    # For demonstration, just concatenate and label the sections
    summary = (
        "=== Refined Resume Summary ===\n"
        f"Extracted Resume Content:\n{raw_resume_text[:1000]}\n\n"
        f"Job Description:\n{job_description[:1000]}\n\n"
        f"Custom Instructions:\n{custom_instructions}\n"
        "=== End of Summary ==="
    )
    return summary

def generate_resume(user_file, job_description, custom_instructions):
    logging.info(f"generate_resume called. User file: {'present' if user_file else 'not present'}, "
                 f"Job description: {'present' if job_description and job_description.strip() else 'not present'}, "
                 f"Custom instructions: {'present' if custom_instructions and custom_instructions.strip() else 'not present'}")

    # Step 1: Extract user resume/skills text
    user_text_or_error = extract_text_from_file(user_file)

    # Check if extraction itself returned an error message or empty string
    if not user_text_or_error.strip() or user_text_or_error.startswith("Error") or user_text_or_error.startswith("Unsupported") or user_text_or_error.startswith("Successfully opened"):
        # This condition catches:
        # 1. Truly empty extraction (e.g. empty file or file_obj was None)
        # 2. Error messages from extract_text_from_file
        # 3. Informative messages like "Successfully opened PDF, but no text..."
        if not user_text_or_error.strip(): # Actual empty string from failed/empty extraction
            final_message = "Could not extract text from the uploaded file or file is empty. Please upload a valid resume or skills file."
            logging.warning(f"File extraction resulted in empty text. User file: {user_file.name if user_file else 'None'}.")
        else: # It's an error or informative message from extract_text_from_file
            final_message = user_text_or_error
            logging.warning(f"File extraction returned a message: {final_message}")

        logging.info(f"generate_resume returning to UI (extraction issue): {final_message[:200]}...")
        return final_message

    logging.info(f"User text extracted successfully (first 100 chars): {user_text_or_error[:100]}...")
    # Step 2: Summarizer/refinement step
    summary = summarizer_tool(user_text_or_error, job_description, custom_instructions)
    logging.info("Summarizer tool completed.")

    # Step 3: Use the summary to generate the resume
    try:
        logging.info("Calling server tools for LaTeX generation...")
        # Step 3.1: Call header_details_latex (dummy data for demo)
        server.header_details_latex(
            name="John Doe",
            mobile_number="1234567890",
            email_id="john.doe@email.com",
            linkedin_profile_link="https://linkedin.com/in/johndoe",
            github_link="https://github.com/johndoe"
        )
        # Step 3.2: Call professional_summary_latex with a placeholder summary
        server.professional_summary_latex("Professional summary will be generated based on the refined summary and job description.")
        # ... You can add more steps to call experience_latex, projects_latex, etc.

        # Step 3.3: Get the final LaTeX resume from the server
        latex_resume = server.get_final_latex_resume()
        logging.info(f"Successfully retrieved final LaTeX resume from server. Length: {len(latex_resume)}")

        final_output = f"{summary}\n\n\n=== Generated Resume (LaTeX) ===\n\n{latex_resume}"
        logging.info(f"Resume generation successful. generate_resume returning to UI (success): {final_output[:200]}...")
        return final_output
    except Exception as e:
        logging.error(f"Exception during resume generation: {e}", exc_info=True)
        error_message = f"Error generating resume: {str(e)}"
        logging.info(f"generate_resume returning to UI (exception): {error_message[:200]}...")
        return error_message

with gr.Blocks(title="AI Resume Generator") as demo:
    gr.Markdown("# AI Resume Generator\nUpload your resume/skills, paste a job description, and add custom instructions to generate a tailored resume.")
    with gr.Row():
        user_file = gr.File(label="Upload Resume/Skills (PDF, Text, or Image)", file_types=[".pdf", ".txt", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"])
        job_description = gr.Textbox(label="Job Description", lines=8, placeholder="Paste the job description here...")
    custom_instructions = gr.Textbox(label="Custom Instructions", lines=4, placeholder="E.g., Focus on leadership, highlight cloud experience, etc.")

    output = gr.Textbox(label="Output: Tailored Resume (LaTeX) and Summary", lines=30, show_copy_button=True)

    with gr.Row():
        generate_btn = gr.Button("Generate Resume")
        clear_btn = gr.ClearButton(components=[user_file, job_description, custom_instructions, output], value="Clear Inputs & Output")

    generate_btn.click(
        fn=generate_resume,
        inputs=[user_file, job_description, custom_instructions, api_key_textbox],
        outputs=output
    )

if __name__ == "__main__":
    logging.info("Starting Gradio App...")
    demo.launch()

