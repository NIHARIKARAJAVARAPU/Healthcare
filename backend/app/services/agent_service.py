from __future__ import annotations

import json
import re
from datetime import datetime

from app.agents.hcp_agent import build_hcp_agent


def _default_form() -> dict:
    return {
        "hcp_name": "",
        "interaction_type": "Meeting",
        "interaction_datetime": datetime.utcnow().replace(microsecond=0).isoformat(),
        "attendees": [],
        "topics_discussed": "",
        "materials_shared": [],
        "samples_distributed": [],
        "sentiment": "Neutral",
        "outcomes": "",
        "follow_up_actions": [],
        "next_step": "",
        "compliance_notes": "",
    }


def _extract_hcp_name(message: str) -> str:
    match = re.search(r"\bDr\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?", message)
    return match.group(0) if match else ""


def _extract_interaction_type(message: str) -> str:
    lower_message = message.lower()
    if "virtual meeting" in lower_message or "virtual visit" in lower_message:
        return "Virtual Visit"
    if "call" in lower_message:
        return "Call"
    if "email" in lower_message:
        return "Email"
    if "conference" in lower_message:
        return "Conference"
    return "Meeting"


def _extract_topics(message: str) -> str:
    match = re.search(r"discussed\s+(.+?)(?:\.|$)", message, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return message.strip()


def _extract_materials(message: str) -> list[str]:
    lower_message = message.lower()
    materials: list[str] = []
    material_map = {
        "brochure": "Brochure",
        "brochures": "Brochure",
        "dosing guide": "Dosing Guide",
        "mechanism of action visual aid": "Mechanism of Action Visual Aid",
        "visual aid": "Mechanism of Action Visual Aid",
        "efficacy deck": "Efficacy Deck",
        "deck": "Efficacy Deck",
    }
    for keyword, label in material_map.items():
        if keyword in lower_message and label not in materials:
            materials.append(label)
    return materials


def _extract_sentiment(message: str) -> str:
    lower_message = message.lower()
    if "positive" in lower_message:
        return "Positive"
    if "negative" in lower_message:
        return "Negative"
    if "neutral" in lower_message:
        return "Neutral"
    return "Neutral"


def _extract_follow_ups(message: str) -> list[str]:
    lower_message = message.lower()
    follow_ups: list[str] = []
    if "send" in lower_message and "deck" in lower_message:
        follow_ups.append("Send efficacy deck by email")
    if "schedule" in lower_message or "follow-up" in lower_message:
        follow_ups.append("Schedule follow-up meeting")
    if "medical affairs" in lower_message:
        follow_ups.append("Connect HCP with medical affairs")
    if "requested additional evidence" in lower_message or "asked for a dosing guide" in lower_message:
        follow_ups.append("Share requested approved materials")
    return follow_ups


def _extract_outcomes(message: str) -> str:
    lower_message = message.lower()
    outcomes: list[str] = []
    if "asked for a dosing guide" in lower_message:
        outcomes.append("HCP requested a dosing guide.")
    if "agreed to send" in lower_message:
        outcomes.append("Rep agreed to send follow-up material.")
    if "medical affairs" in lower_message:
        outcomes.append("Rep will connect the HCP with medical affairs.")
    if "off-label" in lower_message:
        outcomes.append("HCP raised an off-label question.")
    return " ".join(outcomes)


def _extract_compliance_notes(message: str) -> str:
    lower_message = message.lower()
    notes: list[str] = []
    if "off-label" in lower_message:
        notes.append("Off-label question raised. Route follow-up through medical affairs.")
    if "adverse event" in lower_message:
        notes.append("Possible adverse event mention. Review pharmacovigilance workflow.")
    return " ".join(notes)


def _extract_next_step(follow_up_actions: list[str], compliance_notes: str) -> str:
    if compliance_notes:
        return "Review compliance-sensitive content before finalizing the note."
    if follow_up_actions:
        return follow_up_actions[0]
    return "Confirm next rep action with the HCP."


def _build_form_from_message(user_message: str) -> dict:
    extracted_form = _default_form()
    extracted_form["hcp_name"] = _extract_hcp_name(user_message)
    extracted_form["interaction_type"] = _extract_interaction_type(user_message)
    extracted_form["topics_discussed"] = _extract_topics(user_message)
    extracted_form["materials_shared"] = _extract_materials(user_message)
    extracted_form["sentiment"] = _extract_sentiment(user_message)
    extracted_form["follow_up_actions"] = _extract_follow_ups(user_message)
    extracted_form["outcomes"] = _extract_outcomes(user_message)
    extracted_form["compliance_notes"] = _extract_compliance_notes(user_message)
    extracted_form["next_step"] = _extract_next_step(
        extracted_form["follow_up_actions"], extracted_form["compliance_notes"]
    )
    return extracted_form


def chat_with_agent(user_message: str, current_form: dict | None = None) -> dict:
    form = current_form or _default_form()
    updated_form = _build_form_from_message(user_message)
    if not updated_form["hcp_name"] and form.get("hcp_name"):
        updated_form["hcp_name"] = form["hcp_name"]

    assistant_message = (
        "I updated the interaction draft from your note and suggested the next best action."
    )

    try:
        agent = build_hcp_agent()
        workflow_input = {
            "messages": [
                (
                    "user",
                    "Current CRM form draft: "
                    f"{json.dumps(form)}\n\nRepresentative says: {user_message}\n\n"
                    "Return a concise assistant response and embed a JSON object with key "
                    "'updated_form' and a JSON array with key 'suggested_next_actions'.",
                )
            ]
        }
        result = agent.invoke(workflow_input)
        assistant_message = result["messages"][-1].content
    except Exception:
        # Keep the screen usable even before Groq credentials are configured.
        pass

    suggested_next_actions = list(updated_form["follow_up_actions"])
    if updated_form["compliance_notes"]:
        suggested_next_actions.append("Review note for compliance escalation")
    if not suggested_next_actions:
        suggested_next_actions = [
            "Schedule a follow-up meeting",
            "Send approved product material",
        ]

    return {
        "assistant_message": assistant_message,
        "updated_form": updated_form,
        "suggested_next_actions": suggested_next_actions,
    }
