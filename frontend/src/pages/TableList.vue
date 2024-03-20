<template>
  <div class="row">
    <div class="col-lg-12">
      <card class="large-card">
        <template v-slot:title>
          <b class="text-center">{{ disasterTable.title }}</b>
        </template>
        <template v-slot:raw-content>
          <div class="table-responsive-lg">
            <table class="table">
              <thead>
              <tr>
                <th v-for="column in disasterTable.columns" :key="column.field">{{ column.label }}</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="item in disasterTable.data" :key="item.id">
                <td v-for="column in disasterTable.columns" :key="column.field">
                  <!-- Use a conditional to check for the navigation column -->
                  <template v-if="column.field !== 'edit' && column.field !== 'navigation'">
                    {{ item[column.field] }}
                  </template>
                  <template v-else-if="column.field === 'edit'">
                    <div>
                      <button @click="editItem(item)" class="btn btn-primary">Edit</button>
                      <button @click="deleteItem(item)" class="btn btn-danger">Delete</button>
                    </div>
                  </template>
                  <template v-else-if="column.field === 'navigation'">
                    <!-- Add a clickable icon for navigation -->
                    <div @click="navigateToHomepage(item)" style="cursor: pointer;">
                      <i>📍Show the Path</i>
                    </div>
                  </template>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </template>
      </card>
    </div>



  </div>
  <div class="map h-96" id="map"></div>
</template>

<script>
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
      // 53.341676, -6.267914
      disasterTable: {
        title: "Disaster Management",
        subTitle: "",
        data: [
          { id: 1, name: "Earthquake", type: "Natural", latitude:  53.341676, longitude: -6.267914, description: "A sudden shaking of the ground.", createdTime: "2024-03-19T12:00:00" },
          { id: 2, name: "Wildfire", type: "Natural", latitude: 40.7128, longitude: -74.0060, description: "An uncontrolled fire in wild areas.", createdTime: "2024-03-19T13:00:00" },
          { id: 3, name: "Flood", type: "Natural", latitude: 51.5074, longitude: -0.1278, description: "An overflow of water onto normally dry land.", createdTime: "2024-03-19T14:00:00" }
        ],
        columns: [
          { field: "id", label: "Disaster ID" },
          { field: "name", label: "Name" },
          { field: "type", label: "Type" },
          { field: "latitude", label: "Latitude" },
          { field: "longitude", label: "Longitude" },
          { field: "description", label: "Description" },
          { field: "createdTime", label: "Created Time" },
          {
            field: "edit",
            label: "Edit",
            slot: "edit",
          },
          { field: 'navigation', label:"Navigation" }
        ]
      },
    };
  },
  mounted() {
    console.log("Mounted - loading Google Maps Script");
    loadGoogleMapsScript(this.initMap.bind(this));
  },
  methods: {
    editItem(item) {
      console.log("Edit item:", item);
    },
    deleteItem(item) {
      console.log("Delete item:", item);
    },
    async navigateToHomepage(item) {
      console.log("Navigate to homepage:", item.latitude);

      const directionsService = new google.maps.DirectionsService();
      const directionsRenderer = new google.maps.DirectionsRenderer({
        map: this.map,
      });

      const currentLocation = new google.maps.LatLng(this.currentLat, this.currentLng);
      const destination = new google.maps.LatLng(item.latitude, item.longitude);

      const request = {
        origin: currentLocation,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING,
      };

      try {
        const response = await new Promise((resolve, reject) => {
          directionsService.route(request, (result, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
              resolve(result);
            } else {
              reject(new Error("Error displaying directions: " + status));
            }
          });
        });

        // Render the directions on the map
        directionsRenderer.setDirections(response);
      } catch (error) {
        console.error(error.message);
      }
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
            this.currentLat = position.coords.latitude.toFixed(5);
            this.currentLng = position.coords.longitude.toFixed(5);

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
            this.currentLat = pos.lat.toFixed(5); // 更新纬度
            this.currentLng = pos.lng.toFixed(5); // 更新经度
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

          this.currentLat = location.lat().toFixed(5);
          this.currentLng = location.lng().toFixed(5);

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

  }
};
</script>

<style scoped>
.large-card {
  height: 400px;
  width: 1380px;
  background-color: lightgrey;
}
</style>
