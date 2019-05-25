<template>
  <q-page>
    <!-- content -->
    <button class="start-sift" type="button" name="button" @click="getMessage">Start Sift Algorithm</button>
  </q-page>
</template>

<script>

export default {
  methods: {
    startSift: function () {
      console.log('asdsd')
    }
  }
}
</script>

<style>
.start-sift {
  font-size: 20px;
  margin: 5px 0px 0px 5px;
}
</style>
