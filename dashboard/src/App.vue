<template> 
  <div id="app">
    <el-header>

    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    </el-header>
    <el-main>

    <router-view/>
    </el-main>
    <el-footer>
      <span class="el-icon-info">
        All Right Reserved, Yolly Technolog 2019
      </span>
    </el-footer>
  </div>
</template>
<script>
export default {
  
}
</script>

<style>
/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
