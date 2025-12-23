import {useEffect, useState} from "react";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import db_service from "../../api/universe.jsx";


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
        <table>
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
                    border: '5px solid rgb(30,105,216)',
                    borderRadius: '10px',
                    padding: '5px',
                    color: 'rgb(31,118,251)',
                    backgroundColor: 'rgba(13,126,255,0.29)',
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
                    border: '5px solid rgb(30,105,216)',
                    borderRadius: '10px',
                    padding: '5px',
                    backgroundColor: 'rgba(13,126,255,0.29)',
                    fontWeight: 'bolder',
                }}><span style={{
                    color: 'rgb(31,118,251)',
                    userSelect: 'none',
                }}>{item.name}</span><span style={{
                    color: 'rgb(31,118,251)',
                }}>{item.intake}</span></td>
                <td>{item.description}</td>
            </tr>)}
            </tbody>
        </table>
    </div>
}