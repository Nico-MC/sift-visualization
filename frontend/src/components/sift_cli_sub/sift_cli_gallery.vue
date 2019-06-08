<template>
  <div class="octave_container">
    <div class="q-pa-md">
      <div class="q-gutter-md">
        <div class="q-gutter-md row items-start">
          <div v-show="Object.keys(scalespace).length > 0" class="q-gutter-y-md" style="max-width: 400px">
            <q-tabs
              v-model="default_tab"
              class="text-teal"
            >
              <q-tab name="scalespace_tab" icon="mail" label="Scalespace" />
              <q-tab name="dog_tab" icon="alarm" label="DoG" />
            </q-tabs>
          </div>
          <q-tab-panels
            v-model="default_tab"
            animated
            transition-prev="scale"
            transition-next="scale"
          >
            <q-tab-panel class="tab_content" name="scalespace_tab">
              <div v-for="(octave, index) in scalespace" :key="index">
                <h6 class="octave_number q-title text-h6">
                  Octave: {{ parseInt(index) + 1 }}
                </h6>
                <div class="q-gutter-md row items-start">
                  <q-img
                    v-for="(scale, index) in octave"
                    :key="index"
                    :src="'http://localhost:5000/static/scalespace/' + scale + '?' + Math.random()"
                    style="width: 300px"
                    spinner-color="white"
                  >
                    <div class="absolute-bottom-right text-subtitle2">
                      {{ parseInt(index) + 1}}
                    </div>
                  </q-img>
                </div>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { QImg, QTabs, QTab, QTabPanel, QTabPanels } from 'quasar'
import axios from 'axios'

export default {
  components: {
    QImg,
    QTabs,
    QTab,
    QTabPanel,
    QTabPanels
  },
  data () {
    return {
      scalespace: {},
      default_tab: 'scalespace_tab'
    }
  },
  created () {
    this.$eventBus.$on('getScalespace', () => {
      this.getScalespace().then(function (response) {
        this.scalespace = response
      }.bind(this))
    })
    this.$eventBus.$on('resetScalespace', () => {
      this.scalespace = {}
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

<style media="screen">
  .tab_content {
    padding: 0;
  }

  .octave_number {
    margin-bottom: 5px;
    margin-top: 45px;
  }

  .octave_container .q-gutter-y-md > *, .q-gutter-md > * {
  }

  .ovtave_number {
  }
  .octave_container {
    margin-bottom: 45px;
  }
</style>
