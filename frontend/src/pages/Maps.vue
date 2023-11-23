<template>
  <card class="card-map" title="Google Maps">
    <button @click="getCurrentLocation">Get Current Location</button>
    <div class="map">
      <div id="map"></div>
    </div>
  </card>
</template>

<script>
export default {
  data() {
    return {
      map: null,
      marker: null,
      infoWindow: null,
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
    handleLocationError(browserHasGeolocation, infoWindow, pos) {
      infoWindow.setPosition(pos);
      infoWindow.setContent(
        browserHasGeolocation
          ? 'Error: The Geolocation service failed.'
          : "Error: Your browser doesn't support geolocation."
      );
      infoWindow.open(this.map);
    },
  },
};
</script>

<style>
.map {
  height: 400px;
}
</style>