import gradio as gr
import os
import fitz  # PyMuPDF for PDF text extraction
import pytesseract
from PIL import Image
from resume_maker import server

def extract_text_from_file(file_obj):
    if file_obj is None:
        return ""
    name = file_obj.name
    ext = os.path.splitext(name)[-1].lower()
    # PDF
    if ext == ".pdf":
        text = ""
        with fitz.open(file_obj.name) as doc:
            for page in doc:
                text += page.get_text()
        return text
    # Image
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        image = Image.open(file_obj.name)
        text = pytesseract.image_to_string(image)
        return text
    # Text
    elif ext in [".txt"]:
        with open(file_obj.name, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""

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
    # Step 1: Extract user resume/skills text
    user_text = extract_text_from_file(user_file)
    if not user_text.strip():
        return "Could not extract text from the uploaded file. Please upload a valid resume or skills file."
    # Step 2: Summarizer/refinement step
    summary = summarizer_tool(user_text, job_description, custom_instructions)
    # Step 3: Use the summary to generate the resume
    # In a real scenario, you would parse the summary and call the appropriate server tools
    # For demonstration, we call header_details_latex and professional_summary_latex with dummy data
    try:
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
        # For demo, just return the generated LaTeX file
        with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt", "r", encoding="utf-8") as f:
            latex_resume = f.read()
        # Return both the summary and the LaTeX resume for transparency
        return f"{summary}\n\n\n=== Generated Resume (LaTeX) ===\n\n{latex_resume}"
    except Exception as e:
        return f"Error generating resume: {str(e)}"

with gr.Blocks(title="AI Resume Generator") as demo:
    gr.Markdown("# AI Resume Generator\nUpload your resume/skills, paste a job description, and add custom instructions to generate a tailored resume.")
    with gr.Row():
        user_file = gr.File(label="Upload Resume/Skills (PDF, Text, or Image)", file_types=[".pdf", ".txt", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"])
        job_description = gr.Textbox(label="Job Description", lines=8, placeholder="Paste the job description here...")
    custom_instructions = gr.Textbox(label="Custom Instructions", lines=4, placeholder="E.g., Focus on leadership, highlight cloud experience, etc.")
    generate_btn = gr.Button("Generate Resume")
    output = gr.Textbox(label="Refined Summary and Generated Resume (LaTeX)", lines=30)
    generate_btn.click(
        fn=generate_resume,
        inputs=[user_file, job_description, custom_instructions],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()

