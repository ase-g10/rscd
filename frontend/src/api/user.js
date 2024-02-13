import service from "@/utils/request";

export function userLogin(data) {
  return service({
    url: "um/login/log_in/",
    method: "post",
    data,
  })
}