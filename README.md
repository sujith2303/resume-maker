# AI Resume Generator

## Description

The AI Resume Generator is a tool designed to help users tailor their resumes to specific job descriptions. It takes an existing resume or skills document, a job description, and any custom instructions, then (currently in a simulated way) processes this information to generate a LaTeX-formatted resume.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python:** Python 3.10 or newer (as specified in `pyproject.toml`). You can download it from [python.org](https://www.python.org/downloads/).
*   **Tesseract OCR Engine:** Tesseract is required for extracting text from image-based resumes.
    *   It must be installed on your system.
    *   The Tesseract executable must be in your system's PATH.
    *   Installation instructions can be found here: [Tesseract OCR Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html).
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
    This project uses `uv` for fast dependency management, as indicated by the presence of `uv.lock` and a modern `pyproject.toml`. If you don't have `uv` installed, you can install it first:
    ```bash
    pip install uv
    ```
    Then, install the project dependencies:
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
    The application uses a FastMCP server (`server.py`) for its backend logic (like LaTeX generation). `app.py` imports and uses `server.py` as a library. You do **not** need to run `server.py` as a separate process for this application to work.

## How to Use

The application interface is straightforward:

1.  **Upload Resume/Skills:** Click the "Upload Resume/Skills" button to upload your existing resume or a document listing your skills. Supported formats are PDF, TXT, and images (PNG, JPG, JPEG, BMP, TIFF).
2.  **Job Description:** Paste the full job description into the "Job Description" textbox.
3.  **Custom Instructions:** In the "Custom Instructions" textbox, you can add specific requests, such as skills to emphasize or areas to focus on (e.g., "Focus on leadership," "Highlight cloud experience").
4.  **Generate Resume:** Click the "Generate Resume" button. The application will process your inputs and generate a tailored resume.
5.  **View Output:** The "Output: Tailored Resume (LaTeX) and Summary" textbox will display:
    *   A summary section (currently simulated, showing extracted content and inputs).
    *   The generated resume in LaTeX format.
    You can use the copy button on this textbox to easily copy the entire output.
6.  **Clear Fields:** The "Clear Inputs & Output" button can be used to reset all input fields and the output area for a new session.
