<script>
import axios from "axios";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";

dayjs.extend(utc);
dayjs.extend(timezone);

export default {
  name: "BookingHistory",
  data() {
    return {
      bookings: [],
      totalBookings: 0,
      totalHours: 0,
      totalSpent: 0,
    };
  },
  async mounted() {
    try {
      const res = await axios.get("/user/history");
      const data = res.data;

      let totalDuration = 0;
      let totalCost = 0;

      const completedBookings = data.filter((r) => r.start && r.end);

      this.bookings = completedBookings.map((r) => {  
        const checkin = dayjs(r.start).tz("Asia/Kolkata");
        const booking = dayjs(r.booking_time).tz("Asia/Kolkata");
        const checkout = dayjs(r.end).tz("Asia/Kolkata");

        const durationHours = Math.max(Math.round(checkout.diff(booking, 'hour', true)), 1);
        totalDuration += durationHours;
        totalCost += r.cost;

        return {
          lot: r.lot,
          slot: `#${r.spot_id}`,
          date: booking.format("MMM D, YYYY"),
          booking: booking.format("hh:mm A"),
          checkin: checkin.format("hh:mm A"),
          duration: `${durationHours}h`,
          amount: r.cost,
          checkout: checkout.format("MMM D, hh:mm A"),
        };
      });

      this.totalBookings = this.bookings.length;
      this.totalHours = totalDuration;
      this.totalSpent = totalCost.toFixed(2);
    } catch (err) {
      console.error("Error fetching booking history:", err);
    }
  },
  methods: {
    async triggerCSVExport() {
      try {
        const res = await axios.post("/user/export-csv");
        alert(res.data.message);
      } catch (e) {
        alert("Something went wrong.");
      }
    }
  }
};
</script>

<template>
  <div class="bg-light">
    <div class="container py-4 booking-history">
      <!-- Header -->
       <div class="d-flex justify-content-between align-items-center">
        <div class="mb-4">
          <h2 class="fw-bold">Booking History</h2>
          <p class="text-muted">View all your past parking reservations</p>
        </div>
        <button class="btn btn-primary m-4" @click="triggerCSVExport">
          Export Parking History
        </button>
       </div>
      
      <!-- Stats -->
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="card text-white bg-primary h-100 shadow-sm">
            <div
              class="card-body d-flex justify-content-between align-items-center"
            >
              <div>
                <p class="mb-0 fw-semibold">Total Bookings</p>
                <h4 class="fw-bold">{{ totalBookings }}</h4>
              </div>
              <i class="bi bi-car-front fs-2"></i>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div
            class="card text-white h-100 shadow-sm"
            style="background: linear-gradient(135deg, #10b981, #059669)"
          >
            <div
              class="card-body d-flex justify-content-between align-items-center"
            >
              <div>
                <p class="mb-0 fw-semibold">Total Hours</p>
                <h4 class="fw-bold">{{ totalHours }}</h4>
              </div>
              <i class="bi bi-clock-history fs-2"></i>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div
            class="card text-white h-100 shadow-sm"
            style="background: linear-gradient(135deg, #a855f7, #9333ea)"
          >
            <div
              class="card-body d-flex justify-content-between align-items-center"
            >
              <div>
                <p class="mb-0 fw-semibold">Total Spent</p>
                <h4 class="fw-bold">₹ {{ totalSpent }}</h4>
              </div>
              <i class="bi bi-currency-dollar fs-2"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Booking Cards -->
      <div
        v-for="(booking, index) in bookings"
        :key="index"
        class="card shadow-sm mb-4 p-3"
      >
        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center">
            <div class="bg-light rounded-circle p-3 me-3">
              <i class="bi bi-car-front fs-3 text-primary"></i>
            </div>
            <div>
              <h5 class="mb-1 fw-semibold">{{ booking.lot }}</h5>
              <small class="text-muted">Slot {{ booking.slot }}</small>
            </div>
          </div>
          <span class="badge bg-success px-3 py-2">Completed</span>
        </div>

        <hr />

        <div class="row text-center">
          <div class="col-md-3 mb-2">
            <div><i class="bi bi-calendar"></i> <strong>Date</strong></div>
            <div>{{ booking.date }}</div>
          </div>
          <div class="col-md-3 mb-2">
            <div><i class="bi bi-clock"></i> <strong>Booked-at</strong></div>
            <div>{{ booking.booking }}</div>
          </div>
          <div class="col-md-3 mb-2">
            <div><i class="bi bi-clock"></i> <strong>Check-in</strong></div>
            <div>{{ booking.checkin }}</div>
          </div>
          <div class="col-md-3 mb-2">
            <div>
              <i class="bi bi-hourglass-split"></i> <strong>Duration</strong>
            </div>
            <div>{{ booking.duration }}</div>
          </div>
          <div class="col-md-3 mb-2">
            <div><i class="bi bi-credit-card"></i> <strong>Amount</strong></div>
            <div>₹{{ booking.amount }}</div>
          </div>
        </div>

        <hr />
        <div class="d-flex justify-content-between text-muted small">
          <div>
            <i class="bi bi-geo-alt"></i> Check-out: {{ booking.checkout }}
          </div>
          <div>
            <i class="bi bi-check2-circle text-success"></i> Payment Completed
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@media (min-width: 992px) {
  .booking-history {
    max-width: 75%;
    margin: 0 auto;
  }
}
</style>
