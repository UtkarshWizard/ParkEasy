<script>
export default {
  name: 'Pricing',
  data() {
    return {
      plans: [
        {
          name: 'Free',
          price: '0',
          description: 'Perfect for occasional parkers',
          features: [
            'Find nearby parking spots',
            'Basic booking functionality',
            'Payment processing',
            'Email receipts',
            'Basic expense tracking'
          ],
          cta: 'Get Started Free',
          popular: false
        },
        {
          name: 'Smart',
          price: '9.99',
          description: 'Best for regular commuters',
          features: [
            'Everything in Free',
            'Advanced spot filtering',
            'Priority booking',
            'Monthly reports',
            'Budget alerts',
            'Parking history',
            'Customer support'
          ],
          cta: 'Start Free Trial',
          popular: true
        },
        {
          name: 'Business',
          price: '29.99',
          description: 'Ideal for teams and companies',
          features: [
            'Everything in Smart',
            'Team management',
            'Expense reporting',
            'Corporate billing',
            'API access',
            'Custom integrations',
            'Dedicated support'
          ],
          cta: 'Contact Sales',
          popular: false
        }
      ]
    }
  }
}
</script>

<template>
  <section id="pricing" class="py-5 bg-light">
    <div class="container py-5">
      <div class="row justify-content-center text-center mb-5">
        <div class="col-lg-8">
          <h2 class="display-4 fw-bold mb-4">Simple, Transparent Pricing</h2>
          <p class="lead text-muted">
            Choose the plan that fits your parking needs. Start free and upgrade as you grow.
          </p>
        </div>
      </div>
      
      <div class="row g-4 justify-content-center">
        <div 
          v-for="(plan, index) in plans" 
          :key="index"
          class="col-lg-4 col-md-6"
        >
          <div :class="`card pricing-card h-100 ${plan.popular ? 'popular' : ''}`">
            <div v-if="plan.popular" class="card-header text-center border-0">
              <i class="fas fa-star me-2"></i>Most Popular
            </div>
            <div class="card-body text-center p-4">
              <h4 class="card-title fw-bold mb-3">{{ plan.name }}</h4>
              <div class="mb-4">
                <span class="display-4 fw-bold">${{ plan.price }}</span>
                <span class="text-muted">/month</span>
              </div>
              <p class="text-muted mb-4">{{ plan.description }}</p>
              
              <ul class="list-unstyled mb-4">
                <li v-for="(feature, featureIndex) in plan.features" :key="featureIndex" class="mb-2">
                  <i class="fas fa-check text-success me-2"></i>{{ feature }}
                </li>
              </ul>
              
              <router-link to="/signin" :class="`btn w-100 py-3 rounded-pill fw-semibold ${plan.popular ? 'btn-gradient' : 'btn-outline-primary'}`">
                {{ plan.cta }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <div class="text-center mt-5">
        <p class="text-muted mb-3">All plans include a 14-day free trial. No credit card required.</p>
        <div class="d-flex flex-wrap justify-content-center gap-4 small text-muted">
          <span><i class="fas fa-check text-success me-1"></i>Cancel anytime</span>
          <span><i class="fas fa-check text-success me-1"></i>No setup fees</span>
          <span><i class="fas fa-check text-success me-1"></i>24/7 support</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style>

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

.pricing-card {
  transition: all 0.3s ease;
  border: 2px solid #e9ecef;
}

.pricing-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.pricing-card.popular {
  border-color: #667eea;
  transform: scale(1.05);
}

.pricing-card.popular .card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

@media (max-width: 768px) {
  .pricing-card.popular {
    transform: none;
  }
}

</style>