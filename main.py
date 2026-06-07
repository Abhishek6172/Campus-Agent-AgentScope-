import agentscope

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


def main():

    try:
        agentscope.init(
            project="CampusAgent"
        )
    except:
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

            response = (
                master_agent.reply(
                    query
                )
            )

            print(
                "\n--------------------------------"
            )

            print(
                f"Worker : "
                f"{response['worker']}"
            )

            print(
                "--------------------------------"
            )

            print(
                response["response"]
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