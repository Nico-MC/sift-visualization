<template lang="html">
  <div class="dog_container">
    <div class="dog_octave_container" v-for="(octave, o_number) in dogs" :key="'dog_' + o_number">
      <p class="tab_content_header q-title text-h6">
        Octave: {{ parseInt(o_number) + 1 }}
      </p>
      <div class="q-gutter-md column items-start">
        <div
          v-for="(dog, s_number) in octave"
          :id="o_number"
          :key="s_number"
        >
          <q-img
            :src="'http://localhost:5000/static/dog/' + dog + '?' + dogs_randomUuid"
            style="width: 250px"
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

export default {
  components: {
    QImg
  },
  props: {
    dogs: Object,
    defaultWidth: Number,
    dogs_randomUuid: String
  }
}
</script>

<style lang="css" scoped>
  .dog_octave_container {
    flex: 1 1 auto;
  }

  .dog_container {
    display: flex;
    align-items: center;
  }
</style>
