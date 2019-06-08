<template>
  <div class="q-pa-md">
    <div class="q-col-gutter-md row items-start" v-for="(image, index) in images"  :key="index + Math.random()">
      <q-img :src="'http://localhost:5000/static/scalespace/' + image + '?' + Math.random()"></q-img>
    </div>
  </div>
</template>

<script>
import { QImg } from 'quasar'
import axios from 'axios'

export default {
  components: {
    QImg
  },
  data () {
    return {
      images: []
    }
  },
  created () {
    this.$eventBus.$on('pollScalespace', () => {
      this.getScalespace().then(function (response) {
        this.images = response
        console.log(this.images)
      }.bind(this))
    })
  },
  methods: {
    getScalespace () {
      return axios.get('http://localhost:5000/sift_cli_get_filenames/scalespace')
        .then(function (response) {
          // return response.data
          var promise = new Promise(function (resolve, reject) {
            resolve(response.data)
          })
          return promise
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>
