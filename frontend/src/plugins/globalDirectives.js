import { directive as vClickOutside } from "vue3-click-away";

const GlobalDirectives = {
  install(Vue) {
    Vue.directive("click-outside", vClickOutside);
  },
};

export default GlobalDirectives;
