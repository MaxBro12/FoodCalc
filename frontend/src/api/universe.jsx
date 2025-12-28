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
    new_product: async (id, name, description, minerals, calories, energy) => {
        return (await api.post('/v1/products/new', {
            id: id,
            name: name,
            description: description,
            minerals: minerals,
            calories: calories,
            energy: energy,
        })).data.ok || false;
    }
};

export default db_service;