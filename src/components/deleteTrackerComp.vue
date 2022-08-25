<template>
<h2 style="color: red"> are you sure you want to delete the following tracker?</h2>
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
      <td>Tracker Name</td>
      <th> - </th>
      <td>{{ trackerName }}</td>
    </tr>
    <tr>
      <td>Tracker Description</td>
      <th> - </th>
      <td>{{ trackerDescription }}</td>
    </tr>
    <tr>
      <td>Tracker Type</td>
      <th> - </th>
      <td>{{ trackerType }}</td>
    </tr>

  </tbody>
  </table>

    </div>
    <div class="col">
    </div>
  </div>
<div class="row">
    <div class="col" style="font-size: 20px">
      <button class="btn-info" @click="deleteTrackerAPI">Confirm</button>
      <button class="btn-warning" @click="this.$router.push({name: 'Dashboard'})">Cancel</button>
  </div>
</div>
</div>


</template>

<script>
export default {
  name: "deleteTrackerComp",
  data(){
    return{
      trackerName:"",
      trackerDescription:"",
      trackerType:"",
      choices:"",
      time_value:"",
      trackerID: this.$route.params.tracker_id

    }
  },
  methods : {
    deleteTrackerAPI(){

      fetch(`${this.$store.state.base_url}/${this.trackerID}/delete/`, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
        }
      }).then(resp =>
      {
        if(resp.ok){
          return resp.json()
        }
        else throw new Error()
      })
      .then(data => {
        if(data["Deletion"]=="Successful"){
          window.alert("Tracker deleted successfully.")
          this.$router.push({name:"Dashboard"})
        }
      }).catch(e => {
        window.alert("An error occurred while trying to perform this action.")

        this.$router.push({name: "Dashboard"})
      })
    }
  },
  beforeMount() {
    fetch(`${this.$store.state.base_url}/${this.trackerID}/getLogInfo/`,{
      method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
      }
    }).then(resp => {
      if(resp.ok) return resp.json()
      else throw new Error()
    }).then(data => {
      this.trackerName = data.name
      this.trackerDescription = data.desc
      this.trackerType = data.type
      this.choices = data.choices
      this.time_value = data.currentTime


    }).catch(e => {
      window.alert("an error occurred: ", e)
      this.$router.push({name:"Dashboard"})
    })
  }
}
</script>

<style scoped>

</style>