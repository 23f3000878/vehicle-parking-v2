<template>
  <div
    class="register-wrapper d-flex align-items-center justify-content-center min-vh-100 bg-light"
  >
    <div
      class="register-card card shadow-lg border-0 p-4"
      style="width: 100%; max-width: 500px"
    >
      <div class="card-body">
        <h3 class="text-center mb-4 fw-bold text-success">Create an Account</h3>
        <p class="text-center text-muted mb-4">
          Join ParkIt Smart — your parking assistant
        </p>

        <form @submit.prevent="handleRegister">
          <div class="form-floating mb-3">
            <input
              v-model="fullname"
              type="text"
              class="form-control"
              id="fullname"
              placeholder="Full Name"
              required
            />
            <label for="fullname">Full Name</label>
          </div>

          <div class="form-floating mb-3">
            <input
              v-model="email"
              type="email"
              class="form-control"
              id="email"
              placeholder="Email"
              required
            />
            <label for="email">Email Address</label>
          </div>

          <div class="form-floating mb-3">
            <input
              v-model="address"
              type="text"
              class="form-control"
              id="address"
              placeholder="Address (optional)"
            />
            <label for="address">Address (optional)</label>
          </div>

          <div class="form-floating mb-3">
            <input
              v-model="password"
              type="password"
              class="form-control"
              id="password"
              placeholder="Password"
              required
            />
            <label for="password">Password</label>
          </div>

          <div v-if="error" class="alert alert-danger py-2 small">
            {{ error }}
          </div>
          <div v-if="success" class="alert alert-success py-2 small">
            {{ success }}
          </div>

          <button
            type="submit"
            class="btn btn-success w-100"
            :disabled="loading"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            Register
          </button>
        </form>

        <p class="text-center text-muted mt-3 small">
          Already have an account?
          <router-link to="/login">Login</router-link>
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

const fullname = ref("");
const email = ref("");
const address = ref("");
const password = ref("");

const error = ref("");
const success = ref("");
const loading = ref(false);

const router = useRouter();

const handleRegister = async () => {
  error.value = "";
  success.value = "";
  loading.value = true;

  try {
    const res = await axios.post("/auth/register", {
      fullname: fullname.value,
      email: email.value,
      address: address.value || null,
      password: password.value,
    });

    const token = res.data.access_token;
    setToken(token);

    let user = await axios.get("/user/me");
    user = user.data;
    setUser(user);

    // Redirect based on role
    if (user.role === "admin") router.push("/admin/dashboard");
    else router.push("/user/dashboard");
  } catch (err) {
    error.value = err?.response?.data?.msg || "Registration failed";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-wrapper {
  background: linear-gradient(to right, #f8f9fa, #e9ecef);
}
.card-body {
  padding: 1.75rem !important;
}
.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(25, 135, 84, 0.25);
}
</style>
