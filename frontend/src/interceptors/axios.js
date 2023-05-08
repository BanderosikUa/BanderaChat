import axios from "axios";

// axios.defaults.withCredentials = true;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('access_token');
// axios.defaults.baseURL = 'http://34.120.190.133/';  // the FastAPI backend

axios.defaults.baseURL = 'http://127.0.0.1:5000/';  // the FastAPI backend

let refresh = false;

axios.interceptors.response.use(resp => resp, async error => {
    if (error.response.status === 401 && !refresh) {
        refresh = true;
        console.log('pass')

        const {status, data} = await axios.get('auth/refresh', {}, {
            withCredentials: true
        });

        if (status === 200) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;

            return axios(error.config);
        }
        else{
            window.location = '/login';
        }
    }
    refresh = false;
    return error;
});
