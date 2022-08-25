<template>
<h2 style="color: red"> are you sure you want to delete the following log from your tracker?</h2>
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
      <td>Tracker Type</td>
      <th> - </th>
      <td>{{ trackerType }}</td>
    </tr>

    <template v-if="trackerType === 'time_dur'">
    <tr>
      <td>Start time</td>
      <th> - </th>
      <td>{{start_time}}</td>
    </tr>
      <tr>
      <td>End time</td>
      <th> - </th>
      <td>{{ end_time }}</td>
    </tr>
    </template>

    <template v-else-if="trackerType==='mc'">
      <tr>
      <td>Choices Available</td>
      <th> - </th>
      <td>{{ choices }}</td>
    </tr>
      <tr>
      <td>Choices Marked</td>
      <th> - </th>
      <td>{{ choicesMarked }}</td>
    </tr>
    </template>
    <template v-else>
      <tr>
      <td>Logged Value</td>
      <th> - </th>
      <td>{{ logValue }}</td>
    </tr>
    </template>

    <tr>
      <td>Timestamp</td>
      <th> - </th>
      <td>{{ timestamp }}</td>
    </tr>
    <tr>
      <td>Note</td>
      <th> - </th>
      <td>{{ note }}</td>
    </tr>


  </tbody>
  </table>

    </div>
    <div class="col">
    </div>
  </div>
<div class="row">
    <div class="col" style="font-size: 20px">
      <button class="btn-info" @click="deleteLogAPI">Confirm</button>
      <button class="btn-warning" @click="this.$router.push({name: 'trackerDetails'})">Cancel</button>
  </div>
</div>
</div>


</template>

<script>
export default {
  name: "deleteTrackerComp",
  data(){
    return{
      trackerName: "",
      trackerType: "",
      logValue: "",
      start_time: "",
      end_time: "",
      choices: [],
      choicesMarked: [],
      timestamp: "",
      note: "",
      trackerID: this.$route.params.tracker_id,
      logID: this.$route.params.log_id

    }
  },
  methods : {
    deleteLogAPI(){
      fetch(`${this.$store.state.base_url}/${this.trackerID}/${this.logID}/delete/`, {
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
        if(data["Delete"]=="Successful"){
          window.alert("Log deleted successfully.")
          this.$router.push({name:"trackerDetails"})
        }
      }).catch(e => {
        window.alert("An error occurred while trying to perform this action.")

        this.$router.push({name: "trackerDetails"})
      })
    }
  },
  beforeMount() {
    fetch(`${this.$store.state.base_url}/${this.$route.params.tracker_id}/${this.$route.params.log_id}/getLogDetails/`,{
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

      this.trackerName = data.trackerName
      this.trackerType = data.trackerType
      // except time_dur
      this.logValue = data.logValue
      // if time_dur
      this.start_time = data.start_time
      this.end_time = data.end_time
      // if mc
      this.choices = data.choices
      this.choicesMarked = data.choicesMarked

      this.timestamp = data.timestamp
      this.note = data.note.trim()


    }).catch(e => {
      window.alert("an error occurred: ", e)
      this.$router.push({name:"trackerDetails"})
    })
  }
}
</script>

<style scoped>

</style>