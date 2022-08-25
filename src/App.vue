<template>
  <navBar :key="$route.path"></navBar>
<!--  <router-view :key="$route.fullPath"/>-->

  <router-view v-slot="{ Component }">
  <transition name="fade">
    <component :is="Component" />
  </transition>
</router-view>

</template>

<script>
import navBar from '@/components/navBar'
export default {
  name: 'App',
  data(){
    return {
      nav_flag: ''
    }
  },
  components: {
    navBar
  },
  mounted() {
    if(localStorage.login=='true') this.nav_flag = true
    else this.nav_flag = false
  }

}
</script>

<style>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.75s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;

}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

.hoverable{
  color: #328ce5 !important;
}


nav a.router-link-exact-active {
  color: #42b983;
}


</style>
