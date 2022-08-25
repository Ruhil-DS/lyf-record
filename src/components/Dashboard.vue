<template>


<!-- !PAGE CONTENT! -->
<div>
  <div class="w3-main" >

  <!-- Header -->
  <header class="w3-container" style="padding-top:22px">
    <h5 style="color:white;"><b><i class="fa fa-dashboard"></i> My Dashboard</b></h5>
  </header>

  <div class="w3-row-padding w3-margin-bottom">
    <div class="w3-quarter">
      <div class="w3-container w3-white w3-padding-16">
        <div class="w3-left">
          <img src="https://static.thenounproject.com/png/1391881-200.png" height="50" width="50">
        </div>

        <div class="w3-clear"></div>
        <h4>Welcome back, {{user}}</h4>
      </div>
    </div>
    <div class="w3-quarter">
      <div class="w3-container w3-blue w3-padding-16"  style="background-color: blue">
        <div class="w3-left"><i class="fa fa-calendar w3-xxxlarge"></i></div>
        <div class="w3-right">
          <h3 :streak="streak">{{streak}}</h3>
        </div>
        <div class="w3-clear"></div>
        <h4>Current Streak</h4>
      </div>
    </div>
    <div class="w3-quarter">
      <div class="w3-container w3-teal w3-padding-16">
        <div class="w3-left"><i class="fa fa-tv w3-xxxlarge"></i></div>
        <div class="w3-right">
          <h3>{{tracker_count}}</h3>
        </div>
        <div class="w3-clear"></div>
        <h4>No. of trackers</h4>
      </div>
    </div>
    <div class="w3-quarter">
      <div class="w3-container w3-orange w3-text-white w3-padding-16">
        <div class="w3-left"><i class="fa fa-users w3-xxxlarge"></i></div>
        <div class="w3-right">
          <template v-if="'days' == member_since.substring(member_since.length-4)">
              <h3>{{member_since}}</h3>
            </template>
          <template v-else>
              <h3>0 days</h3>
            </template>
        </div>
        <div class="w3-clear"></div>
        <h4>Member Since</h4>
      </div>
    </div>
  </div>

  <div class="w3-panel">
    <div class="w3-row-padding" style="margin:26px">
      <div class="w3-third">
        <h5 style="color: #71b4ff">Summary graph</h5>

        <template v-if="graph_path">
          <img :src="getImgUrl(graph_path)" style="width:80%;" class="w3-white">
        </template>
      </div>
      <div class="w3-twothird">
        <h5 style="color: #71b4ff">Your Trackers</h5>
        <template v-if="empty_trackers == false">
        <table class="table table-dark table-hover">
          <thead>
            <tr>
              <th scope="col">S no</th>
              <th scope="col">Tracker Name</th>
              <th scope="col">Tracker Type</th>
              <th scope="col">Last logged</th>
              <th scope="col">Actions</th>

            </tr>
          </thead>
          <tbody>
            <template v-for="(tracker, key, index) in trackers" :key="key">
              <tr>
                <th scope="row">{{index+1}}</th>
                  <td>{{tracker[0]}}</td>
                  <td>{{tracker[1]}}</td>
                  <td>{{tracker[2]}}</td>
                  <td><router-link :to="{name:'addLog', params:{tracker_id:key}}">log value</router-link> /
                    <router-link :to="{name:'updateTracker', params:{tracker_id:key}}">update</router-link>
                    / <router-link :to="{name:'deleteTracker', params:{tracker_id:key}}">delete</router-link>
                  </td>
              </tr>
            </template>
          </tbody>
        </table>

          <template v-if="!download">
            <button class="btn btn-outline-info me-2 btn-mini" style="width: 20%;" :onclick="downloadTrackers">
            Download Trackers' list
            </button>
          </template>
          <template v-else-if="download">
            <br>
            <img src="@/assets/loading.gif" style="width:10%;">
            <br>
            <h4 style="color: white">Your download is being processed and will be available for download in your inbox...</h4>
            <h4 style="color: white"><u @click="downloadTrackers" id="retryDownload">Click here</u> if you didn't receive any mail</h4>
          </template>
          </template>

        <template v-else-if="empty_trackers">
          <img src="/static/images/404_no_tracker.gif" width="270" height="347">
        </template>



      </div>
    </div>
  </div>
  <br>

<!-- Button trigger modal -->
  <button class="btn btn-outline-info me-2 btn-lg" data-bs-toggle="modal"
          data-bs-target="#exampleModal" style="width: 40%;">
  Click for Tracker functionalities
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">What would you like to do?</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" style="color: #0b0b0b; text-align: left">
        Click on any of the buttons to perform an action.
        <br><br>
        You can create or view all of your trackers.
        <br><br>
        To update or delete, kindly check the "Your Trackers" list, or you could view all the trackers and then make
        relevant changes.
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="$router.push({name: 'view_trackers'})">
          View Trackers
        </button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="$router.push({name: 'create_tracker'})">Add a tracker</button>
      </div>
    </div>
  </div>
</div>

</div>
  </div>

</template>

<script>

export default {
  name: "Dashboard",
  data(){
    return{
      user: localStorage.username,
      streak : "",
      tracker_count : "",
      member_since : "",
      trackers : {},
      graph_path : "",
      empty_trackers: false,
      download: false
    }
  },
  methods: {
    getImgUrl(pet) {
    var images = require.context('../QuantifiedSelfApp-FLASK/static/images/', false, /\.png$/)
    return images(`./${pet.substring(14, 1000)}`)
    },
    downloadTrackers(){
      this.download = false
      fetch(`http://127.0.0.1:5000/api/trackers/download/`, {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
      }
      }).then(resp => resp.json())
      .then(data => {
        if(data['msg'] === "Done"){
          this.download = true
        }
      })

      setTimeout(() => this.download=false, 20000)
    },
  },

  watcher:{
    streak:{
      handler(newV, oldV){
        this.streak = newV;
      },
      immediate: true
    }
  },
  beforeMount() {
    if(!localStorage.login || localStorage.login == 'false' ){
      this.$router.push({name: "signin-up"})
    }
    if(localStorage.login == 'true'){

      fetch(this.$store.state.base_url + "/dashboard/", {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
      }
    }).then(resp => resp.json())
      .then(data => {

        if(data.msg === "Token has expired"){
          this.$store.state.session = true
          localStorage.clear()
          this.$store.login = false;
          localStorage.login = false;
          this.$router.push({ name: 'signin-up' })
        }
        else{
          this.streak = data.streak;
          this.tracker_count = data.tracker_count;
          this.member_since = data.member_since;
          this.trackers = data.trackers;
          this.graph_path = data.graph_path  // "http://127.0.0.1:5000/"+

          if(JSON.stringify(data.trackers) == '{}') this.empty_trackers = true;

          console.log(this.graph_path)



        }

      }).catch(e => {
        console.log("error : ", e)
        this.$router.push({name:"signout"})
      })
  }
  }
}



</script>

<style scoped>
#retryDownload:hover{
  cursor: pointer;
}
</style>