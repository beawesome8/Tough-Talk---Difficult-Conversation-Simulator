export default function StartScreen({ onStart }) {
  return (
    <div className="screen">
      <div className="card">
        <span className="eyebrow">Practice scenario</span>
        <h1>Tough Talk</h1>
        <p>
          Giving someone hard feedback is uncomfortable, so most people either put
          it off or handle it badly. This is a safe place to practise that
          conversation first — before you have it for real.
        </p>

        <h3>Who you're talking to</h3>
        <p>
          You'll be messaging <strong>Sam</strong>, a made-up teammate we built for
          this exercise. Sam is a strong engineer who's missed two deadlines lately.
          What Sam hasn't told anyone: after a colleague left, Sam quietly took on
          their workload too — and it's starting to wear on them.
        </p>

        <h3>How this actually works</h3>
        <p>
          Sam has a "mood" underneath — how much they trust you, how stressed they
          are — but that's tracked by plain, fixed rules in the code, not decided by
          the AI. The AI's only job is to write what Sam says. That's what keeps Sam
          consistent every time, and stops this from being talked out of character
          no matter what you type.
        </p>

        <div className="notice">
          <strong>Sam is fictional.</strong> Nothing you type is stored after your
          session ends, and no real person is involved. This is for practice, not
          for scoring you.
        </div>
        <button onClick={onStart}>Start conversation</button>
      </div>
    </div>
  );
}
