import axios from 'axios';

// 创建 axios 实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL, // 基础 URL，从环境变量中读取
  // baseURL: 'http://localhost:8000', // 基础 URL，从环境变量中读取
  timeout: 10000 // 请求超时时间
});

// 请求拦截器
service.interceptors.request.use(
  // showLoading();
  config => {
    // 在这里添加发送请求之前的逻辑，比如设置请求头等
    // if (localStorage.getItem('token')) {
    //   config.headers.Authorization = localStorage.getItem('token');
    // }
    return config;
  },
  error => {
    // 请求错误处理
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  response => {
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
  error => {
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
    return Promise.reject(error);
  }
);

export default service;
