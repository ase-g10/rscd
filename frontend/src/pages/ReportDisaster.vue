<template>
  <div>
    <div class="card card-compact bg-base-100 shadow-xl p-4">
      <div class="card-body">
        <!-- Flex container adjusted to wrap items if not enough space -->
        <div class="map h-96" id="map"></div>
        <div class="flex flex-wrap justify-between gap-4 mb-4">
          <!-- Latitude -->
          <div class="flex-1 min-w-0">
            <label class="label" for="latitude">
              <span class="label-text">Disaster Latitude:</span>
            </label>
            <input
              type="text"
              id="disasterLatitude"
              v-model="currentLat"
              readonly
              class="input input-bordered w-full"
            />
          </div>

          <!-- Longitude -->
          <div class="flex-1 min-w-0">
            <label class="label" for="longitude">
              <span class="label-text">Disaster Longitude:</span>
            </label>
            <input
              type="text"
              id="disasterLongitude"
              v-model="currentLng"
              readonly
              class="input input-bordered w-full"
            />
          </div>
        </div>



        <!-- Address with flex-auto to take up the remaining space -->
        <div class="flex-auto mb-4">
          <label class="label" for="disasterAddress">
            <span class="label-text">Disaster Address:</span>
          </label>
          <input
            type="text"
            id="disasterAddress"
            v-model="currentAddress"
            class="input input-bordered w-full"
          />
        </div>

        <!-- Disaster Name -->
        <div class="flex-auto mb-4">
          <label class="label" for="disasterName">
            <span class="label-text">Disaster Name:</span>
          </label>
          <input
            type="text"
            id="disasterName"
            v-model="disasterName"
            class="input input-bordered w-full"
            placeholder="Enter the disaster name"
          />
        </div>


        <!-- Email or Phone Number -->
        <div class="flex-auto mb-4">
          <label class="label" for="contactInfo">
            <span class="label-text">Email or Phone Number (Required, Phone Number Must started with +353, followed by 9 digits):</span>
          </label>
          <input
            type="text"
            id="contactInfo"
            v-model="contactInfo"
            class="input input-bordered w-full"
            placeholder="Email or Phone"
          />
        </div>


        <div class="flex-1 min-w-0">
          <label class="label" for="disasterType">
            <span class="label-text">Disaster Type:</span>
          </label>
          <select
            id="disasterType"
            v-model="selectedDisasterType"
            class="input input-bordered w-full"
            placeholder="Select a disaster type."
          >
            <option value="" disabled selected>Select a disaster type</option>
            <option value="car_accident">Car Accident</option>
            <option value="fire_disaster">Fire Disaster</option>
            <option value="fire_disaster">Riot</option>
            <option value="earthquake">Earthquake</option>
            <option value="flood">Flood</option>
            <option value="hurricane">Hurricane</option>
            <option value="tornado">Tornado</option>
            <option value="tsunami">Tsunami</option>
            <option value="volcano">Volcano</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div class="flex-1 min-w-0" v-if="selectedDisasterType === 'other'">
          <label class="label" for="customDisasterType">
            <span class="label-text">Specify Disaster Type:</span>
          </label>
          <input
            type="text"
            id="customDisasterType"
            v-model="customDisasterType"
            class="input input-bordered w-full"
            placeholder="Specify the type of disaster"
          />
        </div>


        <div class="flex-auto mb-4">
          <label class="label" for="disasterDescription">
            <span class="label-text">Disaster Description:</span>
          </label>
          <textarea
            id="disasterDescription"
            v-model="disasterDescription"
            class="input input-bordered w-full"
            placeholder="In WHERE, WHEN, WHAT happened."
          ></textarea>
        </div>

        <!-- Image URL -->
        <div class="flex-auto mb-4">
          <label class="label" for="imageUrl">
            <span class="label-text">Image URL:</span>
          </label>
          <input
            type="text"
            id="imageUrl"
            v-model="imageUrl"
            class="input input-bordered w-full"
            placeholder="http://example.com/image.jpg"
          />
        </div>


        <div class="card-actions justify-end mt-4">
          <button @click="getCurrentLocation" class="btn btn-secondary">
            Get Current Location
          </button>
          <button @click="codeAddress" class="btn btn-secondary">
            Geocode Address
          </button>
          <button @click="submitDisaster" class="btn btn-primary">
            Submit Disaster
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { submitDisasterLocation } from "@/api/disaster";
import NotificationTemplate from "./Notifications/NotificationTemplate";
import loadGoogleMapsScript from "@/utils/googleMapsLoader";

