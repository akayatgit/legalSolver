import os
import json
import cv2
import PyPDF2
import docx
import pytesseract
import nltk
import torch
import uuid
import shutil
from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertForSequenceClassification
from db_connection import check_user_credentials, register_user, initialize_database, save_document_history, get_user_documents, get_document_by_id, get_user_id
from email_service import send_emails_for_analysis

# Download necessary NLTK resources
nltk.download("punkt")

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Initialize the database
initialize_database()

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the 'documents' directory exists for permanent storage
DOCUMENTS_FOLDER = os.path.join("static", "documents")
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)
app.config["DOCUMENTS_FOLDER"] = DOCUMENTS_FOLDER

# Load IPC Sections JSON File
try:
    with open("ipc_sections.json", "r", encoding="utf-8") as file:
        ipc_data = json.load(file)
except FileNotFoundError:
    ipc_data = []

# Load Pretrained Tamil BERT Model
tokenizer = BertTokenizer.from_pretrained("google/muril-base-cased")  # BERT for Tamil & English
model = BertForSequenceClassification.from_pretrained("google/muril-base-cased")

# TF-IDF Vectorizer for Machine Learning Analysis
tfidf_vectorizer = TfidfVectorizer()
ipc_texts = [section["description"]["en"] for section in ipc_data]  # Extract text for training
tfidf_vectorizer.fit(ipc_texts)  # Fit only once

# Function to Extract Text from Files
def extract_text(file_path, file_ext):
    text = ""

    try:
        if file_ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        elif file_ext == ".pdf":
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

        elif file_ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join(para.text for para in doc.paragraphs)

        elif file_ext in [".jpg", ".jpeg", ".png"]:
            text = perform_ocr(file_path)

    except Exception as e:
        print(f"Error extracting text: {e}")

    return text.strip()

# Function to Perform OCR on Images
def perform_ocr(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="eng+tam")  # English & Tamil OCR
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

# Function to Analyze Petition using TF-IDF & BERT
def analyze_petition(petition_text):
    """Analyze the petition text and identify relevant IPC sections"""
    # Preprocess the text
    petition_text = petition_text.lower()
    
    # Vectorize the petition text
    petition_vector = tfidf_vectorizer.transform([petition_text])
    
    # Calculate similarity with each IPC section
    relevant_sections = []
    
    for section in ipc_data:
        # Check if any keywords are present in the petition
        keyword_match = any(keyword.lower() in petition_text for keyword in section["keywords"])
        
        # If keywords match, add to relevant sections
        if keyword_match:
            relevant_sections.append(section)
    
    # Sort by priority
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    relevant_sections.sort(key=lambda x: priority_order.get(x["priority"], 4))
    
    return relevant_sections

