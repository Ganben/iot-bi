import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

// root state object.
// each Vuex instance is just a single state tree.
const state = {
    count: 0,
    token: '',
    login: false,
    roles: []
}

// mutations are operations that actually mutates the state.
// each mutation handler gets the entire state tree as the
// first argument, followed by additional payload arguments.
// mutations must be synchronous and can be recorded by plugins
// for debugging purposes.
const mutations = {
    increment (state) {
        state.cout++
    },
    addToken (state, jwtstr) {
        state.token = jwtstr;
        localStorage.setItem('token', jwtstr);
    },
    loginUser (state, user) {
        state.login = true;
        state.roles.push(user);
    }
}

// actions are functions that cause side effects and can involve
// asynchronous operations.
const actions = {
    increment: ( { commit }) => commit('increment'),
    addToken: ( {commit}, jwtstr ) => commit('addToken', jwtstr),
    login: ({ commit }, user ) => commit('loginUser', user),
    authGet (path) {
        const http = axios.create({
            baseURL: 'https://aishe.org.cn/api/',
            timeout: 1000,
            headers: {'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + btoa('guest' + ':' + 'guest')
        }
          });
        return http.get(path);
    }
}

// getters are functions
const getters = {
    evenOrOdd: state => state.count % 2 === 0 ? 'even' : 'odd',
    loginstatus: state => state.token === '' ? true : false,
    logintoken (state) {
        if (state.token != '') {
            return state.token;
        } else if ( localStorage.getItem('token')) {
            return localStorage.getItem('token');
        } else {
            return
        }
    },
    axiosconfig (state) {
        var config = {
            baseURL: 'http://aishe.org.cn/api/',
            timeout: 1000,
            headers: {'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + btoa('guest' + ':' + 'guest')
            }
        }
        if (state.token != '') {
            config.headers.Authorization = 'Bearer' + state.token;
        } else if ( localStorage.getItem('token')) {
            config.headers.Authorization = 'Bearer ' + localStorage.getItem('token');
        }
        return config;
    },
    axconfs (state) {
        var cf;
        if (state.token != '') {
            cf = 'Bearer' + state.token;
        } else if ( localStorage.getItem('token')) {
            cf = 'Bearer ' + localStorage.getItem('token');
        } else {
            cf = 'Basic ' + btoa('guest' + ':' + 'guest'); 
        }
        return cf;
    }
}

// A Vuex instance is created by combining the state, mutations, actions,
// and getters.
export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
  })