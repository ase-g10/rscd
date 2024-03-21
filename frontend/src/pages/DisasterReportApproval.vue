<template>
  <div class="card card-compact bg-base-100 shadow-xl p-4">
    <div class="card-body">
      <h2 class="card-title">Disaster Report Approval</h2>
      <div class="report-list my-4">
        <ul>
          <li v-for="report in disasterReports" :key="report.id">
            {{ report.fields.disasterType }} at {{ report.fields.location }}
            <button @click="approveReport(report.id)" class="btn btn-primary">Approve</button>
            <button @click="rejectReport(report.id)" class="btn btn-error">Reject</button>
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
      console.log('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW');
      axios.get('/dm/disasterview/read_all_verifying/')
        .then(response => {
          this.disasterReports = response.data.message;
          console.log('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW');
        })
        .catch(error => {
          console.error('There was an error fetching the disaster reports:', error);
        });
    },
    approveReport(reportId) {
      console.log('Approving report with ID:', reportId);
    },
    rejectReport(reportId) {
      console.log('Rejecting report with ID:', reportId);
    },
  },
};
</script>

<style>
@import "@/assets/css/mapsStyles.css";
</style>
