import {Link, Outlet} from "react-router-dom";
import { useDevice } from '@/context/mobile.jsx'

export const UniverseOutlet = () => {
    const {isMobile} = useDevice()

    if (window.location.pathname === '/db') {
        const link_style = {
            textDecoration: 'none',
            userSelect: 'none',
            width: isMobile ? '200px' : '150px',
            padding: isMobile ? '20px' : '10px',
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
            <Link to='/db/products' style={link_style} className='rounded_border'>Продукты</Link>
            <Link to='/db/minerals' style={link_style} className='rounded_border'>Минералы</Link>
            <Link to='/db/types' style={link_style} className='rounded_border'>Типы минералов</Link>
        </div>
    }

    return <Outlet />
}
