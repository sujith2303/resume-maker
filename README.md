# AI Resume Generator

## Description

<<<<<<< HEAD
The AI Resume Generator is a tool designed to help users tailor their resumes to specific job descriptions. It takes an existing resume or skills document, a job description, and any custom instructions, then (currently in a simulated way) processes this information to generate a LaTeX-formatted resume.
=======
The AI Resume Generator is a tool designed to help users tailor their resumes to specific job descriptions. It takes an existing resume or skills document, a job description, and any custom instructions, then uses Google's Gemini LLM to process this information and generate content for a LaTeX-formatted resume.
>>>>>>> feat/productionize-ui-mejoras

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python:** Python 3.10 or newer (as specified in `pyproject.toml`). You can download it from [python.org](https://www.python.org/downloads/).
*   **Tesseract OCR Engine:** Tesseract is required for extracting text from image-based resumes.
    *   It must be installed on your system.
    *   The Tesseract executable must be in your system's PATH.
    *   Installation instructions can be found here: [Tesseract OCR Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html).
<<<<<<< HEAD
=======
*   **Google AI API Key:** To use the resume tailoring features, you'll need an API key for Google's Generative AI services (Gemini). You can obtain one from [Google AI Studio](https://aistudio.google.com/).
>>>>>>> feat/productionize-ui-mejoras
*   **(Optional) Git:** Required if you want to clone the repository. You can download it from [git-scm.com](https://git-scm.com/downloads).

## Setup & Installation

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd resume-maker # Or your project's root directory name
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.

    *   On macOS and Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```

3.  **Install Dependencies:**
<<<<<<< HEAD
    This project uses `uv` for fast dependency management, as indicated by the presence of `uv.lock` and a modern `pyproject.toml`. If you don't have `uv` installed, you can install it first:
    ```bash
    pip install uv
    ```
    Then, install the project dependencies:
=======
    This project uses `uv` for fast dependency management. If you don't have `uv` installed, you can install it first:
    ```bash
    pip install uv
    ```
    Then, install all project dependencies (including `google-generativeai` and others specified in `pyproject.toml`):
>>>>>>> feat/productionize-ui-mejoras
    ```bash
    uv pip install .
    ```
    This command reads the `pyproject.toml` file, resolves dependencies, and installs them into your virtual environment.

## Running the Application

1.  **Start the Gradio Application:**
    Once the setup is complete, you can run the application using the following command from the project's root directory:
    ```bash
    python app.py
    ```
    This will launch the Gradio web interface, and you should see a local URL (e.g., `http://127.0.0.1:7860`) in your terminal. Open this URL in your web browser.

2.  **Note on the Server:**
<<<<<<< HEAD
    The application uses a FastMCP server (`server.py`) for its backend logic (like LaTeX generation). `app.py` imports and uses `server.py` as a library. You do **not** need to run `server.py` as a separate process for this application to work.
=======
    The application uses a FastMCP server component (`server.py`) for its LaTeX generation logic. `app.py` imports and uses `server.py` as a library. You do **not** need to run `server.py` as a separate process for this application to work.
>>>>>>> feat/productionize-ui-mejoras

## How to Use

The application interface is straightforward:

1.  **Upload Resume/Skills:** Click the "Upload Resume/Skills" button to upload your existing resume or a document listing your skills. Supported formats are PDF, TXT, and images (PNG, JPG, JPEG, BMP, TIFF).
2.  **Job Description:** Paste the full job description into the "Job Description" textbox.
<<<<<<< HEAD
3.  **Custom Instructions:** In the "Custom Instructions" textbox, you can add specific requests, such as skills to emphasize or areas to focus on (e.g., "Focus on leadership," "Highlight cloud experience").
4.  **Generate Resume:** Click the "Generate Resume" button. The application will process your inputs and generate a tailored resume.
5.  **View Output:** The "Output: Tailored Resume (LaTeX) and Summary" textbox will display:
    *   A summary section (currently simulated, showing extracted content and inputs).
    *   The generated resume in LaTeX format.
    You can use the copy button on this textbox to easily copy the entire output.
6.  **Clear Fields:** The "Clear Inputs & Output" button can be used to reset all input fields and the output area for a new session.
=======
3.  **LLM API Key:** Enter your Google AI API Key in the 'LLM API Key (Optional)' field. This key is required to connect to the Gemini model for content generation.
4.  **Custom Instructions:** In the "Custom Instructions" textbox, you can add specific requests, such as skills to emphasize or areas to focus on (e.g., "Focus on leadership," "Highlight cloud experience").
5.  **Generate Resume:** Click the "Generate Resume" button. The application will process your inputs and generate a tailored resume.
6.  **View Output:** The "Output: Tailored Resume (LaTeX) and Summary" textbox will display:
    *   The tailored resume content generated by Google's Gemini LLM based on your inputs and the system's predefined instructions. The output is presented in LaTeX format.
    You can use the copy button on this textbox to easily copy the entire output.
7.  **Clear Fields:** The "Clear Inputs & Output" button can be used to reset all input fields and the output area for a new session.

## Core Logic: LLM Integration

This application leverages Google's Gemini model (specifically `gemini-1.5-flash-latest` as configured in `app.py`) to perform the core resume tailoring. When you provide your resume, job description, custom instructions, and API key, this information is processed and sent to the Gemini LLM.

The LLM is guided by a detailed system prompt (defined in `resume-maker-prompt.mdc`). This prompt instructs the LLM on the context of resume writing, the desired tone, ATS optimization strategies, and most importantly, the specific tools and the JSON format it must use for its output.

The LLM's response is expected to be a JSON object where keys are tool names (e.g., `Header_details_latex`, `Professional_summary_latex`) and values are dictionaries of arguments for those tools. The `app.py` script then parses this JSON and sequentially calls the corresponding functions in `server.py` to construct the final LaTeX document.
---

## Future Enhancements

Here are some potential areas for future development and improvement:

*   **LaTeX to PDF Compilation:** Implement functionality to compile the generated LaTeX code into a PDF document directly within the application and offer it as a download.
*   **Support for Multiple LLM Providers:** Allow users to choose from different Large Language Model providers (e.g., OpenAI, Anthropic) or specific models, potentially by configuring different API keys and endpoints through the UI.
*   **Advanced LLM Output Parsing & Error Recovery:** Enhance the robustness of parsing LLM responses. This could involve implementing more sophisticated validation of the JSON structure and developing strategies for retrying LLM calls or correcting outputs that don't perfectly adhere to the requested format.
*   **Enhanced UI/UX:** Further improve the user interface and experience, for example, by adding a live preview of the resume as it's being constructed or providing more interactive ways to edit or refine the LLM-generated content for each section.
*   **Template Customization:** Allow users to select from a variety of resume templates or even customize aspects of the LaTeX template being used to alter the visual style of the generated resume.
*   **Automated Testing:** Develop a comprehensive suite of automated tests (unit tests, integration tests) to ensure the application's stability, verify the correctness of outputs, and facilitate easier refactoring and future development.
*   **Session Management/History:** Allow users to save and revisit previous generation attempts or manage multiple versions of their resume.
*   **Direct LaTeX Editing:** Provide an option for users familiar with LaTeX to directly edit the generated LaTeX code before finalization.
---
>>>>>>> feat/productionize-ui-mejoras
