import {useEffect, useState} from "react";
import db_service from "../../api/universe.jsx";

import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import {Mineral} from "../../components/mineral.jsx";


export const MineralsTypes = () => {
    const [loading, set_loading] = useState(true);
    const [items, set_items] = useState([]);

    const update_items = async () => {
        set_loading(true)
        set_items(await db_service.types());
        set_loading(false)
    }

    useEffect(() => {
        update_items()
    }, [])

    if (loading) {
        return <LoadingAnimation />
    }

    return <div style={{
        padding: '10px',
    }}>
        {items.map((item, index) => <div style={{

        }} key={index}>
            <h3>{item.name}</h3>
            <p style={{margin: '5px 0px', textAlign: 'justify'}}>{item.description}</p>
            <div className='base_flex_row'>
                {item.minerals.map((i, index) => <Mineral key={index} mineral={i} spec_type_id={item.id} compact={true}/>)}
            </div>
        </div>)}
    </div>
}