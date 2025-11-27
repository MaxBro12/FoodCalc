import { useState } from 'react';
import { auth_service } from '../../api/auth';
import {
    Link,
    useNavigate,
} from "react-router-dom"
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";


export const Login = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (await auth_service.login(formData.username, formData.password)) {
                navigate('/')
            }
        } catch (error) {
            setError(error.response?.data?.detail || 'Непредвиденная ошибка');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <LoadingAnimation />
    }

    return (
        <div className='full_screen'>
            <form onSubmit={handleSubmit} className='rounded_border base_margins'>
                <div className='base_flex_row' style={{justifyContent: 'space-between'}}>
                    <label>Логин</label>
                    <input
                        type="text"
                        name="username"
                        className='base_button'
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className='base_flex_row' style={{justifyContent: 'space-between', marginTop: '5px'}}>
                    <label>Пароль</label>
                    <input
                        type="password"
                        name="password"
                        className='base_button'
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                {error && <div style={{ color: 'red' }}>{error}</div>}
                <div className='base_flex_row' style={{marginTop: 5, justifyContent: 'space-between'}}>
                    <button type="submit" disabled={loading} className='base_button'>
                        {loading ? 'Вхожу...' : 'Войти'}
                    </button>
                    <Link to='/auth/register'>Создать аккаунт</Link>
                </div>
            </form>
        </div>
    );
};