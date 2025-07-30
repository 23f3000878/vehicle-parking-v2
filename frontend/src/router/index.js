import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import UserDashboard from "../views/user/UserDashboard.vue";
import AdminDashboard from "../views/admin/AdminDashboard.vue";
import { getToken, getUser } from "../utils/auth";
import AdminLots from "../views/admin/AdminLots.vue";
import AdminUsers from "../views/admin/AdminUsers.vue";
import UserAbout from "../views/user/UserAbout.vue";
import UserSummary from "../views/user/UserSummary.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/user/dashboard",
    component: UserDashboard,
    meta: { requiresAuth: true, role: "user" },
  },
  {
    path: "/user/summary",
    component: UserSummary,
    meta: { requiresAuth: true, role: "user" },
  },
  {
    path: "/user/about",
    component: UserAbout,
    meta: { requiresAuth: true, role: "user" },
  },
  {
    path: "/admin/dashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/lots",
    component: AdminLots,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/users",
    component: AdminUsers,
    meta: { requiresAuth: true, role: "admin" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = getToken();
  const user = getUser();

  if (to.meta.requiresAuth && !token) {
    return next("/login");
  }

  if (to.meta.adminOnly && user?.role !== "admin") {
    return next("/user");
  }

  next();
});

export default router;
