import re

from utils.yaml_loader import YAMLLoader
from tools.academic_tools import AcademicTools


class AcademicAgent:

    def __init__(self):

        self.tools = AcademicTools()

        self.planner = YAMLLoader.load_yaml(
            "planners/academic_planner.yaml"
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
    # Extract Department
    # -------------------------

    def extract_department(
        self,
        query
    ):

        departments = [
            "CSE",
            "ECE",
            "ME",
            "CE"
        ]

        for dept in departments:

            if dept.lower() in query.lower():
                return dept

        return None

    # -------------------------
    # Extract Day
    # -------------------------

    def extract_day(
        self,
        query
    ):

        days = {
            "monday": "Mon",
            "tuesday": "Tue",
            "wednesday": "Wed",
            "thursday": "Thu",
            "friday": "Fri"
        }

        query = query.lower()

        for day, value in days.items():

            if day in query:
                return value

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
            "planners/academic_planner.yaml"
        )

        if not tool:

            return (
                "AcademicAgent could not "
                "find a suitable tool."
            )

        # -------------------------
        # SGPA
        # -------------------------

        if tool == "get_sgpa":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_sgpa(
                student_id
            )

        # -------------------------
        # Results
        # -------------------------

        if tool == "get_results":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_results(
                student_id
            )

        # -------------------------
        # Academic Summary
        # -------------------------

        if tool == "get_academic_summary":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_academic_summary(
                student_id
            )

        # -------------------------
        # Attendance
        # -------------------------

        if tool == "get_attendance":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_attendance(
                student_id
            )

        # -------------------------
        # Hostel
        # -------------------------

        if tool == "get_hostel_details":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_hostel_details(
                student_id
            )

        # -------------------------
        # Leave
        # -------------------------

        if tool == "get_leave_records":

            student_id = self.extract_student_id(
                query
            )

            return self.tools.get_leave_records(
                student_id
            )

        # -------------------------
        # Timetable
        # -------------------------

        if tool == "get_timetable":

            department = self.extract_department(
                query
            )

            day = self.extract_day(
                query
            )

            if day:

                return self.tools.get_day_timetable(
                    department,
                    day
                )

            return self.tools.get_timetable(
                department
            )

        return (
            "AcademicAgent could not "
            "process the query."
        )