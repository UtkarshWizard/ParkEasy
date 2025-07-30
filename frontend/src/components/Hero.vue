<script>
export default {
  name: 'Hero'
}
</script>

<template>
  <section class="hero-section d-flex align-items-center position-relative">
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    
    <div class="container position-relative" style="z-index: 10;">
      <div class="row justify-content-center text-center text-white">
        <div class="col-lg-10">
          <div class="mt-5 mx-4">
            <span class="badge glass-effect px-4 py-2 rounded-pill mb-4">
              <i class="fas fa-circle text-success me-2" style="font-size: 0.5rem;"></i>
              Now Available in 50+ Cities
            </span>
          </div>
          
          <h1 class="display-1 fw-bold mb-4 lh-1">
            Never Worry About<br>
            <span class="text-warning">Parking</span><br>
            Again
          </h1>
          
          <p class="lead mb-5 fs-4" style="max-width: 600px; margin: 0 auto;">
            Find, book, and pay for parking spots instantly. Track your expenses, 
            get monthly reports, and never circle the block again.
          </p>
          
          <div class="d-flex flex-column flex-sm-row gap-3 justify-content-center">
            <router-link to="/signup" class="btn btn-gradient btn-lg px-5 py-3 rounded-pill fw-semibold">
              Start Parking Smart
              <i class="fas fa-arrow-right ms-2"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>

.glass-effect {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
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

.hero-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.3;
}

.floating-element {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  animation: float 6s ease-in-out infinite;
}

.floating-element:nth-child(1) {
  top: 20%;
  left: 10%;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.5);
  animation-delay: 0s;
}

.floating-element:nth-child(2) {
  top: 60%;
  right: 20%;
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.3);
  animation-delay: 2s;
}

.floating-element:nth-child(3) {
  bottom: 20%;
  left: 20%;
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.2);
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.5rem;
  }
}

</style>