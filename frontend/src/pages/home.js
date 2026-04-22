import { useState, useEffect } from "react";
import Navbar from "../components/navbar";
import Carlist from "../components/carlist";
import "./home.css";

export default function Home() {
    // Set up state variables
    const [cars, setCars] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch data from the Django backend when the page loads
    const myToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2ODc0MzkxLCJpYXQiOjE3NzY4NzQwOTEsImp0aSI6ImU4NjZjYTMyMzE4NzRlM2E4NzBiN2NiODBlZWEyMWFhIiwidXNlcl9pZCI6IjEifQ.GDe0OpGuBlz99UQ5IoGXCx4QVlYMWDFTfguRCdA1OYw";

    useEffect(() => {
        fetch("http://localhost:8000/api/cars/", {
            method: "GET",
            headers: {
                // Note: If Django uses JWT, the word is usually "Bearer". 
                // If it uses standard DRF Tokens, the word is usually "Token".
                "Authorization": `Bearer ${myToken}`,
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
                // If Swagger shows a paginated response (data.results), change this to setCars(data.results)
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

                {/* Loading State */}
                {isLoading && (
                    <div className="loading-container">
                        <p className="loading-text">Adatok betöltése folyamatban...</p>
                    </div>
                )}

                {/* Error State */}
                {error && (
                    <div className="error-container" style={{ color: "red", padding: "20px", border: "1px solid red", borderRadius: "5px", marginBottom: "20px" }}>
                        <p className="error-text"><strong>Hiba:</strong> {error}</p>
                        <p>Kérjük, ellenőrizze, hogy a Django szerver fut-e.</p>
                    </div>
                )}

                {/* Success State: Display the Car Grid */}
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