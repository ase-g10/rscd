import service from "@/utils/request";

import axios from 'axios';

export function userLogin(data) {
  return service({
    url: "/um/auth/login/",
    method: "POST",
    data,
  })
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
