export default function StartScreen({ onStart }) {
  return (
    <div className="screen">
      <h1>Tough Talk</h1>
      <p>
        Sam is a strong engineer on your team who has missed two recent deadlines.
        Since a colleague left, Sam has quietly been covering extra work. You're
        about to practise raising this with Sam.
      </p>
      <p>
        <strong>Sam is fictional.</strong> This is a practice simulation — nothing
        you type is stored after your session ends, and no real person is involved.
      </p>
      <button onClick={onStart}>Start conversation</button>
    </div>
  );
}
