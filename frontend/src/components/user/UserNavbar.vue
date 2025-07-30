<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4 d-flex align-items-center"
  >
    <router-link class="navbar-brand fw-bold text-primary" to="/user/dashboard">
      Park<span class="text-dark">Us</span>
    </router-link>

    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarUser"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarUser">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link class="nav-link" to="/user/dashboard">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/user/summary">Summary</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/user/about">About</router-link>
        </li>
      </ul>

      <!-- Right Side Button -->
      <div class="d-flex align-items-center">
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {
  localStorage.clear();
  router.push("/");
};
</script>

<style scoped>
.navbar {
  border-radius: 0 0 10px 10px;
}
</style>
