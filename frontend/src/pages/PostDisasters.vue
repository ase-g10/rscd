<template>
    <div class="container mx-auto px-4">
      <h1 class="text-xl font-semibold my-4">Post Disasters</h1>
      <div v-if="disasters.length">
        <div v-for="disaster in disasters" :key="disaster.id" class="mb-5">
          <h2 class="text-lg font-bold">{{ disaster.name }} - {{ disaster.type }}</h2>
          <p>Description: {{ disaster.description }}</p>
          <p>Location: {{ disaster.location }}</p>
          <p>Date: {{ disaster.date }}</p>
          <div>
            <button @click="viewReport(disaster)" class="btn btn-primary">View Report</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No disasters to show.</p>
      </div>
    </div>
    <Modal v-if="showModal" @close="showModal=false" :report="disasterReport" />
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
        axios.get('/api/disasters/post')
          .then(response => {
            this.disasters = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching the disasters:', error);
          });
      },
    viewReport(disaster) {
        axios.get(`/api/disasters/report/${disaster.id}`)
        .then(response => {
            this.disasterReport = response.data;
            this.showModal = true;
        })
        .catch(error => {
            console.error('There was an error fetching the disaster report:', error);
        });
    },
    },
    components: {
        Modal: {
        props: ['disaster'],
        template: `
            <div class="modal-backdrop">
            <div class="modal">
                <h3>{{ report.title }} - Report</h3>
                <p>{{ report.content }}</p>
                <!-- More disaster details here -->
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
  