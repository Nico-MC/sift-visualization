<template lang="html">
  <form @submit.prevent.stop="submit" class="q-gutter-md">
    <div class="animate_keypoints_image_container" v-show="Object.keys(keypoints.original).length === 6">
      <q-tabs
        v-model="currentKeypointTab"
        class="text-teal keypoint_tabs"
        active-color="primary"
      >
        <q-tab name="step_0" icon="filter_1" label=""/>
        <q-tab name="step_1" icon="filter_2" label=""/>
        <q-tab name="step_2" icon="filter_3" label=""/>
        <q-tab name="step_3" icon="filter_4" label=""/>
        <q-tab name="step_4" icon="filter_5" label=""/>
        <q-tab name="step_5" icon="filter_6" label=""/>
      </q-tabs>

      <q-tab-panel :name="'step_' + step_number"
        v-for="(step, step_number) in keypoints.original"
        :key="'step_' + step_number"
        :class="'step_container tab_content items-start'"
        v-show="currentKeypointTab === 'step_' + step_number"
      >
        <scaleWrapper
          :step_name="steps[step_number]"
          :step_number="parseInt(step_number) + 1"
          :step="step"
          :defaultWidth="defaultWidth"
          :keypoints_randomUuid="keypoints_randomUuid"
        ></scaleWrapper>
      </q-tab-panel>
    </div>
  </form>
</template>

<script>
import scaleWrapper from 'components/sift_cli_sub/gallery/scale_wrapper.vue'
import { QTabs, QTab, QTabPanel } from 'quasar'

export default {
  components: {
    scaleWrapper,
    QTabs,
    QTab,
    QTabPanel
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
      ],
      currentKeypointTab: 'step_0'
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
  }

  .keypoint_tabs {
    margin-top: 75px;
  }

</style>
