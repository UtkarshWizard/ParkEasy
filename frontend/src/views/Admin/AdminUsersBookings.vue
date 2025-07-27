<script>
import axios from "axios";

export default {
  data() {
    return {
      activeTab: "users",
      searchUser: "",
      searchBooking: "",
      filterStatus: "All Status",
      stats: [],
      users: [],
      bookings: [],
      userMap: {},
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter((user) =>
        user.name.toLowerCase().includes(this.searchUser.toLowerCase())
      );
    },
    filteredBookings() {
      return this.bookings.filter((booking) => {
        const matchesSearch = booking.user
          .toLowerCase()
          .includes(this.searchBooking.toLowerCase());
        const matchesStatus =
          this.filterStatus === "All Status" ||
          booking.status === this.filterStatus;
        return matchesSearch && matchesStatus;
      });
    },
  },
  methods: {
    async fetchUsers() {
      const res = await axios.get("/admin/users");
      this.users = res.data.map((u, idx) => {
        const userObj = {
          id: idx + 1,
          name: u.fullname,
          email: u.email,
          totalBookings: 0,
          activeBookings: u.active_reservations,
        };
        this.userMap[u.email] = userObj;
        return userObj;
      });
    },

    parseUTC(datetimeStr) {
      const isoLike = datetimeStr.replace(" ", "T").split(".")[0] + "Z";
      return new Date(isoLike);
    },

    async fetchBookings() {
      const res = await axios.get("/admin/reservations");

      const formatterDate = new Intl.DateTimeFormat("en-IN", {
        timeZone: "Asia/Kolkata",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      });

      const formatterTime = new Intl.DateTimeFormat("en-IN", {
        timeZone: "Asia/Kolkata",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });

      this.bookings = res.data.map((b) => {
        const user = this.findUserByIdOrEmail(b.user_id);
        const location = `${b.lot_name || "Lot"} - ${b.spot_number || "?"}`;

        const startUTC = this.parseUTC(b.parking_timestamp);
        const endUTC = b.leaving_timestamp
          ? this.parseUTC(b.leaving_timestamp)
          : null;

        const date = formatterDate.format(startUTC);
        const startTime = formatterTime.format(startUTC);
        const endTime = endUTC ? formatterTime.format(endUTC) : "Ongoing";

        const duration = this.calculateDuration(startUTC, endUTC);
        const status = endUTC ? "Completed" : "Active";

        if (user) user.totalBookings++;

        return {
          id: b.id,
          user: user?.name || "Unknown",
          email: user?.email || "",
          location,
          duration,
          amount: `₹${b.parking_cost.toFixed(2)}`,
          date,
          startTime,
          endTime,
          status,
        };
      });

      this.updateStats();
    },

    calculateDuration(start, end) {
      const diff = (end || new Date()) - start;

      if (diff <= 0) return "0m";

      const totalMinutes = Math.floor(diff / (1000 * 60));
      const hours = Math.floor(totalMinutes / 60);
      const minutes = totalMinutes % 60;

      if (hours > 0) {
        return `${hours}h ${minutes}m`;
      } else {
        return `${minutes}m`;
      }
    },
    findUserByIdOrEmail(userId) {
      return (
        this.users.find((u) => u.id === userId || u.email === userId) || null
      );
    },

    updateStats() {
      const totalUsers = this.users.length;
      const activeUsers = this.users.filter((u) => u.activeBookings > 0).length;
      const totalBookings = this.bookings.length;
      const activeBookings = this.bookings.filter(
        (b) => b.status === "Active"
      ).length;
      const totalRevenue = this.bookings.reduce(
        (sum, b) => sum + parseFloat(b.amount.replace(/[^\d.]/g, "")),
        0
      );

      this.stats = [
        { label: "Total Users", value: totalUsers, icon: "👤" },
        {
          label: "Active Users",
          value: activeUsers,
          icon: "✅",
          color: "text-success",
        },
        {
          label: "Total Bookings",
          value: totalBookings,
          icon: "📅",
          color: "text-primary",
        },
        {
          label: "Active Bookings",
          value: activeBookings,
          icon: "⏰",
          color: "text-warning",
        },
        {
          label: "Total Revenue",
          value: `₹ ${totalRevenue.toFixed(2)}`,
          icon: "💲",
          color: "text-success",
        },
      ];
    },
  },
  async mounted() {
    await this.fetchUsers();
    await this.fetchBookings();
  },
};
</script>

