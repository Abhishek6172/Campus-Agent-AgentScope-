from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class MongoDB:

    def __init__(self):

        self.client = MongoClient(
            os.getenv("MONGO_URI")
        )

        self.db = self.client[
            os.getenv("DB_NAME")
        ]

        # Collections

        self.student = self.db["student"]

        self.teachers = self.db["teachers"]

        self.semester_results = self.db[
            "semester_results"
        ]

        self.timetable = self.db[
            "timetable"
        ]

        self.attendance = self.db[
            "attendance"
        ]

        self.hostels = self.db[
            "hostels"
        ]

        self.leave_records = self.db[
            "leave_records"
        ]

        self.payroll = self.db[
            "payroll"
        ]

        self.public_people = self.db[
            "public_people"
        ]

    # -------------------------
    # Student
    # -------------------------

    def get_student(self, student_id):

        return self.student.find_one(
            {"student_id": student_id},
            {"_id": 0}
        )

    def get_student_by_name(self, name):

        return self.student.find_one(
            {
                "name": {
                    "$regex": name,
                    "$options": "i"
                }
            },
            {"_id": 0}
        )

    # -------------------------
    # Teacher
    # -------------------------

    def get_teacher(self, teacher_id):

        return self.teachers.find_one(
            {"teacher_id": teacher_id},
            {"_id": 0}
        )

    def get_teacher_by_name(self, name):

        return self.teachers.find_one(
            {
                "name": {
                    "$regex": name,
                    "$options": "i"
                }
            },
            {"_id": 0}
        )

    # -------------------------
    # Results
    # -------------------------

    def get_results(self, student_id):

        return list(
            self.semester_results.find(
                {"student_id": student_id},
                {"_id": 0}
            )
        )

    # -------------------------
    # Timetable
    # -------------------------

    def get_timetable(self, department):

        return list(
            self.timetable.find(
                {"department": department},
                {"_id": 0}
            )
        )

    def get_day_timetable(
        self,
        department,
        day
    ):

        return list(
            self.timetable.find(
                {
                    "department": department,
                    "day": day
                },
                {"_id": 0}
            )
        )

    # -------------------------
    # Attendance
    # -------------------------

    def get_attendance(
        self,
        student_id
    ):

        return self.attendance.find_one(
            {"student_id": student_id},
            {"_id": 0}
        )

    # -------------------------
    # Hostel
    # -------------------------

    def get_hostel(
        self,
        student_id
    ):

        return self.hostels.find_one(
            {"student_id": student_id},
            {"_id": 0}
        )

    # -------------------------
    # Leave
    # -------------------------

    def get_leave_records(
        self,
        student_id
    ):

        return list(
            self.leave_records.find(
                {"student_id": student_id},
                {"_id": 0}
            )
        )

    # -------------------------
    # Payroll
    # -------------------------

    def get_payroll(
        self,
        teacher_id
    ):

        return self.payroll.find_one(
            {"teacher_id": teacher_id},
            {"_id": 0}
        )

    # -------------------------
    # Public People
    # -------------------------

    def get_public_person(
        self,
        person_id
    ):

        return self.public_people.find_one(
            {"person_id": person_id},
            {"_id": 0}
        )

    def get_public_person_by_name(
        self,
        name
    ):

        return self.public_people.find_one(
            {
                "name": {
                    "$regex": name,
                    "$options": "i"
                }
            },
            {"_id": 0}
        )