<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8 ">
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6" action="#">
        <div>
          <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
          <div class="mt-2">
            <input v-model="email" id="email" name="email" type="email" autocomplete="email" required
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between">
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
            <div class="text-sm">
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
            </div>
          </div>
          <div class="mt-2">
            <input v-model="password" id="password" name="password" type="password" autocomplete="current-password"
              required
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <button type="submit" @click="login"
            class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign
            in</button>
        </div>
        <button type="button"
          class="mt-6 w-full flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          @click="loginWithGithub">
          <img src="@/assets/img/github-mark.svg" alt="GitHub" class="h-5 w-5 mr-2" />
          Sign in with GitHub
        </button>
      </form>


      <p class="mt-10 text-center text-sm text-gray-500">
        Not a member?
        <a href="#" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Register here</a>
      </p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, getCurrentInstance } from 'vue';
import { loadRouteLocation, useRouter } from "vue-router";
import { loginWithGithub } from "@/api/auth2";
import NotificationTemplate from "./Notifications/NotificationTemplate";
import { userLogin } from "@/api/user";
import router from "@/router";

export default {
  methods: {
    loginWithGithub() {
      // 直接导航到后端提供的重定向 URL
      window.location.href = process.env.VUE_APP_BACKEND_URL + '/um/auth2/redirect_to_github';
    },
    login(e) {
      e.preventDefault();

      const userData = {
        email: this?.email ?? null,
        password: this?.password ?? null
      };

      userLogin(userData)
        .then(response => {
          console.log(response);
          this.$notify({
            component: NotificationTemplate,
            icon: "ti-check",
            horizontalAlign: "right",
            verticalAlign: "top",
            type: "success",
            title: "successfully log in ",
            text: `${response.data.message}`,
            dangerouslySetInnerHtml: true,
          })
          router.push('/maps');
          ;
        })
        .catch(error => {
          console.log(error);
          this.$notify({
            component: NotificationTemplate,
            icon: "ti-close",
            horizontalAlign: "right",
            verticalAlign: "top",
            type: "error",
            title: "Error",
            text: "PLZ provide correct email or password " + error.message, // 使用 error.message 来获取错误信息
            dangerouslySetInnerHtml: true,
          });
          console.error("incorrect email or password:", error);
        });

    },
  },
  setup() {
    const instance = getCurrentInstance();
    const notify = instance.appContext.config.globalProperties.$notify;
    const router = useRouter();
    const errorMessage = ref(""); // Reactive variable to store the error message

    const email = ref("");
    const password = ref("");

    onMounted(() => {
      const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
      const token = urlParams.get('token');
      const error = urlParams.get('error'); // Capture any error messages

      if (token) {
        localStorage.setItem('token', token);
        console.log("token: " + token);
        window.location.reload(); // Reload the page to update the navbar
      } else if (error) {
        errorMessage.value = error;
        notify({
          component: NotificationTemplate,
          icon: "ti-close",
          horizontalAlign: "right",
          verticalAlign: "top",
          type: "error",
          title: "Error",
          text: "Failed to log in, Please try again. " + error,
          dangerouslySetInnerHtml: true,
        });
      }
    });
    return { errorMessage, email, password };
  },
};
</script>

<style></style>