import Vue from 'vue'
/**权限指令**/
const has = Vue.directive('has', {
　// 当被绑定的元素插入到 DOM 中时……
　inserted: function (el, binding) {
    // 获取指令按钮权限
    let btnPermissions = JSON.parse(JSON.stringify(binding.value))
    if (!Vue.prototype.$_has(btnPermissions)) {
      el.parentNode.removeChild(el);
    }
　}
});
// 权限检查方法
Vue.prototype.$_has = function (value) {
  let isExist = false;
  let btnPermissionsStr = JSON.parse(sessionStorage.getItem("Permissions"));
  if (btnPermissionsStr == undefined || btnPermissionsStr == null) {
    return false;
  }
  if(isContained(btnPermissionsStr, value)){
    isExist = true
  }else{
    return false
  }
  return isExist;
};
function isContained(a, b){ //判断指令内权限数组是否包含在用户的权限数组内
    if(!(a instanceof Array) || !(b instanceof Array)) return false;
    if(a.length < b.length) return false;
    var aStr = a.toString();
    for(var i = 0, len = b.length; i < len; i++){
       if(aStr.indexOf(b[i]) == -1) return false;
    }
    return true;
}

export {has}
