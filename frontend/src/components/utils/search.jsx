import { useState, useEffect, useRef, useCallback } from 'react';


const BaseLine = ({ data }) => {
    return <span>{data?.name}</span>
}

function base_search(query, items) {
    return items.filter(item => item.name.toLowerCase().includes(query.toLowerCase()))
}


export const Search = ({
    current_item,
    items = [],
    handle_select_item = undefined,
    handle_search = base_search,
    Current_item_element = BaseLine,
    Line_element = BaseLine,
    min_len_to_request = 3,
    func_request = undefined,
    delay = 500,
    adt_style = {},
}) => {
    /*
    Компонент для поиска по заданным элементам
    - current_item - текущее выбранное значение
    - items - список элементов для поиска
    - handle_select_item - функция вызываемая при выборе элемента
    - handle_search - функция вызываемая при вводе поискового запроса сопоставляет введенный запрос с элементами из списка items
    - Current_item_element - компонент для отображения текущего выбранного элемента (дополнительная кастомизация если потребуется)
    - Line_element - компонент для отображения элементов в списке suggestions
    - min_len_to_request - минимальная длина для вызова функции запроса
    - func_request - функция для запроса подходящих значений по поисковому запросу должна принимать строку запроса и возвращать массив подходящих элементов
    - delay - задержка для ввода перед началом поиска
    - adt_style - дополнительные стили для компонента
    */
    const [search_term, set_search_term] = useState('');
    const [suggestions, set_suggestions] = useState(items);
    const [is_open, set_is_open] = useState(false);
    const timeoutRef = useRef(null);

    const debouncedSearch = useCallback((value) => {
        // Очищаем предыдущий таймаут
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        // Если строка поиска пустая
        if (value.trim() === '') {
            set_suggestions([]);
            set_is_open(false);
            return;
        }

        // Устанавливаем новый таймаут
        timeoutRef.current = setTimeout(async () => {
            if (value.trim().length <= min_len_to_request) {
                const filtered = handle_search(value.trim(), items);
                set_suggestions(filtered);
                set_is_open(filtered.length > 0);
            } else {
                if (func_request) {
                    const searches = await func_request(value.trim());
                    set_suggestions(searches);
                    set_is_open(searches.length > 0);
                } else {
                    // Если func_request не предоставлен, используем локальный поиск
                    const filtered = handle_search(value.trim(), items);
                    set_suggestions(filtered);
                    set_is_open(filtered.length > 0);
                }
            }
        }, delay);
    }, [items, min_len_to_request, handle_search, func_request, delay]);

    const handle_search_change = (e) => {
        e.preventDefault();
        const value = e.target.value;
        set_search_term(value);
        debouncedSearch(value);
    };

    // Очистка таймаута при размонтировании компонента
    useEffect(() => {
        return () => {
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }
        };
    }, []);

    return <div className="search-container" style={{width: "100%", ...adt_style}}>
        <div className="search-input-container">
            <input
                type="text"
                value={search_term}
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
                        onClick={() => handle_select_item(item)}
                        className="suggestion-item"
                        role="option"><Line_element data={item}/></li>
                    )}
                </ul>
            )}
        </div>
    </div>
}


export default Search;
