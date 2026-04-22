import { Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import Login from "./pages/login";

function App() {
    return (
        <Routes>
            {/* When the path is "/", show the Home page */}
            <Route path="/api/cars" element={<Home />} />

            {/* When the path is "/login", show the Login page */}
            <Route path="/login" element={<Login />} />
        </Routes>
    );
}

export default App;