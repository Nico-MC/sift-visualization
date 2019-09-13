<template lang="html">
  <form @submit.prevent.stop="submit" class="q-gutter-md">
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
          :keypoints_randomUuid="keypoints_randomUuid"
        ></scaleWrapper>
      </div>
    </div>
  </form>
</template>

<script>
import scaleWrapper from 'components/sift_cli_sub/gallery/scale_wrapper.vue'

export default {
  components: {
    scaleWrapper
  },
  props: {
    defaultWidth: Number,
    keypoints: Object,
    keypoints_randomUuid: String
  },
  data () {
    return {
      steps: [
        'Discrete 3D extrema of DoG',
        'Discrete 3D extrema passing a conservative threshold on DoG (DoG soft threshold)',
        'Interpolated 3D extrema (Extrema interpolation)',
        'Interpolated extrema passing the threshold on DoG (DoG threshold)',
        'Interpolated extrema passing the Harris-Stephen edgeness test (On edge response)',
        'Keypoints with reference orientation (far from border)'
      ]
    }
  }
}
</script>

<style lang="css">
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
