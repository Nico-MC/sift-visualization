<template lang="html">
  <form @submit.prevent.stop="submit" class="q-gutter-md">
    <q-btn class="animate_keypoints_button" label="Animate keypoints" type="submit" color="primary" />
    <div class="animate_keypoints_image_container" v-show="Object.keys(keypoints).length === 6">
      <div
        v-for="(step, step_number) in keypoints"
        :key="'step_' + step_number"
        class="step_container"
      >
        <scaleWrapper
          :step_name="steps[step_number]"
          :step_number="parseInt(step_number) + 1"
          :step="step"
          :defaultWidth="defaultWidth"
        ></scaleWrapper>
      </div>
    </div>
  </form>
</template>

<script>
import axios from 'axios'
import scaleWrapper from 'components/sift_cli_sub/gallery/scale_wrapper.vue'

export default {
  components: {
    scaleWrapper
  },
  props: {
    defaultWidth: Number
  },
  data () {
    return {
      keypoints: {},
      steps: [
        'Discrete 3D extrema of DoG',
        'Discrete 3D extrema passing a conservative threshold on DoG (DoG soft threshold)',
        'Interpolated 3D extrema (Extrema interpolation)',
        'Interpolated extrema passing the threshold on DoG (DoG threshold)',
        'Interpolated extrema passing the Harris-Stephen edgeness test (On edge response)',
        'Keypoints with reference orientation (far from border)'
      ]
    }
  },
  methods: {
    submit () {
      var inputImageName = this.$store.inputImageName
      if (inputImageName != null) {
        return axios.get('http://localhost:5000/sift_cli/animate_keypoints?inputImageName=' + inputImageName)
          .then((response) => {
            return axios.get('http://localhost:5000/sift_cli/get_keypoints')
              .then((response) => {
                this.saveKeypoints(response.data)
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
    saveKeypoints (keypoints) {
      this.keypoints = keypoints
    }
  }
}
</script>

<style lang="css">
  .animate_keypoints_button {
    margin: 0 0 25px 50px;
  }

  .animate_keypoints_image_container {
    position: relative;
  }

  .animate_keypoints_image_container .q-img {
    width: auto;
  }

  .step_container {
    margin-bottom: 50px;
    background-color: #f4f4f4;
    padding: 15px 0 25px 32px;
  }

</style>
