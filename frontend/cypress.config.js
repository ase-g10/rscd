const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: 'o4zy9w',
  
  e2e: {
    setupNodeEvents(on, config) {
      // 使用环境变量来设置不同的baseUrl
      let baseUrl;

      // 根据GitHub Actions中设置的环境变量来动态决定baseUrl
      if (process.env.CI_ENVIRONMENT_NAME === 'staging') {
        // Staging环境的URL
        baseUrl = 'https://rscdapistaging.iocky.com';
      } else if (process.env.CI_ENVIRONMENT_NAME === 'production') {
        // 生产环境的URL
        baseUrl = 'https://rscdapi.iocky.com';
      } else {
        baseUrl = 'http://localhost:8080';
      }
      config.baseUrl = baseUrl;
      return config;
    },
    "baseUrl": "http://localhost:8080",
  },
});
