import {useEffect, useState} from "react";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import db_service from "../../api/universe.jsx";
import {useNavigate} from "react-router-dom";
import PaginationTable from "../../components/utils/custom_tables.jsx";
import {not_to_long_text} from "../../components/utils/string_line.jsx";
import {Mineral} from "../../components/mineral.jsx";


const ProductsHeader = () => {
    return <tr>
        <th style={{textAlign: 'left', width: '250px'}}>Название</th>
        <th style={{textAlign: 'left'}}>Описание</th>
    </tr>
}

const ProductLine = ({data, update, action_on_click}) => {
    const handle_click = () => {
        action_on_click(data)
    }
    return <tr>
        <td className='mobile' onClick={() => handle_click()} dangerouslySetInnerHTML={{__html: not_to_long_text(data.name, '', 40)}}></td>
        <td className='desktop' onClick={() => handle_click()} dangerouslySetInnerHTML={{__html: not_to_long_text(data.name, '', 100)}}></td>
        <td className='mobile' dangerouslySetInnerHTML={{__html: not_to_long_text('', data.description, 30)}}></td>
        <td className='desktop' dangerouslySetInnerHTML={{__html: not_to_long_text('', data.description, 100)}}></td>
    </tr>
}

const ProductDetail = ({data, on_close, update}) => {
    const sorted_minerals = {...data}
    sorted_minerals.minerals.sort((a,b)=> a.id - b.id)

    const handleOuterClick = () => {
        on_close();
    };

    const handleInnerClick = (e) => {
        e.stopPropagation(); // Останавливаем всплытие события
    };

    return <div className="overlay-backdrop" onClick={() => handleOuterClick()}>
        <div className="overlay-content base_flex_column rounded_border base_margins desktop" style={{
            width: '50em',
        }} onClick={(e) => handleInnerClick(e)}>
            <div className='base_flex_column' style={{
                alignItems: 'flex-start',
                width: '100%',
            }}>
                <span style={{fontWeight: 'bolder'}}>{data.name}</span>
                <span>EAN-13: {data.id}</span>
                <span>Добавлено: {data.added_by_name}</span>
                <span>{data.description}</span>
                <span>Калорийность: {data.calories} ККал</span>
                <span>Энергетическая ценность: {data.energy} КДж</span>

                {sorted_minerals.minerals.length > 0 && <div className='base_flex_row' style={{
                    padding: '5px',
                }}>
                    {sorted_minerals.minerals.map((mineral, index) => <div key={index} className='base_flex_column rounded_border' style={{
                        flexWrap: 'nowrap',
                        padding: '5px'
                    }}>
                        <Mineral mineral={mineral}/>
                        <span>{mineral.content}</span>
                    </div>)}
                </div>}
            </div>
        </div>
        <div className="base_flex_column mobile" style={{
            width: '100%',
            marginTop: '50px'
        }} onClick={(e) => handleInnerClick(e)}>
            <div className='base_flex_column' style={{
                alignItems: 'flex-start',
                width: '100%',
                padding: '5px'
            }}>
                <span style={{fontWeight: 'bolder'}}>{data.name}</span>
                <span>EAN-13: {data.id}</span>
                <span>Добавлено: {data.added_by_name}</span>
                <span>{data.description}</span>
                <span>Калорийность: {data.calories} ККал</span>
                <span>Энергетическая ценность: {data.energy} КДж</span>

                {sorted_minerals.minerals.length > 0 && <div className='base_flex_row' style={{
                    padding: '5px',
                }}>
                    {sorted_minerals.minerals.map((mineral, index) => <div key={index} className='base_flex_column rounded_border' style={{
                        flexWrap: 'nowrap',
                        padding: '5px'
                    }}>
                        <Mineral mineral={mineral}/>
                        <span>{mineral.content}</span>
                    </div>)}
                </div>}
            </div>
        </div>
    </div>
}


export const Products = () => {
    const [loading, set_loading] = useState(true);
    const navigate = useNavigate()

    const [show_details, set_show_details] = useState(false);
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

    return <div style={{
        height: '100%',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-start',
    }}>
        <div className='base_button mobile' style={{
            width: '100%',
            padding: '10px 20px',
            margin: '10px'
        }} onClick={() => navigate('/db/products/new')}>Добавить продукт</div>
        <div className='base_button desktop' style={{
            margin: '5px'
        }} onClick={() => navigate('/db/products/new')}>Добавить продукт</div>
        <PaginationTable CustomHead={ProductsHeader} Line={ProductLine} Detail={ProductDetail} api_request={db_service.products} adt_style={{
            width: '100%',
            marginTop: '0px'
        }}/>
    </div>
}