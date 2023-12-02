<template>
  <card class="card" title="Edit Profile">
    <div>
      <form @submit.prevent>
        <div class="row">
          <!-- <div class="col-md-5">
              <fg-input
                type="text"
                label="Company"
                :disabled="true"
                placeholder="RSCD Dashboard"
                v-model="user.company"
              >
              </fg-input>
            </div> -->
          <div class="col-md-3">
            <fg-input
              type="text"
              label="Username"
              placeholder="Username"
              v-model:value="user.username"
            >
            </fg-input>
          </div>
          <div class="col-md-4">
            <fg-input
              type="email"
              label="Email"
              placeholder="Email"
              v-model:value="user.email"
            >
            </fg-input>
          </div>
        </div>

        <div class="row">
          <div class="col-md-6">
            <fg-input
              type="text"
              label="First Name"
              placeholder="First Name"
              v-model:value="user.firstName"
            >
            </fg-input>
          </div>
          <div class="col-md-6">
            <fg-input
              type="text"
              label="Last Name"
              placeholder="Last Name"
              v-model:value="user.lastName"
            >
            </fg-input>
          </div>
        </div>

        <div class="row">
          <div class="col-md-12">
            <fg-input
              type="text"
              label="Address"
              placeholder="Home Address"
              v-model:value="user.address"
            >
            </fg-input>
          </div>
        </div>

        <div class="row">
          <div class="col-md-4">
            <fg-input
              type="text"
              label="City"
              placeholder="City"
              v-model:value="user.city"
            >
            </fg-input>
          </div>
          <div class="col-md-4">
            <fg-input
              type="text"
              label="Country"
              placeholder="Country"
              v-model:value="user.country"
            >
            </fg-input>
          </div>
          <div class="col-md-4">
            <fg-input
              type="number"
              label="Postal Code"
              placeholder="ZIP Code"
              v-model:value="user.postalCode"
            >
            </fg-input>
          </div>
        </div>

        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label>About Me</label>
              <textarea
                rows="5"
                class="form-control border-input"
                placeholder="Here can be your description"
                v-model="user.aboutMe"
              >
              </textarea>
            </div>
          </div>
        </div>
        <div class="text-center">
          <p-button type="info" round @click.prevent="updateProfile">
            Update Profile
          </p-button>
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </card>
</template>

<script>
export default {
  data() {
    return {
      user: {
        // company: "RSCD Dashboard",
        username: "group10",
        email: "group10@iocky.com",
        firstName: "First",
        lastName: "Last",
        address: "Trinity",
        city: "Dublin",
        postalCode: "",
        // aboutMe: `We must accept finite disappointment, but hold on to infinite hope.`,
      },
    };
  },
  methods: {
    updateProfile() {
      alert("Your data: " + JSON.stringify(this.user));
    },
  },
};
</script>
