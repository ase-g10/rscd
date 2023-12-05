<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" type="text" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
      axios.post('http://localhost:8000/login/', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        console.log(response.data);
        // Handle login success (e.g., store token, redirect)
      })
      .catch(error => {
        console.error(error);
        // Handle error
      });
    }
  }
};
</script>
