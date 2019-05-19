<template>
  <q-page padding>
    <!-- content -->
    <p class="test" :style="{color: color}">hello world</p>
    <hello-world-component></hello-world-component>
    <q-color-picker v-model="color"></q-color-picker>
    <input type="text" name="" value="" v-model="color">
    <button type="button" name="button" @click="buttonFunction">TestButton</button>
    <input type="text" name="" value="" v-model="link">
    <a :href="testComputed">{{link}}</a>
  </q-page>
</template>

<script>
import helloWorldComponent from '../components/helloWorldComponent.vue'
import { QColorPicker } from 'quasar'

export default {
  // name: 'PageName'
  components: {
    helloWorldComponent,
    QColorPicker
  },
  data () {
    return {
      color: '#FFFFFF',
      link: 'google.de'
    }
  },
  methods: {
    buttonFunction: function () {
      this.color = '#7ea842'
    }
  },
  computed: {
    testComputed: function () {
      return 'http://www.' + this.link
    }
  }
}
</script>

<style>
.test {
  color: #ea3521;
  font-size: 36px;
}
</style>
