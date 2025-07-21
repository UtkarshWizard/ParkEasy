<script>
import axios from 'axios'

export default {
  data() {
    return {
      fullname: '',
      email: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirmPassword: false,
    }
  },
  computed: {
    gradientBtnClass() {
      return 'btn-gradient'
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    toggleConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword
    },
    async signup() {
      if (this.password !== this.confirmPassword) {
        alert('Passwords do not match!')
        return
      }
      try {
        const res = await axios.post('/auth/signup' , {
          email: this.email,
          fullname: this.fullname,
          password: this.password
        })
        this.$router.push('/signin')
      } catch (err) {
        alert(err.response.data.error || 'Signup failed')
      }
    }
  }
}
</script>

<template>
  <div class=" d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="w-100" style="max-width: 400px">
      <div class="text-center mb-4">
        <h2 class="fw-bold">Create Account</h2>
        <p class="text-muted">Join us and start your journey today</p>
      </div>
      <form @submit.prevent="signup">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <div class="input-group">
            <span class="input-group-text bg-white border-end-0">
              <i class="bi bi-person"></i>
            </span>
            <input
              type="text"
              class="form-control rounded-start-0"
              placeholder="Enter your full name"
              v-model="fullname"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Email Address</label>
          <div class="input-group">
            <span class="input-group-text bg-white border-end-0">
              <i class="bi bi-envelope"></i>
            </span>
            <input
              type="email"
              class="form-control rounded-start-0"
              placeholder="Enter your email"
              v-model="email"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <div class="input-group">
            <span class="input-group-text bg-white border-end-0">
              <i class="bi bi-lock"></i>
            </span>
            <input
              :type="showPassword ? 'text' : 'password'"
              class="form-control rounded-start-0"
              placeholder="Enter your password"
              v-model="password"
              required
            />
            <span class="input-group-text bg-white" @click="togglePassword" style="cursor:pointer;">
              <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </span>
          </div>
        </div>

        <div class="mb-4">
          <label class="form-label">Confirm Password</label>
          <div class="input-group">
            <span class="input-group-text bg-white border-end-0">
              <i class="bi bi-lock"></i>
            </span>
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              class="form-control rounded-start-0"
              placeholder="Confirm your password"
              v-model="confirmPassword"
              required
            />
            <span class="input-group-text bg-white" @click="toggleConfirmPassword" style="cursor:pointer;">
              <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </span>
          </div>
        </div>

        <button class="btn w-100 text-white fw-semibold" :class="gradientBtnClass" type="submit">
          Create Account <i class="bi bi-arrow-right ms-1"></i>
        </button>

        <p class="text-center mt-3">
          Already have an account?
          <router-link to="/signin">Sign In</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.btn-gradient {
  background: linear-gradient(to right, #4a00e0, #8e2de2);
  border: none;
  border-radius: 10px;
  padding: 10px 0;
}
.btn-gradient:hover {
  background: linear-gradient(to right, #3a00d0, #7a1cd9);
}
</style>
