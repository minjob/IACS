<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '趋势分析'">
              <el-col :span="6">
                <div class="Datepick platformContainer blackComponents" style="height:310px;">
                    <DatePicker type="date" multiple placeholder="Select date" style="width: 300px" value='valuedate 'size="default" @on-ok="getSelectDate" :open=true :confirm=true></DatePicker>
                </div>
                <div class="platformContainer blackComponents" style="height:750px;">
                    <el-tree 
                      :data="treedata"
                      show-checkbox
                      node-key="id"
                      ref="tree"
                      @check-change='getChecked()'
                      :default-expanded-keys="[2, 3]"
                      :default-checked-keys="[5]"
                      :props="defaultProps">
                    </el-tree>
                </div>
              </el-col>
              <el-col :span="18">
                <div class="platformContainer blackComponents">
                   123
                </div>
              </el-col>
          </el-row>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '数据录入'">
              <span class="color-lightgreen">数据录入</span>
          </el-row>
      </el-col>
  </el-row>
</template>

<script>
  import TabControl from '@/components/TabControl'
  var moment = require('moment');
  import echarts from '@/assets/js/echarts.js'

  export default {
    name: "Home",
    components:{TabControl},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"趋势分析"},
            {name:"数据录入"}
          ]
        },
        treedata:[],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        valuedate:''
      }
    },
    mounted(){
        this.getAsidemenu()
    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      getAsidemenu(){
         var params = {
          tableName:'ParentTagMaintain',
          limit:1000,
          offset:0
        }
         this.axios.get('/api/CUID',{params}).then((res) => {
           var arr=JSON.parse(res.data).rows
           this.treedata=arr.map((item, index) => {
              return { id: index+1,label: item.ParentTagName,children:[{id:index+12,label:'Tag1'},{id:index+23,label:'Tag2'}]}
            })
         })
      },
      getChecked(){
        console.log(this.$refs.tree.getCheckedNodes());
      },
      getSelectDate(){
        console.log(this.valuedate)
      }
    
    }
  }
</script>
<style scoped>
.ivu-date-picker-focused{
  width: 469px!important;
}


</style>