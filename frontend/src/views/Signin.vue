<script>
import axios from 'axios'

export default {
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
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
    async signin() {
      console.log("Sending login request...");
      try {
        const res = await axios.post('/auth/login' , {
          email: this.email,
          password: this.password
        })
        console.log("Login response:", res.data);
        const redirect = res.data.redirect
        this.$router.push(redirect)
      } catch (err) {
        alert(err.response.data.error || 'Login failed')
      }
    }
  }
}
</script>

<template>
  <div class=" d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="w-100" style="max-width: 400px">
      <div class="text-center mb-4">
        <h2 class="fw-bold">Welcome Back !</h2>
        <p class="text-muted">Login to your account</p>
      </div>
      <form @submit.prevent="signin">
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

        <button class="btn w-100 text-white fw-semibold" :class="gradientBtnClass" type="submit">
          Log In <i class="bi bi-arrow-right ms-1"></i>
        </button>

        <p class="text-center mt-3">
          Create an Account !
          <router-link to="/signup">Sign Up</router-link>
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
