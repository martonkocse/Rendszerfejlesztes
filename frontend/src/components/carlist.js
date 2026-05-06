import { useState } from "react";
import "./carlist.css";

export default function Carlist({
    id,
    brand,
    model,
    year,
    licensePlate,
    mileage,
    price,
    available
}) {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleRental = async () => {
        setMessage("");
        setError("");

        if (!startDate || !endDate) {
            setError("Add meg a kezdő és záró dátumot.");
            return;
        }

        if (startDate > endDate) {
            setError("A záró dátum nem lehet korábbi, mint a kezdő dátum.");
            return;
        }

        const token = localStorage.getItem("access");

        if (!token) {
            setError("A bérléshez be kell jelentkezni.");
            return;
        }

        setIsSubmitting(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/rentals/", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    car_id: id,
                    start_date: startDate,
                    end_date: endDate
                })
            });

            const data = await response.json();

            if (!response.ok) {
                if (typeof data === "string") {
                    throw new Error(data);
                }

                if (data.detail) {
                    throw new Error(data.detail);
                }

                if (data.non_field_errors) {
                    throw new Error(data.non_field_errors[0]);
                }

                if (data.start_date) {
                    throw new Error(data.start_date[0]);
                }

                if (data.end_date) {
                    throw new Error(data.end_date[0]);
                }

                if (data.car_id) {
                    throw new Error(data.car_id[0]);
                }

                throw new Error("A bérlési igény rögzítése nem sikerült.");
            }

            setMessage("A bérlési igény rögzítve lett. Státusz: függőben.");
            setStartDate("");
            setEndDate("");
        } catch (err) {
            setError(err.message);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <article className="car-card">
            <div className="car-card-header">
                <h2>{brand} {model}</h2>
                <span className={available ? "status available" : "status unavailable"}>
                    {available ? "Elérhető" : "Nem elérhető"}
                </span>
            </div>

            <div className="car-details">
                <p>Évjárat: {year}</p>
                <p>Rendszám: {licensePlate}</p>
                <p>Kilométeróra: {mileage} km</p>
                <p className="price">Napi díj: {price} Ft</p>
            </div>

            <div className="rental-form">
                <label>Kezdő dátum</label>
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    disabled={!available || isSubmitting}
                />

                <label>Záró dátum</label>
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    disabled={!available || isSubmitting}
                />
            </div>

            {message && <p className="rental-success">{message}</p>}
            {error && <p className="rental-error">{error}</p>}

            <button
                type="button"
                disabled={!available || isSubmitting}
                onClick={handleRental}
            >
                {!available
                    ? "Nem foglalható"
                    : isSubmitting
                        ? "Küldés..."
                        : "Bérlés indítása"}
            </button>
        </article>
    );
}