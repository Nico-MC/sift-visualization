<template lang="html">
  <div>
    <p class="tab_content_header q-title text-h4">
      Filter {{ step_number + ': ' + step_name}}
    </p>
    <p v-if="Object.keys(step).length == 0">SIFT does not found any keypoints in this step.</p>
    <div
      class="q-gutter-md column items-start"
      v-for="(octave, o_number) in step"
      :key="'octave_' + o_number"
    >
      <div>
        <span class="octave_headline">
          Octave: {{ parseInt(o_number) + 1 }}
        </span>
        <div class="scale_container">
          <div
            class="keypoint_image"
            v-for="(scale, s_number) in octave"
            :key="'scale_' + s_number"
          >
            <q-img
              :id="keypoints_randomUuid"
              :src="initImg(step_number-1, o_number, s_number)"
              spinner-color="white"
              v-on:dblclick="zoomImg"
              v-on:click="changeImg(step_number-1, o_number, s_number)"
              style="width: 360px"
              :class="'octave_' + o_number + ' scale_' + s_number"
              :data-stepName="step_name"
              :data-stepNumber="step_number"
              :ref="step_number-1 + '_' + o_number + '_' + s_number"
            >
              <div class="absolute-bottom-right text-subtitle2">
                {{ parseInt(s_number) }}
              </div>
            </q-img>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { QImg } from 'quasar'

export default {
  components: {
    QImg
  },
  props: {
    step: Object,
    defaultWidth: Number,
    step_number: Number,
    step_name: String,
    keypoints_randomUuid: String
  },
  methods: {
    zoomImg (img) {
      this.$store.doubleClicked = true
      try {
        var classes = img.target.parentElement.className.split(' ')
        var octaveOfImage = parseInt(classes[2].split('_')[1]) + 1
        var scaleOfImage = parseInt(classes[3].split('_')[1])
        var stepOfImage = img.target.parentElement.dataset.stepname
        var stepNumberOfImage = img.target.parentElement.dataset.stepnumber

        var srcUrl = img.srcElement.previousSibling.style.backgroundImage
        var modalImgSrc = srcUrl.substring(srcUrl.lastIndexOf('http'), srcUrl.lastIndexOf(')') - 1)
        var caption = 'Filter ' + stepNumberOfImage + ': ' + stepOfImage + '\nOctave: ' + octaveOfImage + ' - Scale: ' + scaleOfImage
        this.$eventBus.$emit('showModalImage', modalImgSrc, caption)
      } catch (e) {
      }
    },
    initImg (step, octave, scale) {
      var src = 'http://localhost:5000/static/keypoints/step_' + step + '/Octave_' +
        octave + '/Original/scale_' + scale + '.jpg?' + this.keypoints_randomUuid
      return src
    },
    changeImg (step, octave, scale) {
      var promise = new Promise((resolve, reject) => {
        setTimeout(() => {
          if (!this.$store.doubleClicked) {
            var newSrc = ''
            var SrcOfClickedComponent = this.$refs[step + '_' + octave + '_' + scale][0].src
            if (SrcOfClickedComponent.includes('Original')) {
              newSrc = 'http://localhost:5000/static/keypoints/step_' + step + '/Octave_' +
                octave + '/DoG/scale_' + scale + '.jpg?' + this.keypoints_randomUuid
            } else if (SrcOfClickedComponent.includes('DoG')) {
              newSrc = 'http://localhost:5000/static/keypoints/step_' + step + '/Octave_' +
                octave + '/Original/scale_' + scale + '.jpg?' + this.keypoints_randomUuid
            }
            this.$refs[step + '_' + octave + '_' + scale][0].src = newSrc
            resolve(newSrc)
          }
        }, 300)
        return promise
      })
    }
  }
}

</script>

<style lang="css">
  #keypoint_caption {
    text-align: center;
    margin-top: 10px;
    font-size: 18pt;
    color: white;
  }

  .keypoint_image {
    margin-right: 15px;
    margin-bottom: 15px;
    transition: all .2s ease-in-out;
    width: 360px;
  }

  .keypoint_image:hover {
    transform: scale(1.03);
    z-index: 1;
  }

  .octave_headline {
    margin-bottom: 0;
    font-size: 14pt;
  }

  .scale_container {
    display: flex;
    flex-wrap: wrap;
  }
</style>
