<template>
  <div>
    <div class="container mx-auto px-4">
      <h1 class="text-xl font-semibold my-4">Post Disasters</h1>
      <div v-if="disasters.length">
        <div v-for="disaster in disasters.slice().reverse()" :key="disaster.pk" class="mb-5">
          <h2 class="text-lg font-bold">{{ disaster.fields.disaster_name }} - {{ disaster.fields.type }}</h2>
          <p>Description: {{ disaster.fields.description }}</p>
          <p>Location: {{ disaster.fields.location }}</p>
          <p>Date: {{ disaster.fields.create_time }}</p>
          <button @click="toggleReport(disaster)" class="btn btn-primary">
            {{ disaster.expanded ? 'Hide Report' : 'View Report' }}
          </button>
          <div v-if="disaster.expanded" v-show="disaster.expanded" class="mt-3">
            <p><strong>Report Details:</strong></p>
            <div v-if="disaster.report">
              <p>Disaster name: {{ disaster.report.fields.disaster_name }}</p>
              <p>Description: {{ disaster.report.fields.description }}</p>
              <p>Latitude: {{ disaster.report.fields.latitude }}</p>
              <p>Longitude: {{ disaster.report.fields.longitude }}</p>
              <p>Location: {{ disaster.report.fields.location }}</p>
              <p>Radius: {{ disaster.report.fields.radius }}</p>
              <p>Type: {{ disaster.report.fields.type }}</p>
              <p>Create time: {{ disaster.report.fields.create_time }}</p>
              <p>Update time: {{ disaster.report.fields.update_time }}</p>
              <p>Responsible team: {{ disaster.report.fields.responsible_team }}</p>
              <p>Image URL: {{ disaster.report.fields.image_url }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No disasters to show.</p>
      </div>
    </div>
  </div>
</template>


  <script>
  import axios from 'axios';

  export default {
    name: 'PostDisasters',
    data() {
      return {
        disasters: [],
      };
    },
    created() {
      this.fetchPostDisasters();
    },
    methods: {
      fetchPostDisasters() {
        axios.get('/etm/emergencyview/read_all_logs/')
          .then(response => {
            // Initialize each disaster with an expanded flag and an empty report
            this.disasters = response.data.message.map(disaster => ({
              ...disaster,
              expanded: false,
              report: null
            }));
            console.log(response.data)
          })
          .catch(error => {
            console.error('There was an error fetching the disasters:', error);
          });
      },
      toggleReport(disaster) {
        if (!disaster.report) {
          axios.get(`/etm/emergencyview/read_specific_log?disaster_id=${disaster.pk}`)
          .then(response => {
              disaster.report = response.data.message[0];
              disaster.expanded = !disaster.expanded; // Toggle after fetching the data
          })
          .catch(error => {
              console.error('There was an error fetching the disaster report:', error);
          });
        } else {
          disaster.expanded = !disaster.expanded; // Toggle visibility if the report is already loaded
        }
      },
    }
  };

  </script>

  <style scoped>
  .container {
    max-width: 1200px;
  }
  </style>
