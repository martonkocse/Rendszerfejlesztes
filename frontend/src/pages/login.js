import React, { useState } from 'react';
import "./login.css";
export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await fetch("http://localhost:8000/api/token/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    password
                })
            });

            const data = await res.json();

            if (!res.ok) throw new Error("Login failed");

            localStorage.setItem("access", data.access);

            console.log("Logged in!");
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className='login-container'>
            <form onSubmit={handleSubmit} className='login-form'>
                <h2>Bejelentkezés</h2>
                <p>Felhasználónév</p>
                <input
                    className='login-input'
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="username"
                />
                <p>Jelszó</p>
                <input
                    className='login-input'
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="password"
                />
                <div className='forgot-password-container'>
                    <p>Elfelejtetted a jelszavad?</p>
                </div>

                <button type="submit" className='login-button'>Login</button>
            </form>
        </div>
    );
}