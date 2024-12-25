# 📝 Flask Blog Application

## 🌟 Overview

The **Flask Blog Application** is a feature-rich web platform for blogging. It allows users to create, edit, and delete blog posts, register and log in, leave comments, and interact with posts. The application uses Flask and SQLAlchemy for backend management, Bootstrap for responsive design, and CKEditor for rich-text editing.

---

## 🛠 Features

- **User Management**:
  - Register and log in with secure password hashing.
  - Gravatar integration for user avatars.
  - Role-based access with admin-only permissions.
- **Blog Management**:
  - Create, edit, and delete blog posts.
  - Rich-text editing with CKEditor.
  - Image support for blog posts.
- **Comments**:
  - Add comments to blog posts.
  - Comments tied to user accounts.
- **Responsive Design**:
  - Styled with Bootstrap for seamless user experience on all devices.
- **Contact Form**:
  - Securely sends emails to the blog owner.

---

## 📂 Project Structure

    .
    ├── app.py                 # Main Flask application
    ├── forms.py               # Flask-WTF forms for user input
    ├── templates/             # HTML templates
    │   ├── index.html         # Homepage displaying all posts
    │   ├── about.html         # About page
    │   ├── contact.html       # Contact page
    │   ├── login.html         # Login form
    │   ├── register.html      # Registration form
    │   ├── post.html          # Individual blog post page
    │   ├── make-post.html     # Create and edit blog posts
    ├── static/                # Static assets (CSS, images)
    ├── blog.db                # SQLite database for storing user and blog data
    ├── requirements.txt       # Project dependencies
    ├── README.md              # Project documentation

---

## 🔧 Setup Guide

**Prerequisites**

- Python 3.x installed.
- SMTP credentials for email functionality.

**Installation**

1. Clone this repository:

    ```bash
    git clone https://github.com/matanohana433/flask-blog-application.git
    cd flask-blog-application
    ```

2. Create and activate a virtual environment (optional but recommended):

**Windows:**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

**macOS/Linux:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

   - Create a `.env` file or set variables manually:

    ```plaintext
    SECRET_KEY=your_secret_key
    OWN_EMAIL=your_email_address
    OWN_PASSWORD=your_email_password
    ```

5. Initialize the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

---

## 🚀 Usage

1. **Run the Application**:

    ```bash
    python app.py
    ```

2. **Home Page**:

   - Displays all blog posts with options for viewing, editing, and deleting (admin-only).

3. **User Actions**:

   - Register for an account and log in to leave comments or create posts (admin only).

4. **Admin Features**:

   - Create and edit blog posts using rich-text editing.
   - Delete blog posts.

5. **Contact Form**:

   - Use the contact form to send messages directly to the blog owner.

---

## 🌟 Key Features

1. **User Management**:
   - Secure login and registration with password hashing.
   - Admin-only access to critical features.

2. **Rich-Text Blog Posts**:
   - Create visually appealing posts with CKEditor.

3. **Responsive Design**:
   - Optimized for desktop and mobile devices using Bootstrap.

4. **Email Integration**:
   - Contact form sends secure emails via SMTP.

---

## 🚀 Future Enhancements

1. Add pagination for blog posts on the homepage.
2. Implement category tagging for better post organization.
3. Enable social sharing for blog posts.
4. Add a search feature for finding posts.

---

## 📬 Contact

For questions or collaboration:

- **Email:** matanohana433@gmail.com
- **GitHub:** [matanohana433](https://github.com/matanohana433)

--- 
