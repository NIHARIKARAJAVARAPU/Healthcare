from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from app.core.config import settings


@dataclass
class AgentContext:
    draft_interaction: dict[str, Any] = field(default_factory=dict)
    catalog_materials: list[str] = field(
        default_factory=lambda: ["Product X Brochure", "MOA Visual Aid", "Dosing Guide"]
    )


agent_context = AgentContext()


@tool
def fetch_hcp_profile(hcp_name: str) -> dict[str, Any]:
    """Fetch the HCP profile and prior engagement summary to personalize the call note."""
    return {
        "hcp_name": hcp_name,
        "specialty": "Cardiology",
        "tier": "High value",
        "preferred_channel": "In-person",
        "last_interaction_summary": "Requested additional efficacy evidence and left with a positive sentiment.",
    }


@tool
def log_interaction(interaction_details: str) -> dict[str, Any]:
    """Capture a new interaction from free text and convert it into structured CRM fields."""
    prompt = (
        "Extract structured HCP interaction details as JSON with keys: "
        "hcp_name, interaction_type, interaction_datetime, attendees, topics_discussed, "
        "materials_shared, samples_distributed, sentiment, outcomes, follow_up_actions, next_step, compliance_notes. "
        "If the user omits a field, infer only when safe, otherwise leave empty."
    )
    llm = ChatGroq(model=settings.groq_model, api_key=settings.groq_api_key, temperature=0)
    response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=interaction_details)])
    agent_context.draft_interaction["raw_extraction"] = response.content
    return {
        "status": "draft_captured",
        "summary": "Interaction draft extracted from conversational input.",
        "raw_extraction": response.content,
    }


@tool
def edit_interaction(edit_request: str) -> dict[str, Any]:
    """Modify an existing draft interaction by applying user corrections or additions."""
    agent_context.draft_interaction["last_edit_request"] = edit_request
    return {
        "status": "draft_updated",
        "summary": f"Applied requested draft edits: {edit_request}",
    }


@tool
def suggest_follow_up_action(context_summary: str) -> dict[str, Any]:
    """Recommend the most relevant next sales action for the representative."""
    return {
        "suggested_actions": [
            "Schedule a follow-up meeting in 2 weeks",
            "Send efficacy evidence deck by email",
            "Notify medical affairs if off-label questions were raised",
        ],
        "reason": f"Based on context: {context_summary}",
    }


@tool
def recommend_materials(topic: str) -> dict[str, Any]:
    """Recommend approved materials or samples relevant to the discussion topic."""
    matches = [item for item in agent_context.catalog_materials if topic.lower() in item.lower()]
    return {"recommended_materials": matches or agent_context.catalog_materials[:2]}


@tool
def compliance_guard(note_text: str) -> dict[str, Any]:
    """Check whether the note contains risk keywords that need compliance review."""
    risk_keywords = ["off-label", "adverse event", "gift", "payment"]
    matches = [word for word in risk_keywords if word in note_text.lower()]
    return {
        "needs_review": bool(matches),
        "matched_keywords": matches,
        "guidance": "Route to compliance or pharmacovigilance if sensitive terms are present.",
    }


def build_hcp_agent():
    llm = ChatGroq(model=settings.groq_model, api_key=settings.groq_api_key, temperature=0)
    prompt = (
        "You are an AI assistant for life-science field representatives using an HCP CRM. "
        "Help users log interactions accurately, stay compliant, and recommend next-best actions. "
        "Always prefer structured, CRM-ready outputs."
    )
    return create_react_agent(
        llm,
        tools=[
            fetch_hcp_profile,
            log_interaction,
            edit_interaction,
            suggest_follow_up_action,
            recommend_materials,
            compliance_guard,
        ],
        state_modifier=prompt,
    )
