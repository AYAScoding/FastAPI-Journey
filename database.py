from contextlib import contextmanager
import sqlite3

class Database:

    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        # We create both tables to handle the nested Enrolements
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS enrolments (
                enrolement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                semester TEXT NOT NULL,
                student_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def get_all(self) -> list:
        # Rule: SELECT must use positional (?) if parameters were needed, 
        # but here we just fetch all.
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get(self, id: int) -> dict | None:
        # Rule: SELECT must use positional (?)
        self.cur.execute("SELECT * FROM students WHERE student_id = ?", (id,))
        row = self.cur.fetchone()
        if not row:
            return None
        
        student_dict = self._row_to_dict(row)
        
        # Fetch nested enrolments
        self.cur.execute("SELECT * FROM enrolments WHERE student_id = ?", (id,))
        enrolment_rows = self.cur.fetchall()
        student_dict["enrolements"] = [
            {"enrolement_id": r[0], "course_name": r[1], "semester": r[2]} 
            for r in enrolment_rows
        ]
        return student_dict

    def create(self, item) -> int:
        # Rule: Use the MAX(id) logic from skeleton
        self.cur.execute("SELECT MAX(student_id) FROM students")
        result = self.cur.fetchone()
        new_id = (result[0] or 0) + 1

        # Rule: INSERT must use Named (:param)
        self.cur.execute("""
            INSERT INTO students (student_id, full_name)
            VALUES (:id, :full_name)
        """, {"id": new_id, "full_name": item.full_name})

        # Insert nested enrolments
        for enrol in item.enrolements:
            self.cur.execute("""
                INSERT INTO enrolments (course_name, semester, student_id)
                VALUES (:course, :sem, :stu_id)
            """, {
                "course": enrol.course_name, 
                "sem": enrol.semester.value, 
                "stu_id": new_id
            })

        self.conn.commit()
        return new_id

    def update(self, id: int, item) -> dict | None:
        # Rule: UPDATE must use Named (:param)
        self.cur.execute("""
            UPDATE students 
            SET full_name = :full_name
            WHERE student_id = :id
        """, {"full_name": item.full_name, "id": id})
        
        # Refresh enrolments (Delete then Insert)
        self.cur.execute("DELETE FROM enrolments WHERE student_id = ?", (id,))
        for enrol in item.enrolements:
            self.cur.execute("""
                INSERT INTO enrolments (course_name, semester, student_id)
                VALUES (:course, :sem, :stu_id)
            """, {
                "course": enrol.course_name, 
                "sem": enrol.semester.value, 
                "stu_id": id
            })

        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        # Rule: DELETE must use positional (?)
        self.cur.execute("DELETE FROM students WHERE student_id = ?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _row_to_dict(self, row) -> dict:
        # Maps the sqlite row tuple to a dictionary
        return {
            "student_id": row[0],
            "full_name": row[1],
            "enrolements": []
        }

@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()
    try:
        yield db
    finally:
        db.close()