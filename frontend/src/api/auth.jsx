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

        //if (response.data.access_token) {
        //    localStorage.setItem('token', response.data.access_token);
        //    localStorage.setItem('name', username);
        //    return true;
        //}
        //return false;
    },

    // Выход
    logout: async () => {
        //localStorage.removeItem('token');
        //localStorage.removeItem('name');
        await api.post('/v1/auth/logout')
        window.location.href = '/auth/login';
    },

    send_feedback: async (msg) => {
        await api.post('/v1/utils/feedback', {
            message: msg,
        })
    },

    user: () => {

    },

    // Проверка авторизации
    isAuthenticated: () => {

    },
};

export default auth_service;
