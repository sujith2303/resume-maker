# server.py
from typing import Any,List
import httpx
from mcp.server.fastmcp import FastMCP


base_resume_latex_file = r"""
%-------------------------
% Resume in Latex
% Author : Sujith
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}
% \usepackage{charter}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

"""


# Initialize FastMCP server
mcp = FastMCP("resume")


@mcp.tool()
def header_details_latex(name: str, mobile_number: str, email_id: str, linkedin_profile_link : str, github_link: str) -> str:
    """
    Generates header details of the person. It will display the name, mobile_number, email_id, linkedin profile and github profile
    
    Args:
        name(str): Name of the candidate
        mobile_number(str): Mobile number of the candidate
        email_id(str): email_id
        linkedin_profile_link(str): Linkedin profile link of the candidate.
        github_link(str): github link of the candidate.
    
    Returns:
        str: Instruction for the next steps
    """
    header_latex = r""" 

            \begin{center}
                \textbf{\Huge \scshape """
    header_latex+= name + r"""} \\ \vspace{1pt}
                \small""" + mobile_number + r""" $|$ \href{mailto:x@x.com}{\underline{"""
    header_latex+= email_id + r"""}} $|$ 
                \href{https://linkedin.com/in/...}{\underline{"""
    header_latex+=linkedin_profile_link + r"""}} $|$
    \href{https://github.com/...}{\underline{"""
    header_latex+=github_link + r"""}}
\end{center}


"""
    with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt","w") as f:
        f.write(base_resume_latex_file + header_latex)
    return "Now call professional_summary_latex_tool"
    
@mcp.tool()
def professional_summary_latex(summary: str) -> str:
    """
    Creates a Professional Experience summary section of the candidate. 
    
    Args:
        summary (str): The generated summary should be in less than 4 lines. It should follow the STAR method while generating the summary. It should speak about the experience and the role he is applying for.
        (e.g: Accomplished Gen AI Specialist with expertise in machine learning (ML), deep learning (DL), generative AI, and AI Agents, proficient in end-to end development from design to deployment. Skilled in problem-solving, data structures and algorithms (DSA), strong analytical abilities, and debugging complex systems. Passionate about optimizing ML model performance to deliver efficient, high-impact AI solutions. Adept at leveraging the full AI stack to drive innovation and achieve business objectives in fast-paced, technology-focused environments)
    
    
    Returns:
        str: Instruction for the next steps
    """
    summary_latex = """
    
    \section{Professional Summary}
    """
    summary_latex += rf"""
    {{{summary}}}
    """
    summary_latex = summary_latex.replace("%","\%")
    with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt","a") as f:
        f.write(summary_latex)
    return "Now call the experience_latex_tool"



@mcp.tool()
def experience_latex(experiences: List[dict]) -> str:
    """
   Creates an Experience section for a user.Processes the user work experiences across different companies and generates a string in latex form which will be used in further steps

    Args:
        experiences (list of dict): A list where each dict contains:
            - company_name (str): Name of the company.
            - place (str): Location of the company.
            - period (str): Employment duration (e.g., "Jan 2020 - Dec 2022").
            - role (str): Title or designation.
            - bullet_points (list of str): Key achievements/responsibilities. These points must be in ATS friendly format, quantifying things and  following the STAR method(situation, task , action and result)(eg. reduced latency by 5ms, improved accuracy by 50%).

    Returns:
        str: Instruction for the next steps
    """
    Experience_latex = r"""
    
    \section{Professional Experience}
    \resumeSubHeadingListStart
    """
    for exp in experiences:
        company = exp['company_name']
        period  = exp['period']
        place   = exp['place']
        role    = exp['role']
        bullet_points = exp['bullet_points']
        Experience_latex += rf"""
            \resumeSubheading
              {{{role}}}{{{period}}}
              {{{company}}}{{{place}}}
              \resumeItemListStart
              
            """
        for item in bullet_points:
            Experience_latex += rf"""
            \resumeItem{{{item}}}
            """
        Experience_latex += r"""
        \resumeItemListEnd
        """
    Experience_latex += r"""
    \resumeSubHeadingListEnd
    """
    Experience_latex = Experience_latex.replace("%","\%")
    with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt",'a') as f:
        f.write(Experience_latex)
    # print(Experience_latex)
    return "Now call the education_latex tool"

