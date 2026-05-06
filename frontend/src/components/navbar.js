import "./navbar.css";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
    const navigate = useNavigate();
    const username = localStorage.getItem("username");

    const handleLogout = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("username");
        navigate("/login");
    };

    return (
        <header className="navbar">
            <Link to="/cars" className="navbar-logo">
                BérAutó
            </Link>

            <nav className="navbar-links">
                <Link to="/cars">Autók</Link>
                <Link to="/my-rentals">Saját bérléseim</Link>
                <Link to="/invoices">Számlák</Link>
                <Link to="/agent/rentals">Ügyintézői felület</Link>
            </nav>

            <div className="navbar-actions">
                {username && <span className="navbar-user">{username}</span>}

                <button type="button" onClick={handleLogout} className="logout-button">
                    Kijelentkezés
                </button>
            </div>
        </header>
    );
}