# ClickShare

ClickShare is a **real-time file sharing web application** built using Django and WebSockets. It allows users to upload and share files, while other connected users receive updates instantly without refreshing the page.

---

## Features

* File upload and download
* Real-time updates using WebSockets
* Multiple users can access shared files
* Basic user authentication

---

## Tech Stack

**Backend**

* Python
* Django
* Django Channels
* WebSockets

**Frontend**

* HTML
* CSS
* JavaScript

**Database**

* SQLite

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/Shivanii30/ClickShare.git
cd ClickShare
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---
