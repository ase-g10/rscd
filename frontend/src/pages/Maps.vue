<template>
  <div>
    <div class="card card-compact bg-base-100 shadow-xl p-4">
      <div class="card-body">
        <!-- Flex container adjusted to wrap items if not enough space -->
        <div id="container" class="flex h-screen"> <!-- Ensure full height and flex display -->
          <div class="map h-full flex-grow" id="map"></div> <!-- Map fills available space -->
          <div id="sidebar" class="bg-white overflow-auto" :style="{ flexBasis: hasRoute ? '250px' : '0px' }">
            <p v-if="hasRoute">Total Distance: <span id="total" class="total-distance"></span></p>
            <div id="panel"></div>
          </div>
          <div id="floating-panel" class="absolute top-0 left-0 z-10 m-10">
            <b>Mode of Travel:</b>
            <select id="mode" v-model="travelMode" class="select select-bordered select-sm">
              <!-- Adjusted for smaller size -->
              <option value="DRIVING">Driving</option>
              <option value="WALKING">Walking</option>
              <option value="BICYCLING">Bicycling</option>
              <option value="TRANSIT">Transit</option>
            </select>
          </div>
        </div>
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
import { getDisasterSafePoint } from "@/api/disaster";
import router from "@/router";
import { updateDrivingLocation, getDrivingLocations } from "@/api/traffic";

