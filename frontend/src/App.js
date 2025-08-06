import React, { useEffect, useState, useRef } from "react";
import "./App.css";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [expenses, setExpenses] = useState([]);
  const [isListening, setIsListening] = useState(false);
  const [partialTranscript, setPartialTranscript] = useState("");
  const totalRef = useRef(0);

  const { transcript, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition();

  useEffect(() => {
    if (!browserSupportsSpeechRecognition) {
      alert("Your browser doesn't support Speech Recognition.");
      return;
    }
  }, [browserSupportsSpeechRecognition]);

  useEffect(() => {
    if (!transcript) return;

    const cleaned = transcript.trim().toLowerCase();

    if (cleaned.includes("done")) {
      SpeechRecognition.stopListening();
      setIsListening(false);
      resetTranscript();
      return;
    }

    const match = cleaned.match(/([a-zA-Z]+)\s+(\d+)/);

    if (match) {
      const item = match[1];
      const amount = parseFloat(match[2]);

      if (!isNaN(amount)) {
        const now = new Date();
        const expense = {
          date: now.toLocaleDateString(),
          time: now.toLocaleTimeString(),
          item,
          amount,
        };

        totalRef.current += amount;
        setExpenses((prev) => [...prev, expense]);
        setPartialTranscript("");
        resetTranscript();

        // 🔗 Send to backend
        fetch(`${BACKEND_URL}/process`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ transcript: `${item} ${amount}` }),
        })
          .then((res) => res.json())
          .then((data) => {
            console.log("Saved to backend:", data);
          })
          .catch((err) => {
            console.error("Backend error:", err);
          });
      }
    } else {
      setPartialTranscript(cleaned);
    }
  }, [transcript, resetTranscript]);

  const handleStart = () => {
    resetTranscript();
    setExpenses([]);
    setPartialTranscript("");
    totalRef.current = 0;
    setIsListening(true);
    SpeechRecognition.startListening({ continuous: true, language: "en-IN" });
  };

  return (
    <div className="app">
      <h1>🎙️ Voice Expense Tracker</h1>

      <button onClick={handleStart} disabled={isListening}>
        🎤 Start Voice Input
      </button>

      {isListening && <p><strong>Say items like:</strong> rice 100, dal 200... Say "done" to stop</p>}
      <p><strong>Listening:</strong> {isListening ? "🎧 On" : "🛑 Off"}</p>
      <p><strong>You said:</strong> {partialTranscript}</p>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Item</th>
              <th>Amount (₹)</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((exp, idx) => (
              <tr key={idx}>
                <td>{exp.date}</td>
                <td>{exp.time}</td>
                <td>{exp.item}</td>
                <td>{exp.amount}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {expenses.length > 0 && (
          <h3 className="total">Total: ₹{totalRef.current}</h3>
        )}
      </div>
    </div>
  );
}

export default App;
