import mysql.connector
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV SAFELY ----------------

# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build path to secrets.env
env_path = os.path.join(BASE_DIR, "secrets.env")

# Load environment variables
load_dotenv(env_path)


# ---------------- DB CONNECTION FUNCTION ----------------

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            port=int(os.getenv("MYSQL_PORT", 4000)),  # Default TiDB port
            database=os.getenv("MYSQL_DB"),
            use_pure=True
        )

        if connection.is_connected():
            print("Connected to MySQL successfully!")
            return connection

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

db = get_connection()


