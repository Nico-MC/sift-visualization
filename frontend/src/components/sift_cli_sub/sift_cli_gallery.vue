<template>
  <div class="octave_container" v-if="Object.keys(scalespace).length > 0">
    <div class="output_tab_navigation q-gutter-md" style="max-width: 600px">
      <q-tabs
        v-model="click"
        class="text-teal"
      >
        <q-tab name="scalespace_tab" icon="layers" label="Scalespace" @click="toggleLines('scalespace_tab')"/>
        <q-tab name="dog_tab" icon="bubble_chart" label="Difference of Gaussian" @click="toggleLines('dog_tab')"/>
        <q-tab name="keypoints_tab" icon="linear_scale" label="Keypoints" @click="toggleLines('keypoints_tab')"/>
      </q-tabs>
    </div>
    <!-- ### SCALESPACE TAB ### -->
    <div class="tab_content items-start" v-show="$store.currentTab === 'scalespace_tab'" v-if="Object.keys(scalespace).length > 0">
      <scalespaceImages
        :scalespace="scalespace"
        :defaultWidth="defaultWidth"
        :scalespace_randomUuid="scalespace_randomUuid"
        ref="scalespaceImages"
      ></scalespaceImages>
    </div>
    <!-- ### DIFFERENCE-OF-GAUSSIAN TAB ### -->
    <div class="tab_content items-start" v-show="$store.currentTab === 'dog_tab'" v-if="Object.keys(dogs).length > 0">
      <dogImages
        :dogs="dogs"
        :scalespace="scalespace"
        :defaultWidth="defaultWidth"
        :dogs_randomUuid="dogs_randomUuid"
        ref="dogImages"
      ></dogImages>
    </div>
    <!-- ### KEYPOINTS TAB ### -->
    <div class="tab_content" v-show="$store.currentTab === 'keypoints_tab'">
      <keypointAnimation
        :defaultWidth="defaultWidth"
        ref="keypointAnimation"
      ></keypointAnimation>
    </div>
  </div>
</template>

<script>
import { QTabs, QTab } from 'quasar'
import axios from 'axios'
import keypointAnimation from 'components/sift_cli_sub/gallery/keypoint_animation.vue'
import scalespaceImages from 'components/sift_cli_sub/gallery/scalespace_images.vue'
import dogImages from 'components/sift_cli_sub/gallery/dog_images.vue'

export default {
  components: {
    QTabs,
    QTab,
    keypointAnimation,
    scalespaceImages,
    dogImages
  },
  data () {
    return {
      scalespace: {},
      dogs: {},
      keypoints: '',
      defaultWidth: 240,
      click: 'scalespace_tab'
    }
  },
  created () {
    this.$store.currentTab = 'scalespace_tab'
    this.$eventBus.$on('buildGallery', (inputImageName) => {
      this.getScalespace().then(function (response) {
        this.scalespace_randomUuid = response.randomUuid
        this.scalespace = response.scalespace
      }.bind(this))
      this.getDogs().then(function (response) {
        this.dogs_randomUuid = response.randomUuid
        this.dogs = response.dogs
      }.bind(this))
    })
    this.$store.scalespaceLines = []
    this.$store.dogLines = []
    this.$eventBus.$on('resetGalleryData', () => {
      this.resetGalleryData()
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
    resetGalleryData () {
      this.$refs.scalespaceImages.removeLines()
      this.scalespace = {}
      this.dogs = {}
      this.keypoints = ''
      this.$store.currentTab = 'scalespace_tab'
    },
    toggleLines (currentTab) {
      this.$store.currentTab = currentTab
      this.click = this.$store.currentTab
      setTimeout(function () {
        window.dispatchEvent(new Event('resize'))
      }, 200)
      if (this.$store.currentTab === 'scalespace_tab') {
        this.$refs.scalespaceImages.enableLines(true)
      } else {
        this.$refs.scalespaceImages.enableLines(false)
      }
      if (this.$store.currentTab === 'dog_tab') {
        this.$refs.dogImages.enableLines(true)
      } else {
        this.$refs.dogImages.enableLines(false)
      }
    }
  }
}
</script>

<style media="screen">
  .tab_content {
    padding: 0;
    /* margin-left: 32px; */
    margin-top: 30px;
  }

  .octave_container {
    margin-bottom: 50px;
  }
</style>
