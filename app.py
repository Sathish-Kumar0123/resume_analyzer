from flask import Flask, request, render_template
import os
import fitz  # PyMuPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Job role keywords database
job_keywords = {
    "data analyst": ["python", "excel", "sql", "power bi", "statistics"],
    "web developer": ["html", "css", "javascript", "react", "node"],
    "java developer": ["java", "spring", "hibernate", "junit"],
    "python developer": ["python", "django", "flask", "pandas", "numpy"],
    "frontend developer": ["html", "css", "javascript", "react", "vue", "bootstrap"],
    "backend developer": ["node", "express", "django", "flask", "java", "sql"],
    "full stack developer": ["html", "css", "javascript", "react", "node", "express", "sql", "mongodb"],
    "tester": ["selenium", "junit", "manual testing", "automation", "bug tracking"],
    "cloud computing": ["aws", "azure", "gcp", "docker", "kubernetes"],
    "ai": ["machine learning", "deep learning", "neural networks", "python", "tensorflow"],
    "ml": ["python", "scikit-learn", "regression", "classification", "clustering"],
    "ds": ["data science", "python", "pandas", "numpy", "visualization", "matplotlib"]
}

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

def get_suitability_score(resume_text, job_role):
    keywords = job_keywords.get(job_role.lower(), [])
    match_count = sum(1 for keyword in keywords if keyword in resume_text)
    score = (match_count / len(keywords)) * 100 if keywords else 0
    suggestions = [kw for kw in keywords if kw not in resume_text]
    return score, suggestions

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>Resume Analyzer</title>
        <style>
            body {
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 400px;
            }
            h2 {
                color: #333;
            }
            input[type="file"], input[type="text"] {
                padding: 10px;
                width: 100%;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Resume Analyzer</h2>
            <form action="/analyze" method="POST" enctype="multipart/form-data">
                <label>Upload your resume (PDF):</label><br>
                <input type="file" name="resume" accept="application/pdf" required><br>
                <label>Job Role:</label><br>
                <input type="text" name="job_role" placeholder="e.g., Data Analyst" required><br>
                <button type="submit">Analyze Resume</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    resume = request.files['resume']
    job_role = request.form['job_role']

    path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    resume.save(path)

    resume_text = extract_text_from_pdf(path)
    score, suggestions = get_suitability_score(resume_text, job_role)

    suggestions_html = '<ul>' + ''.join(f'<li>{s}</li>' for s in suggestions) + '</ul>' if suggestions else '<p>None – Resume is strong!</p>'

    return f'''
    <html>
    <head>
        <title>Result - Resume Analyzer</title>
        <style>
            body {{
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 500px;
            }}
            h2 {{ color: #333; }}
            a {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                background-color: #007bff;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                transition: background-color 0.3s;
            }}
            a:hover {{ background-color: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Suitability Score for '{job_role.title()}': {score:.2f}%</h2>
            <p><strong>Suggestions to Improve:</strong></p>
            {suggestions_html}
            <a href="/">Try another</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
