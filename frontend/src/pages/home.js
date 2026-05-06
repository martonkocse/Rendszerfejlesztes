import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/navbar";
import Carlist from "../components/carlist";
import "./home.css";

export default function Home() {
    const navigate = useNavigate();

    const [cars, setCars] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("access");

        if (!token) {
            navigate("/login");
            return;
        }

        fetch("http://127.0.0.1:8000/api/cars/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        })
            .then(async (response) => {
                if (response.status === 401 || response.status === 403) {
                    localStorage.removeItem("access");
                    localStorage.removeItem("refresh");
                    localStorage.removeItem("username");
                    navigate("/login");
                    return null;
                }

                if (!response.ok) {
                    throw new Error("Nem sikerült betölteni az autókat.");
                }

                return response.json();
            })
            .then((data) => {
                if (!data) {
                    return;
                }

                if (Array.isArray(data)) {
                    setCars(data);
                } else if (Array.isArray(data.results)) {
                    setCars(data.results);
                } else {
                    setCars([]);
                }

                setIsLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setIsLoading(false);
            });
    }, [navigate]);

    return (
        <div>
            <Navbar />

            <main className="home-content">
                <section className="home-header">
                    <h1>Elérhető autók</h1>
                    <p>
                        Itt láthatod a rendszerben szereplő bérelhető járműveket.
                    </p>
                </section>

                {isLoading && <p className="info-message">Betöltés...</p>}

                {error && <p className="error-message">{error}</p>}

                {!isLoading && !error && cars.length === 0 && (
                    <p className="info-message">Jelenleg nincs megjeleníthető autó.</p>
                )}

                {!isLoading && !error && cars.length > 0 && (
                    <div className="car-grid">
                        {cars.map((car) => (
                            <Carlist
                                key={car.id}
                                brand={car.brand}
                                model={car.model}
                                year={car.year}
                                licensePlate={car.license_plate}
                                mileage={car.mileage}
                                price={car.daily_price}
                                available={car.available}
                            />
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}