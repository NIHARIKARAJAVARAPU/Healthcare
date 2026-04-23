# LangGraph Agent Role And Tools

## Role of the LangGraph agent

The LangGraph agent acts as the intelligent workflow layer for HCP interaction management. It does not only answer chat messages. It coordinates a set of tools that help a field representative:

- turn free text into CRM-ready structured data
- retrieve HCP context before or after a visit
- edit existing interaction drafts
- recommend the next best commercial action
- check for compliance-sensitive content

LangGraph is useful because the workflow can be extended into a multi-step decision graph. For example, if the agent detects a possible compliance issue, it can branch into an internal review step before the interaction is finalized.

## Minimum five tools

### 1. Log Interaction

Purpose:

- captures a new HCP interaction from chat text or voice-note transcript

How it works:

- sends the representative's free-text summary to the Groq `gemma2-9b-it` model
- asks the model to extract entities and a structured summary
- returns a CRM draft with fields like HCP name, date, topics, materials shared, sentiment, outcomes, and follow-up

### 2. Edit Interaction

Purpose:

- updates a previously logged interaction or draft

How it works:

- accepts a natural-language correction such as `change sentiment to neutral and add Dr. Patel as an attendee`
- applies those changes to the current draft or saved record
- keeps an audit-friendly workflow by separating create and edit actions

### 3. Fetch HCP Profile

Purpose:

- provides the representative with prior context before logging or planning next steps

What it returns:

- specialty
- preferred engagement channel
- previous interaction summary
- account priority or segment

### 4. Suggest Follow-Up Action

Purpose:

- recommends the next best action after an interaction

Examples:

- schedule follow-up meeting
- send approved efficacy material
- involve medical affairs

### 5. Recommend Materials

Purpose:

- recommends approved material or sample options relevant to the conversation topic

Examples:

- brochure
- dosing guide
- mechanism-of-action visual aid

### 6. Compliance Guard

Purpose:

- checks whether notes mention compliance-sensitive content

Examples:

- off-label use
- adverse event mention
- gifts or payment language

## Groq model choice

Primary model:

- `gemma2-9b-it`

Why:

- cost-effective for extraction, summarization, and structured response generation

Optional context-heavy fallback:

- `llama-3.3-70b-versatile`

Why:

- stronger reasoning for more complex multi-turn context, if needed
