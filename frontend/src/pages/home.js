import { useState } from "react";
import Navbar from "../components/navbar";
import Carlist from "../components/carlist";
import "./home.css";

//use static data before data form the backend
export default function Home() {
    const [cars] = useState([
        { id: 1, brand: "BMW", model: "320d", price: 80 },
        { id: 2, brand: "Audi", model: "A4", price: 75 },
        { id: 3, brand: "Toyota", model: "Corolla", price: 50 },
        { id: 4, brand: "Mercedes", model: "C200", price: 90 },
        { id: 5, brand: "Ford", model: "Focus", price: 45 },
        { id: 6, brand: "Volkswagen", model: "Golf", price: 55 },
        { id: 7, brand: "Škoda", model: "Octavia", price: 60 },
        { id: 8, brand: "Hyundai", model: "i30", price: 48 },
        { id: 9, brand: "Opel", model: "Corsa", price: 35 },
    ]);

    return (
        <div>
            <Navbar />

            <main className="home-content">
                <h1>Elérhető autók</h1>

                <div className="car-grid">
                    {cars.map((car) => (
                        <Carlist
                            key={car.id}
                            brand={car.brand}
                            model={car.model}
                            price={car.price}
                        />
                    ))}
                </div>
            </main>
        </div>
    );
}