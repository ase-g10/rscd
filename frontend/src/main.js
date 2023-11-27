import Vue from "vue";
import App from "./App";
import router from "./router/index";
import axios from "axios";

import rscdDashboard from "./plugins/rscdDashboard";
import "vue-notifyjs/themes/default.css";

Vue.use(rscdDashboard);
Vue.prototype.$backendUrl = process.env.VUE_APP_BACKEND_URL;
Vue.prototype.$axios = axios;

/* eslint-disable no-new */
new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
