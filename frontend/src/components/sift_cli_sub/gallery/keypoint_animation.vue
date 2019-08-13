<template lang="html">
  <form @submit.prevent.stop="submit" class="q-gutter-md">
    <q-btn class="animate_keypoints_button" label="Animate keypoints" type="submit" color="primary" />
    <div class="animate_keypoints_image_container">
      <div v-if="Object.keys(keypoints).length > 0">
        <img
          id="myimg"
          :src="'http://localhost:5000/static/keypoints/' + this.$store.inputImageName + '_gray.jpg?' + keypoints.randomUuid"
          spinner-color="white"
          @load="animateKeypoints"
        />
      </div>
    </div>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      'keypoints': {}
    }
  },
  methods: {
    submit () {
      var inputImageName = this.$store.inputImageName
      if (inputImageName != null) {
        return axios.get('http://localhost:5000/sift_cli/animate_keypoints?inputImageName=' + inputImageName)
          .then(function (response) {
            this.keypoints = response.data
          }.bind(this))
          .catch(function (error) {
            console.log(error)
          })
      }
    },
    animateKeypoints () {
      var img = document.getElementById('myimg')
      var width = img.naturalWidth
      var height = img.naturalHeight
      console.log(width, height)
      img.width = width
      img.height = height
    }
  }
}
</script>

<style lang="css">
  .animate_keypoints_button {
    margin-bottom: 25px;
  }

  .animate_keypoints_image_container {
    /* max-width: 600px; */
    position: relative;
  }

  .animate_keypoints_image_container .q-img {
    width: auto;
    /* max-width: 600px; */
  }

  .circle {
    position: absolute;
    width: 5px;
    height: 5px;
    border-radius: 40px;
    border: 5px solid red;
    left: 620.912231px;
    bottom: 0;
    z-index: 1;
  }
</style>
