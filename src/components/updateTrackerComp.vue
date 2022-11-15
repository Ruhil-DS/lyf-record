<template>

<div class="col-md-5 position-relative position-absolute start-50 translate-middle-x">

    <div class="container row">
      <div class="row justify-content-center display-5"><i><u>Update your Tracker</u></i></div>

      <p></p>
      <br>
      <br>
      <span style="font-family: 'Courier New'; color: gray">
          Here, you can update your <span style="color: #20c4b0">tracker</span>
          <br><br>
          You can only update the <span style="color: #20c4b0">name</span> and the
          <span style="color: #20c4b0">description</span> for your tracker, currently.
      </span>
      <br>


</div>
<br><br>

    <form id="create-tracker-form" @submit.prevent="updateTrackerAPI">
        <div>
            <label>Tracker Name: <span style="color: red">* &nbsp;</span></label>
            <input type="text" name="tracker_name_updated" v-model="trackerName"  required/>
        </div><br><br>

        <div>
            <label>Tracker Type:</label>
            <input class="form-check-input" type="radio" name="tracker_type" id="numerical_radio" value="num" v-model="trackerType" disabled>
            <label class="form-check-label" for="numerical_radio" style="color: white">Numerical </label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" name="tracker_type" id="time_dur_radio" value="time_dur" v-model="trackerType" disabled>
            <label class="form-check-label" for="time_dur_radio" style="color: white">Time Duration</label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" name="tracker_type" id="bool_radio" value="bool" v-model="trackerType" disabled>
            <label class="form-check-label" for="bool_radio" style="color: white">Boolean</label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" name="tracker_type" id="mc_radio" value="mc" v-model="trackerType" disabled>
            <label class="form-check-label" for="mc_radio" style="color: white">Multi Choice</label>&nbsp;
        </div><br><br>

        <div>
            <label>Tracker Description: <span style="color: red">* &nbsp;</span></label>
            <input type="text" name="tracker_desc_updated" v-model="trackerDescription" required/>
        </div><br><br>

        <div>
            <label>Choices(comma sep.)</label>
            <input type="text" name="mc_choices" v-model="choices" disabled/><br>
        </div><br><br>

        <div>
            <input class="btn-outline-primary" type="submit" value = "Submit">
        </div>
    </form>

</div>
</template>

<script>
export default {
  name: "UpdateTrackerComp",
  data(){
    return {
      trackerName: "",
      trackerDescription: "",
      trackerType: "",
      choices : "",
      time_value: "",
      trackerID: this.$route.params.tracker_id
    }
  },
  methods: {
    updateTrackerAPI(){
      fetch(`${this.$store.state.base_url}/${this.$route.params.tracker_id}/update/`, {
        method: "PATCH",
        headers: {
          'Content-Type': 'application/json',
          "mode": "cors",
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
        },
        body: JSON.stringify({
            "tracker_name_updated": this.trackerName,
            "tracker_desc_updated": this.trackerDescription
      })
      }).then(resp =>
      {
        if(resp.ok){
          return resp.json()
        }
        else throw new Error()
      })
      .then(data => {
        if(data["Update"]=="Successful"){
          window.alert("Tracker updated successfully.")
          this.$router.push({name:"Dashboard"})
        }
      }).catch(e => {
        window.alert("An error occurred while trying to perform this action.")
        console.log(e)
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