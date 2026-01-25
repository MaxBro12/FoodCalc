import axios from "axios";

axios.defaults.withCredentials = true;


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
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

// Перехватчик для дебаггинга
//api.interceptors.request.use(config => {
//  console.log('Отправляю запрос с конфигом:', config);
//  return config;
//});


// Интерцептор для обработки ошибок авторизации
api.interceptors.response.use(
    (response) => response,
    (error) => {
        //if (error.response?.status === 401 || error.response?.status === 403) {
        //    window.location.href = '/auth/login';
        //}
        // window.location.href = '/wrong'
        return Promise.reject(error);
    }
);

export default api;
