<script>
export default {
  props: {
    icon: String,
    label: String,
    link: String,
  },
};
</script>

<template>
  <li class="nav-item">
    <router-link 
      :to="link"
      class="nav-link d-flex align-items-center mx-2 px-4 py-2 text-dark hover-bg"
      active-class="active-link"
    >
      <i :class="icon" class="me-2"></i>
      <span class="fs-5">{{ label }}</span>
    </router-link>
  </li>
</template>

<style scoped>
.hover-bg:hover {
  background-color: #f8f9fa;
  border-radius: 8px;
}

.active-link {
  color: #0d6efd !important;
  font-weight: 600;
  background-color: #e9f2ff;
  border-radius: 8px;
}
</style>
