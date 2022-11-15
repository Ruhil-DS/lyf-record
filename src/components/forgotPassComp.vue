<template>
<h2 style="color: red"> Did you forget your password?</h2>
<div class="container text-center">
  <div class="row">
    <div class="col">
    </div>
    <div class="col">
  <table class="table" style="color: white">
  <thead>
    <tr>
      <th scope="col">Key</th>
      <th> - </th>
      <th scope="col">Value</th>

    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Your username</td>
      <th> - </th>
      <td><input v-model="username" placeholder="Enter your username"></td>
    </tr>

  </tbody>
  </table>

    </div>
    <div class="col">
    </div>
  </div>
<div class="row">
    <div class="col" style="font-size: 20px">
      <button class="btn-info" @click="forgotpassAPI">Confirm</button>
      <button class="btn-warning" @click="this.$router.push({name: 'signin-up'})">Cancel</button>
  </div>
</div>
</div>


</template>


<script>
export default {
  name: "forgotPassComp",
  data(){
    return {
      username : ""
    }
  },
  methods: {
    forgotpassAPI(){
      fetch("http://127.0.0.1:5000/api/forgot-password/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      },
        body: JSON.stringify({
          "username": this.username
        })
      }).then(resp => {
        if(resp.ok) return resp.json()
        else throw new Error()
      }).then(data => {
        if(data.msg === "Done"){
          window.alert("If the username matches our record, you will receive a mail on the registered email. " +
              "Please don't share the mail with anyone.")
          this.$router.push({name: "signin-up"})
        }
      }).catch(e => console.log('an error occurred -->>', e))

    }
  }
}
</script>

<style scoped>

</style>