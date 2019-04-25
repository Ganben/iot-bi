import axios from 'axios'
// server: remove port 5000, use nginx port /api to 5000(path withou /api/...)


var myApi = axios.create({
    baseURL: 'https://aishe.org.cn/api/',
    timeout: 1000,
    headers: {'Authorization': localStorage.token}
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
    headers: {'Authorization': token}
    });
};
//above: self written, donno if work

  // another choice is vue interceptor
export default {
      myApi,
      amazonApi,
      authApi
}