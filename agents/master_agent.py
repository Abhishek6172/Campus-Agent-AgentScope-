from utils.yaml_loader import YAMLLoader
from utils.formatter import LLMFormatter

from agents.profile_agent import ProfileAgent
from agents.academic_agent import AcademicAgent
from agents.finance_agent import FinanceAgent


class CampusMasterAgent:

    def __init__(self):

        self.profile_agent = ProfileAgent()

        self.academic_agent = AcademicAgent()

        self.finance_agent = FinanceAgent()

        self.llm_formatter = LLMFormatter()

        self.workflow = YAMLLoader.load_yaml(
            "workflow/task_flow.yaml"
        )

    # --------------------------------
    # Route Query Using YAML
    # --------------------------------

    def get_worker(
        self,
        query
    ):

        return YAMLLoader.get_worker(
            query,
            "workflow/task_flow.yaml"
        )

    # --------------------------------
    # Format Result
    # --------------------------------

    def format_result(
        self,
        query,
        worker_name,
        result
    ):

        try:

            return self.llm_formatter.format_response(
                query,
                worker_name,
                result
            )

        except Exception as e:

            print(
                f"\nLLM Formatting Failed: {e}"
            )

            return str(result)

    # --------------------------------
    # Main Reply
    # --------------------------------

    def reply(
        self,
        query
    ):

        worker = self.get_worker(
            query
        )

        if not worker:

            return {
                "worker": "None",
                "response":
                "No worker found for this query."
            }

        # -----------------------------
        # Profile Worker
        # -----------------------------

        if worker == "profile":

            result = (
                self.profile_agent.reply(
                    query
                )
            )

            return {
                "worker": "ProfileAgent",
                "response": self.format_result(
                    query,
                    "ProfileAgent",
                    result
                )
            }

        # -----------------------------
        # Academic Worker
        # -----------------------------

        if worker == "academic":

            result = (
                self.academic_agent.reply(
                    query
                )
            )

            return {
                "worker": "AcademicAgent",
                "response": self.format_result(
                    query,
                    "AcademicAgent",
                    result
                )
            }

        # -----------------------------
        # Finance Worker
        # -----------------------------

        if worker == "finance":

            result = (
                self.finance_agent.reply(
                    query
                )
            )

            return {
                "worker": "FinanceAgent",
                "response": self.format_result(
                    query,
                    "FinanceAgent",
                    result
                )
            }

        return {
            "worker": "Unknown",
            "response":
            "Unable to process request."
        }