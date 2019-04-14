<template>
<v-layout row_wrap>
  <v-flex xs12>
        <v-card dark color="primary">
          <v-card-text class="px-0">12</v-card-text>
        </v-card>
      
  <div class="home">
      <v-layout justify-space-around>
    <v-icon large color="green darken-2">business</v-icon>

    <v-icon large color="blue darken-2">chat</v-icon>

    <v-icon large color="purple darken-2">dialpad</v-icon>

    <v-icon large color="teal darken-2">email</v-icon>

    <v-icon large color="blue-grey darken-2">call_split</v-icon>

    <v-icon large color="orange darken-2">present_to_all</v-icon>
  </v-layout>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <v-avatar
          :tile="tile"
          :size="avatarSize"
          color="grey lighten-4"
        >
          <img src="https://vuetifyjs.com/apple-touch-icon-180x180.png" alt="avatar">
        </v-avatar>
        <v-badge left>
      <template v-slot:badge>
        <span>6</span>
      </template>
      <v-icon
        large
        color="grey lighten-1"
      >
        shopping_cart
      </v-icon>
    </v-badge>
    <Buttons msg="123"/>
  </div>
  </v-flex>
</v-layout>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import Buttons from '@/components/Buttons.vue'

export default {
  name: 'home',
  components: {
    HelloWorld,
    Buttons
  }
}
</script>
