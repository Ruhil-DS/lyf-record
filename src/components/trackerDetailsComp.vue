<template>

<div class="col-md-5 position-relative position-absolute start-50 translate-middle-x">

    <div class="container row">
      <div class="row justify-content-center display-5"><i><u style="color: white">Details - {{trackerName}}</u></i></div>

      <p></p>
      <br>
      <br>
      <span style="font-family: 'Courier New'; color: gray ">
          All your tracker information are available <span style="color: #20c4b0">below</span>
          <br><br>
      </span>
      <br>
        <span class="h5" style="color: #20c4b0">Graph summary -</span>

      <template v-if="plot">
        <img :src="getImgUrl(plot)" class="w3-white" />
      </template>


        <span></span>
        <br><br>

        <span class="h5" style="color: #20c4b0">All logs -</span>


          <template v-if="type === 'time_dur'">

            <table class="table table-dark table-hover">
            <thead>
            <tr>
              <th scope="col">S no</th>
              <th scope="col">Timestamp</th>
              <th scope="col">Logged Start time</th>
              <th scope="col">Logged End time</th>
              <th scope="col" width="200">Note</th>
              <th scope="col">Actions</th>
            </tr>
            </thead>
            <tbody>


            <template v-for="(log, key, index) in logs">
            <tr>
                <th scope="row">{{index+1}}</th>
                <td>{{log[0]}}</td>
                <td>{{log[1][0]}}</td>
                <td>{{log[1][1]}}</td>
                <td>{{log[2]}}</td>
               <td> <router-link :to="{name:'updateLog', params:{tracker_id:this.$route.params.tracker_id, log_id: key}}">update</router-link> /
                  <router-link :to="{name:'deleteLog', params:{tracker_id:this.$route.params.tracker_id, log_id: key}}">delete</router-link> </td>
            </tr>

              </template>

            </tbody>
            </table>
            </template>



        <template v-else>
        <table class="table table-dark table-hover">
            <thead>
            <tr>
              <th scope="col">S no</th>
              <th scope="col">Timestamp</th>
              <th scope="col">Logged Value</th>
              <th scope="col" width="200">Note</th>
              <th scope="col">Actions</th>
            </tr>
            </thead>
            <tbody>

            <template v-for="(log, key, index) in logs">
            <tr>
                <th scope="row">{{index+1}}</th>
                <td>{{log[0]}}</td>
                <td>{{log[1]}}</td>
                <td>{{log[2]}}</td>
                <td>
                  <router-link :to="{name:'updateLog', params:{tracker_id:this.$route.params.tracker_id, log_id: key}}">update</router-link> /
                  <router-link :to="{name:'deleteLog', params:{tracker_id:this.$route.params.tracker_id, log_id: key}}">delete</router-link> </td>
            </tr>
            </template>

      </tbody>
    </table>
          </template>

</div>


<!-- Button trigger modal -->
  <template v-if="!download">
    <button class="btn btn-outline-primary me-2 btn-lg" :onclick="downloadLogs">Click to download logs</button>
    <br><br>
    </template>
  <template v-else-if="download">
    <br>
    <img src="@/assets/loading.gif" style="width:10%;">
    <br/>
    <h4 style="color: white">Your request is being processed and your download will be available in your inbox...</h4>
    <h4 style="color: white"><u @click="downloadLogs" id="retryDownload">Click here</u> if you don't receive any mail</h4>
  </template>

<br><br>
</div>
</template>

<script>
export default {
  name: "trackerDetailsComp",
  data() {
    return {
      tracker_id: null,
      plot: "",
      type: "",
      trackerName: "",
      logs: {},
      download: false

    }
  },
  methods: {
    downloadLogs(){

      this.download = false
      fetch(`${this.$store.state.base_url}/${this.tracker_id}/details/download/`, {
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

    getImgUrl(pet) {
    let images = require.context('../QuantifiedSelfApp-FLASK/static/images/', false, /\.png$/)
    return images(`./${pet.substring(14, 1000)}`)
    }
  },
  beforeMount() {
    console.log("Before Mount testing")
    this.tracker_id = this.$route.params.tracker_id
    fetch(`${this.$store.state.base_url}/${this.tracker_id}/details/`, {
      method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.access_token}`
      }
    }).then(resp => {
      if(resp.ok) return resp.json()
      else {
        this.$router.push({ name: 'Dashboard' })
        // this.$store.state.session = true
        //   localStorage.clear()
        //   this.$store.login = false;
        //   localStorage.login = false;
        //   this.$router.push({ name: 'signin-up' })
      }
    })
    .then(data => {
      this.plot = data.plot
      this.type = data.type
      this.logs = data.logs
      this.trackerName = data.name


    })
  }
}
</script>

<style scoped>
#retryDownload:hover{
  cursor: pointer;
}
</style>