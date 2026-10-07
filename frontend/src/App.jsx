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

  let activeScreen;
  if (screen === "chat" && session) {
    activeScreen = (
      <ChatScreen
        sessionId={session.session_id}
        openingLine={session.opening_line}
        onEnded={handleEnded}
      />
    );
  } else if (screen === "debrief" && debrief) {
    activeScreen = <DebriefScreen debrief={debrief} onRestart={handleRestart} />;
  } else {
    activeScreen = <StartScreen onStart={handleStart} />;
  }

  return (
    <>
      <div className="bg-glow" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
      </div>
      {activeScreen}
    </>
  );
}
