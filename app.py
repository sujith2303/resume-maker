import gradio as gr
import os
import fitz  # PyMuPDF for PDF text extraction
import pytesseract
from PIL import Image, UnidentifiedImageError # Added UnidentifiedImageError
from PIL import Image, UnidentifiedImageError # Added UnidentifiedImageError
from resume_maker import server
import logging
import google.generativeai as genai
import json # For potential future JSON parsing

# Configure basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

SYSTEM_PROMPT = ""
PROMPT_FILE_NAME = "resume-maker-prompt.mdc"

def load_system_prompt():
    """Loads the system prompt from PROMPT_FILE_NAME into the global SYSTEM_PROMPT."""
    global SYSTEM_PROMPT
    try:
        with open(PROMPT_FILE_NAME, "r", encoding="utf-8") as f:
            SYSTEM_PROMPT = f.read()
        if SYSTEM_PROMPT.strip():
            logging.info(f"Successfully loaded system prompt from {PROMPT_FILE_NAME}.")
        else:
            logging.warning(f"{PROMPT_FILE_NAME} was read, but it's empty. SYSTEM_PROMPT is empty.")
            SYSTEM_PROMPT = "System prompt file was empty. Using default behavior." # Or just leave empty
    except FileNotFoundError:
        logging.error(f"System prompt file '{PROMPT_FILE_NAME}' not found. SYSTEM_PROMPT will be empty or default.")
        SYSTEM_PROMPT = f"System prompt file '{PROMPT_FILE_NAME}' not found. Using default behavior."
    except IOError as e:
        logging.error(f"IOError reading system prompt file '{PROMPT_FILE_NAME}': {e}. SYSTEM_PROMPT will be empty or default.", exc_info=True)
        SYSTEM_PROMPT = f"Error reading system prompt file '{PROMPT_FILE_NAME}'. Using default behavior."
    except Exception as e:
        logging.error(f"Unexpected error loading system prompt from '{PROMPT_FILE_NAME}': {e}.", exc_info=True)
        SYSTEM_PROMPT = f"Unexpected error loading system prompt. Using default behavior."

# Load the system prompt when the application starts
load_system_prompt()

def extract_text_from_file(file_obj):
    if file_obj is None:
        logging.info("extract_text_from_file called with no file_obj.")
        logging.info("extract_text_from_file called with no file_obj.")
        return ""

    name = file_obj.name # This is actually the temp file path in Gradio
    logging.info(f"Attempting to extract text from file: {name}")

    # It's better to use file_obj.name directly as Gradio provides a usable path
    # For file operations. The 'name' attribute of the tempfile object is its path.


    name = file_obj.name # This is actually the temp file path in Gradio
    logging.info(f"Attempting to extract text from file: {name}")

    # It's better to use file_obj.name directly as Gradio provides a usable path
    # For file operations. The 'name' attribute of the tempfile object is its path.

    ext = os.path.splitext(name)[-1].lower()
    logging.info(f"File extension identified as: {ext}")

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