<template>
  <div class="container py-4 px-md-5 px-3">
    <h2 class="fw-bold">Users & Bookings</h2>
    <p class="text-muted mb-4">Manage users and their parking bookings</p>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-2" v-for="stat in stats" :key="stat.label">
        <div class="border rounded p-3 text-center">
          <div class="fw-bold fs-5" :class="stat.color">{{ stat.value }}</div>
          <div class="small text-muted">{{ stat.label }}</div>
          <div v-if="stat.icon" class="text-muted fs-4">{{ stat.icon }}</div>
        </div>
      </div>
    </div>

    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'users' }"
          @click="activeTab = 'users'"
        >
          Users ({{ users.length }})
        </button>
      </li>
      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'bookings' }"
          @click="activeTab = 'bookings'"
        >
          Bookings ({{ bookings.length }})
        </button>
      </li>
    </ul>

    <div v-if="activeTab === 'users'">
      <div class="row mb-3">
        <div class="col-md-4">
          <input
            type="text"
            class="form-control"
            placeholder="Search users..."
            v-model="searchUser"
          />
        </div>
      </div>

      <div class="row">
        <div
          class="col-md-6 col-lg-4 mb-4"
          v-for="user in filteredUsers"
          :key="user.email"
        >
          <div class="border rounded p-3 bg-white">
            <div class="d-flex align-items-center mb-2">
              <div
                class="bg-primary text-white rounded-circle p-3 me-2 text-uppercase"
              >
                {{ user.name[0] }}
              </div>
              <div>
                <h6 class="mb-0 fw-bold">{{ user.name }}</h6>
                <small class="text-muted">{{ user.email }}</small>
              </div>
            </div>
            <div class="small">
              <div>
                <i class="bi bi-calendar me-1"></i
                >{{ user.totalBookings }} total bookings
              </div>
              <div>
                <i class="bi bi-check-circle me-1 text-success"></i
                >{{ user.activeBookings }} active
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bookings Tab -->
    <div v-else>
      <div class="row mb-3">
        <div class="col-md-4">
          <input
            type="text"
            class="form-control"
            placeholder="Search bookings..."
            v-model="searchBooking"
          />
        </div>
        <div class="col-md-3">
          <select class="form-select" v-model="filterStatus">
            <option>All Status</option>
            <option>Active</option>
            <option>Completed</option>
          </select>
        </div>
      </div>

      <div class="list-group">
        <div
          class="list-group-item"
          v-for="booking in filteredBookings"
          :key="booking.id"
        >
          <div class="d-flex justify-content-between">
            <div>
              <div class="fw-bold">
                {{ booking.user }}
                <span
                  class="badge bg-success ms-2"
                  v-if="booking.status === 'Active'"
                  >✔ Active</span
                >
              </div>
              <div class="small text-muted">
                <i class="bi bi-envelope me-1"></i>{{ booking.email }}<br />
                <i class="bi bi-geo me-1"></i>{{ booking.location }}<br />
                <i class="bi bi-clock me-1"></i>{{ booking.duration }}<br />
                <i class="bi bi-currency-dollar me-1"></i>{{ booking.amount }}
              </div>
            </div>
            <div class="text-end">
              <div class="fw-bold">{{ booking.date }}</div>
              <div class="small">
                {{ booking.startTime }} - {{ booking.endTime }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.nav-tabs .nav-link.active {
  font-weight: bold;
  color: #0d6efd;
}
</style>
