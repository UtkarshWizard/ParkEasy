<script>
import axios from "axios";
import StatCard from "@/components/StatCard.vue";

export default {
  components: { StatCard },
  data() {
    return {
      lots: [],
      users: [],
      reservations: [],
      statCards: [],
      totalSpots: 0,
      occupiedSpots: 0,
      totalUsers: 0,
      totalRevenue: 0,
      activeBookings: 0,
    };
  },
  computed: {
    occupancyRate() {
      return this.totalSpots === 0
        ? "0.0"
        : ((this.occupiedSpots / this.totalSpots) * 100).toFixed(1);
    },
    avgOccupancy() {
      return this.occupancyRate + "%";
    },
  },
  async mounted() {
    await Promise.all([
      this.fetchLots(),
      this.fetchUsers(),
      this.fetchReservations(),
    ]);
    this.setupStatCards();
  },
  methods: {
    async fetchLots() {
      try {
        const res = await axios.get("/admin/lots");
        this.lots = res.data;

        this.totalSpots = this.lots.reduce(
          (sum, lot) => sum + lot.no_of_spots,
          0
        );
        this.occupiedSpots = this.lots.reduce(
          (sum, lot) => sum + lot.occupied_spots,
          0
        );
      } catch (err) {
        console.error("Error fetching lots", err);
      }
    },

    async fetchUsers() {
      try {
        const res = await axios.get("/admin/users");
        this.users = res.data;
        this.totalUsers = this.users.length;
      } catch (err) {
        console.error("Error fetching users", err);
      }
    },

    async fetchReservations() {
      try {
        const res = await axios.get("/admin/reservations");
        this.reservations = res.data.map((r) => ({
          ...r,
          status: r.leaving_timestamp ? "Completed" : "Active",
        }));

        this.totalRevenue = this.reservations.reduce(
          (sum, r) => sum + r.parking_cost,
          0
        );
        this.activeBookings = this.reservations.filter(
          (r) => r.status === "Active"
        ).length;
      } catch (err) {
        console.error("Error fetching reservations", err);
      }
    },
    setupStatCards() {
      this.statCards = [
        {
          title: "Total Parking Lots",
          value: String(this.lots.length),
          icon: "bi bi-building",
          color: "primary",
        },
        {
          title: "Total Spots",
          value: String(this.totalSpots),
          icon: "bi bi-geo-alt",
          color: "success",
        },
        {
          title: "Total Users",
          value: String(this.totalUsers),
          icon: "bi bi-people",
          color: "purple",
        },
        {
          title: "Total Revenue",
          value: `₹ ${this.totalRevenue.toFixed(2)}`,
          icon: "bi bi-currency-dollar",
          color: "orange",
        },
      ];
    },
    timeAgo(utcTime) {
      const utcDate = new Date(utcTime);

      // Convert UTC to IST (UTC+5:30)
      const istOffsetMs = 5.5 * 60 * 60 * 1000;
      const istDate = new Date(utcDate.getTime() + istOffsetMs);

      const now = new Date(); // local browser time (assumed IST for Indian users)
      const diffSec = Math.floor((now - istDate) / 1000);

      if (diffSec < 60) return `${diffSec} sec ago`;
      if (diffSec < 3600) return `${Math.floor(diffSec / 60)} min ago`;
      if (diffSec < 86400) return `${Math.floor(diffSec / 3600)} hr ago`;

      const days = Math.floor(diffSec / 86400);
      return `${days} day${days > 1 ? "s" : ""} ago`;
    },
  },
};
</script>

<template>
  <div class="container-fluid py-4 px-md-5 px-3">
    <h2 class="fw-bold mb-1">Dashboard</h2>
    <p class="text-muted">Monitor parking management system performance</p>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4 mb-4">
      <div class="col" v-for="card in statCards" :key="card.title">
        <StatCard :title="card.title" :value="card.value">
          <template #icon>
            <div
              :class="`p-2 rounded bg-${card.color}`"
              style="width: 40px; height: 40px"
            >
              <i :class="card.icon" class="text-white fs-5"></i>
            </div>
          </template>
        </StatCard>
      </div>
    </div>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4 mb-4">
      <div class="col">
        <div class="card h-100 shadow-sm p-3">
          <h6>Occupied Spots</h6>
          <h4 class="fw-bold">
            {{ occupiedSpots }}
            <small class="text-muted">of {{ totalSpots }}</small>
          </h4>
          <div class="progress mt-2" style="height: 8px">
            <div
              class="progress-bar bg-danger"
              :style="{ width: occupancyRate + '%' }"
            ></div>
          </div>
          <small class="text-muted">{{ occupancyRate }}%</small>
        </div>
      </div>
      <div class="col">
        <StatCard title="Active Bookings" :value="String(activeBookings)">
          <template #icon>
            <div
              class="p-2 rounded bg-warning"
              style="width: 40px; height: 40px"
            >
              <i class="bi bi-activity text-white fs-5"></i>
            </div>
          </template>
        </StatCard>
      </div>
      <div class="col">
        <StatCard title="Average Occupancy" :value="avgOccupancy">
          <template #icon>
            <div class="p-2 rounded bg-teal" style="width: 40px; height: 40px">
              <i class="bi bi-graph-up-arrow text-white fs-5"></i>
            </div>
          </template>
        </StatCard>
      </div>
    </div>

    <div class="card shadow-sm p-3">
      <h5 class="fw-bold mb-3">Recent Activity</h5>
      <div
        v-for="r in reservations.slice(0, 10)"
        :key="r.id"
        class="d-flex justify-content-between align-items-center border-top pt-3"
      >
        <div>
          <span
            :class="{
              'text-success fw-semibold': r.status === 'Active',
              'text-muted fw-semibold': r.status === 'Completed',
            }"
          >
            Booking {{ r.status === "Active" ? "started" : "completed" }}
          </span>
          <div class="text-muted small">
            {{ r.lot_name || "Lot" }} - Spot {{ r.spot_number }}
          </div>
        </div>
        <div class="text-muted small">{{ timeAgo(r.booking_timestamp) }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bg-purple {
  background-color: #6f42c1;
}
.bg-orange {
  background-color: #fd7e14;
}
.bg-teal {
  background-color: #20c997;
}
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from {
  transform: translateX(-100%);
}
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
