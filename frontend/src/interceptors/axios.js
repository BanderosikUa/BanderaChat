import axios from "axios";

// axios.defaults.withCredentials = true;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('access_token');


axios.defaults.baseURL = '/api';  // the FastAPI backend

let refresh = false;

axios.interceptors.response.use(resp => resp, async error => {
    if (error.response.status === 401 && !refresh) {
        // Get the current path of the URL
        const currentPath = window.location.pathname;
        // Only execute the refresh token logic if the current path is not "login" or "register"
        if (currentPath !== "/login" && currentPath !== "/register") {
          // Set a flag to indicate that the refresh token logic is currently running
          refresh = true;
  
          await axios.get("auth/refresh").then(response => {
            if (response.status === 200) {
              localStorage.setItem("access_token", response.data.access_token);
              axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access_token}`;
    
              // Retry the original request with the new access token
              return axios(error.config);
            } else {
              window.location = "/login";
            }
          }).catch(e => {
            console.log(e)
            window.location = "/login";
          })
  
        }
    }
    refresh = false;
    return Promise.reject(error);
});
