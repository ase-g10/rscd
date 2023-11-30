// api/user.js
import service from '@/utils/request'; // 引入封装好的 axios 实例

// 不需要单独设置 BASE_URL，因为它已经在 request.js 中设置
export function test(params, year, month) {
  return service({
    url: `/api/test/year=${year}?month=${month}/`,
    method: 'get',
    params,
  });
}

export const test2 = userId => {
  return service.get(`/test/userID/${userId}`);
};
