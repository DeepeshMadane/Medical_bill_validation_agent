from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from tools.ocr_tool import extract_text
from tools.parser_tool import parse_bill
from tools.rag_tool import search_tariff
from tools.compare_tool import compare_cost


# -------------------------------
# STATE
# -------------------------------
class AgentState(TypedDict):
    image_path: str
    text: str
    bill: dict
    results: List
    retry_count: int
    retriever: object
    next: str


# -------------------------------
# NODES
# -------------------------------

# 🧠 AGENT BRAIN (NEW)
from agent.llm_brain import decide_next_step

def agent_node(state):
    print("\n======================")
    print("[LLM AGENT THINKING...]")
    print("STATE:", state)

    decision = decide_next_step(state)

    print("Decision:", decision)
    print("======================")

    return {"next": decision}

def ocr_node(state):
    print("\n[OCR NODE]")
    text = extract_text(state["image_path"])
    return {"text": text}


def parser_node(state):
    print("\n[PARSER NODE]")
    bill = parse_bill(state["text"])
    return {"bill": bill}


# 🔥 Improved parser check (optional retry)
def check_parser_node(state):
    print("\n[CHECK NODE]")

    bill = state.get("bill")
    retry = state.get("retry_count", 0)

    if not bill or not bill.get("items"):
        if retry < 2:
            print("❌ Parser failed → retrying...")
            return {"retry_count": retry + 1, "next": "parse"}
        else:
            print("❌ Parser failed → giving up")
            return {"next": "end"}

    return {"next": "process"}


def process_items_node(state):
    print("\n[PROCESS NODE]")

    bill = state["bill"]
    results = []

    for item in bill["items"]:
        service = item["service"]
        billed = item["billed_cost"]

        print(f"\nProcessing: {service}")

        retrieved = search_tariff(
            state["retriever"], service, bill["hospital"]
        )

        print("Retrieved:", retrieved)

        analysis = compare_cost(billed, retrieved)

        results.append({
            "service": service,
            "billed": billed,
            **analysis
        })

    return {"results": results}


# -------------------------------
# GRAPH
# -------------------------------

def build_graph(retriever):
    graph = StateGraph(AgentState)

    # nodes
    graph.add_node("agent", agent_node)   # 🔥 brain
    graph.add_node("ocr", ocr_node)
    graph.add_node("parse", parser_node)
    graph.add_node("check", check_parser_node)
    graph.add_node("process", process_items_node)

    # entry point
    graph.set_entry_point("agent")

    # 🔥 dynamic routing
    graph.add_conditional_edges(
        "agent",
        lambda state: state["next"],
        {
            "ocr": "ocr",
            "parse": "parse",
            "process": "process",
            "end": END
        }
    )

    # loop back to agent after each step
    graph.add_edge("ocr", "agent")
    graph.add_edge("parse", "check")

    graph.add_conditional_edges(
        "check",
        lambda state: state["next"],
        {
            "parse": "parse",
            "process": "process",
            "end": END
        }
    )

    graph.add_edge("process", "agent")

    # run wrapper
    def run(inputs):
        inputs["retriever"] = retriever
        inputs["retry_count"] = 0
        return graph.compile().invoke(inputs)

    return run