import { createRouter, createWebHistory } from "vue-router";
import Signin from "@/views/Signin.vue";
import Signup from "@/views/Signup.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";
import AdminParkingLot from "@/views/AdminParkingLot.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";
import AdminParkingSpot from "@/views/AdminParkingSpot.vue";
import AdminUsersBookings from "@/views/AdminUsersBookings.vue";

const routes = [
  { path: "/signin", name: "Signin", component: Signin },
  { path: "/signup", name: "Signup", component: Signup },
  {
    path: "/admin",
    component: AdminLayout,
    children: [
      {
        path: "dashboard",
        name: "AdminDashboard",
        component: AdminDashboard,
      },
      {
        path: "parkinglot",
        name: "AdminParkingLot",
        component: AdminParkingLot,
      },
      {
        path: "parkingspot",
        name: "AdminParkingSpot",
        component: AdminParkingSpot,
      },
      {
        path: "users",
        name: "AdminUsersBookings",
        component: AdminUsersBookings,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
