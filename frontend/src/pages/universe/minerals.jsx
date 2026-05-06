import {useEffect, useState} from "react";
import {LoadingAnimation} from "@/components/utils/loading_animation.jsx";
import db_service from "@/api/universe.jsx";
//import {mineral_color} from "@/utils/minerals_colors.jsx";
import {Mineral} from "@/components/mineral.jsx";
import {useDevice} from "@/context/mobile.jsx";


export const MineralsPage = () => {
    const {isMobile} = useDevice()
    const [loading, set_loading] = useState(true);
    const [items, set_items] = useState([]);

    console.log(items)

    useEffect(() => {
        const update_items = async () => {
            set_loading(true)
            set_items((await db_service.minerals.all()).filter(miner => miner.type_id !== 1));
            set_loading(false)
        }
        update_items()
    }, [])

    if (loading) {
        return <LoadingAnimation />
    }

    return <div>
        <table style={{padding: '5px'}}>
            {!isMobile && <thead>
            <tr>
                <th></th>
                <th>Норма (мг)</th>
                <th>Описание</th>
            </tr>
            </thead>}
            {!isMobile && <tbody>
            {items.map((item, index) => <tr key={index}>
                <td><Mineral mineral={item}/></td>
                <td style={{
                    textAlign: 'center',
                }}>{item.daily_value}</td>
                <td>{item.description}</td>
            </tr>)}
            </tbody>}
            {isMobile && <tbody className='mobile'>
            {items.map((item, index) => <tr key={index}>
                <td><Mineral mineral={item} compact={true} adt_str={item.daily_value}/></td>
                <td style={{textAlign: 'justify'}}>{item.description}</td>
            </tr>)}
            </tbody>}
        </table>
    </div>
}
