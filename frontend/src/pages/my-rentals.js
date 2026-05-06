import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/navbar";
import "./my-rentals.css";

export default function MyRentals() {
    const navigate = useNavigate();

    const [rentals, setRentals] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    const logoutAndRedirect = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("username");
        navigate("/login");
    };

    const loadMyRentals = async () => {
        const token = localStorage.getItem("access");

        if (!token) {
            logoutAndRedirect();
            return;
        }

        setIsLoading(true);
        setError("");

        try {
            const response = await fetch("http://127.0.0.1:8000/api/rentals/", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (response.status === 401 || response.status === 403) {
                logoutAndRedirect();
                return;
            }

            if (!response.ok) {
                throw new Error("Nem sikerült betölteni a saját bérléseket.");
            }

            const data = await response.json();

            if (Array.isArray(data)) {
                setRentals(data);
            } else if (Array.isArray(data.results)) {
                setRentals(data.results);
            } else {
                setRentals([]);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadMyRentals();
    }, []);

    const getStatusText = (status) => {
        switch (status) {
            case "PENDING":
                return "Függőben";
            case "APPROVED":
                return "Jóváhagyva";
            case "REJECTED":
                return "Elutasítva";
            case "HANDED_OVER":
                return "Átadva";
            case "RETURNED":
                return "Visszavéve";
            default:
                return status;
        }
    };

    const getStatusClass = (status) => {
        switch (status) {
            case "PENDING":
                return "rental-status pending";
            case "APPROVED":
                return "rental-status approved";
            case "REJECTED":
                return "rental-status rejected";
            case "HANDED_OVER":
                return "rental-status handed-over";
            case "RETURNED":
                return "rental-status returned";
            default:
                return "rental-status";
        }
    };

    const calculateDays = (startDate, endDate) => {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diff = end - start;
        return Math.floor(diff / (1000 * 60 * 60 * 24)) + 1;
    };

    const calculateAmount = (rental) => {
        if (!rental.car || !rental.car.daily_price) {
            return null;
        }

        const days = calculateDays(rental.start_date, rental.end_date);
        return days * rental.car.daily_price;
    };

    return (
        <div>
            <Navbar />

            <main className="my-rentals-page">
                <section className="my-rentals-header">
                    <h1>Saját bérléseim</h1>
                    <p>
                        Itt láthatod a leadott bérlési igényeidet és azok aktuális állapotát.
                    </p>
                </section>

                <div className="my-rentals-toolbar">
                    <button type="button" onClick={loadMyRentals}>
                        Lista frissítése
                    </button>
                </div>

                {isLoading && <p className="my-rentals-info">Betöltés...</p>}

                {error && <p className="my-rentals-error">{error}</p>}

                {!isLoading && !error && rentals.length === 0 && (
                    <p className="my-rentals-info">
                        Még nincs leadott bérlési igényed.
                    </p>
                )}

                {!isLoading && !error && rentals.length > 0 && (
                    <div className="my-rentals-grid">
                        {rentals.map((rental) => {
                            const amount = calculateAmount(rental);
                            const days = calculateDays(rental.start_date, rental.end_date);

                            return (
                                <article className="my-rental-card" key={rental.id}>
                                    <div className="my-rental-card-header">
                                        <h2>
                                            {rental.car?.brand} {rental.car?.model}
                                        </h2>

                                        <span className={getStatusClass(rental.status)}>
                                            {getStatusText(rental.status)}
                                        </span>
                                    </div>

                                    <div className="my-rental-details">
                                        <p>
                                            <strong>Azonosító:</strong> #{rental.id}
                                        </p>

                                        <p>
                                            <strong>Rendszám:</strong>{" "}
                                            {rental.car?.license_plate || "Nincs adat"}
                                        </p>

                                        <p>
                                            <strong>Időszak:</strong>{" "}
                                            {rental.start_date} és {rental.end_date} között
                                        </p>

                                        <p>
                                            <strong>Napok száma:</strong> {days}
                                        </p>

                                        <p>
                                            <strong>Napi díj:</strong>{" "}
                                            {rental.car?.daily_price || "Nincs adat"} Ft
                                        </p>

                                        {amount !== null && (
                                            <p className="my-rental-price">
                                                <strong>Becsült összeg:</strong> {amount} Ft
                                            </p>
                                        )}

                                        <p>
                                            <strong>Ügyintéző:</strong>{" "}
                                            {rental.agent?.username || "Még nincs hozzárendelve"}
                                        </p>

                                        <p>
                                            <strong>Létrehozva:</strong>{" "}
                                            {rental.created_at
                                                ? new Date(rental.created_at).toLocaleString("hu-HU")
                                                : "Nincs adat"}
                                        </p>
                                    </div>
                                </article>
                            );
                        })}
                    </div>
                )}
            </main>
        </div>
    );
}