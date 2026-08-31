from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents import research_agent, pain_point_agent, email_writer_agent, review_agent

# ─── State ────────────────────────────────────────────
class EmailState(TypedDict):
    company_name: str
    website_url: str
    your_service: str
    your_name: str
    your_role: str
    research: str
    pain_points: str
    email_subject: str
    email_body: str
    review: str

# ─── Graph Build ──────────────────────────────────────
def build_graph():
    graph = StateGraph(EmailState)

    # Nodes add karo
    graph.add_node("researcher", research_agent)
    graph.add_node("pain_point", pain_point_agent)
    graph.add_node("writer", email_writer_agent)
    graph.add_node("reviewer", review_agent)

    # Edges — ek ke baad ek
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "pain_point")
    graph.add_edge("pain_point", "writer")
    graph.add_edge("writer", "reviewer")
    graph.add_edge("reviewer", END)

    return graph.compile()

# ─── App ──────────────────────────────────────────────
app = build_graph()