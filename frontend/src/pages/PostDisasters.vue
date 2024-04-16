<template>
  <div>
    <div class="container mx-auto px-4">
      <h1 class="text-xl font-semibold my-4">Post Disasters</h1>
      <div v-if="disasters.length">
        <div v-for="disaster in disasters" :key="disaster.id" class="mb-5">
          <h2 class="text-lg font-bold">{{ disaster.fields.disaster_name }} - {{ disaster.fields.type }}</h2>
          <p>Description: {{ disaster.fields.description }}</p>
          <p>Location: {{ disaster.fields.location }}</p>
          <p>Date: {{ disaster.fields.create_time }}</p>
          <div>
            <button @click="viewReport(disaster)" class="btn btn-primary">View Report</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No disasters to show.</p>
      </div>
    </div>
    <Modal v-if="showModal" :report="disasterReport" @close="showModal=false"/>
  </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    name: 'PostDisasters',
    data() {
      return {
        disasters: [],
        showModal: false,
        disasterReport: null,
      };
    },
    created() {
      this.fetchPostDisasters();
    },
    methods: {
      fetchPostDisasters() {
        axios.get('/etm/emergencyview/read_all_logs/')
          .then(response => {
            this.disasters = response.data.message;
            console.log(response.data)
          })
          .catch(error => {
            console.error('There was an error fetching the disasters:', error);
          });
      },
      viewReport(disaster) {
          axios.get(`/etm/emergencyview/read_specific_log?disaster_id=${disaster.pk}`)
          .then(response => {
              this.disasterReport = response.data.message[0];
              this.showModal = true;
              console.log(response.data)
          })
          .catch(error => {
              console.error('There was an error fetching the disaster report:', error);
          });
      },
    },
    components: {
    Modal: {
    props: ['report'],
    template: `
        <div class="modal-backdrop" @click.self="$emit('close')">
            <div class="modal">
                <h3>{{ report.fields.disaster_name }} - Report</h3>
                <p>Description: {{ report.fields.description }}</p>
                <p>Location: {{ report.fields.location }}</p>
                <p>Type: {{ report.fields.type }}</p>
                <p>Date: {{ report.fields.create_time }}</p>
                <!-- Include additional details as needed -->
                <button @click="$emit('close')">Close</button>
            </div>
        </div>
    `,
    }
}

  };
  </script>

  <style scoped>
  .container {
    max-width: 1200px;
  }
    .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    }
    .modal {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    max-width: 500px;
    width: 100%;
    }
  </style>
