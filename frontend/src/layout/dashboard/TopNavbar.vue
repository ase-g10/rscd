<template>
  <nav class="navbar navbar-expand-lg navbar-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">{{ routeName }}</a>
      <button
        class="navbar-toggler navbar-burger"
        type="button"
        @click="toggleSidebar"
        :aria-expanded="$sidebar.showSidebar"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-bar"></span>
        <span class="navbar-toggler-bar"></span>
        <span class="navbar-toggler-bar"></span>
      </button>
<!--      <div class="collapse navbar-collapse">-->
<!--        <ul class="navbar-nav ml-auto">-->
<!--          <li class="nav-item">-->
<!--            <a href="#" class="nav-link">-->
<!--              <i class="ti-panel"></i>-->
<!--              <p>Stats</p>-->
<!--            </a>-->
<!--          </li>-->
<!--&lt;!&ndash;          <drop-down&ndash;&gt;-->
<!--&lt;!&ndash;            class="nav-item"&ndash;&gt;-->
<!--&lt;!&ndash;            title="5 Notifications"&ndash;&gt;-->
<!--&lt;!&ndash;            title-classes="nav-link"&ndash;&gt;-->
<!--&lt;!&ndash;            icon="ti-bell"&ndash;&gt;-->
<!--&lt;!&ndash;          >&ndash;&gt;-->
<!--&lt;!&ndash;            <a class="dropdown-item" href="#">Notification 1</a>&ndash;&gt;-->
<!--&lt;!&ndash;            <a class="dropdown-item" href="#">Notification 2</a>&ndash;&gt;-->
<!--&lt;!&ndash;            <a class="dropdown-item" href="#">Notification 3</a>&ndash;&gt;-->
<!--&lt;!&ndash;            <a class="dropdown-item" href="#">Notification 4</a>&ndash;&gt;-->
<!--&lt;!&ndash;            <a class="dropdown-item" href="#">Another notification</a>&ndash;&gt;-->
<!--&lt;!&ndash;          </drop-down>&ndash;&gt;-->
<!--          <li class="nav-item">-->
<!--            <a href="#" class="nav-link">-->
<!--              <i class="ti-settings"></i>-->
<!--              <p>Settings</p>-->
<!--            </a>-->
<!--          </li>-->
<!--        </ul>-->
<!--      </div>-->
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    },
  },
  data() {
    return {
      activeNotifications: false,
    };
  },
  methods: {
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    toggleNotificationDropDown() {
      this.activeNotifications = !this.activeNotifications;
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      console.log(this.$sidebar.showSidebar);
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
  },
};
</script>
