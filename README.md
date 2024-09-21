# ResumeAI: Resume Parser and Reviewer
<img src="https://github.com/sinanazem/resume-auto-review/blob/main/src/images/banner.png">

ResumeAI is an advanced tool that leverages the power of Large Language Models (LLMs) to analyze and improve resumes. This Streamlit-based application allows users to upload their resumes, optionally provide a job description, and receive detailed analysis and improvement suggestions.

## Features

- **Resume Parsing**: Extracts text from PDF resumes and parses it into a structured format.
- **Resume Review**: Analyzes the parsed resume, considering an optional job description.
- **Section-by-Section Analysis**: Provides a detailed review of each section of the resume.
- **Improvement Suggestions**: Offers revision suggestions with impact levels for each section.
- **Interactive UI**: User-friendly interface with section navigation and side-by-side comparison of original and revised content.

## Installation

### Prerequisites

Ensure you have the following installed on your machine:
- Python 3.7 or higher
- Git

### Steps

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Set environment variables:
   ```sh
   export OPENAI_API_KEY=<your_openai_api_key>
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   ```

2. Run the Streamlit app:
   ```sh
   streamlit run src/app.py --server.enableXsrfProtection false
   ```

3. Open your web browser and navigate to the provided local URL (usually [http://localhost:8501](http://localhost:8501)).

4. Upload your resume PDF file using the file uploader in the sidebar.

5. (Optional) Enter a job description in the text area provided.

6. Click the "Run Analysis" button to start the resume parsing and review process.

7. Navigate through different sections of your resume using the arrow buttons.

8. Review the original content, revised content, and improvement suggestions for each section.

## Project Structure

```
.
├── src/
│   ├── app.py                 # Main Streamlit application file
│   ├── utils/
│   │   ├── pdf.py             # Functions for extracting text from PDF files
│   │   └── llm.py             # Functions for parsing resumes and reviewing them using LLMs
│   ├── resume_formatter.py    # Handles the formatting of resume content for display
│   └── images/
│       └── banner.png         # Banner image for the application
├── requirements.txt           # List of required dependencies
│
└── README.md                  # Project documentation (this file)
```

## Dependencies

- Streamlit
- PyYAML
- (Other dependencies listed in `requirements.txt`)

---

This revision should help new users get up and running quickly and understand the project structure better.
