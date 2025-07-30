<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4 d-flex align-items-center"
  >
    <router-link
      class="navbar-brand fw-bold text-primary"
      to="/admin/dashboard"
    >
      Park<span class="text-dark">Us</span>
    </router-link>

    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div
      class="collapse navbar-collapse d-flex justify-content-center"
      id="navbarNav"
    >
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <router-link to="/admin/dashboard" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin/lots" class="nav-link">Lots</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin/users" class="nav-link">Users</router-link>
        </li>
        <li class="nav-item">
          <button
            class="btn btn-outline-danger btn-sm ms-3"
            @click="logoutUser"
          >
            Logout
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { logout } from "../../utils/auth";

const router = useRouter();

const logoutUser = () => {
  logout();
  router.push("/login");
};
</script>

<style scoped>
.nav-link {
  font-weight: 500;
}
.navbar-brand {
  font-size: 1.5rem;
}
</style>
