import {useEffect, useState} from "react";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import db_service from "../../api/universe.jsx";
import {mineral_color} from "../../utils/minerals_colors.jsx";


export const Minerals = () => {
    const [loading, set_loading] = useState(true);
    const [items, set_items] = useState([]);

    const update_items = async () => {
        set_loading(true)
        set_items(await db_service.minerals());
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
                <td style={{
                    border: `5px solid ${mineral_color(item.type_name).color}`,
                    borderRadius: '10px',
                    padding: '5px',
                    color: mineral_color(item.type_name).color,
                    backgroundColor: mineral_color(item.type_name).background,
                    fontWeight: 'bolder',
                    textAlign: 'center',
                    userSelect: 'none',
                }}>{item.name}</td>
                <td style={{
                    textAlign: 'center',
                }}>{item.intake}</td>
                <td>{item.description}</td>
            </tr>)}
            </tbody>
            <tbody className='mobile'>
            {items.map((item, index) => <tr key={index}>
                <td className='base_flex_column' style={{
                    border: `5px solid ${mineral_color(item.type_name).color}`,
                    borderRadius: '10px',
                    padding: '5px',
                    backgroundColor: mineral_color(item.type_name).background,
                    fontWeight: 'bolder',
                }}><span style={{
                    color: mineral_color(item.type_name).color,
                    userSelect: 'none',
                }}>{item.name}</span><span style={{
                    color: mineral_color(item.type_name).color,
                }}>{item.intake}</span></td>
                <td style={{textAlign: 'justify'}}>{item.description}</td>
            </tr>)}
            </tbody>
        </table>
    </div>
}