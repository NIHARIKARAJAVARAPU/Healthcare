import { useDispatch, useSelector } from "react-redux";

import { sendAgentMessage, setChatInput } from "../features/interactions/interactionSlice";

export default function AssistantPanel() {
  const dispatch = useDispatch();
  const { chatMessages, chatInput, status } = useSelector((state) => state.interactions);

  return (
    <div className="assistant-shell">
      <div className="assistant-heading">
        <h2>AI Assistant</h2>
      </div>

      <div className="chat-window">
        {chatMessages.map((message, index) => (
          <div key={`${message.role}-${index}`} className={`chat-bubble ${message.role}`}>
            {message.content}
          </div>
        ))}
      </div>

      <div className="chat-composer">
        <textarea
          rows="2"
          value={chatInput}
          onChange={(event) => dispatch(setChatInput(event.target.value))}
          placeholder="Describe..."
        />
        <button
          className="send-button"
          onClick={() => dispatch(sendAgentMessage())}
          disabled={!chatInput.trim() || status === "loading"}
        >
          {status === "loading" ? "..." : "Log"}
        </button>
      </div>
    </div>
  );
}
