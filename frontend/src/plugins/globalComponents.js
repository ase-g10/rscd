import { FormGroupInput, Card, DropDown, Button } from "../components/index";

const GlobalComponents = {
  install(Vue) {
    Vue.component("fg-input", FormGroupInput);
    Vue.component("drop-down", DropDown);
    Vue.component("card", Card);
    Vue.component("p-button", Button);
  },
};

export default GlobalComponents;
