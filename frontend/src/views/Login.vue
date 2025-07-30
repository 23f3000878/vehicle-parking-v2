<template>
  <div
    class="login-wrapper d-flex align-items-center justify-content-center min-vh-100 bg-light"
  >
    <div
      class="login-card card shadow-lg border-0 p-4"
      style="width: 100%; max-width: 420px"
    >
      <div class="card-body">
        <h3 class="text-center mb-4 fw-bold text-primary">Welcome Back</h3>
        <p class="text-center text-muted mb-4">
          Login to your account to continue
        </p>

        <form @submit.prevent="handleLogin">
          <div class="form-floating mb-3">
            <input
              v-model="email"
              type="email"
              class="form-control"
              id="email"
              placeholder="Enter email"
              required
            />
            <label for="email">Email address</label>
          </div>

          <div class="form-floating mb-3">
            <input
              v-model="password"
              type="password"
              class="form-control"
              id="password"
              placeholder="Enter password"
              required
            />
            <label for="password">Password</label>
          </div>

          <div v-if="error" class="alert alert-danger py-2 small">
            {{ error }}
          </div>

          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="loading"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            Login
          </button>
        </form>

        <p class="text-center text-muted mt-3 small">
          Don't have an account?
          <router-link to="/register">Register</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { setToken, setUser } from "../utils/auth";
import axios from "../services/axios";

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const router = useRouter();

const handleLogin = async () => {
  error.value = "";
  loading.value = true;
  try {
    const res = await axios.post("/auth/login", {
      email: email.value,
      password: password.value,
    });

    const token = res.data.access_token;
    setToken(token);

    let user = await axios.get("/user/me");
    user = user.data;
    setUser(user);

    if (user.role === "admin") router.push("/admin/dashboard");
    else router.push("/user/dashboard");
  } catch (err) {
    console.log(err);
    error.value = "Invalid email or password.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-wrapper {
  background: linear-gradient(to right, #f0f2f5, #e6eaf0);
}
.card-body {
  padding: 1.75rem !important;
}
.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}
</style>
