<!-- src/views/Home.vue -->
<template>
  <div
    class="hero-container d-flex flex-column min-vh-100 justify-content-between"
  >
    <!-- Navbar -->
    <header class="bg-white shadow-sm py-3">
      <div class="container d-flex justify-content-between align-items-center">
        <h2>
          <router-link class="navbar-brand fw-bold text-primary" to="/">
            Park<span class="text-dark">Us</span>
          </router-link>
        </h2>
        <div>
          <router-link to="/login" class="btn btn-outline-dark me-2"
            >Login</router-link
          >
          <router-link to="/register" class="btn btn-dark"
            >Register</router-link
          >
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <main
      class="container text-center text-light d-flex flex-column align-items-center justify-content-center flex-grow-1"
    >
      <div class="glass p-4 rounded shadow">
        <img
          src="/assets/parking-icon.png"
          alt="Parking Icon"
          class="mb-4 icon"
        />
        <h1 class="display-5 fw-semibold">
          Find, Book, Park — <span class="gold">Hassle Free!</span>
        </h1>
        <p class="lead text-light mb-4">
          A smarter vehicle parking system for effortless reservation and
          realtime stats.
        </p>
        <router-link to="/login" class="btn btn-primary btn-lg me-3"
          >Get Started</router-link
        >
        <router-link to="/register" class="btn btn-outline-light btn-lg"
          >Create Account</router-link
        >
      </div>
    </main>

    <!-- Footer -->
    <footer class="text-center text-white-50 py-3 small">
      &copy; 2025 ParkIt Smart — All rights reserved.
    </footer>
  </div>
</template>

<script setup>
// No logic needed yet
</script>

<style scoped>
.hero-container {
  background: url("/assets/bg-parking.jpeg") center center / cover no-repeat;
  backdrop-filter: blur(1px);
  position: relative;
}
.gold {
  color: rgb(255, 196, 0);
}

.glass {
  background-color: rgba(0, 0, 0, 0.85);
  max-width: 700px;
}

.icon {
  width: 100px;
  filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.4));
}
</style>
