import { useState } from 'react'
import './css/style.css'
import logo from '/icon.svg'
import {BrowserRouter, Route, Routes} from "react-router-dom";

import {AuthOutlet} from "./pages/auth/outlet.jsx";
import {Login} from "./pages/auth/login.jsx";
import {Register} from "./pages/auth/register.jsx";

import auth_service from "./api/auth.jsx";
import CustomHeader from "./components/custom_header.jsx";


function App() {
    const [theme, set_theme] = useState(localStorage.getItem('theme') || 'dark');

    const headers = [
        {
            path: '/auth',
            label: 'Вход'
        },
    ]

    return <BrowserRouter>
        <div className='App' data-theme={theme}>
            <CustomHeader logo={<img src={logo} alt="logo" style={{
                width: '45px',
                height: '100%',
                backgroundColor: 'var(--header-current-color)',
                padding: '0px 10px',
            }}/>} headers={headers} set_theme={set_theme}/>
            <Routes>
                <Route path="/auth" element={<AuthOutlet />}>
                    <Route path="login" element={<Login />}/>
                    <Route path="register" element={<Register />}/>
                </Route>
            </Routes>
        </div>
    </BrowserRouter>
}

export default App
