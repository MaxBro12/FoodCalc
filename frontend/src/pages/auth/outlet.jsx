import {useEffect} from "react";
import {Navigate, Outlet, useLocation} from 'react-router-dom';
import auth_service from "../../api/auth.jsx";


export const AuthOutlet = () => {
    //useEffect(() => {
    //    if (window.location.pathname === '/auth') {
    //        if (!auth_service.isAuthenticated()) {
    //            window.location.href = '/auth/login';
    //        } else {
    //            window.location.href = '/';
    //        }
    //    }
    //}, []);
    const location = useLocation()
    if (location.pathname === '/auth') {
        return auth_service.isAuthenticated()?
            <Navigate to='/' replace />:
            <Navigate to='/auth/login' replace />
    }

    return <div className='full_screen'>
        <Outlet />
    </div>
};
