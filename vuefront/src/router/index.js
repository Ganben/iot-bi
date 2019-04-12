import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Homepg from '@/components/Homepg';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Homepg',
      component: Homepg,
    },
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld,
    },
  ],
});
