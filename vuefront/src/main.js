// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'vue-material/dist/vue-material.min.css';
import VueMaterial from 'vue-material';
import ECharts from 'vue-echarts';
import Vue from 'vue';
import App from './App';
import router from './router';
// Vue.use(MdButton)
// Vue.use(MdContent)
Vue.use(VueMaterial);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
