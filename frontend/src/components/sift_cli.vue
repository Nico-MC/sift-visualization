<template>
  <div>
    <transition name="bounce">
      <q-spinner-grid
        color="primary"
        size="4em"
        v-if="showLoader"
        class="siftCli_loader"
      />
    </transition>
    <siftCliInput></siftCliInput>
    <siftCliOutput></siftCliOutput>
  </div>
</template>

<script>
import siftCliInput from 'components/sift_cli_sub/sift_cli_input.vue'
import siftCliOutput from 'components/sift_cli_sub/sift_cli_gallery.vue'
import { QSpinnerGrid } from 'quasar'

export default {
  components: {
    siftCliInput,
    siftCliOutput,
    QSpinnerGrid
  },
  data () {
    return {
      showLoader: false
    }
  },
  created () {
    this.$eventBus.$on('showLoader', () => {
      this.showLoader = true
    })
    this.$eventBus.$on('hideLoader', () => {
      this.showLoader = false
    })
  }
}
</script>

<style media="screen">
  .siftCli_loader {
    position: fixed;
    right: 0;
    bottom: 0;
    margin: 15px;
    z-index: 9999;
  }

  .bounce-enter-active {
    animation: bounce-in .5s;
  }
  .bounce-leave-active {
    animation: bounce-in .5s reverse;
  }
  @keyframes bounce-in {
    0% {
      transform: scale(0);
    }
    50% {
      transform: scale(1.5);
    }
    100% {
      transform: scale(1);
    }
  }
</style>
