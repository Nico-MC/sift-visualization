<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { openURL, QLayout } from 'quasar'

export default {
  name: 'MyLayout',
  components: {
    QLayout
  },
  data () {
    return {
      leftDrawerOpen: this.$q.platform.is.desktop
    }
  },
  methods: {
    openURL
  }
}
</script>

<style>
</style>
