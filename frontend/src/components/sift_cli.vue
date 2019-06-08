<template>
  <div>
    <siftCliInput></siftCliInput>
    <siftCliOutput></siftCliOutput>
  </div>
</template>

<script>
import siftCliInput from '../components/sift_cli_sub/sift_cli_input.vue'
import siftCliOutput from '../components/sift_cli_sub/sift_cli_gallery.vue'

export default {
  components: {
    siftCliInput,
    siftCliOutput
  }
}
</script>
