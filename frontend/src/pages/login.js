import React from 'react';
import { Link } from 'react-router-dom';
import "./login.css"; 
import HomeButton from '../components/homebutton';

export default function Login() {
    return (
        <div className="login-container">
            <form className="login-form" onSubmit={(e) => e.preventDefault()}>
                <h2>Bejelentkezés</h2>

                <p>Felhasználónév</p>
                <input type="text" name="username" placeholder="Felhasználónév" required />

                <p>Jelszó</p>
                <input type="password" name="password" placeholder="Jelszó" required />

                <div className="forgot-password-container">
                    <Link to="/forgot-password" title="Elfelejtett jelszó" className="forgot-password-link">
                        Elfelejtette a jelszavát?
                    </Link>
                </div>

                <button type="submit" className="login-button">Bejelentkezés</button>
            </form>
            <p></p>
            <div className="home-button-container">
                <HomeButton />
            </div>
        </div>
    );
}