<script>
import SpotCard from "./SpotCard.vue";

export default {
  name: "LotCard",
  components: { SpotCard },
  props: {
    lot: {
      type: Object,
      required: true,
    },
  },
};
</script>

<template>
  <div class="card mb-4 shadow-sm">
    <div class="card-header fw-bold">
      {{ lot.name }}
      <span class="text-muted small">({{ lot.spots.length }} spots)</span>
    </div>
    <div class="card-body">
      <div class="d-flex flex-wrap">
        <SpotCard v-for="spot in lot.spots" :key="spot.number" :spot="spot" />
      </div>
    </div>
  </div>
</template>