export default {
  data() {
    return {
      map: null,
      marker: null,
      infoWindow: null,
      currentLat: "",
      currentLng: "",
      currentAddress: "",
      submitMessage: "",
      selectedDisasterType: "",
      disasterDescription: "",
      userCircle: null,
      contactInfo: "",
      imageUrl: "",
      customDisasterType: "",
      disasterName: "",
    };
  },
  mounted() {
    console.log("Mounted - loading Google Maps Script");
    loadGoogleMapsScript(this.initMap.bind(this));
  },
  methods: {
    isValidContactInfo(input) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phonePattern = /^(?:\+353|0)8[3-9]\d{7}$/;
    return emailPattern.test(input) || phonePattern.test(input);
  },
    getCurrentLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };
            this.map.setCenter(pos);

            if (this.marker) {
              this.marker.setPosition(pos);
            } else {
              this.marker = new window.google.maps.Marker({
                position: pos,
                map: this.map,
              });
            }

            this.geocodeLatLng(
              position.coords.latitude,
              position.coords.longitude
            );
            this.currentLat = position.coords.latitude;
            this.currentLng = position.coords.longitude;

            this.infoWindow.setPosition(pos);
            this.infoWindow.setContent("Current location");
            this.infoWindow.open(this.map, this.marker);
          },
          () => {
            this.handleLocationError(
              true,
              this.infoWindow,
              this.map.getCenter()
            );
          }
        );
      } else {
        this.handleLocationError(false, this.infoWindow, this.map.getCenter());
      }
    },
    initMap() {
      console.log("Backend URL:", this.$backendUrl);
      console.log("Initializing map...");
      const defaultLatlng = { lat: 53.3437935, lng: -6.254571599999999 }; // TCD
      const mapOptions = {
        zoom: 16,
        center: defaultLatlng,
        scrollwheel: false,
        styles: [
          {
            featureType: "water",
            stylers: [
              { saturation: 43 },
              { lightness: -11 },
              { hue: "#0088ff" },
            ],
          },
          {
            featureType: "road",
            elementType: "geometry.fill",
            stylers: [
              { hue: "#ff0000" },
              { saturation: -100 },
              { lightness: 99 },
            ],
          },
          {
            featureType: "road",
            elementType: "geometry.stroke",
            stylers: [{ color: "#808080" }, { lightness: 54 }],
          },
          {
            featureType: "landscape.man_made",
            elementType: "geometry.fill",
            stylers: [{ color: "#ece2d9" }],
          },
          {
            featureType: "poi.park",
            elementType: "geometry.fill",
            stylers: [{ color: "#ccdca1" }],
          },
          {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [{ color: "#767676" }],
          },
          {
            featureType: "road",
            elementType: "labels.text.stroke",
            stylers: [{ color: "#ffffff" }],
          },
          { featureType: "poi", stylers: [{ visibility: "off" }] },
          {
            featureType: "landscape.natural",
            elementType: "geometry.fill",
            stylers: [{ visibility: "on" }, { color: "#b8cb93" }],
          },
          { featureType: "poi.park", stylers: [{ visibility: "on" }] },
          {
            featureType: "poi.sports_complex",
            stylers: [{ visibility: "on" }],
          },
          { featureType: "poi.medical", stylers: [{ visibility: "on" }] },
          {
            featureType: "poi.business",
            stylers: [{ visibility: "simplified" }],
          },
        ],
      };

      this.map = new window.google.maps.Map(
        document.getElementById("map"),
        mapOptions
      );
      this.infoWindow = new window.google.maps.InfoWindow();

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };
            this.geocodeLatLng(
              position.coords.latitude,
              position.coords.longitude
            );
            this.currentLat = pos.lat; // 更新纬度
            this.currentLng = pos.lng; // 更新经度
            this.map.setCenter(pos);

            this.marker = new window.google.maps.Marker({
              position: pos,
              map: this.map,
              draggable: true,
            });

            this.marker.setIcon('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/w8AAwAB/DE8Eg0AAAAASUVORK5CYII=');

            const userCircle = new window.google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map: this.map,
            center: pos,
            radius: 100, // 默认半径, 例如1000米
            editable: true, // 允许用户编辑大小
            });

            this.userCircle = userCircle;

            // 将圆心绑定到标记的位置
            userCircle.bindTo('center', this.marker, 'position');

            // 添加标记拖动事件监听器
            this.marker.addListener('drag', () => {
              // 拖动标记时，圆形会自动更新其位置
              const markerPos = this.marker.getPosition();
              this.currentLat = markerPos.lat();
              this.currentLng = markerPos.lng();
            });

            // 监听圆的大小和位置变化
            userCircle.addListener('radius_changed', () => {
            });
            userCircle.addListener('center_changed', () => {
              const center = this.userCircle.getCenter();
              this.currentLat = center.lat();
              this.currentLng = center.lng();
              this.geocodeLatLng(this.currentLat, this.currentLng);
            });
          },
          () => {
            this.handleLocationError(
              true,
              this.infoWindow,
              this.map.getCenter()
            );
          }
        );
      } else {
        this.handleLocationError(false, this.infoWindow, this.map.getCenter());
      }
    },
    geocodeLatLng(lat, lng) {
      const geocoder = new google.maps.Geocoder();
      const latlng = { lat: lat, lng: lng };
      geocoder.geocode({ location: latlng }, (results, status) => {
        if (status === "OK") {
          if (results[0]) {
            this.currentAddress = results[0].formatted_address;
          } else {
            window.alert("No address found");
          }
        } else {
          window.alert("Geocoder failed due to: " + status);
        }
      });
    },
    handleLocationError(browserHasGeolocation, infoWindow, pos) {
      infoWindow.setPosition(pos);
      infoWindow.setContent(
        browserHasGeolocation
          ? "Error: The Geolocation service failed."
          : "Error: Your browser doesn't support geolocation."
      );
      infoWindow.open(this.map);
    },
    codeAddress() {
      const address = this.currentAddress; // 使用 v-model 绑定的地址值
      const geocoder = new google.maps.Geocoder();

      geocoder.geocode({ address: address }, (results, status) => {
        if (status == "OK") {
          const location = results[0].geometry.location;
          this.map.setCenter(location);

          if (this.marker) {
            this.marker.setPosition(location);
          } else {
            this.marker = new google.maps.Marker({
              position: location,
              map: this.map,
            });
          }

          this.currentLat = location.lat();
          this.currentLng = location.lng();

          this.infoWindow.setPosition(location);
          this.infoWindow.setContent(results[0].formatted_address);
          this.infoWindow.open(this.map, this.marker);
        } else {
          alert(
            "Geocode was not successful for the following reason: " + status
          );
        }
      });
    },
    submitDisaster() {
      if (!this.currentLat || !this.currentLng) {
        this.$notify({
          component: NotificationTemplate,
          icon: "ti-close",
          horizontalAlign: "right",
          verticalAlign: "top",
          type: "warning",
          title: "Warning",
          text: "Please provide a valid location.",
          dangerouslySetInnerHtml: true,
        });
        return;
      }

      if (!this.disasterName) {
        this.$notify({
          component: NotificationTemplate,
          icon: "ti-close",
          horizontalAlign: "right",
          verticalAlign: "top",
          type: "warning",
          title: "Warning",
          text: "Please provide a disaster name.",
          dangerouslySetInnerHtml: true,
        });
        return;
      }

      if (!this.selectedDisasterType) {
        this.$notify({
            component: NotificationTemplate,
            icon: "ti-close",
            horizontalAlign: "right",
            verticalAlign: "top",
            type: "warning",
            title: "Warning",
            text: "Please select a disaster type.",
            dangerouslySetInnerHtml: true,
        });
        return;
      }

      if (!this.contactInfo || !this.isValidContactInfo(this.contactInfo)) {
        this.$notify({
            component: NotificationTemplate,
            icon: "ti-close",
            horizontalAlign: "right",
            verticalAlign: "top",
            type: "warning",
            title: "Warning",
            text: "Please enter valid email or phone number.", // 使用 error.message 来获取错误信息
            dangerouslySetInnerHtml: true,
          });
        return;
      }

      const data = {
        name: this.disasterName,
        latitude: this.currentLat,
        longitude: this.currentLng,
        location: this.currentAddress,
        type: this.selectedDisasterType === 'other' ? this.customDisasterType : this.selectedDisasterType,
        description: this.disasterDescription,
        contact: this.contactInfo,
        //TODO: Add image upload
        image_url: this.imageUrl,
      };

      if (this.userCircle) {
        data.latitude = this.userCircle.getCenter().lat();
        data.longitude = this.userCircle.getCenter().lng();
        data.radius = this.userCircle.getRadius();
      }

      submitDisasterLocation(data)
        .then((response) => {
          console.log("Reported Data: ",data);
          console.log("Response:", response);
          this.$notify({
            component: NotificationTemplate,
            icon: "ti-check",
            horizontalAlign: "right",
            verticalAlign: "top",
            type: "success",
            title: "Disaster submitted",
            text: `${response.data.message}`,
            dangerouslySetInnerHtml: true,
          });
          console.log("Disaster submitted:", response);
        })
        .catch((error) => {
          console.log("Error:", error);
          this.$notify({
            component: NotificationTemplate,
            icon: "ti-close",
            horizontalAlign: "right",
            verticalAlign: "top",
            type: "error",
            title: "Error",
            text: "Failed to submit the disaster. " + error.message, // 使用 error.message 来获取错误信息
            dangerouslySetInnerHtml: true,
          });
          console.error("Error submitting disaster:", error);
        });
    },
  },
};
</script>

<style>
@import "@/assets/css/mapsStyles.css";
</style>
