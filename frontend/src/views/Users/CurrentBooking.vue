<script>
import axios from "axios";

export default {
  name: "CurrentBooking",
  data() {
    return {
      reservation: null,
      isLoading: true,
      error: null,
      isOccupied: false,
    };
  },
  async mounted() {
    try {
      const res = await axios.get("/user/reservation/current");
      this.reservation = res.data;
      this.isOccupied = res.data.status === "Occupied";
    } catch (err) {
      this.error = err.response?.data?.error || "No current booking found.";
    } finally {
      this.isLoading = false;
    }
  },
  methods: {
    async toggleOccupancy() {
      try {
        if (!this.isOccupied) {
          // Mark as occupied
          await axios.post(`/user/occupy/${this.reservation.id}`);
          this.isOccupied = true;
          alert("✅ Spot marked as occupied.");
        } else {
          // Release and redirect
          await axios.post(`/user/release/${this.reservation.id}`);
          alert("✅ Spot released and booking completed.");
          this.reservation = null; // Clear reservation
          this.$router.push("/user/dashboard");
          return; // Stop further execution
        }

        // Only refresh if not releasing
        const res = await axios.get("/user/reservation/current");
        this.reservation = res.data;
        this.isOccupied = res.data.status === "Occupied";
      } catch (err) {
        alert(err.response?.data?.error || "Action failed.");
      }
    },

    formatTime(timestamp) {
      const dt = new Date(timestamp);
      return dt.toLocaleString({
        timeZone: "Asia/Kolkata",
        hour12: true,
      });
    },
    durationSince(start) {
      const diff = Date.now() - new Date(start).getTime();
      const mins = Math.floor(diff / 60000);
      const hrs = Math.floor(mins / 60);
      return `${hrs}h ${mins % 60}m`;
    },
  },
};
</script>

<template>
  <div class="bg-light">
    <div class="container py-4 mx-auto booking-wrapper">
      <div class="mb-4 text-left">
        <h2 class="fw-bold">Current Booking</h2>
        <p class="text-muted">Manage your active parking reservation</p>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center text-muted fs-5 py-5">
        Loading...
      </div>

      <!-- No Booking -->
      <div v-else-if="error" class="alert alert-warning text-center fs-5">
        {{ error }}
      </div>

      <!-- Reservation Card -->
      <div v-else class="mx-auto">
        <div class="card shadow-sm rounded-4 overflow-hidden">
          <div
            class="header-gradient text-white px-4 py-3 d-flex justify-content-between align-items-center"
          >
            <div>
              <h5 class="mb-0 fw-bold">{{ reservation.lot_name }}</h5>
              <small>{{ reservation.spot_number }}</small>
            </div>
            <span class="badge bg-light text-primary px-3 py-2 fw-semibold">
              {{ reservation.status }}
            </span>
          </div>

          <div class="card-body row px-4 py-3">
            <div class="col-md-6 border-end">
              <h6 class="fw-bold fs-5 text-muted mb-3">Booking Details</h6>
              <div class="mb-3 d-flex align-items-center">
                <i class="bi bi-car-front-fill me-2"></i>
                <div class="d-flex flex-column px-2 text-muted">
                  <strong class="me-1">Slot Number:</strong>
                  {{ reservation.spot_number }}
                </div>
              </div>
              <div class="mb-3 d-flex align-items-center">
                <i class="bi bi-clock me-2"></i>
                <div class="d-flex flex-column px-2 text-muted">
                  <strong class="me-1">Booking Time:</strong>
                  {{ formatTime(reservation.booking_time) }}
                </div>
              </div>
              <div class="mb-3 d-flex align-items-center">
                <i class="bi bi-hourglass-split me-2"></i>
                <div class="d-flex flex-column px-2 text-muted">
                  <strong class="me-1">Duration:</strong>
                  {{ durationSince(reservation.booking_time) }}
                </div>
              </div>
              <div class="mb-3 d-flex align-items-center">
                <i class="bi bi-credit-card me-2"></i>
                <div class="d-flex flex-column px-2 text-muted">
                  <strong class="me-1">Booking ID:</strong>
                  {{ reservation.id }}
                </div>
              </div>
            </div>

            <div class="col-md-6 ps-md-4 pt-4 pt-md-0">
              <h6 class="fw-bold fs-5 text-muted mb-3">Quick Actions</h6>
              <div
                class="alert custom-alert d-flex align-items-center"
                role="alert"
              >
                <i class="bi bi-info-circle-fill me-2 fs-5 text-blue-900"></i>
                <div>
                  <strong class="text-blue-900">Reservation Active</strong
                  ><br />
                  <span class="text-blue-700">
                    Your parking slot is reserved. Mark as occupied when you
                    arrive.
                  </span>
                </div>
              </div>
              <button
                :class="[
                  'btn w-100 mt-2',
                  isOccupied ? 'btn-danger' : 'custom-green-btn',
                ]"
                @click="toggleOccupancy"
              >
                <div class="p-2 fw-bold fs-6">
                  <i
                    :class="
                      isOccupied ? 'bi bi-x-circle' : 'bi bi-check-circle'
                    "
                    class="me-2"
                  ></i>
                  {{ isOccupied ? "Release Spot" : "Mark as Occupied" }}
                </div>
              </button>
            </div>
          </div>

          <div class="card-footer custom-yellow-footer mx-4 my-4 px-4 py-3">
            <h6 class="fw-semibold mb-2">Parking Tips</h6>
            <ul class="mb-0 ps-3">
              <li>Remember to mark your slot as occupied when you arrive</li>
              <li>Keep your booking ID handy for any assistance</li>
              <li>Release the slot when leaving to avoid extra charges</li>
              <li>Minimum booking time is 1 hour.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.booking-wrapper {
  width: 100%;
}

@media (min-width: 992px) {
  .booking-wrapper {
    max-width: 60%;
  }
}

.header-gradient {
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
}

.custom-yellow-footer {
  background-color: #fefce8 !important;
  color: #333;
  border-radius: 0.5rem;
}

.custom-green-btn {
  background-color: #16a34a !important;
  color: white !important;
  font-weight: 600;
  border: none;
}

.custom-alert {
  background-color: #eff6ff;
  color: #1e3a8a;
  border: none;
  font-size: 0.95rem;
}

.text-blue-900 {
  color: #1e3a8a;
}

.text-blue-700 {
  color: #1d4ed8;
}
</style>
