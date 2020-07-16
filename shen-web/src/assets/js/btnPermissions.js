import Vue from 'vue'
/**权限指令**/
const has = Vue.directive('has', {
　// 当被绑定的元素插入到 DOM 中时……
　inserted: function (el, binding) {
    // 获取指令按钮权限
    let btnPermissions = binding.value;
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
  let res = value.filter((x) => {
　　 return btnPermissionsStr.includes(x)
  })
  if (res.length > 0) {
    isExist = true
  }
  return isExist;
};

export {has}