function mockGetDisasterSafePoint({ latitude, longitude }) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Simulate a condition check. You could use latitude and longitude for more realistic scenarios.
      const userIsInDisasterArea = Math.random() < 0.5; // Assume the user is not in a disaster area for this simulation
      console.log("User is in disaster area:", userIsInDisasterArea);

      if (userIsInDisasterArea) {
        // Simulate a successful response
        resolve({
          data: {
            safe_lat: 53.3433840099226, // Mock safe point latitude
            safe_lng: -6.245269005249021, // Mock safe point longitude
          }
        });
      } else {
        // Simulate an error response
        reject({
          response: {
            data: {
              status: "error",
              message: "User is not in any disaster's impact area."
            }
          }
        });
      }
    }, 1000); // Delay to simulate network request
  });
}


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
      directionsService: null,
      directionsRenderer: null,
      travelMode: 'WALKING',
      hasRoute: false,
      locationUpdateTimer: null,
      updateTimer: null,
      drivingMarkers: [],
      markerPool: [],
    };
  },
  async mounted() {
    console.log("Mounted - loading Google Maps Script");
    await loadGoogleMapsScript(this.initMap.bind(this));
    await this.loadDisasters();
    this.$nextTick(() => {
      if (this.travelMode === "DRIVING") {
        this.startLocationUpdates();
      }
      this.startLocationFetching();
    });

  },
  watch: {
    travelMode: {
      handler() {
        // Check if we already have a location to route from/to
        if (this.currentLat && this.currentLng) {
          this.fetchSafePointAndDisplayRoute();
        }
      },
      immediate: false,
    },
    travelMode(newMode) {
      // When the travel mode changes to or from "DRIVING"
      if (newMode === "DRIVING") {
        console.log("Starting location updates...");
        this.startLocationUpdates();
      } else {
        console.log("Stopping location updates...");
        this.stopLocationUpdates();
      }
    },
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

            this.fetchSafePointAndDisplayRoute();
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
      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer({
        draggable: true,
        map: this.map,
        panel: document.getElementById("panel"),
      });

      google.maps.event.addListenerOnce(this.map, 'idle', () => {
        this.loadDisasters();
      });

      // 当路线改变时更新距离
      this.directionsRenderer.addListener("directions_changed", () => {
        const directions = this.directionsRenderer.getDirections();
        if (directions) {
          this.computeTotalDistance(directions);
        }
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
            this.fetchSafePointAndDisplayRoute();

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
    async fetchSafePointAndDisplayRoute() {
      // 假设已有方法获取当前用户位置，此处直接使用
      const userPosition = { lat: parseFloat(this.currentLat), lng: parseFloat(this.currentLng) };
      console.log("Fetching safe point based on...", this.currentLat, this.currentLng)
      console.log("User position:", { latitude: userPosition.lat, longitude: userPosition.lng });
      try {
        const response = await getDisasterSafePoint({ latitude: userPosition.lat, longitude: userPosition.lng });
        // const response = await mockGetDisasterSafePoint({ latitude: userPosition.lat, longitude: userPosition.lng });
        const safePoint = response.data;
        if (safePoint.safe_lat && safePoint.safe_lng) {
          this.hasRoute = true; // User is not in a safe area, display route
          console.log("User position:", userPosition);
          console.log("Safe point:", safePoint);
          this.displayRoute(
            { lat: userPosition.lat, lng: userPosition.lng },
            { lat: safePoint.safe_lat, lng: safePoint.safe_lng },
            this.directionsService,
            this.directionsRenderer
          );
        } else {
          this.hasRoute = false; // User is in a safe area, do not display route
        }
        // const safeLat = safePoint.safe_lat;
        // const safeLng = safePoint.safe_lng;
        // console.log("User position:", userPosition)
        // console.log("Safe point:", safePoint);

        // this.displayRoute(
        //   { lat: userPosition.lat, lng: userPosition.lng },
        //   { lat: safeLat, lng: safeLng },
        //   this.directionsService,
        //   this.directionsRenderer
        // );
      } catch (error) {
        console.error("Failed to fetch safe point:", error);
      }
    },
    displayRoute(origin, destination, service, display) {
      const travelModes = {
        DRIVING: google.maps.TravelMode.DRIVING,
        WALKING: google.maps.TravelMode.WALKING,
        BICYCLING: google.maps.TravelMode.BICYCLING,
        TRANSIT: google.maps.TravelMode.TRANSIT,
      };
      // 更新此方法以接受坐标而非地址作为起点和终点
      service.route({
        origin: origin,
        destination: destination,
        travelMode: travelModes[this.travelMode],
        // 其他路线选项...
      }).then(result => {
        display.setDirections(result);
      }).catch(e => {
        alert("Could not display directions due to: " + e);
        window.location.reload(); //TODO: 这个可能导致页面不断刷新?
      });
    },
    computeTotalDistance(result) {
      let total = 0;
      const myroute = result.routes[0];
      if (!myroute) {
        return;
      }
      for (let i = 0; i < myroute.legs.length; i++) {
        total += myroute.legs[i].distance.value;
      }
      total = total / 1000;
      document.getElementById("total").innerHTML = total + " km";
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
    startLocationUpdates() {
      // Start the periodic location updates
      if (!this.locationUpdateTimer) {
        this.locationUpdateTimer = setInterval(() => {
          this.updateLocation();
        }, 10000); // Update every 30 seconds
      }
    },
    stopLocationUpdates() {
      // Stop the periodic location updates
      if (this.locationUpdateTimer) {
        clearInterval(this.locationUpdateTimer);
        this.locationUpdateTimer = null;
      }
    },
    updateLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            // 成功获取位置，使用当前位置进行上报
            const currentLat = position.coords.latitude;
            const currentLng = position.coords.longitude;
            const data = {
              latitude: currentLat,
              longitude: currentLng,
            };
            console.log("Current location updated directly", data);
            this.sendLocationData(data);
          },
          () => {
            // 获取位置失败，使用预设的固定位置进行上报
            console.error('Failed to fetch current location, using address location instead');
            const data = {
              latitude: this.currentLat,
              longitude: this.currentLng,
            };
            this.sendLocationData(data);
          },
          { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
      } else {
        console.error("Geolocation is not supported by this browser.");
      }
    },
    sendLocationData(data) {
      console.log("Location updated", data);
      updateDrivingLocation(data)
        .then(response => {
          console.log('Location update successful:', response);
        })
        .catch(error => {
          console.error('Location update failed:', error);
        });
    },
    startLocationFetching() {
      this.updateTimer = setInterval(() => {
        this.fetchDrivingLocations();
      }, 10000);
    },
    fetchDrivingLocations() {
      getDrivingLocations().then(response => {
        const locations = response.data.locations;
        console.log('Fetched locations:', response.data);
        this.updateMarkers(locations);
      }).catch(error => {
        console.error('Failed to fetch locations:', error);
      });
    },
    async updateMarkers(locations) {
      const vm = this;
      const roleIcons = {
        'firetruck': 'https://sky.iocky.com/i/2024/04/16/661d88f9c5821.png',
        'emergency_response_team': 'https://sky.iocky.com/i/2024/04/16/661d8908dbbfb.png',
        'police': 'https://sky.iocky.com/i/2024/04/16/661d89fae',
        'rescue': 'https://sky.iocky.com/i/2024/04/16/661d8a4c56ef5.png',
        'administrator': 'https://sky.iocky.com/i/2024/04/16/661d8a1c1e3e1.png',
        'public': 'https://sky.iocky.com/i/2024/04/16/661d8558b2f2d.png',
        'army': 'https://sky.iocky.com/i/2024/04/16/661d8b3b34626.png',
        // 其他角色...
      };
      console.log('Markers to be cleared:', this.drivingMarkers, "markerpool:", this.markerPool);
      // Remove existing markers
      this.drivingMarkers.forEach(marker => {
        marker.setMap(null);
        vm.markerPool.push(marker); // 使用 vm 来访问 markerPool
        console.log('Marker added to pool:', marker, "markerpool:", this.markerPool);
      });
      this.drivingMarkers = [];
      console.log('Driving markers cleared:', this.drivingMarkers);

      console.log('New locations:', locations);
      if (false) {
        locations.push({ latitude: 53.355427961778176, longitude: -6.263842820866124, user_role: "firetruck" });
        locations.push({ latitude: 53.36444248500757, longitude: -6.26897164340078, user_role: "firetruck" });
        locations.push({ latitude: 53.34785944551918, longitude: -6.25956887847702, user_role: "ambulance" });
        locations.push({ latitude: 53.35334802661926, longitude: -6.269516950547101, user_role: "ambulance" });
        locations.push({ latitude: 53.35572672814882, longitude: -6.259175498778991, user_role: "police" });
        locations.push({ latitude: 53.353055505056496, longitude: -6.262115244700755, user_role: "police" });
        locations.push({ latitude: 53.352363840730185, longitude: -6.261097214897715, user_role: "default" });
        locations.push({ latitude: 53.36608042449805, longitude: -6.258274304906397, user_role: "rescue" });
        locations.push({ latitude: 53.348601826525176, longitude: -6.250799770399876, user_role: "army" });
        locations.push({ latitude: 53.352695871981325, longitude: -6.269076223864162, user_role: undefined });


        // 添加一个不符合格式的位置数据进行测试
        locations.push({ lat: 53.350000, long: -6.260000 }); // 故意使用错误的键名以测试数据验证

        console.log('Mock New locations:', locations);
      }

      if (!locations || locations.length === 0 || locations == undefined || locations == null) {
        console.log('No new locations to update');
        return;
      }

      var service = new google.maps.DirectionsService();

      const markerPromises = locations.map(async (loc) => {
        loc.latitude = parseFloat(loc.latitude);
        loc.longitude = parseFloat(loc.longitude);
        if (typeof loc.latitude !== 'number' || typeof loc.longitude !== 'number') {
          console.error('Invalid location data:', loc);
          return null;
        }

        let result = await new Promise(resolve => {
          service.route({
            origin: { lat: loc.latitude, lng: loc.longitude },
            destination: { lat: loc.latitude, lng: loc.longitude },
            travelMode: google.maps.TravelMode.DRIVING
          }, function (result, status) {
            if (status === google.maps.DirectionsStatus.OK) {
              resolve(result);
            } else {
              console.error('Directions request failed due to ' + status);
              resolve(null);
            }
          });
        });

        if (!result) {
          console.error('Failed to get directions for location:', loc);
          return null;
        }

        const iconUrl = roleIcons[loc.user_role] || 'https://sky.iocky.com/i/2024/04/16/661d8558b2f2d.png';
        let marker;
        if (vm.markerPool.length > 0) {
          marker = vm.markerPool.pop();
          marker.setPosition(result.routes[0].legs[0].start_location);
          marker.setTitle(loc.username || "Unknown");
          marker.setIcon(null); // 重置图标属性
          marker.setIcon({
            url: iconUrl,
            scaledSize: new google.maps.Size(40, 40),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(20, 20)
          });
        } else {
          marker = new google.maps.Marker({
            position: result.routes[0].legs[0].start_location,
            map: this.map,
            title: loc.username || "Unknown",
            icon: {
              url: iconUrl,
              scaledSize: new google.maps.Size(40, 40),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(20, 20)
            }
          });
        }

        return marker;
      });

      this.drivingMarkers = await Promise.all(markerPromises);
      this.drivingMarkers = this.drivingMarkers.filter(marker => marker !== null);

      console.log('Driving markers updated:', this.drivingMarkers);



      // Add new markers
      // locations.forEach(loc => {
      //   if (typeof loc.latitude !== 'number' || typeof loc.longitude !== 'number') {
      //     console.error('Invalid location data:', loc);
      //     return;
      //   }
      //   const marker = new google.maps.Marker({
      //     position: { lat: loc.latitude, lng: loc.longitude },
      //     map: this.map,
      //     title: loc.username,
      //     icon : {
      //       url: 'https://sky.iocky.com/i/2024/04/16/661d8558b2f2d.png',
      //       scaledSize: new google.maps.Size(30, 30),
      //       origin: new google.maps.Point(0, 0),
      //       anchor: new google.maps.Point(0, 0)
      //     }
      //   });
      //   this.drivingMarkers.push(marker);
      // });
      // console.log('Driving markers updated:', this.drivingMarkers);
    },
    beforeDestroy() {
      if (this.updateTimer) {
        clearInterval(this.updateTimer);
      }
      this.drivingMarkers.forEach(marker => marker.setMap(null));
    },
  },
};
</script>

<style>
@import "@/assets/css/mapsStyles.css";

#container {
  display: flex;
  height: 100%;
}

#sidebar {
  flex-basis: 250px;
  /* Adjust based on your preference */
  flex-shrink: 0;
  /* Prevents shrinking */
  overflow-y: auto;
  /* Allows scrolling */
  padding: 1rem;
}

#map {
  height: 600px;
  /* Temporarily set a fixed height to debug */
  flex-grow: 1;
}

#floating-panel {
  position: absolute;
  top: 10px;
  left: 25%;
  z-index: 5;
  background-color: #fff;
  padding: 5px;
  border: 1px solid #999;
  text-align: center;
  font-family: "Roboto", "sans-serif";
  line-height: 30px;
  padding-left: 10px;
}

.select-sm {
  /* Smaller select size */
  padding: 0.1rem 0.1rem;
  font-size: 0.875rem;
  line-height: 1rem;
}
</style>
