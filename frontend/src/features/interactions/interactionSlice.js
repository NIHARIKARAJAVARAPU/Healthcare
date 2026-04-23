import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/v1";

const initialForm = {
  hcp_name: "",
  interaction_type: "Meeting",
  interaction_datetime: new Date().toISOString().slice(0, 16),
  attendees: [],
  topics_discussed: "",
  materials_shared: [],
  samples_distributed: [],
  sentiment: "Neutral",
  outcomes: "",
  follow_up_actions: [],
  next_step: "",
  compliance_notes: ""
};

export const submitInteraction = createAsyncThunk(
  "interactions/submitInteraction",
  async (formState) => {
    const payload = {
      ...formState,
      interaction_datetime: new Date(formState.interaction_datetime).toISOString()
    };
    const response = await axios.post(`${API_BASE_URL}/interactions`, payload);
    return response.data;
  }
);

export const sendAgentMessage = createAsyncThunk(
  "interactions/sendAgentMessage",
  async (_, { getState }) => {
    const state = getState().interactions;
    const response = await axios.post(`${API_BASE_URL}/agent/chat`, {
      user_message: state.chatInput,
      current_form: {
        ...state.form,
        interaction_datetime: new Date(state.form.interaction_datetime).toISOString()
      }
    });
    return response.data;
  }
);

const slice = createSlice({
  name: "interactions",
  initialState: {
    form: initialForm,
    chatMessages: [
      {
        role: "assistant",
        content:
          'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.'
      }
    ],
    chatInput: "",
    suggestions: ["Schedule a follow-up", "Share efficacy deck"],
    status: "idle",
    submitStatus: "idle"
  },
  reducers: {
    loadSeedData(state) {
      state.form = initialForm;
    },
    updateField(state, action) {
      const { field, value } = action.payload;
      state.form[field] = value;
    },
    updateListField(state, action) {
      const { field, value } = action.payload;
      state.form[field] = value
        .split(",")
        .map((entry) => entry.trim())
        .filter(Boolean);
    },
    setChatInput(state, action) {
      state.chatInput = action.payload;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(sendAgentMessage.pending, (state) => {
        state.status = "loading";
      })
      .addCase(sendAgentMessage.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.chatMessages.push({ role: "user", content: state.chatInput });
        state.chatMessages.push({
          role: "assistant",
          content: action.payload.assistant_message
        });
        state.form = {
          ...state.form,
          ...action.payload.updated_form,
          interaction_datetime: new Date(action.payload.updated_form.interaction_datetime)
            .toISOString()
            .slice(0, 16)
        };
        state.suggestions = action.payload.suggested_next_actions;
        state.chatInput = "";
      })
      .addCase(sendAgentMessage.rejected, (state) => {
        state.status = "failed";
      })
      .addCase(submitInteraction.pending, (state) => {
        state.submitStatus = "loading";
      })
      .addCase(submitInteraction.fulfilled, (state) => {
        state.submitStatus = "succeeded";
      })
      .addCase(submitInteraction.rejected, (state) => {
        state.submitStatus = "failed";
      });
  }
});

export const { loadSeedData, setChatInput, updateField, updateListField } = slice.actions;
export default slice.reducer;
