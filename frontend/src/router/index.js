import * as Vue from 'vue'
import * as VueRouter from 'vue-router'
import routes from './routes'

// configure router
const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes: routes,
  linkActiveClass: 'active',
})

export default router
