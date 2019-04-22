<template>
<el-col :span="12">
<el-form :model="ruleForm2" status-icon  label-width="120px" class="demo-ruleForm">
  <el-form-item label = "Username" prop="username">
  <el-input v-model="ruleForm2.username"></el-input>
  </el-form-item>
  <el-form-item label="Password" prop="pass">
    <el-input type="password" v-model="ruleForm2.pass" autocomplete="off"></el-input>
  </el-form-item>
  <!-- <el-form-item label="Confirm" prop="checkPass">
    <el-input type="password" v-model="ruleForm2.checkPass" autocomplete="off"></el-input>
  </el-form-item> -->
  <!-- <el-form-item label="Age" prop="age">
    <el-input v-model.number="ruleForm2.age"></el-input>
  </el-form-item> -->
  <el-form-item>
    <el-button type="primary" @click="submitForm('ruleForm2')">Submit</el-button>
    <el-button @click="resetForm('ruleForm2')">Cancel</el-button>
  </el-form-item>
</el-form>
</el-col>
</template>

<script>
import axios from 'axios'
import passwordHash from 'password-hash'

  export default {
    name: 'LoginForm',
    data() {
 
      return {
        ruleForm2: {
          pass: '',
          checkPass: '',
          age: '',
          username: ''
        }
      };
    },
    methods: {
      submitForm(formName) {
        alert('Coming Soon!');
        ldata = {
            username: ruleForm2.username,
            password: passwordHash.generate(ruleForm2.pass)
        };
        //axios use json as  default post 
        axios.post('http://aishe.org.cn:5000/api/login', ldata)
        .then(function (response) {
          this.saveToken(response);
          console.log(''+response);
        })
        .catch(function (error){
          console.log(error);
        })
      },
      saveToken(token) {
          this.addToken(token);
      },
      resetForm(formName) {
        // this.$refs[formName].resetFields();
      },
      ...mapActions([
       'addToken',
       'login'
     ])
    }
  }
</script>