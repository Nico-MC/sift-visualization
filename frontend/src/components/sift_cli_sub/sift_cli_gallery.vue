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
    <div id="myModal" class="modal img-magnifier-container" ref="myModal">
      <span class="close" id="modalImgClose">&times;</span>
      <img class="modal-content" id="modalImg" :src="modalImgSrc" ref="modalImg">
      <pre id="keypoint_caption">{{modalImgCaption}}</pre>
      <div class="img-magnifier-glass" ref="glass"></div>
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
    this.$eventBus.$on('buildGallery', (inputImageName) => {
      this.buildGallery()
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
    getKeypoints (type) {
      var inputImageName = this.$store.inputImageName
      if (inputImageName != null) {
        return axios.get('http://localhost:5000/sift_cli/animate_keypoints?inputImageName=' + inputImageName)
          .then((response) => {
            return axios.get('http://localhost:5000/sift_cli/get_keypoints/' + type)
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
    },
    // Events
    buildGallery () {
      this.getKeypoints('scalespace').then((response) => {
        this.keypointsOriginalImage_randomUuid = response.randomUuid
        this.keypointsOriginalImage = response.keypoints
        this.getKeypoints('dog').then((response) => {
          this.keypointsDog_randomUuid = response.randomUuid
          this.keypointsDog = response.keypoints
        })
      })
      this.getScalespace().then((response) => {
        this.scalespace_randomUuid = response.randomUuid
        this.scalespace = response.scalespace
      })
      this.getDogs().then((response) => {
        this.dogs_randomUuid = response.randomUuid
        this.dogs = response.dogs
      })
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
      var modal = document.getElementById('myModal')
      var modalImgClose = document.getElementById('modalImgClose')
      modal.style.display = 'block'
      this.modalImgSrc = modalImgSrc
      this.modalImgCaption = caption
      modalImgClose.onclick = function () {
        if (modal.style.display === 'block') modal.style.display = 'none'
        else modal.style.display = 'block'
      }
      this.magnify(modalImgSrc)
    },
    createMagnifier (img) {
      // eslint-disable-next-line
      var glass, width, height, myModal
      glass = this.$refs['glass']
      myModal = this.$refs['myModal']
      this.$refs.glass_BackgroundWidth = 3
      this.$refs.glass_Zoom = 2
      // ### --- GLOBAL VARS OF MAGNIFIER GLASS --- ###
      glass.addEventListener('mousemove', this.moveMagnifier)
      img.addEventListener('mousemove', this.moveMagnifier) // touch
      myModal.addEventListener('mousemove', this.CheckIfMagnifierInImage, myModal)
    },
    magnify (modalImgSrc) {
      var glass = this.$refs['glass']
      var img = this.$refs['modalImg']
      // ### --- BACKGROUND PROPERTIES OF MAGNIFIER GLASS --- ###
      glass.style.backgroundImage = 'url("' + modalImgSrc + '")'
      glass.style.backgroundRepeat = 'no-repeat'
      setTimeout(function () {
        glass.style.backgroundSize = (img.width * this.$refs.glass_Zoom) + 'px ' + (img.clientHeight * this.$refs.glass_Zoom) + 'px'
        this.$refs.glass_Width = glass.offsetWidth / 2
        this.$refs.glass_Height = glass.offsetHeight / 2
      }.bind(this), 500)
      // ### --- HOVER EVENT LISTENER OF MAGNIFIER GLASS --- ###
      glass.addEventListener('touchmove', this.moveMagnifier)
      img.addEventListener('touchmove', this.moveMagnifier) // touch
    },
    moveMagnifier (e) {
      var glass = this.$refs['glass']
      // eslint-disable-next-line
      var pos, x, y, width, height, backgroundWidth = 0, zoom
      /* prevent any other actions that may occur when moving over the image */
      e.preventDefault()
      pos = { x: e.clientX, y: e.clientY }
      x = pos.x
      y = pos.y
      width = this.$refs.glass_Width
      height = this.$refs.glass_Height
      zoom = this.$refs.glass_Zoom
      // ### --- SET POSITION OF MAGNIFIER GLASS --- ###
      glass.style.left = x + 'px' // (x - w) + "px"
      glass.style.top = y + 'px' // (y - h) + "px"
      // ### --- COMPUTE LENSE EFFECT OF MAGNIFIER GLASS --- ###
      // eslint-disable-next-line
      var posToImage = this.getCursorPos()
      glass.style.backgroundPosition = '+' + ((posToImage.x * zoom) - width + backgroundWidth) + 'px -' + ((posToImage.y * zoom) - height + backgroundWidth) + 'px'
      console.log(glass.style.backgroundPosition)
    },
    getCursorPos (e) {
      var a, x = 0, y = 0
      var img = this.$refs['modalImg']
      e = e || window.event
      a = img.getBoundingClientRect()
      x = e.pageX - a.left
      y = e.pageY - a.top
      x = x - window.pageXOffset
      y = y - window.pageYOffset
      return { x: x, y: y }
    },
    CheckIfMagnifierInImage (e) {
      if (e.target.id === 'myModal') {
        this.$refs['glass'].style.visibility = 'hidden'
      } else if (e.target.id === 'modalImg') {
        this.$refs['glass'].style.visibility = 'visible'
      }
    }
  },
  mounted () {
    this.createMagnifier(this.$refs['modalImg'], 2)
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
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 9; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.9); /* Black width/ opacity */
  }

  .modal-content {
    margin: auto;
    display: block;
    width: 80%;
    max-width: 50%;
    cursor: pointer;
  }

  .modal-content, #caption {
    animation-name: zoom;
    animation-duration: 0.6s;
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
</style>
