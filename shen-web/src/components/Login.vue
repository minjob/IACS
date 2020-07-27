<template>
  <el-container style="height: 100%;">
    <div id="loginBgCanvas">
      <div class="login-center-bg">
        <div class="login-form-box">
          <div class="login-form-title">桃园地铁站智能分析控制系统</div>
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
    </div>
  </el-container>
</template>

<script>
  import * as Three from 'three'
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
        camera: null,
        scene: null,
        renderer: null,
        mesh: null,
        SEPARATION: 100, AMOUNTX: 50, AMOUNTY: 50,
        container:null,
        particles:null,count:0,
        mouseX:0,mouseY:0,
        windowHalfX: window.innerWidth / 2,
        windowHalfY : window.innerHeight  / 2,
      }
    },
    mounted(){
      this.getCookie()
      this.init()
      this.animate()
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
                    showClose: true,
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
                    showClose: true,
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
      },
      init: function () {
        this.container = document.getElementById('loginBgCanvas')
        this.camera = new Three.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 1, 10000 )
        this.camera.position.z = 1000
        this.scene = new Three.Scene()
        this.scene.background = new Three.Color( 0x1B1E27 );

        var numParticles = this.AMOUNTX * this.AMOUNTY;
				var positions = new Float32Array( numParticles * 3 );
				var scales = new Float32Array( numParticles );
				var i = 0, j = 0;
				for ( var ix = 0; ix < this.AMOUNTX; ix ++ ) {
					for ( var iy = 0; iy < this.AMOUNTY; iy ++ ) {
						positions[ i ] = ix * this.SEPARATION - ( ( this.AMOUNTX * this.SEPARATION ) / 2 ); // x
						positions[ i + 1 ] = 0; // y
						positions[ i + 2 ] = iy * this.SEPARATION - ( ( this.AMOUNTY * this.SEPARATION ) / 2 ); // z
						scales[ j ] = 1;
						i += 3;
						j ++;
					}
				}

        var geometry = new Three.BufferGeometry();
				geometry.setAttribute( 'position', new Three.BufferAttribute( positions, 3 ) );
				geometry.setAttribute( 'scale', new Three.BufferAttribute( scales, 1 ) );
				var material = new Three.ShaderMaterial( {
					uniforms: {
						color: { value: new Three.Color( 0x228AD5 ) },
					},
					vertexShader: document.getElementById( 'vertexshader' ).textContent,
					fragmentShader: document.getElementById( 'fragmentshader' ).textContent
				});

				this.particles = new Three.Points( geometry, material );
				this.scene.add( this.particles );

				this.renderer = new Three.WebGLRenderer( { antialias: true } );
				this.renderer.setPixelRatio( window.devicePixelRatio );
				this.renderer.setSize( window.innerWidth, window.innerHeight );
        this.container.appendChild(this.renderer.domElement)


				document.addEventListener( 'mousemove', this.onDocumentMouseMove, false );
				document.addEventListener( 'touchstart', this.onDocumentTouchStart, false );
				document.addEventListener( 'touchmove', this.onDocumentTouchMove, false );

				window.addEventListener( 'resize', this.onWindowResize, false );
      },
      animate: function () {
        requestAnimationFrame( this.animate );
				this.render();
      },
      onWindowResize(){
        this.windowHalfX = window.innerWidth / 2;
				this.windowHalfY = window.innerHeight / 2;
				this.camera.aspect = window.innerWidth / window.innerHeight;
				this.camera.updateProjectionMatrix();
				this.renderer.setSize( window.innerWidth, window.innerHeight );
      },
      onDocumentMouseMove( event ){
        this.mouseX = event.clientX - this.windowHalfX - 200;
				this.mouseY = event.clientY - this.windowHalfY - 200;
      },
      onDocumentTouchStart( event ){
        if ( event.touches.length === 1 ) {
					event.preventDefault();
					this.mouseX = event.touches[ 0 ].pageX - this.windowHalfX;
					this.mouseY = event.touches[ 0 ].pageY - this.windowHalfY;
				}
      },
      onDocumentTouchMove(event){
        if ( event.touches.length === 1 ) {
					event.preventDefault();
					this.mouseX = event.touches[ 0 ].pageX - this.windowHalfX;
					this.mouseY = event.touches[ 0 ].pageY - this.windowHalfY;
				}
      },
      render(){
        this.camera.position.x += ( this.mouseX - this.camera.position.x ) * .05;
				this.camera.position.y += ( - this.mouseY - this.camera.position.y ) * .05;
				this.camera.lookAt( this.scene.position );
				var positions = this.particles.geometry.attributes.position.array;
				var scales = this.particles.geometry.attributes.scale.array;
				var i = 0, j = 0;
				for ( var ix = 0; ix < this.AMOUNTX; ix ++ ) {
					for ( var iy = 0; iy < this.AMOUNTY; iy ++ ) {
						positions[ i + 1 ] = ( Math.sin( ( ix + this.count ) * 0.3 ) * 50 ) +
										( Math.sin( ( iy + this.count ) * 0.5 ) * 50 );
						scales[ j ] = ( Math.sin( ( ix + this.count ) * 0.3 ) + 1 ) * 8 +
										( Math.sin( ( iy + this.count ) * 0.5 ) + 1 ) * 8;
						i += 3;
						j ++;
					}
				}
				this.particles.geometry.attributes.position.needsUpdate = true;
				this.particles.geometry.attributes.scale.needsUpdate = true;
				this.renderer.render( this.scene, this.camera );
				this.count += 0.1;
      }
    }
  }
</script>

<style scoped>
  #loginBgCanvas{
    position: relative;
    width: 100%;
    height: 100%;
  }
  #loginBgCanvas canvas{
    /*设置display 为 block 可以消除下方5px 的边距!!!*/
    display: block!important;
    width: 100%!important;
    height: 100% !important;
  }
  .login-center-bg{
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items:center;
  }
  .login-form-box{
    position: relative;
    width: 400px;
    height: 360px;
    margin: 0 auto 50px auto;
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
