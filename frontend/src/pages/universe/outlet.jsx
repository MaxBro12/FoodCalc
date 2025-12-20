import {Link, Outlet} from "react-router-dom";

export const UniverseOutlet = () => {
    if (window.location.pathname === '/db') {
        const link_style = {
            textDecoration: 'none',
            userSelect: 'none',
            width: '150px',
            padding: '10px',
            textAlign: 'center',
            color: 'var(--text-color)'
        }
        const link_style_m = {
            textDecoration: 'none',
            userSelect: 'none',
            minWidth: '250px',
            padding: '20px',
            textAlign: 'center',
            color: 'var(--text-color)'
        }

        return <div className='rounded_border base_flex_column' style={{
            padding: '10px',

            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            borderWidth: 0,
            backgroundColor: `var(--bg-color)`,
            color: `var(--text-color)`,
        }}>
            <Link to='/db/products' style={link_style} className='rounded_border desktop'>Продукты</Link>
            <Link to='/db/products' style={link_style_m} className='rounded_border mobile'>Продукты</Link>
            <Link to='/db/minerals' style={link_style} className='rounded_border desktop'>Минералы</Link>
            <Link to='/db/minerals' style={link_style_m} className='rounded_border mobile'>Минералы</Link>
            <Link to='/db/types' style={link_style} className='rounded_border desktop'>Типы минералов</Link>
            <Link to='/db/types' style={link_style_m} className='rounded_border mobile'>Типы минералов</Link>
        </div>
    }


    return <Outlet />
}