import axios from "axios";
const BASE_URL = "http://26.48.41.80:8000"


export async function req(params, request, type) {
    try {
        const config = {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            params: params
        };

        let response;
        switch (type) {
            case 'get':
                response = await axios.get(BASE_URL + request, config);
                break;
            case 'post':
                response = await axios.post(BASE_URL + request, params, config);
                break;
            case 'patch':
                response = await axios.patch(BASE_URL + request, params, config);
                break;
            case 'delete':
                response = await axios.delete(BASE_URL + request, config);
                break;
            default:
                throw new Error(`Unsupported request type: ${type}`);
        }

        console.log(`Success ${type} request!`, request);
        return response.data;

    } catch (error) {
        console.error('Ошибка при запросе:', error.message);
        return null;
    }
};

export async function get_cats(start = 0, end = 12) {
    const params = {
        skip: start,
        limit: end,
    }
    return req(params, '/cats', 'get');
};

export async function search_cats(query) {
    const data = {
        query,
    }
    return req(data, '/search', 'post');
};
