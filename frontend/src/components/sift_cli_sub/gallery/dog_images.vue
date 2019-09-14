<template lang="html">
  <div class="dog_container">
    <div class="dog_octave_container"
      :id="'octave_' + parseInt(o_number)"
      v-for="(octave, o_number) in dogs"
      :key="'dog_' + o_number"
      v-for-callback="{key: o_number, array: dogs, callback: callback}"
    >
      <p class="tab_content_header q-title text-h6">
        Octave: {{ parseInt(o_number) + 1 }}
      </p>
      <div class="scales_and_dogs">
        <div class="q-gutter-md column items-start scales">
          <div
            v-for="(scale, s_number) in scalespace[o_number]"
            :key="s_number"
          >
            <q-img
              :class="'octave_' + parseInt(o_number) + ' ' + 'scale_' + s_number"
              :src="'http://localhost:5000/static/scalespace/' + scale + '?' + dogs_randomUuid"
              :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
              spinner-color="white"
            >
            </q-img>
          </div>
        </div>
        <div class="q-gutter-md column items-start dogs">
          <div
            v-for="(dog, d_number) in octave"
            :key="d_number"
            class="dog_img"
          >
            <q-img
              :class="'octave_' + parseInt(o_number) + ' ' + 'dog_' + d_number"
              :src="'http://localhost:5000/static/dog/' + dog + '?' + dogs_randomUuid"
              :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
              spinner-color="white"
            >
              <div
                class="absolute-full text-subtitle2 flex flex-center dog_caption"
                v-if="d_number > 0 && d_number < Object.keys(octave).length - 1"
                v-on:click="showKeypointsForClickedDog($event)"
              >
                Show extrema
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
import JQuery from 'jquery'

export default {
  components: {
    QImg
  },
  props: {
    dogs: Object,
    scalespace: Object,
    keypoints: Object,
    defaultWidth: Number,
    dogs_randomUuid: String
  },
  methods: {
    callback (numberOfOctaves, numberOfScales) {
      this.removeLines()
      setTimeout(function () {
        for (var i = 0; i < numberOfOctaves; i++) {
          for (var j = 0; j < numberOfScales; j++) {
            var start = JQuery('.dog_container .octave_' + i + '.scale_' + j)[0]
            var startAdjacent = JQuery('.dog_container .octave_' + i + '.scale_' + (j + 1))[0]
            var end = JQuery('.dog_container .octave_' + i + '.dog_' + j)[0]
            var line = null
            var lineAdjacent = null
            // eslint-disable-next-line
            if (i === 0 && j == 0) {
              line = new window.LeaderLine(start, end, { hide: true, size: 2, startLabel: 'Subtract two adjacent LoG scales', endLabel: 'to DoG scale' })
              lineAdjacent = new window.LeaderLine(startAdjacent, end, { hide: true, size: 2 })
            } else {
              line = new window.LeaderLine(start, end, { hide: true, size: 2 })
              lineAdjacent = new window.LeaderLine(startAdjacent, end, { hide: true, size: 2 })
            }
            this.$store.dogLines.push(line)
            this.$store.dogLines.push(lineAdjacent)
          }
        }
        if (this.$store.currentTab === 'dog_tab') {
          this.enableLines(true)
        } else {
          this.enableLines(false)
        }
      }.bind(this), 5000)
    },
    enableLines (enable) {
      for (var i = 0; i < this.$store.dogLines.length; i++) {
        if (enable) {
          this.$store.dogLines[i].show('draw', { animOptions: { duration: 3000, timing: [0.5, 0, 1, 0.42] } })
        } else {
          this.$store.dogLines[i].hide()
        }
      }
    },
    removeLines () {
      for (var i = 0; i < this.$store.dogLines.length; i++) {
        this.$store.dogLines[i].remove()
      }
      this.$store.dogLines = []
    },
    showKeypointsForClickedDog ($event) {
      var caption = ''
      try {
        var classes = $event.target.offsetParent.offsetParent.className.split(' ')
        var octaveOfImage = parseInt(classes[2].split('_')[1])
        var scaleOfImage = parseInt(classes[3].split('_')[1]) - 1
        var src = 'http://localhost:5000/' + this.keypoints[5][octaveOfImage][scaleOfImage].scale
        this.$eventBus.$emit('showModalImage', src, caption)
      } catch (e) {
        caption = 'SIFT does not found any keypoints for this scale.\nOctave: ' + octaveOfImage + ' - Scale: ' + scaleOfImage
        this.$eventBus.$emit('showModalImage', '', caption)
      }
    }
  },
  directives: {
    forCallback (el, binding) {
      let element = binding.value
      var key = element.key
      var keys = Object.keys(element.array)
      var len = keys.length
      key = keys.indexOf(key)
      if (key === len - 1) {
        if (typeof element.callback === 'function') {
          element.callback(Object.values(element.array).length, Object.values(element.array)[0].length)
        }
      }
    }
  }
}
</script>

<style lang="css" scoped>
  .dog_octave_container {
    flex: 1 1 auto;
    background-color: #f4f4f4;
    padding: 5px 0 25px 5px;
    margin-bottom: 50px;
  }

  .dog_container {
    display: flex;
    flex-direction: column;
  }

  .scales_and_dogs {
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-flow: row wrap;
  }

  .dogs {
    align-items: center;
  }

  .dogs .dog_caption {
    opacity: 0;
  }

  .dogs .dog_caption:hover {
    opacity: 1;
    padding: 0;
    cursor: pointer;
  }

</style>
