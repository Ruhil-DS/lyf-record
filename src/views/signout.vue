<template>

</template>

<script>

export default {
  name: "signout",

  beforeMount(){
    {
          this.$store.state.session = true
          localStorage.clear()
          this.$store.login = false;
          localStorage.login = false;
          this.$router.push({ name: 'signin-up' })
    }
  }
}

</script>

<style scoped>

</style>