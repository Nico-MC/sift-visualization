<template>
  <div id="scrollPoint" class="octave_container">
    <div class="q-pa-md">
      <div class="q-gutter-md">
        <div class="q-gutter-md row items-start">
          <div v-show="Object.keys(scalespace).length > 0" class="q-gutter-y-md" style="max-width: 400px">
            <q-tabs
              v-model="currentTab"
              class="text-teal"
            >
              <q-tab name="scalespace_tab" icon="blur_circular" label="Scalespace"/>
              <q-tab name="dog_tab" icon="brightness_1" label="Difference of Gaussian" />
            </q-tabs>
          </div>
          <div class="tab_content" v-show="currentTab === 'scalespace_tab'">
            <div v-for="(octave, index) in scalespace" :key="'scalespace_' + index">
              <h6 class="octave_number q-title text-h6">
                Octave: {{ parseInt(index) + 1 }}
              </h6>
              <div class="q-gutter-md row items-start">
                <q-img
                  v-for="(scale, index) in octave"
                  :key="index"
                  :src="'http://localhost:5000/static/scalespace/' + scale + '?' + scalespace_randomUuid"
                  style="width: 300px"
                  spinner-color="white"
                >
                  <div class="absolute-bottom-right text-subtitle2">
                    {{ parseInt(index) + 1}}
                  </div>
                </q-img>
              </div>
            </div>
          </div>
          <div class="tab_content" v-show="currentTab === 'dog_tab'">
            <div v-for="(octave, index) in dogs" :key="'dog_' + index">
              <h6 class="octave_number q-title text-h6">
                Octave: {{ parseInt(index) + 1 }}
              </h6>
              <div class="q-gutter-md row items-start">
                <q-img
                  v-for="(dog, index) in octave"
                  :key="index"
                  :src="'http://localhost:5000/static/dog/' + dog + '?' + dogs_randomUuid"
                  style="width: 300px"
                  spinner-color="white"
                >
                  <div class="absolute-bottom-right text-subtitle2">
                    {{ parseInt(index) + 1 }}
                  </div>
                </q-img>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { QImg, QTabs, QTab } from 'quasar'
import axios from 'axios'

export default {
  components: {
    QImg,
    QTabs,
    QTab
  },
  data () {
    return {
      scalespace: {},
      dogs: {},
      currentTab: 'scalespace_tab'
    }
  },
  created () {
    this.$eventBus.$on('getScales', () => {
      this.getScalespace().then(function (response) {
        this.scalespace_randomUuid = response.randomUuid
        this.scalespace = response.scalespace
      }.bind(this))
      this.getDogs().then(function (response) {
        this.dogs_randomUuid = response.randomUuid
        this.dogs = response.dogs
      }.bind(this))
    })
    this.$eventBus.$on('resetScales', () => {
      this.scalespace = {}
      this.dogs = {}
    })
  },
  methods: {
    getScalespace () {
      return axios.get('http://localhost:5000/sift_cli/get_filenames/scalespace')
        .then(function (response) {
          var promise = new Promise(function (resolve, reject) {
            resolve(response.data)
          })
          return promise
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    getDogs () {
      return axios.get('http://localhost:5000/sift_cli/get_filenames/dog')
        .then(function (response) {
          var promise = new Promise(function (resolve, reject) {
            resolve(response.data)
          })
          return promise
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    scroll () {
      console.log(111)
      window.scroll({
        top: document.getElementById('scrollPoint').offsetTop
      })
    }
  }
}
</script>

<style media="screen">
  .tab_content {
    width: 100%;
    padding: 0;
  }

  .octave_number {
    margin-bottom: 5px;
    margin-top: 45px;
  }

  .octave_container {
    margin-bottom: 45px;
  }
</style>
