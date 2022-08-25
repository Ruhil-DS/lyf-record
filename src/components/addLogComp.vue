<template>

<div class="col-md-5 position-relative position-absolute start-50 translate-middle-x ">

    <div class="container row">
      <div class="row justify-content-center display-5"><i><u style="color:white;">Logging your Tracker</u></i></div>

      <p></p>
      <br>
      <br>
      <span style="font-family: 'Courier New'; color: gray">
          Here, you can log values to your <span style="color: #20c4b0">tracker</span>
          <br><br>
          Add all the relevant information in the below <span style="color: #20c4b0">form</span>
      </span>
      <br>
    </div>
<br><br>

    <form id="log-tracker-form" @submit.prevent="addLogAPI">
        <div>

            <div class="display-6" style="color: #2974c4;">Logging -  {{trackerName}} </div>
            <br>
            <span style="color: #20c4b0">Description:  </span>
            <span style="font-family: 'Courier New'; color: gray"> {{trackerDescription}}</span>

        </div><br><br>




      <template v-if="trackerType == 'num'">
        <div>
            <label style="color: #2974c4;">Tracker Value: </label>
            <label style="color: red">*</label>
            <br>
            <input type="number" step="0.00001" name="tracker_value" v-model="trackerValue" required/>
        </div><br><br>

        </template>


      <template v-if="trackerType == 'time_dur'">
        <div>
            <label style="color: #2974c4;">Start time :</label>
            <label style="color: red">*</label>
            <br>
            <input type="datetime-local" name="tracker_value_start" v-model="trackerValueStart" required/>
        </div><br><br>
        <div>
            <label style="color: #2974c4;">End time :</label>
            <label style="color: red">*</label>
            <br>
            <input type="datetime-local" name="tracker_value_end" v-model="trackerValueEnd" required/>
        </div><br><br>
      </template>



      <template v-if="trackerType == 'bool'">
        <div>
            <label style="color: #2974c4;">Tracker Value :</label>
            <label style="color: red">*</label><br>
            <input class="form-check-input" type="radio" name="tracker_value" id="true_radio" value="True" v-model="trackerValue" required>
            <label class="form-check-label" for="true_radio" style="color: #c3e5a3;">&nbsp;&nbsp;True</label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" name="tracker_value" id="false_radio" value="False" v-model="trackerValue">
            <label class="form-check-label" for="true_radio" style="color: #e06464;">&nbsp;&nbsp;False</label>&nbsp;
        </div>
      </template>


      <template v-if="trackerType == 'mc'">
        <div>
            <label style="color: #2974c4;">Tracker choices :</label>
            <label style="color: red">*</label><br><br>
            <template v-if="emptyChoices" >
              <span style="color:chartreuse; font-size: 18px">At least one choice is required</span><br>
            </template>
            <template v-for="choice in choices">
              <input class="form-check-input" type="checkbox" name="tracker_value" id="mc_check"
                     :value="choice" v-model="ChoiceSelected">
              <label class="form-check-label" style="color: #dcf0f5;">&nbsp;&nbsp;{{choice}}</label>&nbsp;&nbsp;&nbsp;

            </template>

        </div>

      </template>


        <br><br>

        <div>
            <label style="color: #2974c4;">Timestamp when logging :</label>
            <label style="color: red">*</label><br>
            <br><br>
            <input type="datetime-local" name="tracker_timestamp" id="log_timestamp" v-model="time_value" required>
        </div><br><br>

        <div>
            <label style="color: #2974c4;">Note :</label><br>
            <textarea name="note" style="width: 400px; height: 100px" v-model="note"> </textarea><br>
        </div><br><br>

        <div>
            <input class="btn-outline-primary" type="submit" value = "Submit" >
        </div>
    </form>

  </div>
</template>

<script>
export default {
  name: "addLogComp",
  data(){
    return{
      trackerName: "",
      trackerDescription: "",
      trackerType: "",
      choices : "",
      time_value: "",
      note: "",
      trackerValue: "",
      trackerValueStart: "",
      trackerValueEnd: "",
      ChoiceSelected: [],
      trackerID: this.$route.params.tracker_id,
      emptyChoices: false

    }
  },
  computed:{
    postDATA(){
      let ChoicesToSend = []
      for(var i in this.ChoiceSelected){
        ChoicesToSend.push(this.ChoiceSelected[i])
      }

      return {
          "note": this.note,
          "timestamp": this.time_value,
          "value": this.trackerValue,
          "start_val": this.trackerValueStart,
          "end_val": this.trackerValueEnd,
          "choice_list": String(ChoicesToSend)
        }
    }
  },
  methods:{
    addLogAPI() {


      let dataToSend = this.postDATA


      if(this.emptyChoices === false){
        fetch(`${this.$store.state.base_url}/${this.trackerID}/log/`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': `Bearer ${localStorage.access_token}`
          },
          body: JSON.stringify(dataToSend)
        }).then(resp => {
          if (resp.ok) {
            return resp.json()
          } else throw new Error()
        })
            .then(data => {
              if (data["Logging"] == "Successful") {
                window.alert("Value logged successfully.")
                this.$router.push({name: "Dashboard"})
              }
            }).catch(e => {
          window.alert("An error occurred while trying to perform this action.")
          this.$router.push({name: "Dashboard"})
        })
      }
      else{
        console.log("empty choices received")
      }

    },

  },
  watch: {
    ChoiceSelected: {
      handler(newV, oldV) {
        if (newV[0] === undefined) {
          this.emptyChoices = true
        } else {
          this.emptyChoices = false
        }
        console.log(newV[0])
        console.log(this.emptyChoices)
      },
      immediate: false
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