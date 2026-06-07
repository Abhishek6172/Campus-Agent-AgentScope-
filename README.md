# Campus Agent — AgentScope 2.0

Multi-agent campus information system using pure AgentScope 2.0 master-slave
orchestration. No LLM backend required — all routing is rule-based via YAML.

---

## Architecture

```
User Query (student / teacher / public)
          |
          v
  CampusMasterAgent          <-- reads configs/task_flow.yaml
          |
    ______|______
   |             |
   v             v
AcademicAgent  FinanceAgent  <-- each reads its own planners/*.yaml
   |             |
   v             v
academic_tools  finance_tools
   |             |
   v             v
MongoDB (mock_db.py)   External APIs (external_apis.py)
```

---

## Files

```
campus_agent/
|
|-- main.py                           Entry point
|
|-- agents/
|   |-- master_agent.py               CampusMasterAgent (orchestrator)
|   |-- academic_agent.py             AcademicAgent (worker)
|   |-- finance_agent.py              FinanceAgent (worker)
|   |-- formatter.py                  Plain-text result formatter
|
|-- tools/
|   |-- academic_tools.py             8 academic tools + tool registry
|   |-- finance_tools.py              7 finance tools + tool registry
|   |-- external_apis.py              Attendance, exam, scholarship APIs
|
|-- planners/
|   |-- academic_planner.yaml         Intent -> tool routing for AcademicAgent
|   |-- finance_planner.yaml          Intent -> tool routing for FinanceAgent
|
|-- configs/
|   |-- task_flow.yaml                Master routing rules + merge strategies
|
|-- database/
    |-- mock_db.py                    MongoDB mock (swap with real pymongo)
```

---

## How queries flow

1. User sends a query. Master reads task_flow.yaml and matches a routing rule.
2. For single-worker routes, master calls one worker with the query and context.
3. For compound routes (e.g. net fee after scholarship), master chains workers
   sequentially, extracting values (cgpa, program) from step 1 and injecting
   them into step 2.
4. Each worker reads its own planner YAML, detects intent via keyword match,
   extracts parameters, and calls the corresponding tool function.
5. The tool queries MongoDB or an external API and returns a plain dict.
6. Master formats the result into plain text and returns it to the user.

---

## User roles

- Student (ID: S001, S002): full access to their own data.
- Teacher (ID: T001): profile and department data.
- Public (no ID): school comparison and program fee comparison only.
  Personal queries without an ID are rejected with a clear message.

---

## Connect to real MongoDB

In database/mock_db.py, replace get_db():

    import pymongo, os

    def get_db():
        client = pymongo.MongoClient(os.environ["MONGO_URI"])
        return client["campus_db"]

Then seed the collections from the seed data in the same file.

---

## Connect to real external APIs

In tools/external_apis.py, each function has a comment showing the real
HTTP call. Replace the mock return values and set API_BASE and API_KEY
environment variables.

---

## Run

    pip install agentscope pyyaml

    # Interactive
    python main.py

    # Demo (all query types)
    python main.py demo

---

## Supported queries

| User   | Query                                         | Worker       |
|--------|-----------------------------------------------|--------------|
| Student| Show my profile                               | Academic     |
| Teacher| Show my profile                               | Academic     |
| Student| What are my semester results?                 | Academic     |
| Student| What is my attendance?                        | Academic     |
| Student| When are my upcoming exams?                   | Academic     |
| Student| What is my hostel room and warden?            | Academic     |
| Student| Do I have any library fine?                   | Academic     |
| Student| What is my fee structure?                     | Finance      |
| Student| Show my payment history                       | Finance      |
| Student| Am I eligible for a scholarship?              | Finance      |
| Student| What is my net fee after Merit-50?            | Finance      |
| Student| Give me my Sem-5 fee receipt                  | Finance      |
| Public | Compare fee for all programs                  | Finance      |
| Public | Compare between 5 schools in Bhubaneswar      | Academic     |
