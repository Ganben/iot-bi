// import 'vuetify/dist/vuetify.min.css'
// import 'vuetify/src/stylus/app.styl'
import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
// import BootstrapVue from 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.css'
import 'element-ui/lib/theme-chalk/index.css'
import Element from 'element-ui'
import Vue from 'vue'
import Vuex from 'vuex'
// import Vuetify from 'vuetify'
// import { VApp } from 'vuetify/lib'
// import { Ripple } from 'vuetify/lib/directives'
import App from './App.vue'
import router from './router'

Vue.use(Vuex)
// Vue.use(Vuetify)
Vue.use(Vuex)
Vue.use(Element)
// Vue.use(BootstrapVue)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
