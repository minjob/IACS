<template>
  <el-row :gutter="15">
    <el-col :span="24">
     <div class="navOptionsItem">
      <ul>
        <li v-for="item in TabControl.TabControlOptions" @click="showPage(item.name)"><a href="javascript:;" :class="{ active:item.name===TabControl.TabControlCurrent }" v-html="item.name"></a></li>
      </ul>
    </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "TabControl",
    props:['TabControl'],
    data(){
      return{

      }
    },
    created(){
      this.TabControl.TabControlCurrent = this.TabControl.TabControlOptions[0].name
    },
    methods:{
      showPage(name){
        this.TabControl.TabControlCurrent = name
      }
    }
  }
</script>

<style scoped>

</style>
