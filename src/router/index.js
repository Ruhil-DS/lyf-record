import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SigninUp from '../views/SigninUp'
import Dashboard from '../views/Dashboard'
import ViewTrackers from '../views/ViewTrackers'
import CreateTracker from "../views/createTracker"
import signout from "../views/signout"
import trackerDetails from "../views/trackerDetails"
import addLog from "../views/addLog"
import updateTracker from "../views/UpdateTracker"
import deleteTracker from "../views/deleteTracker"
import updateLog from "../views/updateLog";
import deleteLog from "@/views/deleteLog";
import forgotPass from "@/views/forgotPass";

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
    {
    path: '/signin-up/',
    name: 'signin-up',
    meta: { transition: 'slide-left' },
    component: SigninUp
  },
    {
    path: '/Dashboard/',
    name: 'Dashboard',
    meta: { transition: 'slide-left' },
    component: Dashboard
  },
  {
    name: 'view_trackers',
    path: '/view_trackers/',
    meta: { transition: 'slide-left' },
    component: ViewTrackers
  },
  {
    name: 'create_tracker',
    path: '/create_tracker/',
    meta: { transition: 'slide-left' },
    component: CreateTracker
  },
    {
    name: 'signout',
    path: '/signout/',
    meta: { transition: 'slide-left' },
    component: signout
  },
    {
    name: 'trackerDetails',
    path: '/:tracker_id/details/',
    meta: { transition: 'slide-left' },
    component: trackerDetails
  },
     {
    name: 'addLog',
    path: '/:tracker_id/log/',
    meta: { transition: 'slide-left' },
    component: addLog
  },
    {
    name: 'updateTracker',
    path: '/:tracker_id/update/',
    meta: { transition: 'slide-left' },
    component: updateTracker
  },
    {
    name: 'deleteTracker',
    path: '/:tracker_id/delete/',
    meta: { transition: 'slide-left' },
    component: deleteTracker
  },
    {
    name: 'updateLog',
    path: '/:tracker_id/:log_id/update/',
    meta: { transition: 'slide-right' },
    component: updateLog
  },
    {
    name: 'deleteLog',
    path: '/:tracker_id/:log_id/delete/',
    meta: { transition: 'slide-left' },
    component: deleteLog
  },
    {
    name: 'forgotPass',
    path: '/forgot-pass/',
    meta: { transition: 'slide-left' },
    component: forgotPass
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
