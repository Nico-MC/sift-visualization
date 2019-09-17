<template>
  <div class="octave_container" v-show="Object.keys(scalespace).length > 0">
    <div class="output_tab_navigation q-gutter-md" style="max-width: 600px">
      <q-tabs
        v-model="click"
        class="text-teal"
      >
        <q-tab name="scalespace_tab" icon="layers" label="Scalespace" @click="toggleLines('scalespace_tab')"/>
        <q-tab name="dog_tab" icon="bubble_chart" label="Difference of Gaussian" @click="toggleLines('dog_tab')"/>
        <q-tab name="keypoints_tab" icon="linear_scale" label="Keypoints (original image)" @click="toggleLines('keypoints_tab')"/>
      </q-tabs>
    </div>
    <div class="modal" ref="myModal">
      <span class="close" id="modalImgClose">&times;</span>
      <v-zoomer ref="vue-zoomer" style="height: 100%">
        <div class="">
          <div style="width: 100%; height: 100px"></div>
          <div style="height: 720px">
            <img class="modal-content" :src="modalImgSrc" ref="modalImg">
            <div id="keypoint_caption">{{ modalImgCaption }}</div>
          </div>
        </div>
      </v-zoomer>
    </div>
    <!-- ### SCALESPACE TAB ### -->
    <div class="tab_content items-start scalespace-images" v-show="$store.currentTab === 'scalespace_tab'" v-if="Object.keys(scalespace).length > 0">
      <scalespace-images
        :scalespace="scalespace"
        :keypoints="keypointsOriginalImage"
        :defaultWidth="defaultWidth"
        :scalespace_randomUuid="scalespace_randomUuid"
        ref="scalespaceImages"
      ></scalespace-images>
    </div>
    <!-- ### DIFFERENCE-OF-GAUSSIAN TAB ### -->
    <div class="tab_content items-start dog-images" v-show="$store.currentTab === 'dog_tab'" v-if="Object.keys(dogs).length > 0">
      <dog-images
        :dogs="dogs"
        :scalespace="scalespace"
        :keypoints="keypointsDog"
        :defaultWidth="defaultWidth"
        :dogs_randomUuid="dogs_randomUuid"
        ref="dogImages"
      ></dog-images>
    </div>
    <!-- ### KEYPOINTS TAB ### -->
    <div class="tab_content keypoint-animation" v-show="$store.currentTab === 'keypoints_tab'" v-if="Object.keys(keypointsOriginalImage).length > 0">
      <keypoint-animation
        :keypoints="keypointsOriginalImage"
        :defaultWidth="defaultWidth"
        :keypoints_randomUuid="keypointsOriginalImage_randomUuid"
        ref="keypointAnimation"
      ></keypoint-animation>
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
      keypointsOriginalImage: {},
      keypointsDog: {},
      defaultWidth: 240,
      click: 'scalespace_tab',
      modalImgSrc: '',
      modalImgCaption: ''
    }
  },
  created () {
    // Variables
    this.$store.currentTab = 'scalespace_tab'
    this.$store.scalespaceLines = []
    this.$store.dogLines = []
    // Event-Listener
    this.$eventBus.$on('buildGallery', (drawType) => {
      this.buildGallery(drawType)
    })
    this.$eventBus.$on('resetGalleryData', () => {
      this.resetGalleryData()
    })
    this.$eventBus.$on('showModalImage', (img, caption) => {
      this.showModalImage(img, caption)
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
    getKeypoints (type, drawType) {
      var inputImageName = this.$store.inputImageName
      if (inputImageName != null) {
        return axios.get('http://localhost:5000/sift_cli/animate_keypoints?inputImageName=' + inputImageName + '&drawType=' + drawType)
          .then((response) => {
            return axios.get('http://localhost:5000/sift_cli/get_filenames/keypoints/' + type)
              .then((response) => {
                var promise = new Promise(function (resolve, reject) {
                  resolve(response.data)
                })
                return promise
              })
              .catch(function (error) {
                console.log(error)
              })
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    },
    toggleLines (currentTab) {
      this.$store.currentTab = currentTab
      this.click = this.$store.currentTab
      this.triggerResizeEvent()
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
    },
    // Events
    buildGallery (drawType) {
      var counter = 0
      this.getKeypoints('scalespace', drawType).then((response) => {
        this.keypointsOriginalImage_randomUuid = response.randomUuid
        this.keypointsOriginalImage = response.keypoints
        this.getKeypoints('dog', drawType).then((response) => {
          this.keypointsDog_randomUuid = response.randomUuid
          this.keypointsDog = response.keypoints
          increaseCounter()
        })
      })
      this.getScalespace().then((response) => {
        this.scalespace_randomUuid = response.randomUuid
        this.scalespace = response.scalespace
        increaseCounter()
      })
      this.getDogs().then((response) => {
        this.dogs_randomUuid = response.randomUuid
        this.dogs = response.dogs
        increaseCounter()
      })

      var increaseCounter = () => {
        counter++
        if (counter === 3) {
          this.$eventBus.$emit('hideLoader')
          document.getElementById('sift_cli_button_execute').disabled = false
        }
      }
    },
    resetGalleryData () {
      this.$refs.scalespaceImages.removeLines()
      this.$refs.dogImages.removeLines()
      this.scalespace = {}
      this.dogs = {}
      this.keypointsOriginalImage = {}
      this.keypointsDog = {}
      this.click = 'scalespace_tab'
      this.$store.currentTab = this.click
    },
    showModalImage (modalImgSrc, caption) {
      var modal = this.$refs['myModal']
      var modalImgClose = document.getElementById('modalImgClose')
      modal.style.display = 'block'
      this.modalImgSrc = modalImgSrc
      this.modalImgCaption = caption
      modalImgClose.onclick = function () {
        if (modal.style.display === 'block') modal.style.display = 'none'
        else modal.style.display = 'block'
      }
      this.$refs['modalImg'].ondragstart = function () {
        return false
      }
      var vueZoomer = this.$refs['vue-zoomer']
      vueZoomer.reset()
      this.triggerResizeEvent()
    },
    triggerResizeEvent (timeout = 200) {
      // The plugins (LeaderLine and Zoomer) make some problems
      setTimeout(function () {
        window.dispatchEvent(new Event('resize'))
      }, timeout)
    }
  }
}
</script>

<style media="screen">
  .tab_content.scalespace-images {
    padding: 0px;
    margin-top: 30px;
  }

  .tab_content.dog-images {
    padding: 0px;
    margin-top: 30px;
  }

  .tab_content.keypoint-animation {
    padding: 0px;
    margin-top: 30px;
  }

  .octave_container {
    margin-bottom: 50px;
  }

  #keypoint_caption {
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: inherit;
  }

  /* MODAL */
  .modal {
    z-index: 9999;
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 9; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.9); /* Black width/ opacity */
    padding-top: 0;

  }

  .modal-content {
    margin: auto;
    display: block;
    width: 80%;
    max-width: 50%;
    max-height: 100%;
    cursor: pointer;
  }

  .modal-content, #caption {
    animation-name: zoom;
    animation-duration: 0.6s;
    object-fit: contain;
    width: 100%;
  }

  @keyframes zoom {
    from { transform:scale(0) }
    to { transform:scale(1) }
  }

  .close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #f1f1f1;
    font-size: 40px;
    font-weight: bold;
    transition: 0.3s;
    z-index: 9;
  }

  .close:hover,
  .close:focus {
    color: #bbb;
    text-decoration: none;
    cursor: pointer;
  }

  @media only screen and (max-width: 700px) {
    .modal-content {
      width: 100%;
    }
  }

  .img-magnifier-glass {
    position: absolute;
    border: 3px solid #000;
    border-radius: 50%;
    cursor: none;
    width: 100px;
    height: 100px;
  }

  @media only screen and (max-width: 1700px) {
    .modal-content {
      max-height: 75%;
    }
  }

  @media only screen and (max-width: 1300px) {
    .modal-content {
      max-height: 60%;
    }
  }

  @media only screen and (min-width: 1700px) {
    .modal-content {
      max-height: 90%;
    }
  }
</style>
