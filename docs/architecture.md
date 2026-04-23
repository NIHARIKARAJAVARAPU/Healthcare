# Architecture Notes

## Business objective

This HCP module is designed for life-science field representatives who need to capture compliant, high-quality call notes quickly after meeting healthcare professionals.

## Why the design is AI-first

Instead of forcing the rep to fill every field manually, the system allows a natural-language note or chat entry. The AI agent converts the conversation into structured CRM data and recommends the next best action.

## Log Interaction Screen components

### Frontend

- **Header**: establishes context for the user
- **Structured form**: supports explicit data entry
- **AI assistant panel**: supports conversational logging and inline suggestions
- **Redux store**: keeps form and chat state synchronized

### Backend

- **FastAPI endpoints**: receive form submissions and chat messages
- **Interaction service**: writes and updates interaction records
- **LangGraph agent service**: orchestrates tool use and LLM responses
- **SQLAlchemy model**: maps interactions to PostgreSQL / MySQL tables

### Database entities

- `hcp_interactions`
- future entities can include `hcps`, `products`, `approved_materials`, and `rep_tasks`

## Suggested workflow

1. Rep enters a form manually or types a free-text summary.
2. LangGraph agent invokes `log_interaction`.
3. LLM extracts structured entities such as HCP name, sentiment, materials, and follow-up.
4. Compliance tool checks for risky language.
5. Suggested next step is returned to the UI.
6. Rep reviews, edits, and saves the final interaction.
