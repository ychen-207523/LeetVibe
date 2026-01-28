import { useState } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import './App.css';

function App() {
  // Chat State
  const [messages, setMessages] = useState([
    { sender: "Agent", text: "Hello! I am ready to interview you. What topic shall we practice?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Code Editor State
  const [code, setCode] = useState("// Write your solution here...\nclass Solution {\n    \n}");

  // Send Message Function
  const sendMessage = async () => {
    if (!input.trim()) return;

    // 1. Update UI immediately
    const newMessages = [...messages, { sender: "User", text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      // 2. Prepare Payload (Message + Code)
      const payload = {
        message: input + "\n\nCURRENT CODE:\n" + code,
        thread_id: "user_1"
      };

      // 3. Send to Python Backend
      const res = await axios.post("http://localhost:8000/chat", payload);

      // 4. Update UI with Agent Response
      setMessages([...newMessages, { sender: "Agent", text: res.data.response }]);
    } catch (error) {
      console.error("Error connecting to server:", error);
      setMessages([...newMessages, { sender: "System", text: "Error: Is server.py running?" }]);
    }
    setLoading(false);
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial, sans-serif' }}>

      {/* LEFT PANEL: Chat */}
      <div style={{ width: '40%', padding: '20px', borderRight: '1px solid #444', display: 'flex', flexDirection: 'column', backgroundColor: '#f9f9f9' }}>
        <h2 style={{ margin: '0 0 20px 0', color: '#333' }}>🤖 LeetVibe</h2>

        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '8px', background: 'white' }}>
          {messages.map((msg, index) => (
            <div key={index} style={{ marginBottom: '12px', textAlign: msg.sender === "User" ? "right" : "left" }}>
              <div style={{ fontSize: '0.8em', color: '#888', marginBottom: '4px' }}>{msg.sender}</div>
              <div style={{
                background: msg.sender === "User" ? "#007bff" : "#e9ecef",
                color: msg.sender === "User" ? "white" : "black",
                padding: '10px 14px',
                borderRadius: '12px',
                display: 'inline-block',
                maxWidth: '80%',
                wordWrap: 'break-word'
              }}>
                {msg.text}
              </div>
            </div>
          ))}
          {loading && <div style={{ color: '#666', fontStyle: 'italic' }}>Agent is typing...</div>}
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type a message..."
            style={{ flex: 1, padding: '12px', borderRadius: '4px', border: '1px solid #ccc' }}
          />
          <button
            onClick={sendMessage}
            style={{ padding: '10px 24px', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Send
          </button>
        </div>
      </div>

      {/* RIGHT PANEL: Code Editor */}
      <div style={{ width: '60%', display: 'flex', flexDirection: 'column', backgroundColor: '#1e1e1e' }}>
        <div style={{ padding: '10px 20px', color: '#ccc', borderBottom: '1px solid #333', fontSize: '0.9em' }}>
          JAVA SOLUTION
        </div>
        <Editor
          height="100%"
          defaultLanguage="java"
          defaultValue={code}
          theme="vs-dark"
          onChange={(value) => setCode(value)}
          options={{ minimap: { enabled: false }, fontSize: 14 }}
        />
      </div>

    </div>
  );
}

export default App;