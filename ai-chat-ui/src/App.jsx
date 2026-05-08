import { useState } from "react"
import axios from "axios"

const SESSION_ID = "user-" + Math.random().toString(36).slice(2, 9)
const API_URL = "http://localhost:8000"

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!input.trim()) return
    const userMsg = { role: "user", content: input }
    setMessages(prev => [...prev, userMsg])
    setInput("")
    setLoading(true)

    try {
      const res = await axios.post(`${API_URL}/chat`, {
        session_id: SESSION_ID,
        message: input
      })
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: res.data.reply }
      ])
    } catch {
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: "Error reaching API." }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>AI Chat</h2>
      <div style={{
        border: "1px solid #ddd",
        borderRadius: 8,
        padding: 16,
        minHeight: 300,
        marginBottom: 16,
        overflowY: "auto",
        maxHeight: 500
      }}>
        {messages.length === 0 && (
          <p style={{ color: "#999" }}>Send a message to start chatting...</p>
        )}
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              textAlign: m.role === "user" ? "right" : "left",
              margin: "8px 0"
            }}
          >
            <span style={{
              background: m.role === "user" ? "#0070f3" : "#f0f0f0",
              color: m.role === "user" ? "#fff" : "#000",
              padding: "8px 12px",
              borderRadius: 16,
              display: "inline-block",
              maxWidth: "80%",
              textAlign: "left"
            }}>
              {m.content}
            </span>
          </div>
        ))}
        {loading && (
          <div style={{ color: "#999", fontStyle: "italic" }}>
            Thinking...
          </div>
        )}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send()}
          placeholder="Type a message..."
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: 8,
            border: "1px solid #ddd",
            fontSize: 14
          }}
        />
        <button
          onClick={send}
          disabled={loading}
          style={{
            padding: "10px 20px",
            background: loading ? "#ccc" : "#0070f3",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: 14
          }}
        >
          Send
        </button>
      </div>
    </div>
  )
}
