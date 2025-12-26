import {useEffect, useState} from "react";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import db_service from "../../api/universe.jsx";
import {mineral_color} from "../../utils/minerals_colors.jsx";


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
                {item.minerals.map((i, index) => <div style={{
                    border: `5px solid ${mineral_color(item.name).color}`,
                    borderRadius: '10px',
                    padding: '5px',
                    color: mineral_color(item.name).color,
                    backgroundColor: mineral_color(item.name).background,
                    fontWeight: 'bolder',
                    textAlign: 'center',
                    verticalAlign: 'middle',
                    userSelect: 'none',
                    width: '45px',
                    height: '45px',
                }} key={index}>{i.name}</div>)}
            </div>
        </div>)}
    </div>
}