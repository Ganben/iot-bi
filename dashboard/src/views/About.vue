<template>
  <div class="about">
    <h1>Login into Your Account</h1>
    <LoginForm />
  </div>
</template>
<script>
import { magGetters, mapState, mapActions } from 'vuex'
import LoginForm from '@/components/LoginForm.vue'
export default {
  name: 'about',
  components: {
    LoginForm
  }  
}
</script>
