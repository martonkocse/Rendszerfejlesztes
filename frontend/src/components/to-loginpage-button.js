import "./to-loginpage-button.css";
import { useNavigate } from "react-router-dom";

export default function ToLoginPageButton() {

    const navigate = useNavigate();

    return (
        <button className="to-loginpage-button" onClick={() => navigate("/login")}>
            Bejelentkezés
        </button>
    );
}