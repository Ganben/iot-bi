import axios from 'axios'
// import { store } from 'store'
// server: remove port 5000, use nginx port /api to 5000(path withou /api/...)


const myApi = axios.create({
    baseURL: 'https://aishe.org.cn/api/',
    timeout: 1000,
    headers: {'Authorization': 'Bearer ' + localStorage.getItem('token')}
});
  // if condition not sure:
  // another api service
var amazonApi = axios.create({
    baseURL: 'https://amazon-domain.com/api/',
    timeout: 2000,
    headers: {'X-Custom-Header': 'CustomHeader2'}
});

function authApi(token) {
    return axios.create({
        baseURL: 'https://aishe.org.cn/api/',
    timeout: 1000,
    headers: {'Authorization': 'Bearer '+ token}
    });
}
//above: self written, donno if work

function maxios() {
  if (localStorage.getItem('token')) {
    return axios.create({
      baseURL: 'https://aishe.org.cn/api/',
      timeout: 1000,
      headers: {'Authorization': 'Bearer ' + localStorage.getItem('token')}
    });
  } else {
    var credential = btoa('guest' + ':' + 'guest');
    return axios.create({
      baseURL: 'https://aishe.org.cn/api/',
      timeout: 1000,
      headers: {'Authorization': 'Basic ' + credential}
    });
  }
}
const http = axios.create({
  baseURL: 'https://aishe.org.cn/api/',
  timeout: 1000,
  headers: {'Content-Type': 'application/json'}
});

http.interceptors.request.use(
  function (config) {
    const token = localStorage.getItem('token');
    if ( token ) {
      config.headers.Authorization = `Bearer $(token)`;
      return config;
    } else {
      var credential = btoa('guest' + ':' + 'guest');
      config.headers.Authorization = 'Basic '+credential;
      return config;
    }

  },
  function ( error ) {
    return Promise.reject (error);
  }
);

  // another choice is vue interceptor
export default {
      myApi,
      amazonApi,
      authApi,
      maxios,
      http
}