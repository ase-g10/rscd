import * as VueRouter from "vue-router";
import routes from "./routes";

// configure router
const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes: routes,
  linkActiveClass: "active",
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token');
  const isPrivateRoute = to.matched.some(record => record.meta.requiresAuth);
  const isGuestOnlyRoute = to.matched.some(record => record.meta.guestOnly);

  if (isPrivateRoute && !isLoggedIn) {
    // 如果是需要认证的路由且用户未登录，重定向到登录页
    next({ name: 'login' });
  } else if (isGuestOnlyRoute && isLoggedIn) {
    next({ name: 'stats' });
  }else {
    // 否则正常导航
    next();
  }

});

export default router;
