import re

from utils.yaml_loader import YAMLLoader
from tools.profile_tools import ProfileTools
from tools.api_tools import APITools


class ProfileAgent:

    def __init__(self):

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
    # Main Reply
    # -------------------------

    def reply(
        self,
        query
    ):

        tool = YAMLLoader.get_tool(
            query,
            "planners/profile_planner.yaml"
        )

        # Fallback
        if not tool:

            tool = "get_student_profile"

        # -------------------------
        # Student Profile
        # -------------------------

        if tool == "get_student_profile":

            student_id = (
                self.extract_student_id(
                    query
                )
            )

            if student_id:

                return (
                    self.tools
                    .get_student_profile(
                        student_id=student_id
                    )
                )

            name = self.extract_name(
                query
            )

            return (
                self.tools
                .get_student_profile(
                    name=name
                )
            )

        # -------------------------
        # Teacher Profile
        # -------------------------

        if tool == "get_teacher_profile":

            teacher_id = (
                self.extract_teacher_id(
                    query
                )
            )

            if teacher_id:

                return (
                    self.tools
                    .get_teacher_profile(
                        teacher_id=teacher_id
                    )
                )

            name = self.extract_name(
                query
            )

            return (
                self.tools
                .get_teacher_profile(
                    name=name
                )
            )

        # -------------------------
        # Teacher Subject
        # -------------------------

        if tool == "get_teacher_subject":

            teacher_id = (
                self.extract_teacher_id(
                    query
                )
            )

            if teacher_id:

                return (
                    self.tools
                    .get_teacher_subject(
                        teacher_id=teacher_id
                    )
                )

            name = self.extract_name(
                query
            )

            return (
                self.tools
                .get_teacher_subject(
                    name=name
                )
            )

        # -------------------------
        # Public Person
        # -------------------------

        if tool == "get_public_person":

            name = self.extract_name(
                query
            )

            return (
                self.tools
                .search_public_person(
                    name
                )
            )

        # -------------------------
        # Compare People
        # -------------------------

        if tool == "compare_people":

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

                return (
                    self.tools
                    .compare_people(
                        names[0].strip(),
                        names[1].strip()
                    )
                )

        return (
            "ProfileAgent could not "
            "process the query."
        )