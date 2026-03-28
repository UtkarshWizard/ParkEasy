<script>
import LotCard from "@/components/LotCard.vue";
import axios from "axios";

export default {
  components: { LotCard },
  data() {
    return {
      lots: [],
      stats: [],
      filters: {
        search: "",
        lot: "All Lots",
        status: "All Status",
        type: "All Types",
      },
    };
  },
  computed: {
    filteredLots() {
      return this.lots
        .map((lot) => {
          const filteredSpots = lot.spots.filter((spot) => {
            const matchesSearch = spot.number
              ?.toString()
              .includes(this.filters.search);
            const matchesStatus =
              this.filters.status === "All Status" ||
              spot.status === this.filters.status;
            const matchesType =
              this.filters.type === "All Types" ||
              spot.type === this.filters.type;
            return matchesSearch && matchesStatus && matchesType;
          });

          return {
            ...lot,
            spots: filteredSpots,
          };
        })
        .filter((lot) => {
          return (
            this.filters.lot === "All Lots" || lot.name === this.filters.lot
          );
        });
    },
    uniqueStatuses() {
      const statusSet = new Set();
      this.lots.forEach((lot) => {
        lot.spots.forEach((spot) => {
          if (spot.status) {
            statusSet.add(spot.status);
          }
        });
      });
      return Array.from(statusSet);
    },
  },
  async mounted() {
    try {
      const res = await axios.get("/admin/lots");
      const lots = res.data;

      const lotList = [];

      for (const lot of lots) {
        const spotsRes = await axios.get(`/admin/lots/${lot.id}/spots`);

        const spots = spotsRes.data.map((s, idx) => ({
          number: (idx + 1).toString().padStart(2, "0"),
          status: s.status,
          user: s.user ? s.user.fullname + " (" + s.user.email + ")" : null,
          startTime: s.start_time || null
        }));

        lotList.push({
          id: lot.id,
          name: lot.location_name,
          spots,
        });
      }
      this.lots = lotList;
      this.updateStats();
    } catch (err) {
      console.error("Failed to fetch lots/spots", err);
    }
  },
  methods: {
    updateStats() {
      let total = 0,
        available = 0,
        occupied = 0

      this.lots.forEach((lot) => {
        lot.spots.forEach((spot) => {
          total++;
          const status = spot.status.toLowerCase();
          if (status === "available") available++;
          else if (status === "occupied") occupied++;
        });
      });

      this.stats = [
        { label: "Total Spots", value: total },
        { label: "Available", value: available },
        { label: "Occupied", value: occupied },
      ];
    },
  },
};
</script>

<template>
  <div class="container-fluid py-4 px-md-5 px-3">
    <h2 class="fw-bold">Parking Spots</h2>
    <p class="text-muted mb-4">Monitor and manage individual parking spots</p>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-2" v-for="stat in stats" :key="stat.label">
        <div class="border rounded p-3 text-center">
          <div class="fw-bold fs-5">{{ stat.value }}</div>
          <div class="small text-muted">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search spots number..."
          v-model="filters.search"
        />
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="filters.lot">
          <option value="All Lots">All Lots</option>
          <option v-for="lot in lots" :key="lot.id" :value="lot.name">
            {{ lot.name }}
          </option>
        </select>
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="filters.status">
          <option value="All Status">All Status</option>
          <option
            v-for="status in uniqueStatuses"
            :key="status"
            :value="status"
          >
            {{ status }}
          </option>
        </select>
      </div>
    </div>

    <!-- Legend -->
    <div class="border rounded p-3 mb-4">
      <strong>Legend</strong>
      <div class="d-flex flex-wrap gap-3 mt-2">
        <span class="badge bg-success">Available</span>
        <span class="badge bg-secondary">Occupied</span>
      </div>
    </div>

    <div class="mb-3">
      <div class="row g-2">
        <div>
          <LotCard v-for="lot in filteredLots" :key="lot.id" :lot="lot" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.spot-card {
  border-radius: 0.5rem;
  padding: 0.75rem;
  text-align: center;
  color: white;
  font-weight: bold;
}
</style>
