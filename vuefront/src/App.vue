<template>
  <div id="app" class="page-container">
    <md-app>
      <md-app-toolbar class="md-primary">
        <span class="md-title">IoT Monitoring</span>
      </md-app-toolbar>
    <md-app-content>
    <router-view/>
    </md-app-content>
    </md-app>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
