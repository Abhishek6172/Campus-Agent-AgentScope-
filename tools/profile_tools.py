from database.mongodb import MongoDB


class ProfileTools:

    def __init__(self):

        self.db = MongoDB()

    # -------------------------
    # Student
    # -------------------------

    def get_student_profile(
        self,
        student_id=None,
        name=None
    ):

        student = self.db.find_student(
            student_id or name
        )

        if not student:

            return (
                f"Student not found: "
                f"{student_id or name}"
            )

        return student

    # -------------------------
    # Teacher
    # -------------------------

    def get_teacher_profile(
        self,
        teacher_id=None,
        name=None
    ):

        teacher = self.db.find_teacher(
            teacher_id or name
        )

        if not teacher:

            return (
                f"Teacher not found: "
                f"{teacher_id or name}"
            )

        return teacher

    # -------------------------
    # Teacher Subject
    # -------------------------

    def get_teacher_subject(
        self,
        teacher_id=None,
        name=None
    ):

        teacher = self.db.find_teacher(
            teacher_id or name
        )

        if not teacher:

            return (
                f"Teacher not found: "
                f"{teacher_id or name}"
            )

        return {
            "teacher_id":
            teacher.get(
                "teacher_id"
            ),

            "name":
            teacher.get(
                "name"
            ),

            "course":
            teacher.get(
                "course"
            )
        }

    # -------------------------
    # Public Person
    # -------------------------

    def get_public_person(
        self,
        person_id
    ):

        person = self.db.get_public_person(
            person_id
        )

        if not person:

            return (
                f"{person_id} not found"
            )

        return person

    def search_public_person(
        self,
        name
    ):

        person = (
            self.db
            .get_public_person_by_name(
                name
            )
        )

        if not person:

            return (
                f"{name} not found"
            )

        return person

    # -------------------------
    # Compare People
    # -------------------------

    def compare_people(
        self,
        person_1,
        person_2
    ):

        p1 = (
            self.db
            .get_public_person_by_name(
                person_1
            )
        )

        p2 = (
            self.db
            .get_public_person_by_name(
                person_2
            )
        )

        if not p1:

            return (
                f"{person_1} not found"
            )

        if not p2:

            return (
                f"{person_2} not found"
            )

        return {
            "person_1": p1,
            "person_2": p2
        }