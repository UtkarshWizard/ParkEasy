<script>
import Sidebar from "@/components/Sidebar.vue";
import axios from "axios";

export default {
  components: { Sidebar },
  data() {
    return {
      isSidebarCollapsed: false,
      isMobile: false,
      user: null,
    };
  },
  created() {
    this.checkMobile();
  },
  async mounted() {
    window.addEventListener("resize", this.checkMobile);

    try {
      const res = await axios.get("/auth/check", { withCredentials: true });
      if (res.data.authenticated) {
        this.user = {
          fullname: res.data.fullname,
          email: res.data.email,
          role: res.data.role,
        };
      }
    } catch (err) {
      console.error("Failed to fetch user info", err);
    }
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth < 768;
      this.isSidebarCollapsed = this.isMobile;
    },
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
  },
};
</script>

<template>
  <div
    class="d-md-none bg-white px-3 py-2 border-bottom d-flex align-items-center w-100"
    style="z-index: 1040; position: sticky; top: 0"
  >
    <button class="btn btn-outline-secondary me-2" @click="toggleSidebar">
      <i class="bi bi-list fs-4"></i>
    </button>
    <div class="d-flex align-items-center p-3">
      <i class="bi bi-car-front-fill text-primary fs-4 me-2"></i>
      <span class="fw-bold fs-5">ParkEase</span>
    </div>
  </div>

  <transition name="slide">
    <Sidebar
      v-if="!isSidebarCollapsed || !isMobile"
      :collapsed="isSidebarCollapsed"
      :isMobile="isMobile"
      :user="user"
      class="position-fixed"
      style="z-index: 1040"
    />
  </transition>
  <div
    class="flex-grow-1"
    :class="{ 'pt-5': isMobile }"
    :style="{ marginLeft: isMobile ? '0px' : '250px' }"
  >
    <router-view />
  </div>
</template>

<style scoped>
.ms-250 {
  margin-left: 250px;
}
</style>
