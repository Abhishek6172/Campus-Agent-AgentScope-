from database.mongodb import MongoDB


class AcademicTools:

    def __init__(self):

        self.db = MongoDB()

    # -------------------------
    # SGPA / CGPA
    # -------------------------

    def get_sgpa(
        self,
        student_id
    ):

        results = self.db.get_results(
            student_id
        )

        if not results:
            return f"No result found for {student_id}"

        return results

    # -------------------------
    # Semester Results
    # -------------------------

    def get_results(
        self,
        student_id
    ):

        results = self.db.get_results(
            student_id
        )

        if not results:
            return f"No results found for {student_id}"

        return results

    # -------------------------
    # Academic Summary
    # -------------------------

    def get_academic_summary(
        self,
        student_id
    ):

        results = self.db.get_results(
            student_id
        )

        if not results:
            return f"No records found for {student_id}"

        total_sgpa = 0

        for record in results:

            total_sgpa += record.get(
                "sgpa",
                0
            )

        average_sgpa = round(
            total_sgpa / len(results),
            2
        )

        return {
            "student_id": student_id,
            "total_semesters": len(results),
            "average_sgpa": average_sgpa
        }

    # -------------------------
    # Attendance
    # -------------------------

    def get_attendance(
        self,
        student_id
    ):

        attendance = self.db.get_attendance(
            student_id
        )

        if not attendance:
            return f"No attendance found for {student_id}"

        return attendance

    # -------------------------
    # Hostel
    # -------------------------

    def get_hostel_details(
        self,
        student_id
    ):

        hostel = self.db.get_hostel(
            student_id
        )

        if not hostel:
            return f"No hostel record found for {student_id}"

        return hostel

    # -------------------------
    # Leave Records
    # -------------------------

    def get_leave_records(
        self,
        student_id
    ):

        records = self.db.get_leave_records(
            student_id
        )

        if not records:
            return f"No leave records found for {student_id}"

        return records

    # -------------------------
    # Timetable
    # -------------------------

    def get_timetable(
        self,
        department
    ):

        timetable = self.db.get_timetable(
            department
        )

        if not timetable:
            return f"No timetable found for {department}"

        return timetable

    # -------------------------
    # Day Timetable
    # -------------------------

    def get_day_timetable(
        self,
        department,
        day
    ):

        timetable = self.db.get_day_timetable(
            department,
            day
        )

        if not timetable:
            return (
                f"No timetable found for "
                f"{department} on {day}"
            )

        return timetable