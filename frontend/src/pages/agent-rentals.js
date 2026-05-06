import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/navbar";
import "./agent-rentals.css";

export default function AgentRentals() {
    const navigate = useNavigate();

    const [rentals, setRentals] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const getToken = () => {
        return localStorage.getItem("access");
    };

    const logoutAndRedirect = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("username");
        navigate("/login");
    };

    const loadRentals = async () => {
        const token = getToken();

        if (!token) {
            logoutAndRedirect();
            return;
        }

        setIsLoading(true);
        setError("");
        setMessage("");

        try {
            const response = await fetch("http://127.0.0.1:8000/api/rentals/", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (response.status === 401 || response.status === 403) {
                throw new Error("Nincs jogosultságod az ügyintézői felülethez.");
            }

            if (!response.ok) {
                throw new Error("Nem sikerült betölteni a kölcsönzéseket.");
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
        loadRentals();
    }, []);

    const handleAction = async (rentalId, actionName, successText) => {
        const token = getToken();

        if (!token) {
            logoutAndRedirect();
            return;
        }

        setMessage("");
        setError("");

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/rentals/${rentalId}/${actionName}/`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            const data = await response.json();

            if (!response.ok) {
                if (data.detail) {
                    throw new Error(data.detail);
                }

                if (data.status) {
                    throw new Error(data.status);
                }

                throw new Error("A művelet nem sikerült.");
            }

            setMessage(successText);
            await loadRentals();
        } catch (err) {
            setError(err.message);
        }
    };

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
                return "status-badge pending";
            case "APPROVED":
                return "status-badge approved";
            case "REJECTED":
                return "status-badge rejected";
            case "HANDED_OVER":
                return "status-badge handed-over";
            case "RETURNED":
                return "status-badge returned";
            default:
                return "status-badge";
        }
    };

    const renderActions = (rental) => {
        if (rental.status === "PENDING") {
            return (
                <>
                    <button
                        className="action-button approve-button"
                        onClick={() => handleAction(rental.id, "approve", "A kölcsönzés jóvá lett hagyva.")}
                    >
                        Jóváhagyás
                    </button>

                    <button
                        className="action-button reject-button"
                        onClick={() => handleAction(rental.id, "reject", "A kölcsönzés el lett utasítva.")}
                    >
                        Elutasítás
                    </button>
                </>
            );
        }

        if (rental.status === "APPROVED") {
            return (
                <button
                    className="action-button handover-button"
                    onClick={() => handleAction(rental.id, "handover", "Az autó átadása rögzítve lett.")}
                >
                    Autó átadása
                </button>
            );
        }

        if (rental.status === "HANDED_OVER") {
            return (
                <button
                    className="action-button return-button"
                    onClick={() => handleAction(rental.id, "return_car", "Az autó visszavétele rögzítve lett.")}
                >
                    Autó visszavétele
                </button>
            );
        }

        return <span className="no-action">Nincs elérhető művelet</span>;
    };

    return (
        <div>
            <Navbar />

            <main className="agent-page">
                <section className="agent-header">
                    <h1>Ügyintézői felület</h1>
                    <p>
                        Itt kezelhetők a beérkezett kölcsönzési igények, az autó átadása és visszavétele.
                    </p>
                </section>

                <div className="agent-toolbar">
                    <button onClick={loadRentals} className="refresh-button">
                        Lista frissítése
                    </button>
                </div>

                {isLoading && <p className="agent-info">Betöltés...</p>}

                {message && <p className="agent-success">{message}</p>}
                {error && <p className="agent-error">{error}</p>}

                {!isLoading && rentals.length === 0 && !error && (
                    <p className="agent-info">Jelenleg nincs kölcsönzési igény.</p>
                )}

                {!isLoading && rentals.length > 0 && (
                    <div className="rentals-table-wrapper">
                        <table className="rentals-table">
                            <thead>
                                <tr>
                                    <th>Azonosító</th>
                                    <th>Autó</th>
                                    <th>Ügyfél</th>
                                    <th>Időszak</th>
                                    <th>Státusz</th>
                                    <th>Műveletek</th>
                                </tr>
                            </thead>

                            <tbody>
                                {rentals.map((rental) => (
                                    <tr key={rental.id}>
                                        <td>#{rental.id}</td>

                                        <td>
                                            <strong>
                                                {rental.car?.brand} {rental.car?.model}
                                            </strong>
                                            <br />
                                            <span className="muted-text">
                                                {rental.car?.license_plate}
                                            </span>
                                        </td>

                                        <td>
                                            <strong>{rental.customer?.username}</strong>
                                            <br />
                                            <span className="muted-text">
                                                {rental.customer?.email || "Nincs e-mail"}
                                            </span>
                                        </td>

                                        <td>
                                            {rental.start_date} <br />
                                            {rental.end_date}
                                        </td>

                                        <td>
                                            <span className={getStatusClass(rental.status)}>
                                                {getStatusText(rental.status)}
                                            </span>
                                        </td>

                                        <td>
                                            <div className="action-list">
                                                {renderActions(rental)}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </main>
        </div>
    );
}