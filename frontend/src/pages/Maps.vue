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
              <span class="label-text">Latitude:</span>
            </label>
            <input type="text" id="latitude" v-model="currentLat" readonly class="input input-bordered w-full" />
          </div>

          <!-- Longitude -->
          <div class="flex-1 min-w-0">
            <label class="label" for="longitude">
              <span class="label-text">Longitude:</span>
            </label>
            <input type="text" id="longitude" v-model="currentLng" readonly class="input input-bordered w-full" />
          </div>
        </div>

        <!-- Address with flex-auto to take up the remaining space -->
        <div class="flex-auto mb-4">
          <label class="label" for="address">
            <span class="label-text">Address:</span>
          </label>
          <input type="text" id="address" v-model="currentAddress" class="input input-bordered w-full" />
        </div>

        <div class="card-actions justify-end mt-4">
          <button @click="getCurrentLocation" class="btn btn-secondary">
            Get Current Location
          </button>
          <button @click="codeAddress" class="btn btn-secondary">
            Geocode Address
          </button>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
import loadGoogleMapsScript from "@/utils/googleMapsLoader";
import { getDisasterData } from "@/api/disaster";

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
    };
  },
  async mounted() {
    console.log("Mounted - loading Google Maps Script");
    await loadGoogleMapsScript(this.initMap.bind(this));
    await this.loadDisasters();

  },
  methods: {
    async loadDisasters() {
      getDisasterData().then(response => {
        // 假设响应数据在data字段中，并且实际的灾难数据在message字段中
        const disasters = response.data.message;
        console.log("Disasters:", disasters);

        disasters.forEach(disaster => {
          // 从disaster.fields中解构所需的字段
          const { latitude, longitude, radius, name, description, image_url: image_url } = disaster.fields;
          const position = { lat: parseFloat(latitude), lng: parseFloat(longitude) };

          if (radius > 0) {
            const disasterCircle = new google.maps.Circle({
              strokeColor: '#FF0000',
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: '#FF0000',
              fillOpacity: 0.35,
              map: this.map,
              center: position,
              radius: radius,
            });

            // 点击圆显示详细信息
            google.maps.event.addListener(disasterCircle, 'click', () => {
              let contentString = `<h3>${name}</h3><p>${description}</p>`;
              if (image_url) {
                contentString += `<img src="${image_url}" alt="${name}" style="width:100%;max-width:200px;">`;
              }
              this.infoWindow.setContent(contentString);
              this.infoWindow.setPosition(position);
              this.infoWindow.open(this.map);
              console.log("Disaster circle added:", disasterCircle);
            });
          } else {
            const marker = new google.maps.Marker({
              position,
              map: this.map,
              title: name
            });

            // 点击标记显示详细信息
            google.maps.event.addListener(marker, 'click', () => {
              let contentString = `<h3>${name}</h3><p>${description}</p>`;
              if (image_url) {
                contentString += `<img src="${image_url}" alt="${name}" style="width:100%;max-width:200px;">`;
              }
              this.infoWindow.setContent(contentString);
              this.infoWindow.open(this.map, marker);
              console.log("Disaster marker added:", marker);
            });
          }
        });
      }).catch(error => {
        console.error("Failed to load disasters:", error);
      });
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

      google.maps.event.addListenerOnce(this.map, 'idle', () => {
        this.loadDisasters();
      });

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
            });

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
    geocodeLatLng(lat, lng) {
      // eslint-disable-next-line no-undef
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
      // eslint-disable-next-line no-undef
      const geocoder = new google.maps.Geocoder();

      geocoder.geocode({ address: address }, (results, status) => {
        if (status == "OK") {
          const location = results[0].geometry.location;
          this.map.setCenter(location);

          if (this.marker) {
            this.marker.setPosition(location);
          } else {
            // eslint-disable-next-line no-undef
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
  },
};
</script>

<style>
@import "@/assets/css/mapsStyles.css";
</style>
