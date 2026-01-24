import axios from "axios";


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
})


// Интерцептор для добавления токена к запросам
//api.interceptors.request.use(
//    (config) => {
//        config.withCredentials = true;
//        return config;
//    },
//    (error) => {
//        return Promise.reject(error);
//    }
//);

// Интерцептор для обработки ошибок авторизации
api.interceptors.response.use(
    (response) => response,
    (error) => {
        //if (error.response?.status === 401 || error.response?.status === 403) {
        //    window.location.href = '/auth/login';
        //}
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        //window.location.href = '/wrong'
        return Promise.reject(error);
    }
)

export default api;
