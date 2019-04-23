<template>
<el-col :span="12">
<el-form status-icon  label-width="120px" class="demo-ruleForm">
  <el-form-item label = "Username" prop="username">
  <el-input placeholder="your account name" v-model="username"></el-input>
  </el-form-item>
  <el-form-item label="Password" prop="pass">
    <el-input type="password" v-model="pass" autocomplete="off"></el-input>
  </el-form-item>

  <el-form-item>
    <el-button type="primary" @click="submitForm">Submit</el-button>
    <el-button @click="resetForm">Cancel</el-button>
  </el-form-item>
  <p> Result is: {{ logintoken }}</p>
</el-form>
</el-col>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'
import passwordHash from 'password-hash'

  export default {
    name: 'LoginForm',
    data() {
      return {
        // logintoken: '',
        username: '',
        pass: ''
      };
    },
    computed: mapGetters([
      'logintoken',
      'loginstatus'
    ]),
    methods: {
      submitForm() {
        // alert('Coming Soon!');
        var ldata = {
            username: this.username,
            password: passwordHash.generate(this.pass)
        };
        //axios use json as  default post 
        axios.post('http://aishe.org.cn:5000/api/login', ldata)
        .then((response) => {
          // this.saveToken(response);
          this.logintoken = response.data;
          console.log('123123' + response.data);
          this.saveToken(response.data);
        })
        .catch(function (error){
          alert('Network Error' + error);
        })
      },
      saveToken(token) {
          this.addToken(token);
          this.login('user');
          axios.defaults.headers.common['Authorization'] = "Bearer "+token;
          console.log('exe token');
      },
      resetForm() {
        this.pass = '';
        this.username = '';
      },
      ...mapActions([
       'addToken',
       'login'
     ])
    }
  }
</script>