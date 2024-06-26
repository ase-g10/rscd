import service from "@/utils/request";

import axios from 'axios';

export function userLogin(data) {
  return service({
    url: "/um/auth/login/",
    method: "POST",
    data,
  }).then(response => {
    if (response.status === 200 && response.data.access_token) {
      // 存储token
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  }).catch(error => {
    throw new Error('Login failed');
  });
}


export const userRegister = async (userData) => {
  const response = await service({
    url:"/um/auth/register/",
    method: 'POST',
    data: userData,
  });
  if (response.status !== 201) {
    throw new Error('Failed to register');
  }
  return response.data;
};

export const getUserInfo = async () => {
  return service({
    url: "/um/user_info/get_user_info/",
    method: 'GET'
  });
};