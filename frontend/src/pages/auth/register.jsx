import { useState } from 'react';
import { auth_service } from '../../api/auth';
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import {
    Link,
    useNavigate,
} from "react-router-dom"


export const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: '',
        key: '',
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

        if (formData.username.length < 6 || formData.password.length < 6) {
            setError('Пароль или имя пользователя меньше 6 символов')
            setLoading(false);
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setError('Пароли не совпадают');
            setLoading(false);
            return;
        }

        try {
            const res = await auth_service.register(formData.username, formData.password, formData.key);
            if (res.ok === true) {
                navigate('/auth/login')
            }
        } catch (error) {
            setError(error.response?.data?.detail || 'Регистрация не удалась');
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
                <div className='base_flex_row' style={{justifyContent: 'space-between', marginTop: '5px'}}>
                    <label>Повтор пароля</label>
                    <input
                        type="password"
                        name="confirmPassword"
                        className='base_button'
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className='base_flex_row' style={{justifyContent: 'space-between', marginTop: '5px'}}>
                    <label>Ключ</label>
                    <input
                        type="text"
                        name="key"
                        className='base_button'
                        value={formData.key}
                        onChange={handleChange}
                        required
                    />
                </div>
                {error && <div style={{ color: 'red' }}>{error}</div>}
                <div className='base_flex_row' style={{marginTop: 5, justifyContent: 'space-between'}}>
                    <button type="submit" disabled={loading} className='base_button'>
                        {loading ? 'Регистрируюсь...' : 'Регистрация'}
                    </button>
                    <Link to='/auth/login'>Есть аккаунт</Link>
                </div>
            </form>
        </div>
    );
};
