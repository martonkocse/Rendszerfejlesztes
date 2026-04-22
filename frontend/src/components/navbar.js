import "./navbar.css";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
    const navigate = useNavigate();

    const goHome = () => {
        navigate("/api/cars");
    };

    return (
        <header className="navbar">
            <button className="home-button" onClick={ goHome }>
                Főoldal
            </button>

            <button className="login-button">
                Bejelentkezés
            </button>

            
        </header>


    );
}