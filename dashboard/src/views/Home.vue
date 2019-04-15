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
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import Buttons from '@/components/Buttons.vue'
import MqController from '@/components/MqController.vue'
// import Anim from '@/components/Anim.vue'
// import Vuetify from 'vuetify'

export default {
  name: 'home',
  components: {
    HelloWorld,
    Buttons,
    MqController
    // Anim
  },
  mounted() {
    this.$mqtt.subscribe('webdev/#', {callback: console.log('mqtt con')})
  }
}
</script>
