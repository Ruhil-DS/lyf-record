<template>

<div class="col-md-5 position-relative position-absolute start-50 translate-middle-x">

    <div class="container row">
      <div class="row justify-content-center display-5"><i><u>Add a Tracker</u></i></div>

      <p></p>
      <br>
      <br>
      <span style="font-family: 'Courier New'; color: gray">
          Here, you can add your <span style="color: #20c4b0">desired trackers</span>
      </span>
      <br>


</div>
<br><br>

    <form id="create-tracker-form" @submit.prevent="createTrackerAPI">
        <div>
            <label>Tracker Name:</label>
            <label style="color: red">*</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="text" name="tracker_name" v-model="trackerName" required />
        </div><br><br>

        <div>
            <label>Tracker Type:</label>
            <label style="color: red">*</label> &nbsp;&nbsp;&nbsp;
            <input class="form-check-input" type="radio" name="tracker_type" id="numerical_radio" value="num" v-model="Choice" required>
            <label class="form-check-label" for="numerical_radio">Numerical </label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" name="tracker_type" id="time_dur_radio" value="time_dur" v-model="Choice">
            <label class="form-check-label" for="time_dur_radio">Time Duration</label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" name="tracker_type" id="bool_radio" value="bool" v-model="Choice">
            <label class="form-check-label" for="bool_radio">Boolean</label>&nbsp;&nbsp;&nbsp;

            <input class="form-check-input" type="radio" name="tracker_type" id="mc_radio" value="mc" v-model="Choice">
            <label class="form-check-label" for="mc_radio">Multi Choice</label>&nbsp;
        </div><br><br>

        <div>
            <label>Tracker Description:</label>
            <input type="text" name="tracker_desc" v-model="trackerDesc" />
        </div><br><br>

        <div>
            <label>Choices(comma sep.)</label>
            <input type="text" name="mc_choices" v-model="Choices" :required="mcReq()"/><br>
            <span style="color: red">(Fill this only if choosing Multi Choice option)</span>
        </div><br><br>

        <div>
            <input type="submit" value = "Submit" >
        </div>
    </form>



</div>
</template>

<script>
export default {
  name: "createTrackerComp",
  data(){
    return{
      trackerName: '',
      Choice: null,
      trackerDesc: '',
      Choices: '',
    }
  },
  methods:{
    mcReq(){
      if(this.Choice == "mc") return true
      return false
    },
    createTrackerAPI(){
      fetch(this.$store.state.base_url+ '/trackers/create/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
      },
        body: JSON.stringify({
              "tracker_name": this.trackerName,
              "tracker_type": this.Choice,
              "tracker_desc": this.trackerDesc,
              "mc_choices": this.Choices
              })
    }).then(resp => {
        if (resp.ok) {
          return resp.json()
        }
        else {
          console.log("inside else of first then")
          throw new Error()
        }

      })
      .then(data => {

        if(data.creation == "Successful"){
          this.$router.push({name: 'Dashboard'})
        }
        else if(data.creation == "Failed"){
          window.alert("ERROR OCCURRED")
        }

      }).catch(e => {
        console.log(e, "error in catch block, hehehehe")
        this.$store.state.session = true
            localStorage.clear()
            this.$store.login = false;
            localStorage.login = false;
            this.$router.push({name: 'signin-up'})
      })

    },

  },

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
        label, span,div {color: white}

</style>