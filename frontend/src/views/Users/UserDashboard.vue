<script>
import axios from 'axios';

export default {
  data() {
    return {
      stats: [
        { label: "Total Parking Lots", value: 0, color: "#007bff" },
        { label: "Available Slots", value: 0, color: "#28a745" },
        { label: "Total Capacity", value: 0, color: "#6f42c1" },
      ],
      searchQuery: "",
      sortKey: "name",
      lots: [],
    };
  },
  computed: {
    filteredLots() {
      let results = this.lots.filter(
        (lot) =>
          lot.address.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          lot.location_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      if (this.sortKey === "name") {
        results.sort((a, b) => a.location_name.localeCompare(b.location_name));
      } else if (this.sortKey === "price") {
        results.sort((a, b) => a.price_per_hour - b.price_per_hour);
      } else if (this.sortKey === "available") {
        results.sort((a, b) => b.available_spots - a.available_spots);
      }
      return results;
    },
  },
  async mounted() {
    await this.fetchlots()
  },
  methods: {
    async fetchlots() {
      try {
        const res = await axios.get('/user/lots');
        this.lots = res.data;

        const totalLots = this.lots.length;
        const totalAvailable = this.lots.reduce((sum, lot) => sum + lot.available_spots, 0);
        const totalCapacity = this.lots.reduce((sum, lot) => sum + (lot.total_spots || 0), 0);

        this.stats[0].value = totalLots;
        this.stats[1].value = totalAvailable;
        this.stats[2].value = totalCapacity;
      } catch (error) {
        console.error("Failed to fetch lots:", error);
      }
    },

    async bookspot(lotId) {
      try {
        const res = await axios.post(`/user/reserve/${lotId}`);

        alert(`✅ Spot reserved!\nSpot ID: ${res.data.spot_id}\nReservation ID: ${res.data.reservation_id}`);

        await this.fetchlots()

        this.$router.push("/user/currentbooking");
      } catch (err) {
        alert(err.response?.data?.error || "Booking failed");
      }
    }
  }
};
</script>

<template>
  <div class="bg-light">
    <div class="container py-4">
      <!-- Header -->
      <h2 class="fw-bold mb-4 text-left">Find Your Perfect Parking Spot</h2>
  
      <!-- Stats Cards -->
      <div class="row mb-4 g-3">
        <div class="col-md-4" v-for="(stat, i) in stats" :key="i">
          <div
            :class="`card text-white shadow h-100 animate__animated animate__fadeInUp animate__delay-${i}s`"
            :style="{ backgroundColor: stat.color }"
          >
            <div class="card-body text-center">
              <h4>{{ stat.label }}</h4>
              <h2 class="fw-bold">{{ stat.value }}</h2>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Search and Sort -->
      <div class="row mb-4 g-2 align-items-center">
        <div class="col-md-8">
          <input
            v-model="searchQuery"
            class="form-control"
            placeholder="Search by location name or address..."
          />
        </div>
        <div class="col-md-4">
          <select v-model="sortKey" class="form-select">
            <option value="name">Sort by Address</option>
            <option value="price">Sort by Price</option>
            <option value="available">Sort by Availability</option>
          </select>
        </div>
      </div>
  
      <!-- Parking Cards -->
      <div class="row g-4">
        <div class="col-md-4" v-for="(lot, index) in filteredLots" :key="index">
          <div class="card-hover bg-white shadow-sm h-100 animate__animated animate__fadeInUp ">
            <div class="card-body d-flex flex-column p-4">
              <div class="d-flex justify-content-between">
                <h5 class="fw-bold">{{ lot.address }}</h5>
                <span class="text-primary fw-bold"
                  >₹{{ lot.price_per_hour }}<small class="text-muted">/hr</small></span
                >
              </div>
              <div class="text-muted mb-2">
                <i class="bi bi-geo-alt"></i> {{ lot.location_name }}
              </div>
  
              <!-- Availability -->
              <div class="pt-4">
                <div class="d-flex justify-content-between align-items-center">
                  <div class="small fw-semibold">Availability</div>
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="badge badge-availability"
                      >{{ lot.available_spots }} / {{ lot.total_spots }} available</span
                    >
                  </div>
                </div>
  
                <div class="progress mt-3" style="height: 8px">
                  <div
                    class="progress-bar bg-warning"
                    :style="{ width: (lot.available_spots / lot.total_spots) * 100 + '%' }"
                  ></div>
                </div>
              </div>
  
              <button class="btn btn-primary mt-4 w-100" @click="bookspot(lot.id)">
                Book Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css";
@import "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css";

.card {
  border-radius: 8px;
  transition: transform 0.25s ease , box-shadow 0.25s ease;
}
.badge-availability {
  background-color: #d1fadf; 
  color: #065f46;
  font-weight: 500;
}
</style>
