import api from './base.jsx'


export const db_service = {
    types: {
        // Все методы связанные типами минералов
        all: async () => {
            // Получение всех типов минералов или пустого массива если связь не установлена
            return (await api.get('/v1/universe/types')).data.types || [];
        },
    },
    minerals: {
        all: async () => {
            // Получение всех минералов или пустого массива если связь не установлена
            return (await api.get('/v1/universe/minerals')).data.minerals || [];
        },
    },
    products: {
        all: async ({skip = 0, limit = 10}) => {
            // Получение списка продуктов с параметров пагинации
            return (await api.get('/v1/products/', {
                params: {
                    skip: skip,
                    limit: limit,
                }
            })).data.products || [];
        },
        detail: async (product_id) => {
            // Получение детальной информации о продукте по ID
            return (await api.get(`/v1/products/details/${product_id}`)).data;
        },
        names: async (limit_ = 500) => {
            // Получение списка названий продуктов с лимитом
            return (await api.get('/v1/products/names', {
                params: {
                    limit: limit_,
                }
            })).data.names || [];
        },
        search: async (query) => {
            // Поисковой запрос по имени или ID, возвращает список названий с поисковым индексом
            return (await api.post('/v1/products/search', {id_or_name: query})).data.names || [];
        },
        new: async ({id, name, description, minerals, calories, energy}) => {
            return (await api.post('/v1/products/new', {
                id: id.toString(),
                name: name,
                description: description,
                minerals: minerals,
                calories: calories,
                energy: energy,
            })).data.ok || false;
        }
    },
};

export default db_service;
