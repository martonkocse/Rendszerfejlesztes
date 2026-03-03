import "./carlist.css";
export default function Carlist({ brand, model, price }) {
    return (
        <div className="car-card">
            <h2>{brand} {model}</h2>
            <p>Ár naponta: {price}Ft</p>
            <button>Bérlés</button>
        </div>
    );
}