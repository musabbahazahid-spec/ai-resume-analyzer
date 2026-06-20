from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from app.ai_engine import get_score
import pypdf

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    # Updated form with enctype="multipart/form-data" to allow file uploads
    return """
    <h2>AI Resume Analyzer (Advanced)</h2>

    <form method='post' enctype='multipart/form-data'>
        <b>Upload Resume (PDF only):</b><br>
        <input type="file" name="resume_file" accept=".pdf" required>

        <br><br>
        <b>Job Description:</b><br>
        <textarea name='job' rows='10' cols='50' required></textarea>

        <br><br>
        <button type='submit'>Analyze Resume</button>
    </form>
    """

@app.post("/", response_class=HTMLResponse)
async def analyze(resume_file: UploadFile = File(...), job: str = Form(...)):
    # 1. Read and extract text from the uploaded PDF
    pdf_reader = pypdf.PdfReader(resume_file.file)
    resume_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    # 2. Pass the extracted text and job description to your AI model
    score = get_score(resume_text, job)

    # 3. Return the result
    return f"""
    <h2>Result</h2>
    <h3>Match Score: {round(score, 2)}%</h3>
    <p><i>Successfully extracted and analyzed text from: {resume_file.filename}</i></p>
    <a href='/'>Back</a>
    """