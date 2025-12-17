import auth_service from "../api/auth.jsx";
import {Link, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";


const MobileHeaderView = ({headers, set_show}) => {
    const navigate = useNavigate();

    const handleOuterClick = () => {
        set_show(false);
    };

    const handleInnerClick = (e) => {
        e.stopPropagation(); // Останавливаем всплытие события
    };

    const nav = (path) => {
        set_show(false);
    }

    return <div className='overlay-backdrop' onClick={() => handleOuterClick()}>
        <div className='overlay-content base_flex_column rounded_border' style={{
            flexWrap: 'nowrap',

            backgroundColor: 'var(--header-color)',
            color: 'var(--header-text-color)',

            height: '30vh',
            width: '80%',
        }} onClick={(e) => handleInnerClick(e)}>
            {headers.map((header, i) => <Link key={i} style={{
                backgroundColor: is_current_window(header.path) ? 'var(--header-current-color)': 'inherit',
                color: is_current_window(header.path) ? 'var(--header-current-text-color)': 'var(--header-text-color)',
                textDecoration: 'none',
                ...header.d_style,
            }} to={header.path} className='header_a'>{header.label}</Link>)}
        </div>
    </div>
}


const CustomHeader = ({logo, headers, username, set_theme}) => {
    const navigate = useNavigate();

    const [mobile_show_view, set_mobile_show_view] = useState(false);

    function is_current_window(path) {
        return window.location.pathname.startsWith(path)
    }
    function get_current_window() {
        for (const i of headers) {
            if (window.location.pathname.startsWith(i.path)) {
                return i.label
            }
        }
        return ''
    }

    useEffect(() => {

    }, []);

    return <header style={{
        backgroundColor: 'var(--header-color)',
        width: '100%',
        height: '50px',
        flexShrink: 0,
    }}>
        <div className='desktop base_flex_row' style={{
            backgroundColor: 'var(--header-color)',
            alignItems: 'center',
            height: '100%',

            gap: 0,
            flexWrap: 'nowrap',
        }}>
            {logo}
            {headers.map((header, i) => <Link key={i} style={{
                backgroundColor: is_current_window(header.path) ? 'var(--header-current-color)': 'inherit',
                color: is_current_window(header.path) ? 'var(--header-current-text-color)': 'var(--header-text-color)',
                textDecoration: 'none',
                ...header.d_style,
            }} to={header.path} className='header_a'>{header.label}</Link>)}
        </div>
        <div className='mobile base_flex_row' style={{
            backgroundColor: 'var(--header-color)',
            alignItems: 'center',
            height: '100%',
            gap: 0,
            flexWrap: 'nowrap',
        }}>
            {logo}
            <span className='header_a' style={{

            }}>{get_current_window()}</span>
            <button className='header_a' style={{
                marginLeft: 'auto',
                marginRight: '5px',
                padding: '15px',
                color: 'var(--header-current-text-color)',
                backgroundColor: 'var(--header-color)',
            }} onClick={() => set_mobile_show_view(!mobile_show_view)}>···</button>
            {mobile_show_view && <MobileHeaderView headers={headers} set_show={set_mobile_show_view}/>}
        </div>
    </header>
}


export default CustomHeader;