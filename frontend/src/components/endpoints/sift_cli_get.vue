<template>
  <button class="siftCli-button-execute" type="button" name="button" @click="this.siftCli_execute">Start Sift Algorithm</button>
</template>

<script>
import axios from 'axios'

export default {
  name: 'siftCli',
  methods: {
    siftCli_execute () {
      const path = 'http://localhost:5000/get'
      axios.get(path)
        .then((res) => {
          this.msg = res.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    }
  }
}
</script>

<style>
.siftCli-button-execute {
  font-size: 20px;
  margin: 5px 0px 0px 5px;
}
</style>
