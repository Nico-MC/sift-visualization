<template lang="html">
  <div class="dog_container">
    <div class="dog_octave_container" v-for="(octave, o_number) in dogs" :key="'dog_' + o_number">
      <p class="tab_content_header q-title text-h6">
        Octave: {{ parseInt(o_number) + 1 }}
      </p>
      <div class="scales_and_dogs">
        <div class="q-gutter-md column items-start scales">
          <div
            v-for="(scale, s_number) in scalespace[o_number]"
            :id="o_number"
            :key="s_number"
          >
            <q-img
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
            :id="o_number"
            :key="d_number"
          >
            <q-img
              :src="'http://localhost:5000/static/dog/' + dog + '?' + dogs_randomUuid"
              :style="{ width: defaultWidth / (Math.pow(2, parseInt(o_number))) + 'px' }"
              spinner-color="white"
            >
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
    dogs: Object,
    scalespace: Object,
    defaultWidth: Number,
    dogs_randomUuid: String
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
</style>
