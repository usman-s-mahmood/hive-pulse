
# Hive‑Pulse 🎬🧠📰

[![Live Site](https://img.shields.io/badge/Live%20Demo-Hive%20Pulse-brightgreen)](https://hive-pulse-engzc8begwbscgc5.westindia-01.azurewebsites.net/)


**Hive‑Pulse** is a full-stack Django web application that combines an intelligent **movie clustering engine**, a **custom CMS-powered blog**, and a **robust user authentication system** — all built from scratch.

It allows users to search for **movies and TV shows** via the TMDB API, like content they enjoy, and get clustered insights using **KMeans or KNN** machine learning algorithms. It also includes a feature-rich blog section and a secure, production-ready authentication workflow.

---

## 🌐 Live Demo on Azure

🚀 Hive‑Pulse is **deployed on Microsoft Azure** using a robust **CI/CD pipeline powered by GitHub Actions**. Every push to the main branch triggers an automated deployment!

👉 **Visit now**: [https://hive-pulse-engzc8begwbscgc5.westindia-01.azurewebsites.net/](https://hive-pulse-engzc8begwbscgc5.westindia-01.azurewebsites.net/)

> This reflects the live production version with all features enabled, including movie search, clustering, blog system, and full authentication.

---

## 🧩 Features

### 🎞️ Movie Discovery & Clustering

* TMDB API–based movie & TV show search
* Users can **like** content they enjoy
* ML-based clustering using **KMeans or KNN** to group liked content
* Personalized discovery experience powered by unsupervised learning

### 📰 CMS Blog System

* Custom-built **BlogApp** with full CMS capabilities
* Rich-text editing powered by **django-ckeditor**
* Users can read, explore, and comment on posts via **django-comments-dab**

### 🔐 Authentication

* Secure and extendable **AuthApp** built from scratch
* User registration, login/logout, password change
* Built-in Django auth combined with modern security practices

---

## 🗂️ Project Structure (Simplified)

```
HIVE-PULSE/
├── AuthApp/                     # Custom user auth app
├── BlogApp/                     # CMS-style blog app
├── MoviesApp/                   # Movie/TV logic, clustering
├── helpers/
│   └── TMDB_API.py              # TMDB integration
├── HivePulse/                   # Project settings & URLs
├── media/                       # Uploaded media files
├── static/                      # Static assets (CSS, JS)
├── staticfiles/                 # Collected static files
├── templates/                   # Shared templates (implied)
├── .env                         # Environment config
├── requirements.txt             # Dependencies
├── gunicorn_config.py           # Deployment config
├── startup.sh                   # Startup script
├── manage.py
├── tmdb_5000_movies.csv
└── README.md
```

---

## ⚙️ Installation

### 1. Clone & Setup Virtual Environment

```bash
git clone https://github.com/usman-s-mahmood/hive-pulse.git
cd hive-pulse
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create `.env` File

This project relies on several environment variables to run correctly. Here’s a sample:

```
SECRET_KEY="your-django-secret-key"
DEBUG=True

DB_NAME="your-db-name"
DB_USER="your-db-user"
DB_PASSWORD="your-db-password"
DB_HOST="localhost"
DB_PORT="3306"

EMAIL_HOST="smtp.mail.example.com"
EMAIL_HOST_USER="your-email@example.com"
EMAIL_HOST_PASSWORD="your-email-password"

IMAGEKIT_PUB_KEY="your-imagekit-public-key"
IMAGEKIT_PRIV_KEY="your-imagekit-private-key"
IMAGEKIT_URL="https://ik.imagekit.io/your_url"

AIVEN_CA="optional_ca_cert_path"
TMDB="your_tmdb_api_key"
```

---

## 🧠 Clustering Engine

Hive‑Pulse uses **scikit-learn** (optional, added manually or integrated later) to cluster liked movies/TV shows:

* **KMeans**: Groups user favorites into similar clusters
* **KNN**: Finds neighbors based on movie metadata
* Works on the backend once user data reaches a minimum threshold

---

## 📦 Requirements (from `requirements.txt`)

Key dependencies include:

* `Django==5.2.2`
* `django-ckeditor`, `django-comments-dab`
* `dj-static`, `static3`
* `imagekitio`, `pillow`
* `requests`, `python-decouple`
* `gunicorn` (for deployment)
* `PyMySQL` (MySQL support)

> Full list in `requirements.txt`

---

## 🧪 Running the Project Locally

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000)

---

## 💻 Azure Deployment with GitHub CI/CD

* Fully automated deployment using **GitHub Actions**
* Every push to `main` deploys to Azure Web Service
* Uses `gunicorn_config.py` and `startup.sh` for Linux-based deployment
* Ideal for scalable production setups with secure environment variables

---

## 🙌 Contribution

Feel free to fork, clone, and PR! Open issues for suggestions or bugs.

---

## 📄 License

```txt
MIT License

Copyright (c) 2025 Usman Shahid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

Developed by [Usman Shahid](https://github.com/usman-s-mahmood)
Need help or suggestions? Open an issue or contact me via GitHub.

---


