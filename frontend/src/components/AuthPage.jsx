import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authApi } from "../api.js";

export default function AuthPage({ onAuth }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const fn = mode === "login" ? authApi.login : authApi.register;
      const data = await fn(username, password);
      localStorage.setItem("token", data.token);
      onAuth(data.token);
      navigate("/analyze");
    } catch (e) {
      setError(e.response?.data || "Something went wrong.");
    }
  };

  return (
    <div className="card" style={{ maxWidth: 380, margin: "40px auto" }}>
      <h2>{mode === "login" ? "Log in" : "Create an account"}</h2>
      <form onSubmit={submit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password (min 6 chars)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" style={{ width: "100%" }}>
          {mode === "login" ? "Log in" : "Sign up"}
        </button>
      </form>
      {error && <p className="error-text">{String(error)}</p>}
      <p className="muted" style={{ marginTop: 14 }}>
        {mode === "login" ? "No account yet?" : "Already have an account?"}{" "}
        <a
          href="#"
          onClick={(e) => {
            e.preventDefault();
            setMode(mode === "login" ? "register" : "login");
          }}
        >
          {mode === "login" ? "Sign up" : "Log in"}
        </a>
      </p>
    </div>
  );
}
