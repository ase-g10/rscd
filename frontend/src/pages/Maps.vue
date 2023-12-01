<template>
  <card class="card-map" title="Google Maps">
    <div>
      <label for="latitude">Latitude:</label>
      <input type="text" id="latitude" v-model="currentLat" readonly>

      <label for="longitude">Longitude:</label>
      <input type="text" id="longitude" v-model="currentLng" readonly>

      <label for="address">Address:</label>
      <input type="text" id="address" v-model="currentAddress">
    </div>

    <button @click="getCurrentLocation">Get Current Location</button>
    <button @click="codeAddress">Geocode Address</button>
    <button @click="submitDisaster">Submit Disaster</button>

    <div class="map">
      <div id="map"></div>
    </div>
  </card>
</template>


<script>
import { submitDisasterLocation } from '@/api/disaster';

export default {
  data() {
    return {
      map: null,
      marker: null,
      infoWindow: null,
      currentLat: '',
      currentLng: '',
      currentAddress: '',
      submitMessage: '',
    };
  },
  mounted() {
    console.log("Mounted - loading Google Maps Script");
    this.loadGoogleMapsScript();
    window.initMap = this.initMap.bind(this);
  },
  methods: {

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

            this.infoWindow.setPosition(pos);
            this.infoWindow.setContent('Current location');
            this.infoWindow.open(this.map, this.marker);
          },
          () => {
            this.handleLocationError(true, this.infoWindow, this.map.getCenter());
          }
        );
      } else {
        this.handleLocationError(false, this.infoWindow, this.map.getCenter());
      }
    },
    loadGoogleMapsScript() {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.VUE_APP_GOOGLE_MAP_API}&callback=initMap`;
      script.async = true;
      document.head.appendChild(script);
    },
    initMap() {
      console.log("后端 URL:", this.$backendUrl);
      console.log("Initializing map...");
      const defaultLatlng = { lat: 53.3437935, lng: -6.254571599999999 }; // TCD
      const mapOptions = {
        zoom: 16,
        center: defaultLatlng,
        scrollwheel: false,
        styles: [
        {
          featureType: "water",
          stylers: [{ saturation: 43 }, { lightness: -11 }, { hue: "#0088ff" }],
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
        ]
      };

      this.map = new window.google.maps.Map(document.getElementById('map'), mapOptions);
      this.infoWindow = new window.google.maps.InfoWindow();

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };
            this.geocodeLatLng(position.coords.latitude, position.coords.longitude);
            this.currentLat = pos.lat.toFixed(5); // 更新纬度
            this.currentLng = pos.lng.toFixed(5); // 更新经度
            this.map.setCenter(pos);

            this.marker = new window.google.maps.Marker({
              position: pos,
              map: this.map,
            });

            this.infoWindow.setPosition(pos);
            this.infoWindow.setContent('Current location');
            this.infoWindow.open(this.map, this.marker);
          },
          () => {
            this.handleLocationError(true, this.infoWindow, this.map.getCenter());
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
          ? 'Error: The Geolocation service failed.'
          : "Error: Your browser doesn't support geolocation."
      );
      infoWindow.open(this.map);
    },
    codeAddress() {
      const address = this.currentAddress; // 使用 v-model 绑定的地址值
      const geocoder = new google.maps.Geocoder();

      geocoder.geocode({ 'address': address }, (results, status) => {
        if (status == 'OK') {
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

          this.currentLat = location.lat().toFixed(5);
          this.currentLng = location.lng().toFixed(5);

          this.infoWindow.setPosition(location);
          this.infoWindow.setContent(results[0].formatted_address);
          this.infoWindow.open(this.map, this.marker);
        } else {
          alert('Geocode was not successful for the following reason: ' + status);
        }
      });
    },
    submitDisaster() {
      const data = {
        latitude: this.currentLat,
        longitude: this.currentLng,
      };

      submitDisasterLocation(data)
        .then(response => {
          this.submitMessage = 'Location successfully submitted';
          setTimeout(() => {
            this.submitMessage = '';
          }, 10000);  // 10秒后清除消息
          console.log('Location submitted:', response);
          alert('Location successfully submitted');
        })
        .catch(error => {
          this.submitMessage = 'Failed to submit location';
          setTimeout(() => {
            this.submitMessage = '';
          }, 10000);  // 10秒后清除消息
          console.error('Error submitting location:', error);
          alert('Failed to submit location');
        });
    },
  },
};
</script>

<style>
.map {
  height: 400px;
}
</style>