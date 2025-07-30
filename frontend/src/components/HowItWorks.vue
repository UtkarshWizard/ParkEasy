<script>
export default {
  name: 'HowItWorks',
  data() {
    return {
      steps: [
        {
          icon: 'fas fa-search',
          title: 'Search',
          description: 'Enter your destination and find available parking spots nearby.',
          bgColor: 'bg-primary'
        },
        {
          icon: 'fas fa-map-marker-alt',
          title: 'Select',
          description: 'Choose your preferred parking spot from the interactive map view.',
          bgColor: 'bg-info'
        },
        {
          icon: 'fas fa-credit-card',
          title: 'Book & Pay',
          description: 'Reserve your spot and pay securely through the app.',
          bgColor: 'bg-success'
        },
        {
          icon: 'fas fa-check-circle',
          title: 'Park',
          description: 'Navigate to your reserved spot and park hassle-free.',
          bgColor: 'bg-warning'
        }
      ]
    }
  }
}
</script>

<template>
  <section id="how-it-works" class="py-5 bg-white">
    <div class="container py-5">
      <div class="row justify-content-center text-center mb-5">
        <div class="col-lg-8">
          <h2 class="display-4 fw-bold mb-4">How It Works</h2>
          <p class="lead text-muted">
            Parking made simple in just 4 easy steps. No more circling around looking for spots.
          </p>
        </div>
      </div>
      
      <div class="row g-4">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          class="col-lg-3 col-md-6"
        >
          <div class="text-center">
            <div class="step-number">{{ index + 1 }}</div>
            <div :class="`p-3 rounded-circle d-inline-flex mb-4 ${step.bgColor}`">
              <i :class="`${step.icon} text-white fs-4`"></i>
            </div>
            <h5 class="fw-bold mb-3">{{ step.title }}</h5>
            <p class="text-muted">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>

.step-number {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  margin: 0 auto 1rem;
}

</style>