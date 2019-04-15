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
import VueMqtt from 'vue-mqtt'

// import Vuetify from 'vuetify'
// import { VApp } from 'vuetify/lib'
// import { Ripple } from 'vuetify/lib/directives'
import App from './App.vue'
import router from './router'

// options = {
//   username: 'guest',
//   password: 'guest'
// };

Vue.use(Vuex)
// Vue.use(Vuetify)
Vue.use(Vuex)
// Vue.use(VueMqtt, 'ws://www.aishe.org.cn/ws', options)
// Vue.use(VueMqtt, 'ws://iot.eclipse.org:80/ws', {clientId: 'WebClient-' + parseInt(Math.random() * 100000)})
Vue.use(VueMqtt, 'ws://www.aishe.org.cn:9883', {clientId: 'WebClient-' + parseInt(Math.random() * 100000)})

Vue.use(Element)
// Vue.use(BootstrapVue)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
