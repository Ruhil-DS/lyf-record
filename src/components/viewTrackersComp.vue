<template>

<div class="col-md-5 position-relative position-absolute start-50 translate-middle-x">

    <div class="container row">
      <div class="row justify-content-center display-5"><i><u style="color: white">Your Trackers</u></i></div>

      <p></p>
      <br>
      <br>
      <span style="font-family: 'Courier New'; color: gray">
          Here is a list of <span style="color: #20c4b0">your trackers</span>
          <br> Click on a tracker row to view more details.
      </span>
      <br>
</div>
<br><br>

<table class="table table-dark table-hover">
<thead>
    <tr>
      <th scope="col">S no</th>
      <th scope="col">Tracker Name</th>
      <th scope="col">Tracker Description</th>
      <th scope="col">Tracker Type</th>
      <th scope="col">Last logged value</th>
    </tr>
  </thead>
  <tbody>

   <template v-for="(tracker, key, index) in trackers">
    <tr class="table-row"  @click="this.$router.push({name: 'trackerDetails', params:{tracker_id:key}})">
      <th scope="row">{{index+1}}</th>
      <td>{{tracker[0]}}</td>
      <td>{{tracker[1]}}</td>
      <td>{{tracker[2]}}</td>
      <td>{{tracker[3]}}</td>
    </tr>
  </template>


  </tbody>
</table>
</div>

</template>

<script>
export default {
  name: "viewTrackers",
  data() {
    return {
      trackers : {}
    }
  },

  beforeMount() {
    fetch(this.$store.state.base_url+ '/trackers/view/', {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
      }
    }).then(resp => {
      if(resp.ok)  {
        return resp.json()
      }
      else {
        this.$store.state.session = true
          localStorage.clear()
          this.$store.login = false;
          localStorage.login = false;
          this.$router.push({ name: 'signin-up' })
      }
        })
    .then(data => {
      this.trackers = data
    }).catch(e => {
      this.$router.push({ name: 'signin-up' })
    })
  }
}

</script>

<style scoped>
  .btn-outline-success:hover{
    background-color: #46b8da !important;
  }
  .btn-outline-success{

    color: #f6f6f6 !important;
    border: #46b8da !important;
  }

  html,body,h1,h2,h3,h4,h5 {font-family: "Raleway", sans-serif}

  .table-row {
    cursor:pointer;
  }

</style>