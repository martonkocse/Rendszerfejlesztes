import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/navbar";
import "./invoices.css";

export default function Invoices() {
    const navigate = useNavigate();

    const [invoices, setInvoices] = useState([]);
    const [rentals, setRentals] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    const logoutAndRedirect = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("username");
        navigate("/login");
    };

    const getToken = () => {
        return localStorage.getItem("access");
    };

    const loadInvoices = async () => {
        const token = getToken();

        if (!token) {
            logoutAndRedirect();
            return;
        }

        setIsLoading(true);
        setError("");

        try {
            const invoiceResponse = await fetch("http://127.0.0.1:8000/api/invoices/", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (invoiceResponse.status === 401 || invoiceResponse.status === 403) {
                logoutAndRedirect();
                return;
            }

            if (!invoiceResponse.ok) {
                throw new Error("Nem sikerült betölteni a számlákat.");
            }

            const invoiceData = await invoiceResponse.json();

            if (Array.isArray(invoiceData)) {
                setInvoices(invoiceData);
            } else if (Array.isArray(invoiceData.results)) {
                setInvoices(invoiceData.results);
            } else {
                setInvoices([]);
            }

            const rentalResponse = await fetch("http://127.0.0.1:8000/api/rentals/", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (rentalResponse.ok) {
                const rentalData = await rentalResponse.json();

                if (Array.isArray(rentalData)) {
                    setRentals(rentalData);
                } else if (Array.isArray(rentalData.results)) {
                    setRentals(rentalData.results);
                } else {
                    setRentals([]);
                }
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadInvoices();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const findRental = (rentalId) => {
        return rentals.find((rental) => rental.id === rentalId);
    };

    const formatDate = (date) => {
        if (!date) {
            return "Nincs adat";
        }

        return new Date(date).toLocaleDateString("hu-HU");
    };

    return (
        <div>
            <Navbar />

            <main className="invoices-page">
                <section className="invoices-header">
                    <h1>Számlák</h1>
                    <p>
                        Itt láthatók a lezárt bérlésekhez tartozó számlák.
                    </p>
                </section>

                <div className="invoices-toolbar">
                    <button type="button" onClick={loadInvoices}>
                        Lista frissítése
                    </button>
                </div>

                {isLoading && <p className="invoices-info">Betöltés...</p>}

                {error && <p className="invoices-error">{error}</p>}

                {!isLoading && !error && invoices.length === 0 && (
                    <p className="invoices-info">
                        Jelenleg nincs megjeleníthető számla.
                    </p>
                )}

                {!isLoading && !error && invoices.length > 0 && (
                    <div className="invoices-table-wrapper">
                        <table className="invoices-table">
                            <thead>
                                <tr>
                                    <th>Számla</th>
                                    <th>Bérlés</th>
                                    <th>Autó</th>
                                    <th>Ügyfél</th>
                                    <th>Kiállítás dátuma</th>
                                    <th>Összeg</th>
                                    <th>Fizetve</th>
                                </tr>
                            </thead>

                            <tbody>
                                {invoices.map((invoice) => {
                                    const rental = findRental(invoice.rental);

                                    return (
                                        <tr key={invoice.id}>
                                            <td>#{invoice.id}</td>

                                            <td>#{invoice.rental}</td>

                                            <td>
                                                {rental ? (
                                                    <>
                                                        <strong>
                                                            {rental.car?.brand} {rental.car?.model}
                                                        </strong>
                                                        <br />
                                                        <span className="muted-text">
                                                            {rental.car?.license_plate || "Nincs rendszám"}
                                                        </span>
                                                    </>
                                                ) : (
                                                    <span className="muted-text">Nincs adat</span>
                                                )}
                                            </td>

                                            <td>
                                                {rental ? (
                                                    <>
                                                        <strong>
                                                            {rental.customer?.username || "Nincs adat"}
                                                        </strong>
                                                        <br />
                                                        <span className="muted-text">
                                                            {rental.customer?.email || "Nincs e-mail"}
                                                        </span>
                                                    </>
                                                ) : (
                                                    <span className="muted-text">Nincs adat</span>
                                                )}
                                            </td>

                                            <td>{formatDate(invoice.issued_date)}</td>

                                            <td>
                                                <strong>{invoice.amount} Ft</strong>
                                            </td>

                                            <td>
                                                <span className={invoice.paid ? "paid-badge paid" : "paid-badge unpaid"}>
                                                    {invoice.paid ? "Igen" : "Nem"}
                                                </span>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </main>
        </div>
    );
}