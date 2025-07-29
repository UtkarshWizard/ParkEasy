<script>
import axios from 'axios';

export default {
  name: "UserNavbar",
  props: {
    user: Object
  },
  computed: {
    userInitials() {
      if (!this.user || !this.user.fullname) return "V";
      console.log(this.user)
      return this.user.fullname
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase();
    },
  },
  methods: {
    async logout() {
     try {
      await axios.post("/auth/logout");
      window.location.href = "/signin";
     } catch (err) {
      console.error("Logout failed", err);
     }
    },
  },
};
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3">
    <div class="container">
      <!-- Brand -->
      <router-link to="/" class="navbar-brand d-flex align-items-center gap-2 fw-bold fs-4">
        <i class="bi bi-car-front text-primary fs-3"></i> ParkEasy
      </router-link>

      <!-- Toggle Button -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Collapsible Section -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav gap-3 align-items-center">
          <li class="nav-item">
            <router-link to="/user/dashboard" class="nav-link" active-class="active">
              <i class="bi bi-speedometer2 me-1"></i> Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/currentbooking" class="nav-link" active-class="active">
              <i class="bi bi-calendar-check me-1"></i> Current Booking
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/bookinghistory" class="nav-link" active-class="active">
              <i class="bi bi-clock-history me-1"></i> History
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/analytics" class="nav-link" active-class="active">
              <i class="bi bi-clock-history me-1"></i> Analytics
            </router-link>
          </li>

          <!-- User Avatar -->
          <li class="nav-item">
            <div class="rounded-circle bg-primary text-white d-flex justify-content-center align-items-center" style="width: 36px; height: 36px;">
              {{ userInitials }}
            </div>
          </li>

          <!-- Logout -->
          <li class="nav-item">
            <button @click="logout" class="btn btn-outline-danger btn-sm ms-2">
              <i class="bi bi-box-arrow-right me-1"></i> Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav-link {
  font-weight: 500;
  transition: all 0.2s ease-in-out;
}

.nav-link:hover,
.nav-link.active {
  color: #0d6efd;
}
</style>
