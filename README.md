# Placement_Eligibility_Streamlit_Application
## Project Overview

This project is a data-driven Streamlit application designed to filter and identify students eligible for placement based on customizable criteria.

It uses a relational database to store student performance data and applies SQL queries for insights and analytics.

---

## Features

- Dynamic eligibility filtering
- SQL-based analytics insights
- Interactive Streamlit dashboard
- OOP-based modular Python code
- Secure database connection using environment variables

---

## Tech Stack

- Python
- Streamlit
- MySQL / TiDB
- SQL
- Faker (for synthetic data generation)
- Pandas

---

## Database Schema

- Students Table
- Programming Table
- Soft Skills Table
- Placements Table

All tables are connected using `student_id`.

---

## How to Run this Project
### Clone the Repository
git clone https://github.com/MahalakshmiM12/Placement_Eligibility_Streamlit_Application.git
### Navigate to the Project Folder
cd Placement_Eligibility_Streamlit_Application
### Create a Virtual Environment (Recommended)
python -m venv .venv
Activate the environment (Windows):
.venv\Scripts\activate
### Install Required Dependencies
pip install -r requirements.txt
### Configure Environment Variables
Create a .env(secrets.env) file in the project root and add your database credentials:
MYSQL_HOST=your_host
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DB=student_data
MYSQL_PORT=4000
Ensure that db_connection.py reads these environment variables correctly.
### Create Database Tables
Execute the schema file:
mysql -u your_user -p student_data < db_schema.sql
Or run the SQL file manually in your MySQL/TiDB client.
### Insert Synthetic Data
python faker_data/data_generator.py
This will populate all four tables with realistic sample data.
### Run the Streamlit Application
streamlit run app.py
The application will be available at:
http://localhost:8501
Open the URL in your browser to access the dashboard.
