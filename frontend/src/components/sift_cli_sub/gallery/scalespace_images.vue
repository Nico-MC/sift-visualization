<template lang="html">
  <div class="scalespace_container">
    <div class="scalespace_octave_container"
      v-for="(octave, o_number) in scalespace"
      :key="'scalespace_' + o_number"
      v-bind:class="'octave_' + parseInt(o_number)"
    >
      <p class="tab_content_header q-title text-h6">
        Octave: {{ parseInt(o_number) + 1 }}
      </p>
      <div style="font-size: 12pt; text-align: center; margin-top: -9px" v-if="parseInt(o_number) === 0">(doubled by interpolation)</div>
      <div class="q-gutter-md column items-start scales">
        <div
          v-for="(scale, s_number) in octave"
          :key="s_number"
          :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
        >
          <q-img
            :class="'octave_' + parseInt(o_number) + ' ' + 'scale_' + s_number + ' scalespace-image'"
            :src="scale + '?' + keypoints_randomUuid"
            @load="loaded(Object.keys(scalespace).length * Object.keys(octave).length, Object.keys(octave).length)"
            :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
            spinner-color="white"
          >
            <div class="absolute-top text-center q-pa-xs" v-if="parseInt(o_number) === 0 && parseInt(s_number) === (Object.keys(octave).length - 1)">
              {{ 'Top of stack' }}
            </div>
            <div
              class="absolute-full text-subtitle2 flex flex-center scale_caption"
              v-if="s_number > 0 && s_number < Object.keys(octave).length - 2"
              v-on:click="showKeypointsForClickedScale($event)"
            >
              Show extrema
            </div>
          </q-img>
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
  data () {
    return {
      counter: 0
    }
  },
  props: {
    scalespace: Object,
    keypoints: Object,
    defaultWidth: Number,
    keypoints_randomUuid: String
  },
  methods: {
    loaded (maxScales, scalesPerOctave) {
      this.counter++
      if (this.counter === maxScales) {
        this.counter = 0
        setTimeout(() => {
          this.drawLines(scalesPerOctave)
        }, 2000)
      }
    },
    created () {
      this.removeLines()
    },
    drawLines (scalesPerOctave) {
      this.removeLines()
      var start = document.getElementsByClassName('scalespace-image scale_' + (scalesPerOctave - 3))
      var end = document.getElementsByClassName('scalespace-image scale_0')
      for (var i = 0; i < start.length - 1; i++) {
        var line = null
        var startElement = start[i],
          endElement = end[i + 1]
        if (i === 0) {
          // eslint-disable-next-line
          line = new window.LeaderLine(LeaderLine.pointAnchor(startElement, { y: '100%' }), LeaderLine.pointAnchor(endElement, { y: 0 }), { startSocket: 'bottom', endSocket: 'top', path: 'fluid', hide: true, size: 2, startLabel: 'take this...', endLabel: '...and halve it.' })
        } else {
          // eslint-disable-next-line
          line = new window.LeaderLine(LeaderLine.pointAnchor(startElement, { y: '100%' }), LeaderLine.pointAnchor(endElement, { y: 0 }), { startSocket: 'bottom', endSocket: 'top', path: 'fluid', hide: true, size: 2 })
        }
        this.$store.scalespaceLines.push(line)
      }
      if (this.$store.currentTab === 'scalespace_tab') {
        this.enableLines(true)
      } else {
        this.enableLines(false)
      }
    },
    enableLines (enable) {
      for (var i = 0; i < this.$store.scalespaceLines.length; i++) {
        if (enable) {
          this.$store.scalespaceLines[i].show('draw', { animOptions: { duration: 3000, timing: [0.5, 0, 1, 0.42] } })
        } else {
          this.$store.scalespaceLines[i].hide()
        }
      }
    },
    removeLines () {
      for (var i = 0; i < this.$store.scalespaceLines.length; i++) {
        this.$store.scalespaceLines[i].remove()
      }
      this.$store.scalespaceLines = []
    },
    showKeypointsForClickedScale ($event) {
      var caption = ''
      try {
        var classes = $event.target.offsetParent.offsetParent.className.split(' ')
        var octaveOfImage = parseInt(classes[2].split('_')[1])
        var scaleOfImage = parseInt(classes[3].split('_')[1])

        // Only show keypoints of first step
        var src = this.keypoints.scalespace[0][octaveOfImage][scaleOfImage] + '?' + this.keypoints_randomUuid
        if (src.split('?')[0] === 'undefined') throw new Error('undefined')
        caption = 'Octave: ' + (octaveOfImage + 1) + ' - Scale: ' + scaleOfImage
        this.$eventBus.$emit('showModalImage', src, caption)
      } catch (e) {
        console.log(e)
        caption = 'SIFT does not found any keypoints for this scale.\nOctave: ' + (octaveOfImage + 1) + ' - Scale: ' + scaleOfImage
        this.$eventBus.$emit('showModalImage', '', caption)
      }
    }
  }
}
</script>

<style lang="css">
  .tab_content_header {
    text-align: center;
    margin-bottom: 0;
  }

  .scalespace_octave_container {
    flex: 1 0 auto;
    margin-bottom: 50px;
  }

  .scalespace_container {
    display: flex;
    align-items: center;
    flex-direction: column;
  }

  .leader-line {
    white-space: pre-line;
    /* visibility: hidden; */
  }

  @media screen and (max-width: 720px) {
    .tab_content_header  {
      font-size: 16px
    }
  }

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
    background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
  }

  .modal-content {
    margin: auto;
    display: block;
    width: 80%;
    max-width: 50%;
  }

  .modal-content, #caption {
    animation-name: zoom;
    animation-duration: 0.6s;
  }

  @keyframes zoom {
    from {transform:scale(0)}
    to {transform:scale(1)}
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

  @media only screen and (max-width: 700px){
    .modal-content {
      width: 100%;
    }
  }

  .scalespace_container .scalespace_octave_container .scales {
    align-items: center;
    justify-content: center;
    display: flex;
    flex-direction: row;
    margin-bottom: 75px;
    margin-top: -12px
  }

  .scalespace_container .scales .scale_caption {
    opacity: 0;
  }

  .scalespace_container .scales .scale_caption:hover {
    opacity: 1;
    padding: 0;
    cursor: pointer;
  }
</style>
