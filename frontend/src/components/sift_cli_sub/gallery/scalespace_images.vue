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
      <div class="q-gutter-md column items-start">
        <div
          v-for="(scale, s_number) in octave"
          :id="'scale_' + s_number"
          :key="s_number"
          :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
        >
          <q-img
            :class="'octave_' + parseInt(o_number) + ' ' + 'scale_' + s_number"
            :src="scale + '?' + scalespace_randomUuid"
            @load="loaded(Object.keys(scalespace).length * Object.keys(octave).length)"
            :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
            spinner-color="white"
            @click="showKeypointsForClickedScale"
          >
          </q-img>
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
  data () {
    return {
      counter: 0
    }
  },
  props: {
    scalespace: Object,
    keypoints: Object,
    defaultWidth: Number,
    scalespace_randomUuid: String
  },
  methods: {
    loaded (maxScales) {
      this.counter++
      if (this.counter === maxScales) {
        setTimeout(() => {
          this.drawLines()
        }, 2000)
      }
    },
    created () {
      this.removeLines()
    },
    drawLines () {
      this.removeLines()
      var start = JQuery('.scalespace_container #scale_2')
      var end = JQuery('.scalespace_container #scale_0')
      for (var i = 0; i < start.length - 1; i++) {
        var line = null
        var startElement = start[i],
          endElement = end[i + 1]
        if (i === 0) {
          // eslint-disable-next-line
          line = new window.LeaderLine(startElement, endElement, { hide: true, size: 2, startLabel: 'take this...', endLabel: '...and halve it.' })
        } else {
          // eslint-disable-next-line
          line = new window.LeaderLine(startElement, endElement, { hide: true, size: 2 })
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
    showKeypointsForClickedScale (img) {
      try {
        // var classes = img.target.parentElement.className.split(' ')
        // var octaveOfImage = parseInt(classes[2].split('_')[1])
        // var scaleOfImage = parseInt(classes[3].split('_')[1])
      } catch (e) {
      }
    }
  }
}
</script>

<style lang="css">
  .scalespace_octave_container {
    flex: 1 0 auto;
  }

  .scalespace_container {
    display: flex;
    align-items: center;
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
</style>
