<script>
import SidebarLink from "./Sidebarlink.vue";
import axios from "axios";

export default {
  name: "Sidebar",
  props: {
    isMobile: Boolean,
    collapsed: Boolean,
    user: Object,
  },
  components: { SidebarLink },
  computed: {
    userInitials() {
      if (!this.user || !this.user.fullname) return "";
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
        await axios.post("/auth/logout", {}, { withCredentials: true });
        window.location.href = "/";
      } catch (err) {
        console.error("Logout failed", err);
      }
    },
  },
};
</script>

<template>
  <div
    class="sidebar bg-white border-end shadow-sm d-flex flex-column justify-content-between"
    :class="[
      { active: isMobile && !collapsed },
      { 'd-none d-md-block': isMobile && collapsed },
      { 'd-block': !isMobile },
    ]"
  >
    <div>
      <div
        class="d-flex justify-content-between align-items-center p-3 border-bottom"
        :class="[
          { 'd-none d-md-flex': isMobile && !collapsed },
          { 'd-flex': !isMobile },
        ]"
      >
        <div class="d-flex align-items-center">
          <i class="bi bi-car-front-fill text-primary fs-4 me-2"></i>
          <span class="fw-bold fs-5">ParkEase</span>
        </div>
      </div>

      <ul class="nav flex-column mt-3">
        <SidebarLink icon="bi bi-grid" label="Dashboard" link="/admin/dashboard" />
        <SidebarLink icon="bi bi-building" label="Parking Lots" link="/admin/parkinglot" />
        <SidebarLink icon="bi bi-geo-alt" label="Parking Spots" link="/admin/parkingspot" />
        <SidebarLink icon="bi bi-people" label="Users & Bookings" link="/admin/users" />
      </ul>
    </div>

    <div class="p-3 border-top">
      <div v-if="user" class="d-flex align-items-center mb-3">
        <div class="badge bg-primary text-white fs-6 p-2 rounded-circle me-2">
          {{ userInitials }}
        </div>
        <div class="fw-semibold">{{ user.fullname }}</div>
      </div>
      <button class="btn btn-outline-danger w-100" @click="logout">
        <i class="bi bi-box-arrow-right me-2"></i> Logout
      </button>
    </div>
  </div>
</template>


<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
}
@media (max-width: 768px) {
  .sidebar {
    transition: transform 0.3s ease-in-out;
    transform: translateX(-100%);
    height: 80vh;
  }
  .sidebar.active {
    transform: translateX(0);
  }
}
</style>
