import { createRouter, createWebHistory } from "vue-router";
import Signin from "@/views/Signin.vue";
import Signup from "@/views/Signup.vue";
import AdminDashboard from "@/views/Admin/AdminDashboard.vue";
import AdminParkingLot from "@/views/Admin/AdminParkingLot.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";
import AdminParkingSpot from "@/views/Admin/AdminParkingSpot.vue";
import AdminUsersBookings from "@/views/Admin/AdminUsersBookings.vue";
import UserDashboard from "@/views/Users/UserDashboard.vue";
import UserLayout from "@/layouts/UserLayout.vue";
import CurrentBooking from "@/views/Users/CurrentBooking.vue";
import BookingHistory from "@/views/Users/BookingHistory.vue";
import axios from "axios";
import AdminAnalytics from "@/views/Admin/AdminAnalytics.vue";
import UserAnalytics from "@/views/Users/UserAnalytics.vue";
import Landing from "@/views/Landing.vue";

const routes = [
  { path: "/" , name: "Landingpage" , component: Landing},
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
      {
        path: "analytics",
        name: "AdminAnalytics",
        component: AdminAnalytics,
      },
    ],
  },
  {
    path: "/user",
    component: UserLayout,
    children: [
      {
        path: "dashboard",
        name: "UserDashboard",
        component: UserDashboard,
      },
      {
        path: "currentbooking",
        name: "CurrentBooking",
        component: CurrentBooking
      },
      {
        path: "bookinghistory",
        name: "BookingHistory",
        component: BookingHistory
      },
      {
        path: "analytics",
        name: "UserAnalytics",
        component: UserAnalytics
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  try {
    const res = await axios.get("/auth/check", {
      withCredentials: true,
    });

    const role = res.data.role;

    if (to.path.startsWith("/admin")) {
      if (role === "admin") {
        return next();
      } else {
        return next("/user/dashboard");
      }
    }

    if (to.path.startsWith("/user")) {
      if (role === "user") {
        return next();
      } else {
        return next("/admin/dashboard");
      }
    }

    return next();
  } catch (err) {
    if (to.path.startsWith("/admin") || to.path.startsWith("/user")) {
      return next("/signin");
    }

    return next();
  }
});


export default router;
