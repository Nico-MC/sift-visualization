<template>
  <div style="padding: 100px;">
    <div>
      zoomed: {{ zoomed }}
      <button @click="$refs.zoomer.zoomIn()">+</button>
      <button @click="$refs.zoomer.zoomOut()">-</button>
    </div>
    <v-zoomer
      ref="zoomer"
      style="width: 500px; height: 500px; border: solid 1px silver;"
      :max-scale="10"
      :zoomed.sync="zoomed"
    >
      <img src="../assets/landscape-1.jpg" style="object-fit: contain; width: 100%; height: 100%;">
    </v-zoomer>
  </div>
</template>

<script>
export default {
  data () {
    return {
      zoomed: false,
    }
  },
}
</script>
