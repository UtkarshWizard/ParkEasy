<script>
export default {
  name: "Header",
  methods: {
    toggleMenu() {},
  },
};
</script>

<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top"
  >
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="#">
        <div class="bg-gradient p-2 rounded me-2">
          <i class="fas fa-car text-white"></i>
        </div>
        <span class="fw-bold gradient-text fs-4">ParkEase</span>
      </a>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        @click="toggleMenu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto me-4">
          <li class="nav-item">
            <a class="nav-link fw-medium" href="#features">Features</a>
          </li>
          <li class="nav-item">
            <a class="nav-link fw-medium" href="#how-it-works">How it Works</a>
          </li>
          <li class="nav-item">
            <a class="nav-link fw-medium" href="#pricing">Pricing</a>
          </li>
        </ul>
        <router-link
          to="/signin"
          class="btn btn-gradient px-4 py-2 rounded-pill fw-medium"
        >
          Get Started
        </router-link>
      </div>
    </div>
  </nav>
</template>

<style>
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.btn-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
  color: white;
}
</style>
