import { useNavigate } from "react-router-dom";

function Banner() {
    /* Include Home button image the Basket component, login/sign out button*/

    const navigate = useNavigate()

    return(
        <div className="Banner">
            <h1>Fucking</h1>
            <button type="text" onClick={() => navigate(`/register`)}> Register </button>
            <button type="text" onClick={() => navigate(`/login`)}> Log in </button>
            <button type="text" onClick={() => navigate(`/logout`)}> Log out </button>
            <button type="text" onClick={() => navigate(`/seller`)}> Seller </button>
            <button type="text" onClick={() => navigate(`/admin`)}> Admin </button>
            <button type="text" onClick={() => navigate(`/basket`)}> Basket </button>
        </div>
        
    );
        
}
export default Banner