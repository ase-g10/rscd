<template>
  <div class="wrapper">
    <side-bar>
      <template v-slot:links>
        <!-- 以下链接的 name 属性与路由配置中的 name 属性相匹配 -->
        <sidebar-link to="/maps" name="maps" icon="ti-map" />
        <sidebar-link
          to="/report-disaster"
          name="report-disaster"
          icon="ti-alert"
        />
        <!-- 如果有 dashboard 路由，取消以下注释
        <sidebar-link to="/dashboard" name="dashboard" icon="ti-panel" /> 
        -->
        <sidebar-link to="/stats" name="stats" icon="ti-user" />
        <sidebar-link
          to="/table-list"
          name="table-list"
          icon="ti-view-list-alt"
        />
        <!-- 如果有 typography 路由，取消以下注释
        <sidebar-link to="/typography" name="typography" icon="ti-text" />
        -->
        <!-- 如果有 icons 路由，取消以下注释
        <sidebar-link to="/icons" name="icons" icon="ti-pencil-alt2" />
        -->
        <sidebar-link to="/notifications" name="notifications" icon="ti-bell" />
      </template>
      <mobile-menu>
        <li class="nav-item">
          <a class="nav-link">
            <i class="ti-panel"></i>
            <p>Stats</p>
          </a>
        </li>
        <drop-down
          class="nav-item"
          title="5 Notifications"
          title-classes="nav-link"
          icon="ti-bell"
        >
          <a class="dropdown-item">Notification 1</a>
          <a class="dropdown-item">Notification 2</a>
          <a class="dropdown-item">Notification 3</a>
          <a class="dropdown-item">Notification 4</a>
          <a class="dropdown-item">Another notification</a>
        </drop-down>
        <li class="nav-item">
          <a class="nav-link">
            <i class="ti-settings"></i>
            <p>Settings</p>
          </a>
        </li>
        <li class="divider"></li>
      </mobile-menu>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click="toggleSidebar"> </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
    MobileMenu,
  },
  methods: {
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
  },
};
</script>
