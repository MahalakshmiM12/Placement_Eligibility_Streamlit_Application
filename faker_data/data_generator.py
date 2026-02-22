from faker import Faker
import random
from db_connection import get_connection


class PlacementDataGenerator:
    def __init__(self, num_students=500):
        self.num_students = num_students
        self.fake = Faker('en_IN')

        # DB connection
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # ---------------- STUDENTS ----------------
    def create_students(self):
        data = []

        for i in range(1, self.num_students + 1):
            enrollment_year = random.randint(2020, 2025)

            data.append((
                i,
                self.fake.unique.name(),
                random.randint(18, 25),
                random.choice(['Male', 'Female', 'Other']),
                self.fake.email(),
                self.fake.phone_number(),
                enrollment_year,
                f'Batch_{random.randint(1, 10)}',
                self.fake.city(),
                enrollment_year + random.randint(3, 4)
            ))

        query = """
        INSERT INTO students
        (student_id, name, age, gender, email, phone,
         enrollment_year, course_batch, city, graduation_year)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.executemany(query, data)
        self.conn.commit()
        print(f"Inserted {len(data)} students.")

    # ---------------- PROGRAMMING ----------------
    def create_programming(self):
        data = []

        for i in range(1, self.num_students + 1):
            data.append((
                i, i,
                random.choice(['Python', 'SQL', 'Java', 'C++']),
                random.randint(50, 500),
                random.randint(5, 20),
                random.randint(1, 5),
                random.randint(0, 3),
                random.randint(70, 100)
            ))

        query = """
        INSERT INTO programming
        (programming_id, student_id, language, problems_solved,
         assessments_completed, mini_projects, certifications_earned, latest_project_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.executemany(query, data)
        self.conn.commit()
        print(f"Inserted {len(data)} programming records.")

    # ---------------- SOFT SKILLS ----------------
    def create_soft_skills(self):
        data = []

        for i in range(1, self.num_students + 1):
            data.append((
                i, i,
                random.randint(60, 100),
                random.randint(60, 100),
                random.randint(60, 100),
                random.randint(60, 100),
                random.randint(60, 100),
                random.randint(60, 100)
            ))

        query = """
        INSERT INTO soft_skills
        (soft_skill_id, student_id, communication, teamwork, presentation,
         leadership, critical_thinking, interpersonal_skills)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.executemany(query, data)
        self.conn.commit()
        print(f"Inserted {len(data)} soft skill records.")

    # ---------------- PLACEMENTS ----------------
    def create_placements(self):
        data = []
        statuses = ['Ready', 'Not Ready', 'Placed', 'Seeking']
        
        self.cursor.execute("SELECT student_id FROM students")
        student_ids = [row[0] for row in self.cursor.fetchall()] 

        for i in range(1, self.num_students + 1):
            status = random.choice(statuses)

            data.append((
                i, i,
                random.randint(50, 100),
                random.randint(0, 3),
                status,
                self.fake.company() if status == 'Placed' else None,
                round(random.uniform(50000, 150000), 2) if status == 'Placed' else None,
                random.randint(1, 5),
                self.fake.date_this_year() if status == 'Placed' else None
            ))

        query = """
        INSERT INTO placements
        (placement_id, student_id, mock_interview_score, internships_completed,
         placement_status, company_name, placement_package,
         interview_rounds_cleared, placement_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.executemany(query, data)
        self.conn.commit()
        print(f"Inserted {len(data)} placement records.")


    # ---------------- GENERATE ALL ----------------
    def generate_all(self):
        students_df = self.create_students()
        programming_df = self.create_programming()
        soft_skills_df = self.create_soft_skills()
        placements_df = self.create_placements()

        # close DB
        self.cursor.close()
        self.conn.close()


# ---------------- RUN ----------------
if __name__ == "__main__":
    generator = PlacementDataGenerator(num_students=500)
    generator.generate_all()
