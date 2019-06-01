<template>
  <div class="siftCli-div">
    <form @submit="siftCli_execute">
      <input type="text" v-model="ss_noct" placeholder="Octaves">
      <input type="text" v-model="ss_nspo" placeholder="Scales">
      <input type="text" v-model="ss_dmin" placeholder="Scales">
      <input type="text" v-model="ss_smin" placeholder="Scales">
      <input type="text" v-model="ss_sin" placeholder="Scales">
      <input type="text" v-model="thresh_dog" placeholder="Scales">
      <input type="text" v-model="thresh_edge" placeholder="Scales">
      <input type="text" v-model="ori_nbins" placeholder="Scales">
      <input type="text" v-model="ori_thresh" placeholder="Scales">
      <input type="text" v-model="ori_lambda" placeholder="Scales">
      <input type="text" v-model="descr_nhist" placeholder="Scales">
      <input type="text" v-model="descr_nori" placeholder="Scales">
      <input type="text" v-model="descr_lambda" placeholder="Scales">

      <button class="siftCli-button-execute" type="button" name="button" @click="this.siftCli_execute">Start Sift Algorithm</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'siftCli',
  data () {
    return {
      ss_noct: '8', // number of octaves
      ss_nspo: '3', // number of scales per octave
      ss_dmin: '0.5', // number of scales per octave
      ss_smin: '0.8', // number of scales per octave
      ss_sin: '0.5', // number of scales per octave
      thresh_dog: '0.0133', // number of scales per octave
      thresh_edge: '10', // number of scales per octave
      ori_nbins: '36', // number of scales per octave
      ori_thresh: '0.8', // number of scales per octave
      ori_lambda: '1.5', // number of scales per octave
      descr_nhist: '4', // number of scales per octave
      descr_nori: '8', // number of scales per octave
      descr_lambda: '6', // number of scales per octave
      verb_keys: '1', // number of scales per octave
      verb_ss: '1' // number of scales per octave
    }
  },
  methods: {
    siftCli_execute (e) {
      e.preventDefault()
      axios.get('http://localhost:5000/sift_cli', {
        params: {
          ss_noct: (this.ss_noct === '' ? this.ss_noct = '8' : this.ss_noct),
          ss_nspo: (this.ss_nspo === '' ? this.ss_nspo = '3' : this.ss_nspo),
          ss_dmin: (this.ss_dmin === '' ? this.ss_dmin = '0.5' : this.ss_dmin),
          ss_smin: (this.ss_smin === '' ? this.ss_smin = '0.8' : this.ss_smin),
          ss_sin: (this.ss_sin === '' ? this.ss_sin = '0.5' : this.ss_sin),
          thresh_dog: (this.thresh_dog === '' ? this.thresh_dog = '0.0133' : this.thresh_dog),
          thresh_edge: (this.thresh_edge === '' ? this.thresh_edge = '10' : this.thresh_edge),
          ori_nbins: (this.ori_nbins === '' ? this.ori_nbins = '36' : this.ori_nbins),
          ori_thresh: (this.ori_thresh === '' ? this.ori_thresh = '0.8' : this.ori_thresh),
          ori_lambda: (this.ori_lambda === '' ? this.ori_lambda = '1.5' : this.ori_lambda),
          descr_nhist: (this.descr_nhist === '' ? this.descr_nhist = '4' : this.descr_nhist),
          descr_nori: (this.descr_nori === '' ? this.descr_nori = '8' : this.descr_nori),
          descr_lambda: (this.descr_lambda === '' ? this.descr_lambda = '6' : this.descr_lambda),
          verb_keys: (this.verb_keys === '' ? this.verb_keys = '0' : this.verb_keys),
          verb_ss: (this.verb_ss === '' ? this.verb_ss = '0' : this.verb_ss)
        }
      })
        .then((res) => {
          console.log(res.data)
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
.siftCli-div {
  margin: 5px 0px 0px 5px;
}

.siftCli-button-execute {

}
</style>
