import {BrowserRouter, Route, Routes} from "react-router-dom";
import './css/style.css'

import {useTheme} from "@/context/theme.jsx";
import CustomHeader from "@/components/utils/custom_header.jsx";

import {LoginPage} from "@/pages/auth/login.jsx";
import {LogoutPage} from "@/pages/auth/logout.jsx";
import {RegisterPage} from "@/pages/auth/register.jsx";
import {AuthOutlet} from "@/pages/auth/outlet.jsx";
import {UserPage} from "@/pages/auth/user.jsx";

import { AboutPage } from '@/pages/about/about.jsx'

import {UniverseOutlet} from "@/pages/universe/outlet.jsx";
import {MineralsTypesPage} from "@/pages/universe/types.jsx";
import {MineralsPage} from "@/pages/universe/minerals.jsx";
import {ProductsPage} from "./pages/universe/products.jsx";
//import {Calculator} from "./pages/calculator/calculator.jsx";
//import {AboutPage} from "./pages/about/about.jsx";
//import {DebugPage} from "./pages/about/send_feedback.jsx";
//import { NewProductView } from "./pages/universe/new_product.jsx";


function App() {
    const { theme } = useTheme();

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
            no_user_show: false,
        },
    ]

    return <BrowserRouter>
        <div className='App' data-theme={theme}>
            <CustomHeader headers={headers} />
            <Routes>
                <Route path="/auth" element={<AuthOutlet />}>
                    <Route path="login" element={<LoginPage />}/>
                    <Route path="logout" element={<LogoutPage />}/>
                    <Route path="register" element={<RegisterPage />}/>
                    <Route path="user" element={<UserPage />}/>
                </Route>
                <Route path='/about' element={<AboutPage />} />

                <Route path='/db' element={<UniverseOutlet />} />
                <Route path='/db/types' element={<MineralsTypesPage />}/>
                <Route path='/db/minerals' element={<MineralsPage />}/>
                <Route path='/db/products' element={<ProductsPage />}/>
                {/*<Route path='/about/debug' element={<DebugPage />}/>
                <Route path='/about/error' element={<WrongPage />}/>
                <Route path='/test' element={<TestPage />}/>
                <Route path='/calc' element={<Calculator />} />
                <Route path='/db/products/new' element={<NewProductView />}/>*/}
            </Routes>
        </div>
    </BrowserRouter>
}

export default App
