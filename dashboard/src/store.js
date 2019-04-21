import Vue from 'vue'
import Vuex from 'vuex'

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
        state.token = jwtstr
    }
}

// actions are functions that cause side effects and can involve
// asynchronous operations.
const actions = {
    increment: ( { commit }) => commit('increment'),
    addToken: ( {commit}, jwtstr ) => commit('addToken', jwtstr),
    login: ({ commit }, user ) 
}

// getters are functions
const getters = {
    evenOrOdd: state => state.count % 2 === 0 ? 'even' : 'odd'
}

// A Vuex instance is created by combining the state, mutations, actions,
// and getters.
export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
  })