def generate_resume(user_file, job_description, custom_instructions, api_key):
    logging.info(f"generate_resume called. User file: {'present' if user_file else 'not present'}, "
                 f"Job description: {'present' if job_description and job_description.strip() else 'not present'}, "
                 f"Custom instructions: {'present' if custom_instructions and custom_instructions.strip() else 'not present'}, "
                 f"API Key: {'provided' if api_key and api_key.strip() else 'not provided'}") # Check if api_key is not just whitespace

    if not api_key or not api_key.strip():
        logging.error("API Key is missing.")
        return "API Key is required for LLM interaction. Please provide a valid API Key."

    if not SYSTEM_PROMPT or SYSTEM_PROMPT.startswith("System prompt file") or SYSTEM_PROMPT.startswith("Error reading system prompt") or SYSTEM_PROMPT.startswith("Unexpected error loading") or SYSTEM_PROMPT.startswith("System prompt file was empty"):
        logging.error(f"System prompt is not loaded correctly. Current status: {SYSTEM_PROMPT if SYSTEM_PROMPT else 'Empty'}")
        return "System prompt is not loaded correctly. Cannot proceed with LLM interaction. Check server logs for prompt file issues."
    else:
        logging.info(f"System Prompt loaded successfully (length: {len(SYSTEM_PROMPT)}).")

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
    # Step 2: Summarizer/refinement step (will be replaced by LLM, but keep its output for now)
    summary_placeholder = summarizer_tool(user_text_or_error, job_description, custom_instructions)
    logging.info("Placeholder summarizer_tool completed.")

    # Step 3: LLM Interaction
    try:
        logging.info("Configuring Gemini API...")
        genai.configure(api_key=api_key)

        logging.info("Initializing Gemini model...")
        # model = genai.GenerativeModel('gemini-pro') # Original suggestion
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using a potentially faster/cheaper model for testing

        user_prompt = (
            f"Here is my resume: {user_text_or_error}\n\n"
            f"Here is the job description: {job_description}\n\n"
            f"Follow these instructions: {custom_instructions}\n\n"
            "Please provide the arguments for each LaTeX tool specified in the system prompt, in JSON format. "
            "The main JSON object should have keys corresponding to each tool name, and the value for each key "
            "should be a dictionary of arguments for that tool. Ensure the JSON is well-formed."
        )

        full_prompt = SYSTEM_PROMPT + "\n\n--- USER REQUEST ---\n\n" + user_prompt

        logging.info(f"Sending prompt to Gemini (User prompt part - first 300 chars): {user_prompt[:300]}...")
        # For very long prompts, consider logging only a summary or specific parts.
        # logging.debug(f"Full prompt to Gemini:\n{full_prompt}") # Potentially too verbose for INFO

        response = model.generate_content(full_prompt)

        llm_raw_output = response.text
        logging.info(f"Raw response from Gemini (first 300 chars): {llm_raw_output[:300]}...")

        # Step 4: Parse LLM Response
        try:
            # Attempt to strip potential markdown ```json ... ```
            if llm_raw_output.strip().startswith("```json"):
                llm_raw_output = llm_raw_output.strip()[7:-3].strip()
            elif llm_raw_output.strip().startswith("```"): # General markdown code block
                 llm_raw_output = llm_raw_output.strip()[3:-3].strip()

            logging.info(f"Attempting to parse LLM JSON response (first 300 chars): {llm_raw_output[:300]}...")
            llm_data = json.loads(llm_raw_output)
            logging.info(f"Successfully parsed LLM JSON response. Keys: {list(llm_data.keys())}")
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing LLM JSON response: {e}. Problematic text (first 500 chars): {llm_raw_output[:500]}", exc_info=True)
            return f"Error parsing LLM response. Expected JSON, but received something else. Raw LLM output (first 200 chars): {llm_raw_output[:200]}"

        # Step 5: Extract Arguments and Call Server Tools
        try:
            logging.info("Extracting arguments and calling server tools...")

            tool_call_order = [
                "Header_details_latex", "Professional_summary_latex", "Experience_latex",
                "Projects_latex", "Skills_latex", "Education_latex", "Achievements_latex"
            ]

            for tool_name in tool_call_order:
                tool_args = llm_data.get(tool_name)
                if tool_args is None:
                    logging.warning(f"No arguments found for tool '{tool_name}' in LLM response. Skipping this tool.")
                    # Decide if this is a critical error or can be skipped. For now, skipping.
                    # Example: if tool_name == "Header_details_latex": raise ValueError("Header details are critical and missing.")
                    continue # Skip to next tool if args are not found

                logging.info(f"Calling {tool_name} with args (keys): {list(tool_args.keys()) if isinstance(tool_args, dict) else 'Not a dict'}")

                # Dynamically get the server function
                server_function = getattr(server, tool_name.lower() + "_tool", None) # Assuming tools are named like header_details_latex_tool in server
                # Correction: server functions are named directly like header_details_latex
                server_function = getattr(server, tool_name.lower(), None)


                if server_function:
                    # Ensure args are a dictionary before unpacking
                    if not isinstance(tool_args, dict):
                        logging.error(f"Arguments for {tool_name} are not a dictionary: {tool_args}. Skipping call.")
                        # Potentially raise an error or return a message
                        return f"Error: LLM provided malformed arguments for tool {tool_name} (expected a dictionary)."

                    server_function(**tool_args) # Unpack dictionary as keyword arguments
                else:
                    logging.error(f"Server function for tool '{tool_name}' not found.")
                    # This indicates a mismatch between prompt and server.py - should be a critical error
                    return f"Error: Server function for tool {tool_name} not found. Cannot proceed."

            logging.info("All server tools called successfully.")

            # Step 6: Get Final LaTeX
            latex_resume = server.get_final_latex_resume()
            logging.info(f"Successfully retrieved final LaTeX resume from server. Length: {len(latex_resume)}")

            final_ui_output = f"LLM-Generated Content (Processed to LaTeX):\n\n=== Generated Resume (LaTeX) ===\n\n{latex_resume}"
            logging.info(f"generate_resume returning to UI (LaTeX success): {final_ui_output[:200]}...")
            return final_ui_output

        except KeyError as e:
            logging.error(f"Missing key in LLM data or tool arguments: {e}", exc_info=True)
            return f"Error processing LLM data: Missing expected key '{e}'. Check LLM output structure."
        except TypeError as e: # Catches errors like trying to unpack non-dict args
            logging.error(f"Type error during server tool call, likely due to incorrect arg structure from LLM: {e}", exc_info=True)
            return f"Error calling server tool due to mismatched arguments: {e}. Check LLM output structure and types."
        except Exception as e: # Catch-all for other errors during tool calls / final LaTeX retrieval
            logging.error(f"Error during server tool execution or final LaTeX retrieval: {e}", exc_info=True)
            return f"Error processing generated content: {str(e)}"

    except Exception as e: # This outer try-except is for the Gemini API call itself
        logging.error(f"Error during Gemini LLM interaction: {e}", exc_info=True)
        error_message = f"Error during LLM interaction: {str(e)}. Please check API key and server logs."
        logging.info(f"generate_resume returning to UI (LLM exception): {error_message[:200]}...")
        return error_message

