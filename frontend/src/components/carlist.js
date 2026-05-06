import "./carlist.css";

export default function Carlist({
    brand,
    model,
    year,
    licensePlate,
    mileage,
    price,
    available
}) {
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

            <button disabled={!available}>
                {available ? "Bérlés indítása" : "Nem foglalható"}
            </button>
        </article>
    );
}