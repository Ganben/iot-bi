<template> 
  <div id="app">
    <el-header>
      <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-menu-item index="1"><router-link to="/">Dashboard</router-link></el-menu-item>
  <el-submenu index="2">
    <template slot="title">Shelves</template>
    <el-menu-item index="2-1">Shelve #01</el-menu-item>
    <el-menu-item index="2-2">Shelve #02</el-menu-item>
    <el-menu-item index="2-3">Shelve #03</el-menu-item>
  </el-submenu>
  <el-menu-item index="3" disabled>Management</el-menu-item>
      <el-menu-item index="4">
        <router-link to="/about">Login</router-link>
      </el-menu-item>
</el-menu>
    </el-header>
    <el-main>

    <router-view/>
    </el-main>
    <el-footer>
      <span class="el-icon-info">
        All Rights Reserved, Yolly Technolog 2019
      </span>
    </el-footer>
  </div>
</template>
<script>
export default {
  mounted() {
    
  }
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
