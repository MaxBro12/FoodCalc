import {useEffect, useState} from "react";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import db_service from "../../api/universe.jsx";


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
            <p>{item.description}</p>
            <div className='base_flex_row'>
                {item.minerals.map((i, index) => <div style={{
                    border: '5px solid rgb(30,105,216)',
                    borderRadius: '10px',
                    padding: '5px',
                    color: 'rgb(31,118,251)',
                    backgroundColor: 'rgba(13,126,255,0.29)',
                    fontWeight: 'bolder',
                    textAlign: 'center',
                    verticalAlign: 'middle',
                    userSelect: 'none',
                    width: '30px',
                    height: '30px',
                }} key={index}>{i.name}</div>)}
            </div>
        </div>)}
    </div>
}