<template>
  <el-container style="height: 100%;">
    <div class="login-img-bg">
      <div class="login-mask-bg"></div>
      <div class="login-form-box">
        <div class="login-form-title">辽宁好护士能耗管理系统</div>
        <div class="login-form-mask"></div>
        <div class="login-form">
          <el-form ref="ruleForm" :model="loginForm" :rules="rules" style="width: 100%;">
            <el-form-item prop="WorkNumber">
              <el-input placeholder="请输入工号" v-model="loginForm.WorkNumber">
                <i slot="prefix" class="el-input__icon el-icon-s-custom"></i>
              </el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input placeholder="请输入密码" v-model="loginForm.password" show-password>
                <i slot="prefix" class="el-input__icon el-icon-lock"></i>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="loginForm.rememb" class="remembCheckbox">记住密码</el-checkbox>
            </el-form-item>
          </el-form>
        </div>
        <div class="login-form-submit" :class="isSubLoadding?'submitLoadding':''" @click="submitForm('ruleForm')">登录</div>
      </div>
    </div>
  </el-container>
</template>

<script>
  export default {
    name: "login",
    data(){
      return{
        color:"#082F4C",
        loginForm:{
          WorkNumber:"",
          password:"",
          rememb:false
        },
        rules:{
          WorkNumber:[
            {required: true, message: '请输入工号', trigger: 'blur'}
          ],
          password:[
            {required: true, message: '请输入密码', trigger: 'blur'}
          ]
        },
        isSubLoadding:false,
      }
    },
    mounted(){
      this.getCookie()
    },
    methods:{
      submitForm(formName){
        let params = {
          WorkNumber:this.loginForm.WorkNumber,
          password:this.loginForm.password
        };
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.isSubLoadding == false){
              this.isSubLoadding = true
              this.axios.post('/api/account/userloginauthentication',this.qs.stringify(params)).then(res =>{
                if(res.data == "OK"){
                  this.$message({
                    message: "登录成功",
                    type: 'success'
                  });
                  var that = this;
                  this.isSubLoadding = false
                  setTimeout(function(){
                    that.$router.push("/")
                  },1000)
                  this.$store.commit('setUser',this.loginForm.WorkNumber);
                  if(this.loginForm.rememb){
                    this.setCookie(this.loginForm.WorkNumber,this.loginForm.password,this.loginForm.rememb,7)
                  }else{
                    this.clearCookie()
                  }
                }else{
                  this.$message({
                    type: 'info',
                    message: res.data
                  });
                  this.isSubLoadding = false
                }
              },res =>{
                console.log("请求错误")
                this.isSubLoadding = false
              })
            }
          }
        })
      },
      setCookie(c_name, c_pwd,c_rememb, exdays) {
        var exdate = new Date(); //获取时间
        exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays); //保存的天数
        //字符串拼接cookie
        window.document.cookie = "userName" + "=" + c_name + ";path=/;expires=" + exdate.toGMTString();
        window.document.cookie = "userPwd" + "=" + c_pwd + ";path=/;expires=" + exdate.toGMTString();
        window.document.cookie = "rememb" + "=" + c_rememb + ";path=/;expires=" + exdate.toGMTString();
      },
      getCookie:function () {
        if (document.cookie.length>0) {
          var arr=document.cookie.split('; ');//这里显示的格式需要切割一下自己可输出看下
          for(var i=0;i<arr.length;i++){
            var arr2=arr[i].split('=');//再次切割
            //判断查找相对应的值
            if(arr2[0]=='userName'){
              this.loginForm.WorkNumber=arr2[1];//保存到保存数据的地方
            }else if(arr2[0]=='userPwd'){
              this.loginForm.password=arr2[1];
            }else if(arr2[0]=='rememb'){
              this.loginForm.rememb=Boolean(arr2[1]);
            }
          }
        }
      },
      clearCookie:function () {
        this.setCookie("","","",-1);
      }
    }
  }
</script>

<style scoped>
  .login-img-bg{
    position: relative;
    width: 100%;
    height: 100%;
    /*background: url("../assets/imgs/loginBg.jpg") no-repeat;*/
    background-size:cover;
    -webkit-background-size: cover;
    -o-background-size: cover;
    background-position: center 0;
    display: flex;
    align-items:center;
  }
  .login-mask-bg{
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    background: #082F4C;
    opacity: 0.52;
  }
  .login-form-box{
    position: relative;
    width: 400px;
    height: 360px;
    margin: 0 auto;
  }
  .login-form-mask{
    position: absolute;
    width: 100%;
    height: 100%;
    background: #fff;
    border-radius:8px;
    opacity: 0.33;
  }
  .login-form{
    width: 100%;
    height: 100%;
    padding: 40px;
    display: flex;
    align-items: center;
  }
  .login-form-title{
    position: relative;
    top: 20px;
    height: 40px;
    line-height: 40px;
    display: table;
    padding: 0 40px;
    background: #082F4C;
    color: #fff;
    border-radius:8px;
    margin: 0 auto;
    z-index: 1;
  }
  .login-form-submit{
    position: relative;
    bottom: 30px;
    width: 60px;
    height: 60px;
    line-height: 60px;
    text-align: center;
    display: table;
    background: #082F4C;
    color: #fff;
    border-radius:50%;
    margin: 0 auto;
    cursor: pointer;
    z-index: 1;
  }
  .login-form-submit.submitLoadding{
    background: #EEEEEE;
    color: rgba(8,47,76,0.58);
    cursor: not-allowed;
  }
</style>
