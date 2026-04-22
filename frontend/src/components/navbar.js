import "./navbar.css";
import { useNavigate } from "react-router-dom";
import HomeButton from "./homebutton";
import ToLoginPageButton from "./to-loginpage-button";

export default function Navbar() {
    
    return (
        <header className="navbar">
            <HomeButton />

            <ToLoginPageButton />

            
        </header>


    );
}