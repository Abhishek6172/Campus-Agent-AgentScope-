import asyncio
import agentscope

from agentscope.message import Msg

from agents.master_agent import CampusMasterAgent
from database.mongodb import MongoDB


def startup():

    print("\n--------------------------------")
    print("Campus Agent Started...")
    print("--------------------------------")

    try:

        MongoDB()

        print("MongoDB Connected...")

    except Exception as e:

        print("MongoDB Connection Failed")
        print(e)

        return False

    print("Workers Loaded...")
    print("Workflow Loaded...")
    print("Ready For Queries...\n")

    return True


async def process_query(
    master_agent,
    query
):

    message = Msg(
        name="user",
        role="user",
        content=query
    )

    response = await master_agent.reply(
        message
    )

    return response


def main():

    try:

        agentscope.init(
            project="CampusAgent"
        )

    except Exception:
        pass

    if not startup():
        return

    master_agent = CampusMasterAgent()

    while True:

        query = input("> ")

        if query.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            print(
                "\nCampus Agent Stopped."
            )

            break

        try:

            response = asyncio.run(
                process_query(
                    master_agent,
                    query
                )
            )

            print(
                "\n--------------------------------"
            )

            print(
                "Campus Agent Response"
            )

            print(
                "--------------------------------"
            )

            print(
                response.content
            )

            print()

        except Exception as e:

            print(
                "\nError Occurred:"
            )

            print(e)

            print()


if __name__ == "__main__":

    main()