# JOB BOARD APPLICATION

This documentation provides an overview of a job board application (linkedin/indeed) . The application is designed to help users find and apply for jobs, with administrative features for job management.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [User Registration and Authentication](#user-registration-and-authentication)
7. [Job Management](#job-management)
8. [Application Submission](#application-submission)
9. [Admin Panel](#admin-panel)
10. [Running the Application](#running-the-application)

## Introduction

This application serves as a platform for users to search for job opportunities and apply for them. It incorporates user registration and authentication, job management, and an admin panel for job administrators.

## Prerequisites

Before setting up and running the application, make sure you have the following prerequisites:

- Python 3.x
- Flask
- Flask-WTF
- Flask-Login
- Flask-Bcrypt
- SQLite (for user management)
- MongoDB (for job data)
- Required Python packages (use `pip install -r requirements.txt`)

## Installation

1. Clone the repository to your local machine.

2. Set up a virtual environment to isolate project dependencies.

3. Install the required packages using `pip install -r requirements.txt`.

## Project Structure

The project is organized as follows:

- `main.py`: The main application file.
- `templates/`: Contains HTML templates for rendering web pages.
- `static/`: Contains static files (e.g., images).

## Configuration

The application relies on environment variables for configuration. These variables should be set in a `.env` file. The following variables are used:

- `SECRET_KEY`: A secret key for securing session data.
- `MONGO_URI`: MongoDB connection URI.
- `SQLITE_DB_PATH`: Path to the SQLite database for user management.

## User Registration and Authentication

### User Registration

- Users can register for an account by accessing the `/signup` route.
- They provide a username, password, and can optionally choose to register as an admin.

### User Authentication

- Users can log in using their registered credentials on the `/login` route.
- User sessions are managed securely using Flask-Login.
- Passwords are hashed for security using Flask-Bcrypt.

## Job Management

- The application allows administrators to add job listings.
- Admins can access the admin panel at `/admin`.
- A form at `/add_job` enables the addition of job listings.

## Application Submission

- Users can view job details on the `/jobs` route and submit applications.
- Job details can be accessed at `/job/<job_id>`, where `job_id` is the unique identifier of the job.
- Users submit applications via a form and are redirected to the job listings page upon successful submission.

## Admin Panel

- The admin panel at `/admin` is accessible only to users with admin privileges.
- Admins can access the job management form at `/add_job` to add new job listings.

## Running the Application

To run the application, execute the following command:

```bash
python app.py
```

By default, the application runs on port 8080 in debug mode. Access the application in your web browser by navigating to `http://localhost:8080`.

