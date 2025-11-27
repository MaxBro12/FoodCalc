import api from './main.jsx'


export const auth_service = {
    // Регистрация
    register: async (username, password, key) => {
        return (await api.post('/v1/auth/register', {
            username: username,
            password: password,
            key: key,
        })).data;
    },

    // Логин
    login: async (username, password) => {
        const response = await api.post('/v1/auth/login', {
            username: username,
            password: password,
        });

        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
            return true;
        }
        return false;
    },

    // Выход
    logout: () => {
        localStorage.removeItem('token');
        window.location.href = '/auth/login';
    },

    // Проверка авторизации
    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },
};

export default auth_service;