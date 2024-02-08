const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: 'o4zy9w',
  
  e2e: {
    setupNodeEvents(on, config) {
      return config;
    },
    "baseUrl": "http://localhost:8080",
  },
});
