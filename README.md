# 📇 Contact Manager (Python – OOP Edition)

A clean and professional **command-line Contact Manager** built with Python using **Object-Oriented Programming (OOP)** principles.

This project demonstrates strong fundamentals in Python, clean code practices, file handling, validation, and defensive programming.

---

## 🚀 Features

- ✅ Add new contacts
- 📄 View all saved contacts
- 🔍 Search for a contact by name
- 🗑️ Delete contacts
- 💾 Persistent storage using a text file
- 🧠 OOP design with clear separation of concerns
- 🛡️ Input validation & error handling
- 📂 Handles malformed file data safely

---

## 🧱 Project Structure


---

## 🧠 Design Overview

### Contact
- Represents a single contact (name + phone)
- Validates input
- Converts data to/from file format

### ContactManager
- Handles all file operations (CRUD)
- Prevents duplicate contacts
- Safely loads valid contacts only

### CLI Interface
- User-friendly menu
- Graceful error handling
- Clean output formatting

---

## ▶️ How to Run

### Requirements
- Python **3.9+**

### Run the app
```bash
python contact_manager.py
