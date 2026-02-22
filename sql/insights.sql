-- 1. Students of every batch
SELECT * FROM students WHERE course_batch = 'Batch_1';

-- 2. Top 5 students whose age is more than 20
SELECT * FROM students WHERE age > 20 LIMIT 5;

-- 3. chennai students
SELECT * FROM students WHERE city = 'Chennai';

-- 4. Placed students
SELECT * FROM placements WHERE placement_status = 'Placed';

-- 5. Students who learned Python 
SELECT * FROM programming WHERE language = 'Python';

-- 6. Students who solved more than 50 problems
SELECT * FROM programming WHERE problems_solved > 50;

-- 7. Students whose communication skills are more than 80
SELECT * FROM soft_skills WHERE communication > 80;

-- 8. Students whose have done more than 2 interships
SELECT * FROM placements WHERE internships_completed > 2;

-- 9. Students who will graduate in 2026
SELECT * FROM students WHERE graduation_year = 2026;

-- 10. Female students
SELECT * FROM students WHERE gender = 'Female';
