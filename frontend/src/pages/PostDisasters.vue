<template>
  <div>
    <div class="container mx-auto px-4">
      <h1 class="text-xl font-semibold my-4">Post Disasters</h1>
      <div v-if="disasters.length">
        <div v-for="disaster in disasters" :key="disaster.pk" class="mb-5">
          <h2 class="text-lg font-bold">{{ disaster.fields.disaster_name }} - {{ disaster.fields.type }}</h2>
          <p>Description: {{ disaster.fields.description }}</p>
          <p>Location: {{ disaster.fields.location }}</p>
          <p>Date: {{ disaster.fields.create_time }}</p>
          <button @click="toggleReport(disaster)" class="btn btn-primary">
            {{ disaster.expanded ? 'Hide Report' : 'View Report' }}
          </button>
          <div v-if="disaster.expanded" v-show="disaster.expanded" class="mt-3">
            <p><strong>Report Details:</strong></p>
            <p>{{ disaster.report ? disaster.report.content : 'Loading...' }}</p>
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
              disaster.report = response.data.message;
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
