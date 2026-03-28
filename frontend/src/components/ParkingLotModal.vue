<script>
export default {
  name: "ParkingLotModal",
  props: {
    show: Boolean,
    parkingLot: {
      type: Object,
      default: null,
    },
  },
  emits: ["submit", "close"],
  data() {
    return {
      formData: {
        name: "",
        address: "",
        totalSpots: 0,
        hourlyRate: 0,
        pincode: "",
      },
    };
  },
  computed: {
    isEditMode() {
      return !!this.parkingLot;
    },
  },
  watch: {
    parkingLot: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.formData = { ...newVal };
        } else {
          this.resetForm();
        }
      },
    },
  },
  methods: {
    submitForm() {
      this.$emit("submit", { ...this.formData });
    },
    resetForm() {
      this.formData = {
        name: "",
        address: "",
        totalSpots: 0,
        hourlyRate: 0,
        pincode: "",
      };
    },
  },
};
</script>

<template>
  <div
    class="modal fade show d-block"
    tabindex="-1"
    v-if="show"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content rounded-4">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ isEditMode ? "Edit Parking Lot" : "Add New Parking Lot" }}
          </h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input
                v-model="formData.name"
                type="text"
                class="form-control"
                required
                placeholder="Enter parking lot name"
              />
            </div>
            <div class="mb-3">
              <label class="form-label">Address</label>
              <input
                v-model="formData.address"
                type="text"
                class="form-control"
                required
                placeholder="Enter address"
              />
            </div>
            <div class="row">
              <div class="col mb-3">
                <label class="form-label">Total Spots</label>
                <input
                  v-model.number="formData.totalSpots"
                  type="number"
                  min="0"
                  class="form-control"
                  required
                />
              </div>
              <div class="col mb-3">
                <label class="form-label">Hourly Rate (Rs.)</label>
                <input
                  v-model.number="formData.hourlyRate"
                  type="number"
                  min="0"
                  class="form-control"
                  required
                />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Pincode</label>
                <input
                  v-model="formData.pincode"
                  type="text"
                  class="form-control"
                  placeholder="Enter pincode"
                  required
                />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline-secondary" @click="$emit('close')">
            Cancel
          </button>
          <button class="btn btn-primary" @click="submitForm">
            {{ isEditMode ? "Update" : "Add Parking Lot" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal {
  z-index: 1050;
}
</style>
