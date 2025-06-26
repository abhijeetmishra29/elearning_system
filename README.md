# 📚 E-Learning System

An online learning platform built with Django that supports instructor-led courses, student enrollment, assignments, grading, and more.

---

## 🚀 Features

- User authentication (register/login/logout)
- Instructor profile & course management
- Student course enrollment
- Assignment creation, submission, and grading
- Bootstrap 4-based responsive UI
- Role-based navigation and permissions

---

## 🛠️ Tech Stack

- Python 3.13
- Django 5.2.3
- SQLite3 (default, easy for development)
- Bootstrap 4 for frontend styling

---

## 🧪 Setup Instructions

### 🔁 Clone the Repository

```bash
git clone https://github.com/abhijeetmishra29/elearning_system.git
cd elearning_system
```

### 🔒 Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔄 Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 👤 Create Superuser (optional)

```bash
python manage.py createsuperuser
```

### ▶️ Run the Development Server

```bash
python manage.py runserver
```

Then open your browser and go to:  
[http://localhost:8000](http://localhost:8000)

---

## 📦 Create `requirements.txt`

If not already present, generate it using:

```bash
pip freeze > requirements.txt
```

---

## 📁 Project Structure (simplified)

```
elearning_system/
├── core/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   └── core/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── elearning_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧑‍💻 Author

**Abhijeet Mishra**  
[GitHub Profile](https://github.com/abhijeetmishra29)
