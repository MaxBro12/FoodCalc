import {Mineral} from "@/components/mineral.jsx";


export const ProductDetail = ({ data, on_close, update }) => {
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
                <span>Код: {data.id}</span>
                <span>Добавлено: {data.added_by_name}</span>
                <span>{data.description}</span>
                <span>Калорийность: {data.calories} ККал</span>
                <span>Энергетическая ценность: {data.energy} КДж</span>

                {sorted_minerals.minerals.length > 0 && <div className='base_flex_row' style={{
                    padding: '5px',
                }}>
                    {sorted_minerals.minerals.map((mineral, index) => <Mineral key={index} mineral={mineral} adt_str={mineral.content}/>)}
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
                <span>Код: {data.id}</span>
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
                        <Mineral mineral={mineral} compact={true}/>
                        <span>{mineral.content}</span>
                    </div>)}
                </div>}
            </div>
        </div>
    </div>
}
