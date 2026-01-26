import axios from "axios";

axios.defaults.withCredentials = true;


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
})


let queue = [];
let refreshing = false;


const processQueue = (error, token = null) => {
    queue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });

    queue = [];
};


const refresh = async () => {
    try {
        return await api.post('/v1/auth/refresh').data?.ok || false;
    } catch (error) {
        await api.post('/v1/auth/logout')
        window.location.href = '/auth/login';
    }
}


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
    async (error) => {
        const originalRequest = error.config;
        if (
            error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url.includes('/refresh') &&
            !originalRequest.url.includes('/login')
        ) {
            console.log('Начали обновлять токен');
            if (refreshing) {
                return new Promise((resolve, reject) => {
                    queue.push({ resolve, reject });
                }).then(() => {
                    return api(originalRequest);
                }).catch((err) => {
                    return Promise.reject(err);
                });
            }
        }

        originalRequest._retry = true;
        refreshing = true;

        try {
            if (await refresh() === false) {
                queue = []
                refreshing = false
                if (window.location.pathname !== '/auth/login') {
                  window.location.href = '/auth/login';
                }
            }

            // Повторяем оригинальный запрос
            const retryResponse = await api(originalRequest);

            // Обрабатываем ожидающие запросы
            processQueue(null);

            return retryResponse;
        } catch (refresh_error) {
            processQueue(refresh_error);
            processQueue(refresh_error, null);
            if (window.location.pathname !== '/auth/login') {
              window.location.href = '/auth/login';
            }
            return Promise.reject(refresh_error);
        } finally {
            refreshing = false;
        }

        //if (error.response?.status === 401 || error.response?.status === 403) {
        //    window.location.href = '/auth/login';
        //}
        // window.location.href = '/wrong'
        return Promise.reject(error);
    }
);

export default api;
