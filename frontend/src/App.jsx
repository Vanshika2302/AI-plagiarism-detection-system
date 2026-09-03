import React, { useState } from "react";
import { Routes, Route, Link, Navigate } from "react-router-dom";
import ComparePage from "./components/ComparePage.jsx";
import AnalyzePage from "./components/AnalyzePage.jsx";
import HistoryPage from "./components/HistoryPage.jsx";
import AuthPage from "./components/AuthPage.jsx";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div>
      <nav className="navbar">
        <div>
          <span className="brand">PlagiarismChecker</span>
          <Link to="/compare" style={{ marginLeft: 24 }}>Compare</Link>
          <Link to="/analyze">Analyze</Link>
          <Link to="/history">History</Link>
        </div>
        <div>
          {token ? (
            <button onClick={logout}>Log out</button>
          ) : (
            <Link to="/auth">Log in / Sign up</Link>
          )}
        </div>
      </nav>

      <div className="container">
        <Routes>
          <Route path="/" element={<Navigate to="/compare" />} />
          <Route path="/compare" element={<ComparePage />} />
          <Route
            path="/analyze"
            element={token ? <AnalyzePage /> : <Navigate to="/auth" />}
          />
          <Route
            path="/history"
            element={token ? <HistoryPage /> : <Navigate to="/auth" />}
          />
          <Route
            path="/auth"
            element={<AuthPage onAuth={(t) => setToken(t)} />}
          />
        </Routes>
      </div>
    </div>
  );
}
