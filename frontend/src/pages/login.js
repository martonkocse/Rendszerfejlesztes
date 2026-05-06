import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

export default function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        setMessage("");
        setIsLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/token/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error("Hibás felhasználónév vagy jelszó.");
            }

            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            localStorage.setItem("username", username);

            navigate("/cars");
        } catch (error) {
            setMessage(error.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="login-card">
                <h1>BérAutó</h1>
                <p className="login-subtitle">
                    Jelentkezz be az autók megtekintéséhez és a kölcsönzés indításához.
                </p>

                <form onSubmit={handleSubmit} className="login-form">
                    <label>Felhasználónév</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="például customer1"
                        autoComplete="username"
                        required
                    />

                    <label>Jelszó</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="jelszó"
                        autoComplete="current-password"
                        required
                    />

                    {message && <p className="login-error">{message}</p>}

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? "Bejelentkezés..." : "Bejelentkezés"}
                    </button>
                </form>
            </div>
        </div>
    );
}