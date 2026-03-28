<template>
  <footer class="bg-dark text-white py-5">
    <div class="container">
      <div class="row g-4">
        <div class="col-lg-6">
          <div class="d-flex align-items-center mb-4">
            <div class="bg-gradient p-2 rounded me-3">
              <i class="fas fa-car text-white"></i>
            </div>
            <span class="fs-3 fw-bold">ParkSmart</span>
          </div>
          <p class="text-light mb-4 fs-5">
            The smartest way to find, book, and pay for parking. Join thousands of happy parkers saving time and money every day.
          </p>
          <div class="d-flex gap-3">
            <a href="#" class="btn btn-outline-light btn-sm rounded-circle">
              <i class="fab fa-facebook-f"></i>
            </a>
            <a href="#" class="btn btn-outline-light btn-sm rounded-circle">
              <i class="fab fa-twitter"></i>
            </a>
            <a href="#" class="btn btn-outline-light btn-sm rounded-circle">
              <i class="fab fa-instagram"></i>
            </a>
            <a href="#" class="btn btn-outline-light btn-sm rounded-circle">
              <i class="fab fa-linkedin-in"></i>
            </a>
          </div>
        </div>
        
        <div class="col-lg-3 col-md-6">
          <h5 class="fw-bold mb-4">Product</h5>
          <ul class="list-unstyled">
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">Features</a></li>
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">How it Works</a></li>
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">Pricing</a></li>
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">API</a></li>
          </ul>
        </div>
        
        <div class="col-lg-3 col-md-6">
          <h5 class="fw-bold mb-4">Support</h5>
          <ul class="list-unstyled">
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">Help Center</a></li>
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">Contact Us</a></li>
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">Privacy Policy</a></li>
            <li class="mb-2"><a href="#" class="text-light text-decoration-none">Terms of Service</a></li>
          </ul>
        </div>
      </div>
      
      <hr class="my-4 border-secondary">
      
      <div class="text-center">
        <p class="text-light mb-0">
          © 2025 ParkSmart. All rights reserved. Made with ❤️ for smart parkers everywhere.
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>