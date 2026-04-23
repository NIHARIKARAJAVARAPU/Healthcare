import { useDispatch, useSelector } from "react-redux";

import { submitInteraction } from "../features/interactions/interactionSlice";

const interactionTypes = ["Meeting", "Call", "Email", "Conference", "Virtual Visit"];
const sentiments = ["Positive", "Neutral", "Negative"];

function parseList(value) {
  return Array.isArray(value) ? value.join(", ") : "";
}

export default function LogInteractionForm() {
  const dispatch = useDispatch();
  const { form, submitStatus, suggestions } = useSelector((state) => state.interactions);

  const onSubmit = (event) => {
    event.preventDefault();
    dispatch(submitInteraction(form));
  };

  return (
    <form className="interaction-form" onSubmit={onSubmit}>
      <div className="section-heading">
        <h2>Interaction Details</h2>
        <p>Filled through AI Assistant only</p>
      </div>

      <div className="grid-two">
        <label>
          <span>HCP Name</span>
          <input value={form.hcp_name} readOnly placeholder="Search or select HCP..." />
        </label>

        <label>
          <span>Interaction Type</span>
          <select value={form.interaction_type} disabled>
            {interactionTypes.map((type) => (
              <option key={type}>{type}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="grid-two">
        <label>
          <span>Date and Time</span>
          <input type="datetime-local" value={form.interaction_datetime} readOnly />
        </label>

        <label>
          <span>Attendees</span>
          <input value={parseList(form.attendees)} readOnly placeholder="Enter names..." />
        </label>
      </div>

      <label>
        <span>Topics Discussed</span>
        <textarea rows="4" value={form.topics_discussed} readOnly placeholder="Discussion points..." />
      </label>

      <div className="grid-two">
        <label>
          <span>Materials Shared</span>
          <input value={parseList(form.materials_shared)} readOnly placeholder="Brochure, deck..." />
        </label>

        <label>
          <span>Samples Distributed</span>
          <input value={parseList(form.samples_distributed)} readOnly placeholder="Samples..." />
        </label>
      </div>

      <label>
        <span>HCP Sentiment</span>
        <div className="pill-row">
          {sentiments.map((item) => (
            <button key={item} type="button" className={form.sentiment === item ? "pill active" : "pill"} disabled>
              {item}
            </button>
          ))}
        </div>
      </label>

      <label>
        <span>Outcomes</span>
        <textarea rows="3" value={form.outcomes} readOnly placeholder="Outcomes..." />
      </label>

      <div className="grid-two">
        <label>
          <span>Follow-up Actions</span>
          <input value={parseList(form.follow_up_actions)} readOnly placeholder="Follow-up..." />
        </label>

        <label>
          <span>Next Best Step</span>
          <input value={form.next_step} readOnly placeholder="Next step..." />
        </label>
      </div>

      <label>
        <span>Compliance Notes</span>
        <textarea rows="3" value={form.compliance_notes} readOnly placeholder="Compliance notes..." />
      </label>

      <div className="suggestions-card">
        <h3>AI Suggestions</h3>
        <ul>
          {suggestions.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>

      <button className="primary-button" type="submit">
        {submitStatus === "loading" ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