# Route to Upload and Analyze Petition
@app.route("/upload", methods=["POST"])
def upload():
    # Check if user is logged in
    if "username" not in session:
        flash("Please log in to upload documents", "error")
        return redirect(url_for("login"))
    
    # Check if file was uploaded
    if "document" not in request.files:
        flash("No file selected", "error")
        return redirect(url_for("home"))
    
    file = request.files["document"]
    
    # Check if file is empty
    if file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("home"))
    
    # Generate a unique filename
    original_filename = file.filename
    file_ext = os.path.splitext(original_filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    # Save the file temporarily
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    file.save(temp_path)
    
    # Extract text from the document
    extracted_text = extract_text(temp_path, file_ext)
    
    if not extracted_text:
        flash("Could not extract text from the document", "error")
        os.remove(temp_path)  # Clean up
        return redirect(url_for("home"))
    
    # Analyze the petition
    analysis_results = analyze_petition(extracted_text)
    
    # Save the document permanently
    permanent_path = os.path.join(app.config["DOCUMENTS_FOLDER"], unique_filename)
    shutil.copy2(temp_path, permanent_path)
    
    # Save to database - convert analysis_results to JSON string
    username = session["username"]
    doc_id = save_document_history(username, original_filename, permanent_path, json.dumps(analysis_results))
    
    # Send emails to relevant departments
    sent_departments = []
    found_departments = []
    if analysis_results:
        # Get unique departments from analysis results
        found_departments = set(section.get("department") for section in analysis_results if section.get("department"))
        
        # Get user_id from session
        user_id = session.get("user_id")
        print(f"User ID from session: {user_id}")
        
        if not user_id:
            user_id = get_user_id(username)
            print(f"User ID from database: {user_id}")
            
            # Store user_id in session for future use
            if user_id:
                session["user_id"] = user_id
        
        if user_id:
            success, sent_departments = send_emails_for_analysis(
                user_id, 
                original_filename, 
                permanent_path, 
                analysis_results
            )
            print(f"Email sending result: {success}, Departments: {sent_departments}")
        else:
            print("Could not determine user_id for email sending")
    
    # Clean up temporary file
    os.remove(temp_path)
    
    # Redirect to email notification page if emails were sent
    if sent_departments:
        return redirect(url_for("email_notification", doc_id=doc_id, departments=",".join(sent_departments)))
    elif found_departments:
        # Departments were found but emails couldn't be sent
        return redirect(url_for("email_error", doc_id=doc_id, departments=",".join(found_departments)))
    else:
        flash("Document analyzed but no relevant departments found", "info")
        return redirect(url_for("view_analysis", doc_id=doc_id))

@app.route("/email_notification")
def email_notification():
    """Show email notification dialog"""
    # Check if user is logged in
    if "username" not in session:
        return redirect(url_for("login"))
    
    doc_id = request.args.get("doc_id")
    departments_str = request.args.get("departments", "")
    departments = departments_str.split(",") if departments_str else []
    
    # URL to redirect to after clicking OK
    redirect_url = url_for("view_analysis", doc_id=doc_id)
    
    return render_template("email_notification.html", departments=departments, redirect_url=redirect_url)

@app.route("/email_error")
def email_error():
    """Show email error dialog when departments were found but emails couldn't be sent"""
    # Check if user is logged in
    if "username" not in session:
        return redirect(url_for("login"))
    
    doc_id = request.args.get("doc_id")
    departments_str = request.args.get("departments", "")
    departments = departments_str.split(",") if departments_str else []
    
    # URL to redirect to after clicking OK
    redirect_url = url_for("view_analysis", doc_id=doc_id)
    
    return render_template("email_error.html", departments=departments, redirect_url=redirect_url)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get user's document history
    documents = get_user_documents(session['username'])
    return render_template('history.html', username=session['username'], documents=documents)

@app.route('/download/<doc_id>')
def download_document(doc_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get document details
    document = get_document_by_id(doc_id)
    if not document:
        flash('Document not found.')
        return redirect(url_for('history'))
    
    # Check if the file exists
    file_path = document['file_path']
    if not os.path.exists(file_path):
        flash('Document file not found.')
        return redirect(url_for('history'))
    
    # Return the file for download
    return send_file(file_path, as_attachment=True, download_name=document['original_filename'])

@app.route('/view_analysis/<doc_id>')
def view_analysis(doc_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get document details
    document = get_document_by_id(doc_id)
    if not document:
        flash('Document not found.')
        return redirect(url_for('history'))
    
    # Extract text from the document
    file_path = document['file_path']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if not os.path.exists(file_path):
        flash('Document file not found.')
        return redirect(url_for('history'))
    
    try:
        petition_text = extract_text(file_path, file_ext)
        
        # Parse the JSON analysis results
        analysis_results_json = document['analysis_results']
        try:
            analysis_results = json.loads(analysis_results_json)
        except json.JSONDecodeError:
            analysis_results = analysis_results_json  # Use as is if not valid JSON
        
        return render_template('home.html', username=session['username'], 
                              petition_text=petition_text, 
                              analysis_results=analysis_results,
                              from_history=True)
    except Exception as e:
        flash(f'Error viewing document: {str(e)}')
        return redirect(url_for('history'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        full_name = request.form['full_name']
        
        # Validate passwords match
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")
        
        # Register the user
        success, message = register_user(username, password, email, full_name)
        
        if success:
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', error=message)
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = check_user_credentials(username, password)
        if user:
            session['username'] = username
            session['user_id'] = user[0]  # Store user_id in session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)



