import { useState } from 'react'
import './css/style.css'
import {BrowserRouter, Route, Routes} from "react-router-dom";

import {AuthOutlet} from "./pages/auth/outlet.jsx";
import {Login} from "./pages/auth/login.jsx";
import {Register} from "./pages/auth/register.jsx";


function App() {
    const [theme, set_theme] = useState(localStorage.getItem('theme') || 'dark');

    return <BrowserRouter>
        <div className='App' data-theme={theme}>
            <div style={{padding: '5px', height: '100%'}}>
                <Routes>

                    <Route path="/auth" element={<AuthOutlet />}>
                        <Route path="login" element={<Login />}/>
                        <Route path="register" element={<Register />}/>
                    </Route>
                </Routes>
            </div>
        </div>
    </BrowserRouter>
}

export default App
