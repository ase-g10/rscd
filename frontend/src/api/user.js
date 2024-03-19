import service from "@/utils/request";

import axios from 'axios';

export function userLogin(data) {
  return service({
    url: "um/login/log_in/",
    method: "post",
    data,
  })
}

//TODO: 后端补全注册信息入库，此处仅为示例代码
// 模拟一个成功的注册响应
const mockResponse = {
  data: {
    user: {
      id: 1,
      email: "example@example.com",
      name: "gg",
    },
    message: "Registration successful",
  },
};

export const userRegister = async (userData) => {
  return new Promise((resolve, reject) => {
    // 模拟网络延迟
    setTimeout(() => {
      // 假设所有的注册请求都是有效的，直接解析模拟的响应
      // 在实际的应用中，你可以在这里添加一些逻辑来根据 userData 的不同返回成功或失败的响应

      // 例如，模拟一个注册错误
      if (userData.email === "error@example.com") {
        reject({
          message: "This email is already in use.",
        });
      } else {
        resolve(mockResponse);
      }
    }, 1000); // 1秒后解析 Promise
  });
};
