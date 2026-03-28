<script>
export default {
  name: "SpotCard",
  props: {
    spot: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showTooltip: false,
    };
  },
  computed: {
    cardClass() {
      switch ((this.spot.status || "").toLowerCase()) {
        case "available":
          return "bg-success text-white";
        case "occupied":
          return "bg-secondary text-white";
        default:
          return "bg-light text-dark";
      }
    },
    iconClass() {
      return "bi bi-car-front";
    },

    formattedStartTime() {
      if (!this.spot.startTime) return null;

      // Parse the UTC ISO string
      const utcDate = new Date(this.spot.startTime);

      // Convert to IST (UTC + 5:30)
      const istOffsetMs = 5.5 * 60 * 60 * 1000;
      const istDate = new Date(utcDate.getTime() + istOffsetMs);

      // Format IST date as "28 Jul 2025, 05:31 PM"
      return istDate.toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    },
  },
};
</script>

<template>
  <div
    class="spot-card position-relative"
    :class="cardClass"
    @mouseenter="showTooltip = true"
    @mouseleave="showTooltip = false"
  >
    <i :class="iconClass" class="mb-1"></i>
    <span>{{ spot.number }}</span>

    <div v-if="showTooltip" class="tooltip-box shadow-lg text-white">
      <div class="fw-bold mb-1">{{ spot.number || "" }}</div>
      <div
        v-if="spot.status.toLowerCase() === 'occupied' && spot.user"
        class="small mt-1"
      >
        <i class="bi bi-person me-1"></i>{{ spot.user }}
      </div>
      <div
        v-if="spot.status.toLowerCase() === 'occupied' && formattedStartTime"
        class="small"
      >
        <i class="bi bi-calendar me-1"></i>{{ formattedStartTime }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.spot-card {
  width: 55px;
  height: 60px;
  font-size: 0.9rem;
  padding: 6px;
  border-radius: 8px;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}

.tooltip-box {
  position: absolute;
  top: -110px;
  left: 50%;
  transform: translateX(-50%);
  background: #212529;
  padding: 10px 12px;
  border-radius: 8px;
  min-width: 160px;
  z-index: 10;
  font-size: 0.75rem;
  pointer-events: none;
  transition: 0.2s ease-in-out;
}
</style>