with gr.Blocks(title="AI Resume Generator") as demo:
    gr.Markdown("# AI Resume Generator\nUpload your resume/skills, paste a job description, and add custom instructions to generate a tailored resume.")
    with gr.Row():
        user_file = gr.File(label="Upload Resume/Skills (PDF, Text, or Image)", file_types=[".pdf", ".txt", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"])
        job_description = gr.Textbox(label="Job Description", lines=8, placeholder="Paste the job description here...")
    custom_instructions = gr.Textbox(label="Custom Instructions", lines=4, placeholder="E.g., Focus on leadership, highlight cloud experience, etc.")
    api_key_textbox = gr.Textbox(label="LLM API Key (Optional)", type="password", placeholder="Enter your LLM API key if needed for summarization/refinement...")

    output = gr.Textbox(label="Output: Tailored Resume (LaTeX) and Summary", lines=30, show_copy_button=True)

    with gr.Row():
        generate_btn = gr.Button("Generate Resume")
        clear_btn = gr.ClearButton(components=[user_file, job_description, custom_instructions, api_key_textbox, output], value="Clear Inputs & Output")

    generate_btn.click(
        fn=generate_resume,
        inputs=[user_file, job_description, custom_instructions, api_key_textbox],
        outputs=output
    )

if __name__ == "__main__":
    logging.info("Starting Gradio App...")
    logging.info("Starting Gradio App...")
    demo.launch()

