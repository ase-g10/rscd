import axios from "axios";
import { useRouter } from 'vue-router'

// 创建 axios 实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL, // 基础 URL，从环境变量中读取
  timeout: 10000, // 请求超时时间
});

// 请求拦截器
service.interceptors.request.use(
  // showLoading();
  (config) => {
    if (config.url.includes('/api/private/')) { // 如果是私有接口则设置请求头
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    useRouter().push('/login')
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    // closeLoading();
    // const res = response.data;
    // // 错误处理
    // if (res.code != 0 && res.msg) {
    //     Message.error({
    //         content: res.msg,
    //     });
    //     alert(res.message);
    //     if (res.code == 2) {
    //         resetTokenAndClearUser();
    //         router.push('login');
    //     }
    //     return Promise.reject();
    // }
    // return res;
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // 用户未授权/Token失效
      // 这里可以处理登录逻辑，比如清除本地 token，跳转到登录页等
      localStorage.removeItem('token');
      useRouter().push('/login');
    }
    return Promise.reject(error);
  
    // 响应错误处理
    // closeLoading();
    // if (error.name == 'Error') {
    //     Message.error({
    //         content: error.msg,
    //     });
    // } else {
    //     Message.error({
    //         content: error.response.data.data || error.message,
    //     });
    // }
    // alert(error.message);
    // if(JSON.stringify(error.response.status)==='401') {
    //     self.location='/login';
    //     resetTokenAndClearUser();
    // }
  }
);

export default service;