@mcp.tool()
def projects_latex(projects: List[dict]) -> str :
    """
    Creates an projects section for a user. Processes the projects and generates a string in latex form which will be used in further steps

    Args:
        projects (list of dict): A list where each dict contains:
            - project_name (str): Name of the project.
            - tools_used (list[str]): Tools and technologies used in the project (eg Python, Flask, React, PostgreSQL, Docker). It is a list of strings.
            - period (str): Employment duration (e.g., "Jan 2020 - Dec 2022").
            - role (str): Title or designation.
            - bullet_points (list of str): Key achievements/responsibilities.These points must be in ATS friendly format, quantifying things and  following the STAR method(situation, task , action and result)(eg. reduced latency by 5ms, improved accuracy by 50%).

    Returns:
        str: Instruction for the next steps
    """
    Projects_latex = r"""
    
    \section{Projects}
    \resumeSubHeadingListStart
    """
    for project in projects:
        project_name = project['project_name']
        period = project['period']
        tools = ", ".join(project['tools_used'])
        role = project['role']
        bullet_points = project['bullet_points']
        
        Projects_latex += rf"""
        \resumeProjectHeading
            {{\textbf{{{project_name}}} \textit{{| {tools}}}}}{{}}
        \resumeItemListStart"""
        
        for item in bullet_points:
            Projects_latex += rf"""\resumeItem{{{item}}}"""
            
        Projects_latex += r"""\resumeItemListEnd"""
        
    Projects_latex += r"""\resumeSubHeadingListEnd"""
    Projects_latex = Projects_latex.replace("%","\%")
    
    with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt",'a') as f:
        f.write(Projects_latex)
        
    return "Now call the skills_latex tool"

@mcp.tool()
def education_latex(education : List[dict]) -> str:
    """
    Generates an Education section for the candidate. It generates a string which will be processed in the further steps.

    Args:
        experiences (list of dict): A list where each dict contains:
            - Institute (str): Name of the Institute.
            - place (str): Location of the Institute.
            - period (str): Education duration (e.g., "Jan 2020 - Dec 2022").
            - specialization (str): Specialization of education (e.g., "Bachelors in computer science", "Intermediate", "High School")

    Returns:
        str: Instruction for the next steps
    """
    Education_latex = r"""
    
    \section{Education}
    \resumeSubHeadingListStart
    """
    for edu in education:
        institute_name = edu["Institute"]
        place = edu["place"]
        period = edu["period"]
        specialization = edu["specialization"]
        studies = rf"""
        \resumeSubheading
            {{{institute_name}}}{{{place}}}
            {{{specialization}}}{{{period}}}
        """
        Education_latex+=studies
    Education_latex = Education_latex.replace("%","\%")
    with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt",'a') as f:
        f.write(Education_latex)
    return "Created a file in you pc"


@mcp.tool()
def skills_latex(Programming_languages : List[str], Technologies : List[str], other_skills: dict) -> str:
    """
    Generates an technical skills section for the candidate.It includes programming langugage the candidate is aware of, frameworks, developer tools, technologies. It generates a string which will be processed in the further steps.

    Args:
        Programming_languages (list of strings): contains a list of all the programming languages the candidate is aware of and the new job is expecting. (eg. Python,java,js, HTML, CSS)
        Technologies (list of strings): contains a list of all the technologies which are relevant to the Job description as well as the technologies which the candidate is aware of.
        other_skills (dict): Contains a list of keyworded arguments specifying more about the skills. Each key is the heading like ML Framworks, Developer tools,etc and the values are a list of strings containing the details. Here is an example (eg. kwargs = {"Frameworks": ["React", "Node.js", "Express.js", "UIKit", "SwiftUI", ".NET Core"],"ML Frameworks & tools":[ TensorFlow, PyTorch, Hugging Face, LangChain, Llama Index, JAX, ML Flow, Chroma DB, CrewAI, Numpy,Databricks, Pandas, Hadoop, Pyspark, scikit-learn]})
    Returns:
        str: Instruction for the next steps
    """

    skills_latex = r"""
    
    \section{Technical Skills}
    \begin{itemize}[leftmargin=0.15in, label={}]
        \small{\item{
            \textbf{Languages}{: """ + ", ".join(Programming_languages) + r"""} \\
            \textbf{Technologies}{: """ + ", ".join(Technologies) + r"""}
            """

    for category, items in other_skills.items():
        skills_latex += rf""" \\
            \textbf{{{category}}}{{{": " + ", ".join(items)}}}
            """

    skills_latex += r"""
        }}
    \end{itemize}
    """

    with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt",'a') as f:
        f.write(skills_latex)
    return "Now call the achievements_latex"

@mcp.tool()
def achievements_latex(achievements : List[str]) -> str:
    """
    Generates an achievements section for the candidate's resume in LaTeX format.

    Args:
        achievements (List[str]): List of achievement strings to be included in the resume

    Returns:
        str: Instruction for the next steps
    """
    achievements_latex = r"""
    
    \section{Achievements}
    \resumeItemListStart"""

    for achievement in achievements:
        achievements_latex += rf"""
        \resumeItem{{{achievement}}}"""
        
    achievements_latex += r"""
    \resumeItemListEnd

    \end{document}
    """
    achievements_latex = achievements_latex.replace("%","\%")

    with open(r"D:\PC_Downloads\OpenSource\ResumeMaker\MCP_Server\resume_maker\resume.txt",'a') as f:
        f.write(achievements_latex)
    return "Created a file in your pc"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')