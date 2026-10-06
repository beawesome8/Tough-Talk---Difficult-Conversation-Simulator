import { useState } from "react";
import StartScreen from "./components/StartScreen.jsx";
import ChatScreen from "./components/ChatScreen.jsx";
import DebriefScreen from "./components/DebriefScreen.jsx";
import { startSession } from "./api.js";

export default function App() {
  const [screen, setScreen] = useState("start");
  const [session, setSession] = useState(null);
  const [debrief, setDebrief] = useState(null);

  async function handleStart() {
    const result = await startSession();
    setSession(result);
    setScreen("chat");
  }

  function handleEnded(debriefData) {
    setDebrief(debriefData);
    setScreen("debrief");
  }

  function handleRestart() {
    setSession(null);
    setDebrief(null);
    setScreen("start");
  }

  if (screen === "chat" && session) {
    return (
      <ChatScreen
        sessionId={session.session_id}
        openingLine={session.opening_line}
        onEnded={handleEnded}
      />
    );
  }
  if (screen === "debrief" && debrief) {
    return <DebriefScreen debrief={debrief} onRestart={handleRestart} />;
  }
  return <StartScreen onStart={handleStart} />;
}
