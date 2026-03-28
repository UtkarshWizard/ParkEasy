<script>
export default {
  props: ["lot"],
  computed: {
    occupancyPercent() {
      return Math.round((this.lot.occupied / this.lot.totalSpots) * 100);
    },
    availableSpots() {
      return this.lot.totalSpots - this.lot.occupied;
    },
  },
  methods: {
    editLot() {
      this.$emit("edit", this.lot);
    },
    deleteLot() {
      this.$emit("delete", this.lot.id);
    },
  },
};
</script>

<template>
  <div class="col-12 col-md-6 col-lg-4">
    <div class="card h-100 shadow-sm">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <div>
            <h5 class="fw-bold">{{ lot.name }}</h5>
            <div class="text-muted small mb-2">
              <i class="bi bi-geo-alt me-1"></i>{{ lot.address }}
            </div>
          </div>
          <div class="d-flex gap-2">
            <i class="bi bi-pencil-square cursor-pointer" @click="editLot"></i>
            <i class="bi bi-trash text-danger cursor-pointer" @click="deleteLot"></i>
          </div>
        </div>

        <div
          class="badge mb-2 bg-success text-light"
        >
          {{ lot.pincode }}
        </div>

        <div class="text-end text-muted small mb-2">₹{{ lot.hourlyRate }}/hour</div>

        <div>
          <div class="fw-semibold small mb-1">Occupancy</div>
          <div class="progress mb-1" style="height: 8px">
            <div
              class="progress-bar"
              role="progressbar"
              :style="{ width: occupancyPercent + '%' }"
              aria-valuemin="0"
              aria-valuemax="100"
            ></div>
          </div>
          <div class="text-muted small">
            {{ availableSpots }} spots available • {{ occupancyPercent }}%
            occupied
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
