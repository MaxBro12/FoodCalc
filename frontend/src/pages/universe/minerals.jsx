import {useEffect, useState} from "react";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import db_service from "../../api/universe.jsx";
import {mineral_color} from "../../utils/minerals_colors.jsx";
import {Mineral} from "../../components/mineral.jsx";


export const Minerals = () => {
    const [loading, set_loading] = useState(true);
    const [items, set_items] = useState([]);

    const update_items = async () => {
        set_loading(true)
        const minerals = (await db_service.minerals()).filter(miner => miner.type_id !== 1)
        set_items(minerals);
        set_loading(false)
    }

    useEffect(() => {
        update_items()
    }, [])

    if (loading) {
        return <LoadingAnimation />
    }

    return <div>
        <table style={{padding: '5px'}}>
            <thead className='desktop'>
            <tr>
                <th></th>
                <th>Норма (мг)</th>
                <th>Описание</th>
            </tr>
            </thead>
            <tbody className='desktop'>
            {items.map((item, index) => <tr key={index}>
                <td><Mineral mineral={item}/></td>
                <td style={{
                    textAlign: 'center',
                }}>{item.intake}</td>
                <td>{item.description}</td>
            </tr>)}
            </tbody>
            <tbody className='mobile'>
            {items.map((item, index) => <tr key={index}>
                <td><Mineral mineral={item} compact={true} adt_str={item.intake}/></td>
                <td style={{textAlign: 'justify'}}>{item.description}</td>
            </tr>)}
            </tbody>
        </table>
    </div>
}