import api from './main.jsx'


export const db_service = {
    types: async () => {
        console.log(await api.get('/v1/universe/types/'))
        return (await api.get('/v1/universe/types/')).data.types || [];
    },
    minerals: async () => {
        return (await api.get('/v1/universe/minerals')).data.minerals || [];
    },
    products: async (skip_= 0, limit_= 10) => {
        return (await api.get('/v1/products/', {
            params: {
                skip: skip_,
                limit: limit_,
            }
        })).data.products || [];
    },
    products_names: async (limit_= 500) => {
        return (await api.get('/v1/products/names', {
            params: {
                limit: limit_,
            }
        })).data.names || [];
    },
    products_search: async (query) => {
        return (await api.post('/v1/products/search', {id_or_name: query})).data.names || [];
    },
    new_product: async (id, name, description, minerals, calories, energy) => {
        return (await api.post('/v1/products/new', {
            id: id.toString(),
            name: name,
            description: description,
            minerals: minerals,
            calories: calories,
            energy: energy,
        })).data.ok || false;
    }
};

export default db_service;
