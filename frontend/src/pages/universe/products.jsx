import {useEffect, useState} from "react";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import db_service from "../../api/universe.jsx";


export const Products = () => {
    const [loading, set_loading] = useState(true);
    const [items, set_items] = useState([]);

    const update_items = async () => {
        set_loading(true)
        set_items(await db_service.products());
        set_loading(false)
    }

    useEffect(() => {
        update_items()
    }, [])

    if (loading) {
        return <LoadingAnimation />
    }

    return <div>
        {items.map((item, index) => <div style={{

        }} key={index}>
            <h3>{item.name}</h3>
            <p>{item.description}</p>
        </div>)}
    </div>
}