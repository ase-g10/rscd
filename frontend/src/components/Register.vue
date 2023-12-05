<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="Register">
      <input v-model="username" type="text" placeholder="Username" />
      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    register() {
      axios.post('http://localhost:8000/register/', {
        username: this.username,
        email: this.email,
        password: this.password
      })
      .then(response => {
        console.log(response.data);
        // Redirect or show success message
      })
      .catch(error => {
        console.error(error);
        // Handle error
      });
    }
  }
};
</script>
