import "./homebutton.css";
import { useNavigate } from "react-router-dom";

export default function HomeButton() {

    const navigate = useNavigate();

    return (
        <button className="home-button" onClick={() => navigate("/api/cars")}>
            Főoldal
        </button>
    );
}
