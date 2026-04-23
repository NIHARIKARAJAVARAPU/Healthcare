import { useEffect } from "react";
import { useDispatch } from "react-redux";

import AssistantPanel from "./components/AssistantPanel";
import Header from "./components/Header";
import LogInteractionForm from "./components/LogInteractionForm";
import { loadSeedData } from "./features/interactions/interactionSlice";

export default function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(loadSeedData());
  }, [dispatch]);

  return (
    <div className="page-shell">
      <Header />
      <main className="screen-grid">
        <section className="screen-panel form-panel">
          <LogInteractionForm />
        </section>
        <aside className="screen-panel assistant-panel">
          <AssistantPanel />
        </aside>
      </main>
    </div>
  );
}
