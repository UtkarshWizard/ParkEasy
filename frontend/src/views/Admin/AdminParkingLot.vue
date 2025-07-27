<script>
import ParkingLotCard from "@/components/ParkingLotCard.vue";
import ParkingLotModal from "@/components/ParkingLotModal.vue";
import axios from "axios";

export default {
  components: {
    ParkingLotCard,
    ParkingLotModal,
  },
  data() {
    return {
      showModal: false,
      currentEditLot: null,
      parkingLots: [],
    };
  },
  computed: {
    totalLots() {
      return this.parkingLots.length;
    },
    totalSpots() {
      return this.parkingLots.reduce((sum, lot) => sum + lot.totalSpots, 0);
    },
    avgRate() {
      if (this.parkingLots.length === 0) return 0;
      const totalRate = this.parkingLots.reduce(
        (sum, lot) => sum + lot.hourlyRate,
        0
      );
      return (totalRate / this.parkingLots.length).toFixed(2);
    },
  },
  methods: {
    async fetchLots() {
      try {
        const res = await axios.get("/admin/lots");
        this.parkingLots = res.data.map((lot) => ({
          id: lot.id,
          name: lot.location_name,
          address: lot.address,
          hourlyRate: lot.price_per_hour,
          pincode: lot.pincode,
          occupied: lot.occupied_spots,
          totalSpots: lot.no_of_spots,
        }));
      } catch (err) {
        console.error("Error fetching lots:", err);
      }
    },
    openAddModal() {
      this.currentEditLot = null;
      this.showModal = true;
    },
    openEditModal(lot) {
      this.currentEditLot = lot;
      this.showModal = true;
    },
    async handleModalSubmit(data) {
      try {
        if (this.currentEditLot) {
          await axios.put(`/admin/lots/${this.currentEditLot.id}`, {
            location_name: data.name,
            address: data.address,
            price_per_hour: data.hourlyRate,
            pincode: data.pincode,
            no_of_spots: data.totalSpots
          });
        } else {
          await axios.post("/admin/lots", {
            location_name: data.name,
            address: data.address,
            price_per_hour: data.hourlyRate,
            pincode: data.pincode,
            no_of_spots: data.totalSpots,
          });
        }
        this.showModal = false;
        this.fetchLots();
      } catch (err) {
        console.error("Failed to submit:", err);
      }
    },
    async deleteLot(id) {
      if (!confirm("Are you sure you want to delete this lot?")) return;
      try {
        await axios.delete(`/admin/lots/${id}`);
        this.fetchLots();
      } catch (err) {
        console.error("Error deleting lot:", err);
      }
    },
  },
  mounted() {
    this.fetchLots();
  },
};
</script>

<template>
  <div class="container-fluid py-4 px-md-5 px-3">
    <div
      class="d-flex justify-content-between align-items-center flex-wrap mb-4"
    >
      <div>
        <h2 class="fw-bold">Parking Lots</h2>
        <p class="text-muted">Manage parking lot locations</p>
      </div>
      <button class="btn btn-primary mt-2 mt-md-0" @click="openAddModal">
        <i class="bi bi-plus-lg me-1"></i> Add Parking Lot
      </button>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-md-4">
        <div class="card text-center shadow-sm h-100">
          <div class="card-body">
            <i class="bi bi-grid-1x2-fill fs-3 text-primary mb-2"></i>
            <h5 class="fw-bold mb-0">{{ totalLots }}</h5>
            <small class="text-muted">Total Lots</small>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="card text-center shadow-sm h-100">
          <div class="card-body">
            <i class="bi bi-car-front fs-3 text-success mb-2"></i>
            <h5 class="fw-bold mb-0">{{ totalSpots }}</h5>
            <small class="text-muted">Total Spots</small>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="card text-center shadow-sm h-100">
          <div class="card-body">
            <i class="bi bi-currency-dollar fs-3 text-warning mb-2"></i>
            <h5 class="fw-bold mb-0">{{ avgRate }}</h5>
            <small class="text-muted">Avg. Hourly Rate</small>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <ParkingLotCard
        v-for="lot in parkingLots"
        :key="lot.id"
        :lot="lot"
        @edit="openEditModal"
        @delete="deleteLot"
      />
    </div>

    <ParkingLotModal
      :show="showModal"
      :parkingLot="currentEditLot"
      @close="showModal = false"
      @submit="handleModalSubmit"
    />
  </div>
</template>

<style scoped>
.card {
  border-radius: 12px;
}
</style>
