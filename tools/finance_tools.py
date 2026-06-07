from database.mongodb import MongoDB


class FinanceTools:

    def __init__(self):

        self.db = MongoDB()

    # -------------------------
    # Fee Details
    # -------------------------

    def get_fee_details(
        self,
        student_id
    ):

        student = self.db.get_student(
            student_id
        )

        if not student:
            return (
                f"Student {student_id} "
                f"not found"
            )

        return {
            "student_id": student.get(
                "student_id"
            ),
            "name": student.get(
                "name"
            ),
            "fee_total": student.get(
                "fee_total"
            ),
            "fee_paid": student.get(
                "fee_paid"
            ),
            "fee_status": student.get(
                "fee_status"
            )
        }

    # -------------------------
    # Fee Status
    # -------------------------

    def get_fee_status(
        self,
        student_id
    ):

        student = self.db.get_student(
            student_id
        )

        if not student:
            return (
                f"Student {student_id} "
                f"not found"
            )

        return {
            "student_id": student.get(
                "student_id"
            ),
            "name": student.get(
                "name"
            ),
            "fee_status": student.get(
                "fee_status"
            )
        }

    # -------------------------
    # Pending Fee
    # -------------------------

    def get_pending_fee(
        self,
        student_id
    ):

        student = self.db.get_student(
            student_id
        )

        if not student:
            return (
                f"Student {student_id} "
                f"not found"
            )

        fee_total = student.get(
            "fee_total",
            0
        )

        fee_paid = student.get(
            "fee_paid",
            0
        )

        pending_fee = max(
            0,
            fee_total - fee_paid
        )

        return {
            "student_id": student.get(
                "student_id"
            ),
            "name": student.get(
                "name"
            ),
            "fee_total": fee_total,
            "fee_paid": fee_paid,
            "pending_fee": pending_fee
        }

    # -------------------------
    # Payroll
    # -------------------------

    def get_payroll(
        self,
        teacher_id
    ):

        payroll = self.db.get_payroll(
            teacher_id
        )

        if not payroll:
            return (
                f"No payroll record "
                f"found for {teacher_id}"
            )

        return payroll

    # -------------------------
    # Salary
    # -------------------------

    def get_salary(
        self,
        teacher_id
    ):

        payroll = self.db.get_payroll(
            teacher_id
        )

        if not payroll:
            return (
                f"No payroll record "
                f"found for {teacher_id}"
            )

        if "salary" in payroll:

            return {
                "teacher_id": teacher_id,
                "salary": payroll.get(
                    "salary"
                )
            }

        return payroll