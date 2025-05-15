# 📄 Resume Analyzer Web App

A simple Flask-based web application that allows users to upload their resume (PDF) and input the type of job they are applying for. The system scans the resume, checks if the user is a good fit for the selected job based on keyword matching, and provides a suitability score along with improvement suggestions.

## 🚀 Features

- Upload resume in PDF format
- Choose the job role you're applying for
- Get a **suitability score**
- Receive **custom suggestions** to improve your resume
- Clean and responsive UI for mobile and desktop users

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS (inline in Flask)
- **PDF Parsing**: PyMuPDF (fitz)

## 📦 Requirements

Install dependencies with:

pip install flask pymupdf
