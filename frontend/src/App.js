import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/home";
import Login from "./pages/login";
import Register from "./pages/register";
import AgentRentals from "./pages/agent-rentals";
import MyRentals from "./pages/my-rentals";
import Invoices from "./pages/invoices";

function App() {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/cars" replace />} />
            <Route path="/cars" element={<Home />} />
            <Route path="/my-rentals" element={<MyRentals />} />
            <Route path="/invoices" element={<Invoices />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/agent/rentals" element={<AgentRentals />} />
            <Route path="*" element={<Navigate to="/cars" replace />} />
        </Routes>
    );
}

export default App;