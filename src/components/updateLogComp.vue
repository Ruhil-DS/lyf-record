<template>



<div class="col-md-5 position-relative position-absolute start-50 translate-middle-x">

    <div class="container row">
      <div class="row justify-content-center display-5"><i><u>Updating Logs</u></i></div>

      <p></p>
      <br>
      <br>
      <span style="font-family: 'Courier New'; color: gray">
          Here, you can update the log values for your <span style="color: #20c4b0">tracker</span>
          <br><br>
          Update all the relevant information in the below <span style="color: #20c4b0">form</span>
      </span>
      <br>


</div>
<br><br>

    <form id="log-tracker-form" @submit.prevent="updateLogAPI">
        <div>

            <div class="display-6">Updating log for : <div style="color:white;"><u>{{trackerName}}</u> </div></div>

        </div><br><br>

      <template v-if="trackerType ==='num'">

        <div>
          <label>Tracker Value :</label>
          <label style="color: red">*</label>
          <br>
          <input type="number" v-model="logValue" step="0.0001"  required/>
        </div><br><br>

      </template>

      <template v-else-if="trackerType === 'time_dur'">
        <div>
            <label>Start time :</label>
            <label style="color: red">*</label>
            <br>
            <input type="datetime-local"  v-model="start_time"
                   required/>
        </div><br><br>
        <div>
            <label>End time :</label>
            <label style="color: red">*</label>
            <br>
            <input type="datetime-local" v-model="end_time" required/>
        </div><br><br>

      </template>


      <template v-else-if="trackerType === 'bool'">
        <div>
            <label>Tracker Value :</label>
            <label style="color: red">*</label><br>


          <template v-if="logValue === 'True'">
            <input class="form-check-input" type="radio" id="true_radio" value="True" v-model="logValue"
                   required checked>
            <label class="form-check-label" for="true_radio">True</label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" id="false_radio" value="False" v-model="logValue">
            <label class="form-check-label" for="false_radio">False</label>&nbsp;
          </template>

          <template v-else-if="logValue === 'False'">
            <input class="form-check-input" type="radio" id="true_radio" value="True" v-model="logValue"
                   required>
            <label class="form-check-label" for="true_radio">True</label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" id="false_radio" value="False" v-model="logValue"
                   checked>
            <label class="form-check-label" for="false_radio">False</label>&nbsp;

          </template>

        </div>
      </template>


      <template v-else-if="trackerType === 'mc'">
        <div>
            <label>Tracker choices :</label>
            <label style="color: red">*</label><br><br>


          <template v-for="choice in choices">

              <template v-if="choicesMarked.indexOf(choice) !== -1">

            <input class="form-check-input" type="checkbox" id="mc_check"
                   :value="choice" v-model="choicesMarked" checked>
            <label class="form-check-label">{{choice}}</label>&nbsp;&nbsp;&nbsp;


                </template>
            <template v-else>
            <input class="form-check-input" type="checkbox" id="mc_check"
                   :value="choice" v-model="choicesMarked">
            <label class="form-check-label">{{choice}}</label>&nbsp;&nbsp;&nbsp;
              </template>

            </template>
        </div>

      </template>


        <br><br>

        <div>
            <label>Timestamp when logging :</label>
            <label style="color: red">*</label><br>

            <br><br>
          <input type="datetime-local" id="log_timestamp" v-model="timestamp" required>
        </div><br><br>

        <div>
            <label>Note :</label><br>
            <textarea style="width: 400px; height: 100px" v-model="note"> {{note}} </textarea><br>
        </div><br><br>

        <div>
            <input class="btn-outline-primary" type="submit" value = "Submit" >
        </div>
    </form>
</div>

</template>

<script>
export default {
  name: "updateLogComp",
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

    }
  },
  computed:{
    postDATA(){
      let ChoicesToSend = []
      for(var i in this.choicesMarked){
        ChoicesToSend.push(this.choicesMarked[i])
      }

      return {
          "note": this.note,
          "timestamp": this.timestamp,
          "value": this.logValue,
          "start_val": this.start_time,
          "end_val": this.end_time,
          "choice_list": String(ChoicesToSend)
        }
    }
  },
  methods:{
    updateLogAPI(){
      let dataToSend = this.postDATA
      console.log("testing update function")
      fetch(`${this.$store.state.base_url}/${this.$route.params.tracker_id}/${this.$route.params.log_id}/update/`, {
      method: "PATCH",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
      },
        body: JSON.stringify(dataToSend)
      }).then(resp =>
      {
        if(resp.ok){
          return resp.json()
        }
        else throw new Error()
      })
      .then(data => {
        if(data["Update"]=="Successful"){
          window.alert("Log updated successfully.")
          this.$router.push({name:"trackerDetails", params:{tracker_id: this.$route.params.tracker_id }})
        }
      }).catch(e => {
        window.alert("An error occurred while trying to perform this action.")
        this.$router.push({name: "Dashboard"})
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