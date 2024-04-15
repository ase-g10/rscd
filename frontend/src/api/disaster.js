// api/user.js
import service from "@/utils/request"; // 引入封装好的 axios 实例

// 不需要单独设置 BASE_URL，因为它已经在 request.js 中设置
export function submitDisasterLocation(data) {
  return service({
    url: "dm/disasterview/post_location/",
    method: "post",
    data,
  });
}

export const getDisasterData = () => {
  return service.get("dm/disasterview/read_all_verified/");
};

export const getDisasterDataFroVerify = () => {
  return service.get("dm/disasterview/read_all_verifying/");
};

export const getDisasterSafePoint = (data) => {
  return service({
    url: "dm/disasterview/calculate_safePoint/",
    method: "post",
    data,
  });
};

