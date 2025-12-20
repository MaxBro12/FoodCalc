import api from './main.jsx'


export const db_service = {
    types: async () => {
        console.log(await api.get('/v1/universe/types/'))
        return (await api.get('/v1/universe/types/')).data.types || [];
    },
    minerals: async () => {
        return (await api.get('/v1/universe/minerals')).data.minerals || [];
    },
    products: async () => {
        return (await api.get('/v1/products/')).data.products || [];
    },
};

export default db_service;