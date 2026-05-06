import {useEffect, useState} from "react";
import db_service from "../../api/universe.jsx";
import {Mineral} from "../../components/mineral.jsx";


const ShowMaterials = ({minerals, set_close, set_choose}) => {

    const handleOuterClick = () => {
        set_close(false);
    };

    const handleInnerClick = (e) => {
        e.stopPropagation(); // Останавливаем всплытие события
    };

    return <div className='overlay-backdrop' onClick={handleOuterClick}>
        <div className='overlay-content base_flex_row rounded_border' onClick={handleInnerClick}>
            {minerals.map((mineral, index) => <div key={index} onClick={() => set_choose(mineral)}>
                <Mineral mineral={mineral} />
            </div>)}
        </div>
    </div>
}


export const NewProductView = () => {
    const [minerals, set_minerals] = useState([]);
    const [target_minerals, set_target_minerals] = useState([]);
    const [show_materials, set_show_materials] = useState(false);

    const [formData, setFormData] = useState({
        product_id: '',
        product_name: '',
        product_desc: '',
        minerals: [],
        calories: 0,

        energy: 0,
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        await db_service.new_product(
            formData.product_id,
            formData.product_name,
            formData.product_desc,
            target_minerals,
            formData.calories,
            formData.energy,
        );
    }
    const on_choose = (e) => {
        if (target_minerals.length === 0) {
            const new_material = {...e}
            new_material.content = 0
            const new_list = [new_material]
            set_target_minerals(new_list)
        }
        if (!target_minerals.some(item => e.id === item.id)) {
            const new_material = {...e}
            new_material.content = 0
            const new_list = [...target_minerals, new_material  ]
            new_list.sort((a, b) => a.id - b.id)
            set_target_minerals(new_list)
        }
        set_show_materials(false)
    }

    const handle_change_content = (mineral, e) => {
        const new_minerals = [...target_minerals.filter(item => mineral.id !== item.id)];
        const new_mineral = target_minerals.find(item => mineral.id === item.id)
        new_mineral.content = Number(e);
        const new_list = [...new_minerals, new_mineral]
        new_list.sort((a, b) => a.id - b.id)
        set_target_minerals(new_list);
    }

    const update_minerals = async () => {
        set_minerals(await db_service.minerals());
    }

    useEffect(() => {
        update_minerals()
    }, []);

    return <div style={{maxWidth: '600px', padding: '5px'}} className='base_flex_column'>
        {show_materials && <ShowMaterials minerals={minerals} set_close={set_show_materials} set_choose={on_choose} />}
        <form onSubmit={handleSubmit} className='base_flex_column'>
            <input
                type="number"
                name="product_id"
                placeholder="Код товара"
                className='base_button'
                style={{
                    textAlign: 'left',
                    width: '100%',
                }}
                max='9999999999999'
                min='1000000000000'
                value={formData.product_id}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="product_name"
                placeholder="Название"
                className='base_button'
                style={{
                    textAlign: 'left',
                    width: '100%',
                }}
                value={formData.product_name}
                onChange={handleChange}
                required
            />
            <textarea value={formData.product_desc} onChange={handleChange}
                      placeholder='Описание'
                      name='product_desc'
                      style={{
                          padding: '8px 16px',
                          height: 200,
                          width: '100%',
                          border: "1px solid var(--border-color)",
                          backgroundColor: 'var(--button-color)',
                          color: 'var(--text-color)',
                          borderRadius: 10,
                          textAlign: 'left',
                          verticalAlign: 'top',
                          display: "block",
                          position: "relative",
                          marginLeft: "auto",
                          marginRight: "auto",
                      }}/>
            <div className='base_flex_row' style={{flexWrap: 'nowrap', width: '100%'}}>
                <label>Калории (ККАЛ)</label>
                <input
                    type="number"
                    name="calories"
                    placeholder="0"
                    min='0'
                    className='base_button'
                    style={{
                        textAlign: 'center',
                        width: '100%',
                    }}
                    value={formData.calories}
                    onChange={handleChange}
                />
            </div>
            <div className='base_flex_row' style={{flexWrap: 'nowrap', width: '100%'}}>
                <label>Энергоценность (КДж)</label>
                <input
                    type="number"
                    name="energy"
                    placeholder="0"
                    min='0'
                    className='base_button'
                    style={{
                        textAlign: 'center',
                        width: '100%',
                    }}
                    value={formData.energy}
                    onChange={handleChange}
                />
            </div>
            {target_minerals.length > 0 ? <div className='base_flex_column rounded_border' style={{
                padding: target_minerals.length > 0 ? '5px' : 0,
                width: '100%',
            }}>
                <div className='base_button' onClick={() => set_show_materials(true)}>
                    Добавить минерал
                </div>
                {target_minerals.map((mineral, i) => <div key={i} style={{
                    flexWrap: 'nowrap',
                    width: '100%',
                }} className='base_flex_row'>
                    <Mineral mineral={mineral} compact={true}/>
                    <input
                        type="number"
                        placeholder="0"
                        min='0'
                        className='base_button'
                        style={{
                            textAlign: 'center',
                            width: '100%',
                        }}
                        value={mineral.content}
                        onChange={(e) => handle_change_content(mineral, e.target.value)}
                    />
                    <label>мг</label>
                </div>)}
            </div>:<div className='base_button' onClick={() => set_show_materials(true)}>
                Добавить минерал
            </div>}
            <input type='submit' className='base_button'/>
        </form>
    </div>
}