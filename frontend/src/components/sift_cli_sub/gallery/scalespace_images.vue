<template lang="html">
  <div class="scalespace_container">
    <div class="scalespace_octave_container"
      v-for="(octave, o_number) in scalespace"
      :key="'scalespace_' + o_number"
      v-for-callback="{key: o_number, array: scalespace, callback: callback}"
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
        >
          <q-img
            :src="'http://localhost:5000/static/scalespace/' + scale + '?' + scalespace_randomUuid"
            :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
            spinner-color="white"
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
  props: {
    scalespace: Object,
    defaultWidth: Number,
    scalespace_randomUuid: String
  },
  methods: {
    callback (numberOfScales) {
      this.removeLines()
      setTimeout(function () {
        var start = JQuery('.scalespace_container #scale_2')
        var end = JQuery('.scalespace_container #scale_0')
        for (var i = 0; i < start.length - 1; i++) {
          var startElement = start[i],
            endElement = end[i + 1]
          if (i === 0) {
            // eslint-disable-next-line
            var line = new window.LeaderLine(startElement, endElement, { hide: true, size: 2, startLabel: 'take this...', endLabel: '...and halve it.' })
          } else {
            // eslint-disable-next-line
            var line = new window.LeaderLine(startElement, endElement, { hide: true, size: 2 })
          }
          line.show('draw', { duration: 300, timing: [1, 1, 1, 1] })
          this.$store.lines.push(line)
        }
      }.bind(this), 5000)
    },
    enableLines (enable) {
      for (var i = 0; i < this.$store.lines.length; i++) {
        if (enable) {
          this.$store.lines[i].show()
        } else {
          this.$store.lines[i].hide()
        }
      }
    },
    removeLines () {
      for (var i = 0; i < this.$store.lines.length; i++) {
        this.$store.lines[i].remove()
      }
      this.$store.lines = []
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
          element.callback(Object.values(element.array)[0].length)
        }
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
  }

  @media screen and (max-width: 720px) {
    .tab_content_header  {
      font-size: 16px
    }
  }
</style>
