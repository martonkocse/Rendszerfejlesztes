import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./register.css";

export default function Register() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: "",
        password: "",
        passwordAgain: "",
        first_name: "",
        last_name: "",
        email: ""
    });

    const [message, setMessage] = useState("");
    const [success, setSuccess] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setMessage("");
        setSuccess("");

        if (formData.password !== formData.passwordAgain) {
            setMessage("A két jelszó nem egyezik.");
            return;
        }

        setIsLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: formData.username,
                    password: formData.password,
                    first_name: formData.first_name,
                    last_name: formData.last_name,
                    email: formData.email
                })
            });

            const data = await response.json();

            if (!response.ok) {
                if (data.username) {
                    throw new Error("Ez a felhasználónév már foglalt.");
                }

                if (data.password) {
                    throw new Error("A megadott jelszó nem megfelelő.");
                }

                if (data.email) {
                    throw new Error("Az e-mail cím nem megfelelő.");
                }

                throw new Error("A regisztráció nem sikerült.");
            }

            setSuccess("Sikeres regisztráció. Átirányítás a bejelentkezéshez...");

            setTimeout(() => {
                navigate("/login");
            }, 1200);
        } catch (error) {
            setMessage(error.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="register-page">
            <div className="register-card">
                <h1>Regisztráció</h1>
                <p className="register-subtitle">
                    Hozz létre ügyfélfiókot az autókölcsönzés használatához.
                </p>

                <form onSubmit={handleSubmit} className="register-form">
                    <label>Felhasználónév</label>
                    <input
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="például customer4"
                        autoComplete="username"
                        required
                    />

                    <label>Jelszó</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="jelszó"
                        autoComplete="new-password"
                        required
                    />

                    <label>Jelszó újra</label>
                    <input
                        type="password"
                        name="passwordAgain"
                        value={formData.passwordAgain}
                        onChange={handleChange}
                        placeholder="jelszó újra"
                        autoComplete="new-password"
                        required
                    />

                    <label>Keresztnév</label>
                    <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        placeholder="keresztnév"
                    />

                    <label>Vezetéknév</label>
                    <input
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                        placeholder="vezetéknév"
                    />

                    <label>E-mail cím</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="pelda@email.hu"
                    />

                    {message && <p className="register-error">{message}</p>}
                    {success && <p className="register-success">{success}</p>}

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? "Regisztráció..." : "Regisztráció"}
                    </button>
                </form>

                <p className="login-link-text">
                    Már van fiókod? <Link to="/login">Bejelentkezés</Link>
                </p>
            </div>
        </div>
    );
}