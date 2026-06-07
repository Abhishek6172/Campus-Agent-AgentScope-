from database.mongodb import MongoDB


class AcademicTools:

    def __init__(self):

        self.db = MongoDB()

    # -------------------------
    # Resolve Student
    # -------------------------

    def resolve_student_id(
        self,
        student_id=None,
        name=None
    ):

        if student_id:
            return student_id

        if name:

            return (
                self.db
                .get_student_id_by_name(
                    name
                )
            )

        return None

    # -------------------------
    # Results
    # -------------------------

    def get_results(
        self,
        student_id=None,
        name=None
    ):

        student_id = (
            self.resolve_student_id(
                student_id,
                name
            )
        )

        if not student_id:
            return "Student not found"

        return self.db.get_results(
            student_id
        )

    # -------------------------
    # Attendance
    # -------------------------

    def get_attendance(
        self,
        student_id=None,
        name=None
    ):

        student_id = (
            self.resolve_student_id(
                student_id,
                name
            )
        )

        if not student_id:
            return "Student not found"

        return self.db.get_attendance(
            student_id
        )

    # -------------------------
    # Hostel
    # -------------------------

    def get_hostel(
        self,
        student_id=None,
        name=None
    ):

        student_id = (
            self.resolve_student_id(
                student_id,
                name
            )
        )

        if not student_id:
            return "Student not found"

        return self.db.get_hostel(
            student_id
        )

    # -------------------------
    # Leave
    # -------------------------

    def get_leave_records(
        self,
        student_id=None,
        name=None
    ):

        student_id = (
            self.resolve_student_id(
                student_id,
                name
            )
        )

        if not student_id:
            return "Student not found"

        return self.db.get_leave_records(
            student_id
        )