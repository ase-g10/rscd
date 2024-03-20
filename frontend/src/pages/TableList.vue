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
</template>

<script>
export default {
  data() {
    return {
      disasterTable: {
        title: "Disaster Management",
        subTitle: "",
        data: [
          { id: 1, name: "Earthquake", type: "Natural", latitude: 34.0522, longitude: -118.2437, description: "A sudden shaking of the ground.", createdTime: "2024-03-19T12:00:00" },
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
  methods: {
    editItem(item) {
      console.log("Edit item:", item);
    },
    deleteItem(item) {
      console.log("Delete item:", item);
    },
    navigateToHomepage(item) {
      // Implement navigation logic here
      console.log("Navigate to homepage:", item);
      // For example, you can use router.push('/home') to navigate to the homepage
    }
  }
};
</script>

<style scoped>
.large-card {
  height: 700px;
  width: 1380px;
  background-color: lightgrey;
}
</style>
