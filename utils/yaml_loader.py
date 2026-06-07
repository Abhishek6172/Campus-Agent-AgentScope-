import yaml
from pathlib import Path


class YAMLLoader:

    @staticmethod
    def load_yaml(file_path):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"{file_path} not found"
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file)

    @staticmethod
    def get_worker(query, workflow_file):

        workflow = YAMLLoader.load_yaml(
            workflow_file
        )

        query = query.lower()

        routes = workflow.get(
            "routes",
            {}
        )

        for worker, config in routes.items():

            keywords = config.get(
                "keywords",
                []
            )

            for keyword in keywords:

                if keyword.lower() in query:

                    return worker

        return None

    @staticmethod
    def get_tool(
        query,
        planner_file
    ):

        planner = YAMLLoader.load_yaml(
            planner_file
        )

        query = query.lower()

        tools = planner.get(
            "tools",
            {}
        )

        for tool_name, config in tools.items():

            keywords = config.get(
                "keywords",
                []
            )

            for keyword in keywords:

                if keyword.lower() in query:

                    return tool_name

        return None