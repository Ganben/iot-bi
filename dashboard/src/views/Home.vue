<template>

      
  <div class="home">
      <el-row>
  <el-col :span="24"><div class="grid-content bg-purple-dark">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    </div></el-col>
      </el-row>
      <el-row>

<Buttons msg="123"/>




</el-row>

  </div>

</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import Buttons from '@/components/Buttons.vue'
// import Anim from '@/components/Anim.vue'
// import Vuetify from 'vuetify'

export default {
  name: 'home',
  components: {
    HelloWorld,
    Buttons
    // Anim
  }
}
</script>
