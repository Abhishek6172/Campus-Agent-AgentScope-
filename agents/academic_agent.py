import re

from agentscope.agent import AgentBase
from agentscope.message import Msg

from utils.yaml_loader import YAMLLoader
from tools.academic_tools import AcademicTools


class AcademicAgent(AgentBase):

    def __init__(self):

        super().__init__()

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
    # AgentScope Reply
    # -------------------------

    async def reply(
        self,
        msg: Msg
    ) -> Msg:

        query = msg.content

        tool = YAMLLoader.get_tool(
            query,
            "planners/academic_planner.yaml"
        )

        if not tool:

            return Msg(
                name="AcademicAgent",
                role="assistant",
                content=(
                    "AcademicAgent could not "
                    "find a suitable tool."
                )
            )

        result = None

        # -------------------------
        # SGPA
        # -------------------------

        if tool == "get_sgpa":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_sgpa(
                student_id
            )

        # -------------------------
        # Results
        # -------------------------

        elif tool == "get_results":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_results(
                student_id
            )

        # -------------------------
        # Academic Summary
        # -------------------------

        elif tool == "get_academic_summary":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_academic_summary(
                student_id
            )

        # -------------------------
        # Attendance
        # -------------------------

        elif tool == "get_attendance":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_attendance(
                student_id
            )

        # -------------------------
        # Hostel
        # -------------------------

        elif tool == "get_hostel_details":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_hostel_details(
                student_id
            )

        # -------------------------
        # Leave Records
        # -------------------------

        elif tool == "get_leave_records":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_leave_records(
                student_id
            )

        # -------------------------
        # Timetable
        # -------------------------

        elif tool == "get_timetable":

            department = self.extract_department(
                query
            )

            day = self.extract_day(
                query
            )

            if day:

                result = self.tools.get_day_timetable(
                    department,
                    day
                )

            else:

                result = self.tools.get_timetable(
                    department
                )

        if result is None:

            result = (
                "AcademicAgent could not "
                "process the query."
            )

        return Msg(
            name="AcademicAgent",
            role="assistant",
            content=str(result)
        )