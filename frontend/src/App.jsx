import { useState } from 'react'
import './css/style.css'
import logo from '/icon.svg'
import dark from '/dark.svg'
import light from '/light.svg'

import {BrowserRouter, Route, Routes} from "react-router-dom";

import {AuthOutlet} from "./pages/auth/outlet.jsx";
import {Login} from "./pages/auth/login.jsx";
import {Register} from "./pages/auth/register.jsx";

import auth_service from "./api/auth.jsx";
import CustomHeader from "./components/utils/custom_header.jsx";
import {Logout} from "./pages/auth/logout.jsx";
import {UniverseOutlet} from "./pages/universe/outlet.jsx";
import {MineralsTypes} from "./pages/universe/types.jsx";
import {Products} from "./pages/universe/products.jsx";
import {Minerals} from "./pages/universe/minerals.jsx";
import {Calculator} from "./pages/calculator/calculator.jsx";
import {AboutPage} from "./pages/about/about.jsx";
import {DebugPage} from "./pages/about/send_feedback.jsx";
import {NewProductView} from "./pages/universe/new_product.jsx";
import { WrongPage } from "./pages/about/wrong.jsx";
import {TestPage} from "./utils/tests.jsx";


function App() {
    const [theme, set_theme] = useState(localStorage.getItem('theme') || 'dark');
    const [username, set_username] = useState('');

    const change_theme = () => {
        set_theme(theme === 'dark' ? 'light' : 'dark');
    }
    const handle_theme = (new_theme) => {
        set_theme(new_theme);
        localStorage.setItem('theme', new_theme);
    }

    const headers = [
        {
            path: '/calc',
            label: 'Калькулятор',
        },
        {
            path: '/db',
            label: 'База'
        },
        {
            path: '/about',
            label: 'О нас',
        },
        {
            path: '/test',
            label: 'ssss',
        },
        {
            path: '/debug',
            label: 'О нас',
            d_style: {
                display: 'none',
            },
            m_style: {
                display: 'none',
            }
        },
        {
            path: undefined,
            label: theme === 'dark' ? <img src={light} alt="светлая тема" style={{
                width: '25px',
                height: '25px',
                backgroundColor: 'var(--header-color)',
                padding: '1px',
            }} onClick={() => handle_theme('light')}/>: <img src={dark} alt="темная тема" style={{
                width: '25px',
                height: '25px',
                backgroundColor: 'var(--header-color)',
                padding: '1px',
            }} onClick={() => handle_theme('dark')}/>,
            d_style: {
                marginLeft: 'auto',
                marginRight: '10px',
            }
        },
        ...username === '' ? [{
            path: '/auth',
            label: 'Вход',
            d_style: {
                marginRight: '10px',
            }
        }]:[{
            path: '/auth/logout',
            label: `Выход (${username})`,
            d_style: {
                marginRight: '10px',
            }
        }],
    ]

    return <BrowserRouter>
        <div className='App' data-theme={theme}>
            <CustomHeader logo={<img src={logo} alt="logo" style={{
                width: '45px',
                height: '100%',
                backgroundColor: 'var(--header-current-color)',
                padding: '0px 10px',
            }}/>} headers={headers} username={username} theme={theme} change_theme={change_theme}/>
            <Routes>
                <Route path='/calc' element={<Calculator />} />
                <Route path='/db' element={<UniverseOutlet />} />
                <Route path='/db/types' element={<MineralsTypes />}/>
                <Route path='/db/minerals' element={<Minerals />}/>
                <Route path='/db/products' element={<Products />}/>
                <Route path='/db/products/new' element={<NewProductView />}/>
                <Route path="/auth" element={<AuthOutlet />}>
                    <Route path="login" element={<Login set_username={set_username} />} />
                    <Route path="register" element={<Register />} />
                    <Route path="logout" element={<Logout />}/>
                </Route>
                <Route path='/debug' element={<DebugPage />}/>
                <Route path='/about' element={<AboutPage />}/>
                <Route path='/wrong' element={<WrongPage />} />
                <Route path='/test' element={<TestPage />} />
            </Routes>
        </div>
    </BrowserRouter>
}

export default App
