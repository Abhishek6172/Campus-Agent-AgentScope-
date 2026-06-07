import re

from agentscope.agent import AgentBase
from agentscope.message import Msg

from utils.yaml_loader import YAMLLoader
from tools.profile_tools import ProfileTools
from tools.api_tools import APITools


class ProfileAgent(AgentBase):

    def __init__(self):

        super().__init__()

        self.tools = ProfileTools()

        self.api_tools = APITools()

        self.planner = YAMLLoader.load_yaml(
            "planners/profile_planner.yaml"
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
    # Extract Name
    # -------------------------

    def extract_name(
        self,
        query
    ):

        query = query.strip()

        patterns = [

            r"details of (.+)",

            r"profile of (.+)",

            r"show student details of (.+)",

            r"show teacher details of (.+)",

            r"show student (.+)",

            r"show teacher (.+)",

            r"tell me about (.+)",

            r"who is (.+)",

            r"what subject does (.+) teach",

            r"subject of (.+)",

            r"(.+) details"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                query,
                re.IGNORECASE
            )

            if match:

                return (
                    match.group(1)
                    .strip()
                )

        return query.strip()

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
            "planners/profile_planner.yaml"
        )

        if not tool:

            tool = "get_student_profile"

        result = None

        if tool == "get_student_profile":

            student_id = self.extract_student_id(
                query
            )

            if student_id:

                result = self.tools.get_student_profile(
                    student_id=student_id
                )

            else:

                name = self.extract_name(
                    query
                )

                result = self.tools.get_student_profile(
                    name=name
                )

        elif tool == "get_teacher_profile":

            teacher_id = self.extract_teacher_id(
                query
            )

            if teacher_id:

                result = self.tools.get_teacher_profile(
                    teacher_id=teacher_id
                )

            else:

                name = self.extract_name(
                    query
                )

                result = self.tools.get_teacher_profile(
                    name=name
                )

        elif tool == "get_teacher_subject":

            teacher_id = self.extract_teacher_id(
                query
            )

            if teacher_id:

                result = self.tools.get_teacher_subject(
                    teacher_id=teacher_id
                )

            else:

                name = self.extract_name(
                    query
                )

                result = self.tools.get_teacher_subject(
                    name=name
                )

        elif tool == "get_public_person":

            name = self.extract_name(
                query
            )

            result = self.tools.search_public_person(
                name
            )

        elif tool == "compare_people":

            text = (
                query.lower()
                .replace(
                    "compare",
                    ""
                )
                .strip()
            )

            names = text.split(
                "and"
            )

            if len(names) == 2:

                result = self.tools.compare_people(
                    names[0].strip(),
                    names[1].strip()
                )

        if result is None:

            result = (
                "ProfileAgent could not "
                "process the query."
            )

        return Msg(
            name="ProfileAgent",
            role="assistant",
            content=str(result)
        )