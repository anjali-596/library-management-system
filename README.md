#  Library Management System

A web-based Library Management System built using **Python**, **Flask**, and **Object-Oriented Programming (OOP)** principles.

The application allows administrators to manage books and users, search books by prefix, borrow and return books, and view library records through an intuitive web interface.

---

## Features

### Book Management

* Add new books
* Store book ID, title, and quantity
* View all available books
* Search books by prefix

### User Management

* Register new users
* View all registered users

### Borrowing System

* Borrow books
* Return books
* Track users who currently have borrowed books

### Web Interface

* Responsive UI built with HTML and Tailwind CSS
* Flash messages for operation feedback
* Interactive dashboard for library operations

---

## Technologies Used

* Python
* Flask
* HTML5
* Tailwind CSS
* Object-Oriented Programming (OOP)

---

## Project Structure

```text
Library-Management-System/
│
├── app.py
├── requirements.txt
│
├── backend/
│   ├── admin.py
│   ├── book.py
│   ├── user.py
│   ├── utility.py
│   └── OperationsManager.py
│
├── templates/
│   └── index.html
│
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## OOP Concepts Implemented

* Classes and Objects
* Encapsulation
* Composition
* Modular Programming
* Separation of Concerns

---

## Future Improvements

* Database integration using SQLite or MySQL
* User authentication and authorization
* Book categories and filtering
* Persistent data storage
* Issue and return history tracking
* REST API support

---

## Author

Anjali Chahal

AI & Machine Learning Student | Python Developer | Aspiring AI Engineer

```
```
