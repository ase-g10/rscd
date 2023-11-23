import Vue from "vue";
import App from "./App";
import router from "./router/index";

import rscdDashboard from "./plugins/rscdDashboard";
import "vue-notifyjs/themes/default.css";

Vue.use(rscdDashboard);

/* eslint-disable no-new */
new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
