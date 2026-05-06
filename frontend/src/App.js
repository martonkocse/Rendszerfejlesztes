import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/home";
import Login from "./pages/login";
import Register from "./pages/register";
import AgentRentals from "./pages/agent-rentals";

function App() {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/cars" replace />} />
            <Route path="/cars" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/agent/rentals" element={<AgentRentals />} />
            <Route path="*" element={<Navigate to="/cars" replace />} />
        </Routes>
    );
}

export default App;