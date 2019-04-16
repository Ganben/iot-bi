<template>

<el-form :model="ruleForm2" status-icon :rules="rules2" ref="ruleForm2" label-width="120px" class="demo-ruleForm">
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
  
</template>

<script>
  export default {
    name: 'LoginForm',
    data() {
      var checkAge = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('Please input the age'));
        }
        setTimeout(() => {
          if (!Number.isInteger(value)) {
            callback(new Error('Please input digits'));
          } else {
            if (value < 18) {
              callback(new Error('Age must be greater than 18'));
            } else {
              callback();
            }
          }
        }, 1000);
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please input the password'));
        } else {
          if (this.ruleForm2.checkPass !== '') {
            this.$refs.ruleForm2.validateField('checkPass');
          }
          callback();
        }
      };
      // var validatePass2 = (rule, value, callback) => {
      //   if (value === '') {
      //     callback(new Error('Please input the password again'));
      //   } else if (value !== this.ruleForm2.pass) {
      //     callback(new Error('Two inputs don\'t match!'));
      //   } else {
      //     callback();
      //   }
      // };
      return {
        ruleForm2: {
          pass: '',
          checkPass: '',
          age: '',
          username: 'your username'
        },
        rules2: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
          age: [
            { validator: checkAge, trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('Coming Soon!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>