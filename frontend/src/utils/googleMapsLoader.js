// googleMapsLoader.js
let scriptLoaded = false;

export default function loadGoogleMapsScript(onLoadCallback) {
  if (scriptLoaded) {
    onLoadCallback();
    return;
  }

  window.initMap = () => {
    scriptLoaded = true;
    onLoadCallback();
  };

  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.VUE_APP_GOOGLE_MAP_API}&callback=initMap`;
  script.async = true;
  document.head.appendChild(script);
}
