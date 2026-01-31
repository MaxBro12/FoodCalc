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
        return (await api.post('/v1/auth/login', {
            username: username,
            password: password,
        })).data?.ok || false;
    },

    // Выход
    logout: async () => {
        await api.post('/v1/auth/logout')
        window.location.href = '/auth/login';
    },

    send_feedback: async (msg) => {
        await api.post('/v1/utils/feedback', {
            message: msg,
        })
    },

    status: async () => {
        return (await api.post('/v1/utils/status', {}, {
            withCredentials: true,
        })).data?.ok || false
    },

    user: () => {

    },

    // Проверка авторизации
    isAuthenticated: () => {

    },
};

export default auth_service;
