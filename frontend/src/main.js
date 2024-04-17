import { createApp } from "vue";
import App from "./App";
import router from "./router/index";
import axios from "axios";
import "./assets/css/tailwind.css";

import rscdDashboard from "./plugins/rscdDashboard";
import WebSocketNotifier from "@/pages/Notifications/WebSocketNotifier";
import Notification from "@kyvg/vue3-notification"; // 导入 notification 组件

const app = createApp(App);

app.use(router); // 首先添加路由插件

app.config.globalProperties.$backendUrl = process.env.VUE_APP_BACKEND_URL;
app.config.globalProperties.$axios = axios;
app.config.globalProperties.routerAppend = (path, pathToAppend) => {
  return path + (path.endsWith("/") ? "" : "/") + pathToAppend;
};
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;

app.use(rscdDashboard); // 然后添加 rscdDashboard 插件
app.component("WebSocketNotifier", WebSocketNotifier);
app.mount("#app");
