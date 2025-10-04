# 📘 Question Paper Generator

An AI-powered web application that generates **subjective and objective exam questions** from text or images using **Flask, NLTK, and Tesseract OCR**. Users can customize marks distribution, create multiple-choice questions with auto-generated options, and export the final paper as a **PDF**. Designed to help teachers and students save time and effort in preparing question papers.

---

## 📖 About

The **Question Paper Generator** is a Flask-based web application that leverages **Natural Language Processing (NLP)** and **OCR** to create exam-ready question papers automatically.

It allows users to input text directly or upload an image (from which text is extracted using **Tesseract OCR**) and then generates:

* **Subjective questions** with customizable marks distribution (2, 5, 10 marks)
* **Objective questions (MCQs)** with automatically generated answer options

The application also provides authentication features (register/login), organizes generated questions, and allows users to **download the paper as a PDF**.

---

## ✨ Features

* 🔑 User authentication (Register/Login with SQLite)
* 📝 Generate **Subjective questions** (2, 5, 10 marks)
* 🎯 Generate **Objective questions** (MCQs with auto-generated options)
* 📷 OCR support using **Tesseract** (extracts text from uploaded images)
* 📄 Export generated questions to **PDF**
* 🎨 Simple web interface with Flask templates

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, SQLAlchemy
* **Frontend:** HTML, Jinja2 Templates
* **Database:** SQLite
* **Libraries:**

  * `nltk` (text processing & question generation)
  * `pytesseract` (OCR)
  * `Pillow` (image processing)
  * `xhtml2pdf` (PDF export)

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/question-paper-generator.git
   cd question-paper-generator
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**

   * [Download here](https://github.com/tesseract-ocr/tesseract)
   * Update the Tesseract path in `app.py`:

     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

5. **Initialize the database**

   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   ```

6. **Run the app**

   ```bash
   python app.py
   ```

   Visit: [http://localhost:5000](http://localhost:5000)

---

## 🎯 Usage

1. Register/Login
2. Upload text or an image (to extract text via OCR)
3. Choose question type:

   * Subjective (2, 5, 10 marks)
   * Objective (MCQs)
4. Generate and view the questions
5. Download as PDF

---

## 📂 Project Structure

```
📦 question-paper-generator
 ┣ 📜 app.py               # Flask app with routes
 ┣ 📜 subjective.py        # Subjective question generation logic
 ┣ 📜 objective.py         # Objective question generation logic
 ┣ 📂 templates/           # HTML templates (login, register, results, pdf, etc.)
 ┣ 📂 static/              # Static files (CSS, JS, images)
 ┣ 📜 requirements.txt     # Dependencies
 ┗ 📜 README.md
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo, create a new branch, and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License** – you’re free to use, modify, and distribute it.

---

## 🙌 Acknowledgments

* [NLTK](https://www.nltk.org/) for NLP
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for image-to-text
* [Flask](https://flask.palletsprojects.com/) for the web framework
* [xhtml2pdf](https://xhtml2pdf.readthedocs.io/) for PDF generation
