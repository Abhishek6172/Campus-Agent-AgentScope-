import re

from utils.yaml_loader import YAMLLoader
from tools.finance_tools import FinanceTools


class FinanceAgent:

    def __init__(self):

        self.tools = FinanceTools()

        self.planner = YAMLLoader.load_yaml(
            "planners/finance_planner.yaml"
        )

    # -------------------------
    # Extract Student ID
    # -------------------------

    def extract_student_id(
        self,
        query
    ):

        match = re.search(
            r"S\d+",
            query,
            re.IGNORECASE
        )

        if match:
            return match.group().upper()

        return None

    # -------------------------
    # Extract Teacher ID
    # -------------------------

    def extract_teacher_id(
        self,
        query
    ):

        match = re.search(
            r"T\d+",
            query,
            re.IGNORECASE
        )

        if match:
            return match.group().upper()

        return None

    # -------------------------
    # Main Reply
    # -------------------------

    def reply(
        self,
        query
    ):

        tool = YAMLLoader.get_tool(
            query,
            "planners/finance_planner.yaml"
        )

        if not tool:

            return (
                "FinanceAgent could not "
                "find a suitable tool."
            )

        # -------------------------
        # Fee Details
        # -------------------------

        if tool == "get_fee_details":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_fee_details(
                student_id
            )

        # -------------------------
        # Fee Status
        # -------------------------

        if tool == "get_fee_status":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_fee_status(
                student_id
            )

        # -------------------------
        # Pending Fee
        # -------------------------

        if tool == "get_pending_fee":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_pending_fee(
                student_id
            )

        # -------------------------
        # Salary
        # -------------------------

        if tool == "get_salary":

            teacher_id = self.extract_teacher_id(
                query
            )

            return self.tools.get_salary(
                teacher_id
            )

        # -------------------------
        # Payroll
        # -------------------------

        if tool == "get_payroll":

            teacher_id = self.extract_teacher_id(
                query
            )

            return self.tools.get_payroll(
                teacher_id
            )

        return (
            "FinanceAgent could not "
            "process the query."
        )