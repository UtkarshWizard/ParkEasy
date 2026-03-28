<script>
export default {
  props: {
    title: String,
    value: String,
  }
}
</script>

<template>
  <div class="card h-100 shadow-sm">
    <div class="card-body d-flex align-items-center">
      <div class="me-3">
        <slot name="icon" />
      </div>
      <div>
        <h5 class="mb-1">{{ title }}</h5>
        <h4 class="fw-bold">{{ value }}</h4>
      </div>
    </div>
  </div>
</template>

