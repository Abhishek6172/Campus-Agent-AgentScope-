import re

from agentscope.agent import AgentBase
from agentscope.message import Msg

from utils.yaml_loader import YAMLLoader
from tools.finance_tools import FinanceTools


class FinanceAgent(AgentBase):

    def __init__(self):

        super().__init__()

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
    # AgentScope Reply
    # -------------------------

    async def reply(
        self,
        msg: Msg
    ) -> Msg:

        query = msg.content

        tool = YAMLLoader.get_tool(
            query,
            "planners/finance_planner.yaml"
        )

        if not tool:

            return Msg(
                name="FinanceAgent",
                role="assistant",
                content=(
                    "FinanceAgent could not "
                    "find a suitable tool."
                )
            )

        result = None

        # -------------------------
        # Fee Details
        # -------------------------

        if tool == "get_fee_details":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_fee_details(
                student_id
            )

        # -------------------------
        # Fee Status
        # -------------------------

        elif tool == "get_fee_status":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_fee_status(
                student_id
            )

        # -------------------------
        # Pending Fee
        # -------------------------

        elif tool == "get_pending_fee":

            student_id = self.extract_student_id(
                query
            )

            result = self.tools.get_pending_fee(
                student_id
            )

        # -------------------------
        # Salary
        # -------------------------

        elif tool == "get_salary":

            teacher_id = self.extract_teacher_id(
                query
            )

            result = self.tools.get_salary(
                teacher_id
            )

        # -------------------------
        # Payroll
        # -------------------------

        elif tool == "get_payroll":

            teacher_id = self.extract_teacher_id(
                query
            )

            result = self.tools.get_payroll(
                teacher_id
            )

        if result is None:

            result = (
                "FinanceAgent could not "
                "process the query."
            )

        return Msg(
            name="FinanceAgent",
            role="assistant",
            content=str(result)
        )