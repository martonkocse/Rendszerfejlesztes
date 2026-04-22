import { useState, useEffect } from "react";
import Navbar from "../components/navbar";
import Carlist from "../components/carlist";
import "./home.css";

export default function Home() {
    const [cars, setCars] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("access");

        if (!token) {
            setError("Nincs bejelentkezve.");
            setIsLoading(false);
            return;
        }

        fetch("http://localhost:8000/api/cars/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Hiba történt a szerverhez való csatlakozáskor.");
                }
                return response.json();
            })
            .then((data) => {
                setCars(data);
                setIsLoading(false);
            })
            .catch((err) => {
                console.error("API Error:", err);
                setError(err.message);
                setIsLoading(false);
            });
    }, []);

    return (
        <div>
            <Navbar />

            <main className="home-content">
                <h1>Elérhető autók</h1>

                {isLoading && <p>Betöltés...</p>}

                {error && <p style={{ color: "red" }}>{error}</p>}

                {!isLoading && !error && (
                    <div className="car-grid">
                        {cars.map((car) => (
                            <Carlist
                                key={car.id}
                                brand={car.brand}
                                model={car.model}
                                price={car.daily_price}
                            />
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}