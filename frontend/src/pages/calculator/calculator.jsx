import { useEffect, useState } from "react";
import db_service from "../../api/universe.jsx";
import {Minerals} from "../universe/minerals.jsx";
import {Mineral} from "../../components/mineral.jsx";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";


const ProductsSearch = ({items, set_current, search_length = 3}) => {
    const [search, set_search] = useState("");
    const [suggestions, set_suggestions] = useState([]);
    const [is_open, set_is_open] = useState(false);

    const handleSelectItem = (item) => {
        set_search(item.name);
        set_current(item)
        set_search('')
        set_suggestions([])
        set_is_open(false);
    };

    const handle_search_change = async (e) => {
        e.preventDefault()
        const value = e.target.value
        if (value.trim() === '') {
            set_suggestions([]);
            set_is_open(false);
        } else if (value.trim().length <= search_length) {
            const filtered = items.filter(item =>
                item.name.toLowerCase().includes(value.toLowerCase())
            );
            set_suggestions(filtered);
            set_is_open(filtered.length > 0);
        } else {
            const searches = await db_service.products_search(value);
            set_suggestions(searches);
            set_is_open(searches.length > 0);
        }
        set_search(value);
    }

    return <div className="search-container" style={{width: "100%"}}>
        <div className="search-input-container">
            <input
                type="text"
                value={search}
                onChange={(e) => handle_search_change(e)}
                placeholder='Название продукта или код'
                className="search-input rounded_border"
                aria-haspopup="listbox"
                aria-expanded={is_open}
            />
            {is_open && (
                <ul className="dropdown-menu" role="listbox">
                    {suggestions.map(item => <li
                        key={item.id}
                        onClick={() => handleSelectItem(item)}
                        className="suggestion-item"
                        role="option">{item.name}</li>
                    )}
                </ul>
            )}
        </div>
    </div>
}


export const Calculator = () => {
    const [loading, set_loading] = useState(false);

    const [products_names, set_products_names] = useState([]);
    const [products, set_products] = useState([]);

    const get_products_names = async () => {
        let items = await db_service.products_names()
        let new_items = [...items]
        for (const item of items) {
            new_items.push({id: item.id, name: item.id, search_index: item.search_index});
        }
        new_items.sort((a, b) => b.search_index - a.search_index)
        set_products_names(new_items)
    }

    const handle_current = async (e) => {
        if (products.length === 0) {
            set_loading(true);
            set_products([await db_service.product_detail(e.id)])
            set_loading(false);
        } else {
            if (!products.some(product => product.id === e.id)) {
                set_loading(true);
                set_products([...products, await db_service.product_detail(e.id)])
                set_loading(false);
            }
        }
    }
    const handle_delete = (id) => {
        set_products(products.filter(product => product.id !== id));
    }

    useEffect(() => {
        get_products_names();
    }, []);

    if (loading) {
        return <LoadingAnimation />
    }

    return <div style={{padding: '5px', width: '100%', justifyContent: 'flex-start'}} className='full_screen'>
        <ProductsSearch items={products_names} set_current={handle_current} />
        {products.length > 0 && <ul className='rounded_border base_flex_column' style={{
            listStyleType: 'none',
            textAlign: 'left',
            padding: '5px',
            margin: '5px 0px 0px 0px',
            alignItems: 'flex-start',
            width: '100%'
        }}>
            <span>Выбранные продукты:</span>
            {products.map((item, i) => <li key={i} style={{
                width: '100%'
            }}><div className='base_flex_row'>
                {item.name}{item.minerals?.map((mineral, i) => <Mineral mineral={mineral} adt_style={{
                    height: 25,
                    width: 25,
                    fontSize: 13,
                    borderWidth: 1,
            }} key={i} compact={true}/>)}
                <span onClick={() => handle_delete(item.id)} style={{
                    userSelect: 'none',
                }}>❌</span>
            </div>
                </li>)}
        </ul>}
        <div>

        </div>
    </div>
}
