import service from "@/utils/request";


export function updateDrivingLocation(data) {
  return service({
    url: "tm/trafficview/save_driving_location/",
    method: "post",
    data,
  });
}