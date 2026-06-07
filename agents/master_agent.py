from agentscope.agent import AgentBase
from agentscope.message import Msg

from utils.yaml_loader import YAMLLoader
from utils.formatter import LLMFormatter

from agents.profile_agent import ProfileAgent
from agents.academic_agent import AcademicAgent
from agents.finance_agent import FinanceAgent


class CampusMasterAgent(AgentBase):

    def __init__(self):

        super().__init__()

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

        worker = YAMLLoader.get_worker(
            query,
            "workflow/task_flow.yaml"
        )

        return worker

    # --------------------------------
    # AgentScope Reply
    # --------------------------------

    async def reply(
        self,
        msg: Msg
    ) -> Msg:

        query = msg.content

        worker = self.get_worker(
            query
        )

        if not worker:

            return Msg(
                name="CampusMasterAgent",
                role="assistant",
                content="No worker found for query."
            )

        # -----------------------------
        # Profile Worker
        # -----------------------------

        if worker == "profile":

            worker_msg = Msg(
                name="Master",
                role="user",
                content=query
            )

            result = await self.profile_agent.reply(
                worker_msg
            )

            formatted = (
                self.llm_formatter.format_response(
                    query,
                    "ProfileAgent",
                    result.content
                )
            )

            return Msg(
                name="CampusMasterAgent",
                role="assistant",
                content=formatted
            )

        # -----------------------------
        # Academic Worker
        # -----------------------------

        elif worker == "academic":

            worker_msg = Msg(
                name="Master",
                role="user",
                content=query
            )

            result = await self.academic_agent.reply(
                worker_msg
            )

            formatted = (
                self.llm_formatter.format_response(
                    query,
                    "AcademicAgent",
                    result.content
                )
            )

            return Msg(
                name="CampusMasterAgent",
                role="assistant",
                content=formatted
            )

        # -----------------------------
        # Finance Worker
        # -----------------------------

        elif worker == "finance":

            worker_msg = Msg(
                name="Master",
                role="user",
                content=query
            )

            result = await self.finance_agent.reply(
                worker_msg
            )

            formatted = (
                self.llm_formatter.format_response(
                    query,
                    "FinanceAgent",
                    result.content
                )
            )

            return Msg(
                name="CampusMasterAgent",
                role="assistant",
                content=formatted
            )

        return Msg(
            name="CampusMasterAgent",
            role="assistant",
            content="Unable to process request."
        )