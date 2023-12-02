import Sidebar from './SideBar.vue'
import SidebarLink from './SidebarLink'

const SidebarStore = {
  showSidebar: false,
  sidebarLinks: [
    { to: '/maps', name: 'maps', icon: 'ti-map', title: 'Maps' },
    { to: '/report-disaster', name: 'report-disaster', icon: 'ti-alert', title: 'Report Disaster' },
    { to: '/stats', name: 'stats', icon: 'ti-user', title: 'User Profile' },
    { to: '/table-list', name: 'table-list', icon: 'ti-view-list-alt', title: 'Table List' },
    { to: '/notifications', name: 'notifications', icon: 'ti-bell', title: 'Notifications' },
    // { to: '/dashboard', name: 'dashboard', icon: 'ti-panel', title: 'Dashboard' },
    // { to: '/icons', name: 'icons', icon: 'ti-pencil-alt2', title: 'Icons' },
    // { to: '/typography', name: 'typography', icon: 'ti-text', title: 'Typography' },
  ],
  displaySidebar(value) {
    this.showSidebar = value
  },
}

const SidebarPlugin = {
  install(app) {
    app.config.globalProperties.$sidebar = SidebarStore;
    app.component('side-bar', Sidebar);
    app.component('sidebar-link', SidebarLink);
  },
}

export default SidebarPlugin
