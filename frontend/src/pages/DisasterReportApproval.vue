<template>
  <div class="card card-compact bg-base-100 shadow-xl p-4">
    <div class="card-body">
      <h2 class="card-title">Disaster Report Approval</h2>
      <div class="report-list my-4">
        <ul>
          <li v-for="report in disasterReports" :key="report.id" class="mb-4 p-2 border rounded">
            <h3>{{ report.fields.name }} - {{ report.fields.type }}</h3>
            <p>Description: {{ report.fields.description }}</p>
            <p>Location: {{ report.fields.location }}</p>
            <p>Latitude: {{ report.fields.latitude }}, Longitude: {{ report.fields.longitude }}</p>
            <p>Contact: {{ report.fields.contact }}</p>
            <p>Report Time: {{ new Date(report.fields.create_time).toLocaleString() }}</p>
            <p>Status: {{ report.fields.verified_status === '0' ? 'Awaiting Verification' : 'Verified' }}</p>
            <img :src="report.fields.image_url" alt="Disaster Image" class="disaster-image" v-if="report.fields.image_url">
            <div>
              <button @click="approveReport(report)" class="btn btn-primary">Approve</button>
              <button @click="rejectReport(report)" class="btn btn-error">Reject</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DisasterReportApproval',
  data() {
    return {
      disasterReports: [],
    };
  },
  created() {
    this.fetchDisasterReports();
  },
  methods: {
    fetchDisasterReports() {
      axios.get('/dm/disasterview/read_all_verifying/')
        .then(response => {
          this.disasterReports = response.data.message;
        })
        .catch(error => {
          console.error('There was an error fetching the disaster reports:', error);
        });
    },
    approveReport(report) {
      const postData = {
        latitude: report.fields.latitude,
        longitude: report.fields.longitude,
        verified_status: '1',
      };
      axios.post('/dm/disastermodify/write/', postData)
        .then(response => {
          console.log('Report approved:', response.data.message);
          this.fetchDisasterReports();
        })
        .catch(error => {
          console.error('There was an error approving the disaster report:', error);
        });
    },
    rejectReport(report) {
      const postData = {
        latitude: report.fields.latitude,
        longitude: report.fields.longitude,
        verified_status: '-1',
      };
      axios.post('/dm/disastermodify/write/', postData)
        .then(response => {
          console.log('Report rejected:', response.data.message);
          this.fetchDisasterReports();
        })
        .catch(error => {
          console.error('There was an error rejecting the disaster report:', error);
        });
    },
  },
};
</script>

<style>
@import "@/assets/css/mapsStyles.css";

.disaster-image {
  max-width: 100%;
  height: auto;
}
</style>
