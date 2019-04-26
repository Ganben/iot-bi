<template>
  <div class="home">
      <el-row>
  <el-col :span="24"><div class="grid-content bg-purple-dark">
    <HelloWorld msg="Dashboard of Smart IoT Shelves"/>
    </div></el-col>
      </el-row>
      <el-row>
<!-- <Buttons msg="123"/> -->
</el-row>
<MqController />
<p> {{loginstatus}} </p>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
// import Buttons from '@/components/Buttons.vue'
import MqController from '@/components/MqController.vue'
import { mapGetters } from 'vuex'
// import axios from 'axios'
// import Anim from '@/components/Anim.vue'
// import Vuetify from 'vuetify'
// login reload can use $forceUpdate
// use conditional render in the first place to refractor vue archi
// end of this version due to explorer and re config( need auth configed axios file )

export default {
  name: 'home',
  components: {
    HelloWorld,
    // Buttons,
    MqController
    // Anim
  },
  computed: mapGetters([
    'loginstatus',
    'logintoken'
  ]),
  mounted() {
    // if (localStorage.token) {
    //   axios.defaults.headers.common['Authorization'] = "Bearer "+this.logintoken;
    //   console.log('axios header set with' + this.logintoken);
    //   console.log('ls:'+ localStorage.token);
    // }
    // this.$mqtt.subscribe('webdev/#', {callback: console.log('mqtt con')});
    // if (this.loginstatus) {
    //   axios.defaults.headers.common['Authorization'] = "Bearer "+this.logintoken;
    //   console.log('axios header set with' + this.logintoken);
    // }
  }
}
</script>
