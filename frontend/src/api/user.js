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
  try {
    // Make the GET request to the user info API endpoint
    const response = await service({
      url: "/um/user_info/get_user_info/",
      method: 'GET'
    });

    // Check if the request was successful
    if (response.status === 200) {
      console.log(response.data);
      return response.data;  // Return the user information
    } else {
      console.log(response.data);
      throw new Error('Failed to retrieve user information');
    }
  } catch (error) {
    console.log(error);
    // If an error occurs, handle it by throwing an error with a message
    throw new Error('User information retrieval failed: ' + error.message);
  }
};