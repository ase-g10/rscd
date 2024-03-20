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
  const response = await fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  if (!response.ok) {
    throw new Error('Failed to register');
  }
  return response.json();
};
