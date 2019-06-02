<template>
  <div class="q-pa-md">
    <div class="q-gutter-md row items-start">
      <form @submit.prevent.stop="siftCli_execute" @reset.prevent="reset()" class="q-gutter-md">
        <q-input v-model="siftCliParams.ss_noct" filled type="text" hint="Octaves" />
        <q-input v-model="siftCliParams.ss_nspo" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.ss_dmin" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.ss_smin" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.ss_sin" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.thresh_dog" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.thresh_edge" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.ori_nbins" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.ori_thresh" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.ori_lambda" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.descr_nhist" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.descr_nori" filled type="text" hint="Scales" />
        <q-input v-model="siftCliParams.descr_lambda" filled type="text" hint="Scales" />
        <div>
          <q-btn label="Start Sift Algorithm" type="submit" color="primary" />
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { QInput } from 'quasar'
import axios from 'axios'

var siftCliParamsDefault = {
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

export default {
  components: {
    QInput
  },
  data () {
    return {
      siftCliParams: Object.assign({}, siftCliParamsDefault)
    }
  },
  methods: {
    siftCli_execute (e) {
      e.preventDefault()
      var siftCliParams = this.siftCliParams
      axios.get('http://localhost:5000/sift_cli', {
        params: {
          ss_noct: (siftCliParams.ss_noct === '' ? siftCliParams.ss_noct = siftCliParamsDefault.ss_noct : siftCliParams.ss_noct),
          ss_nspo: (siftCliParams.ss_nspo === '' ? siftCliParams.ss_nspo = siftCliParamsDefault.ss_nspo : siftCliParams.ss_nspo),
          ss_dmin: (siftCliParams.ss_dmin === '' ? siftCliParams.ss_dmin = siftCliParamsDefault.ss_dmin : siftCliParams.ss_dmin),
          ss_smin: (siftCliParams.ss_smin === '' ? siftCliParams.ss_smin = siftCliParamsDefault.ss_smin : siftCliParams.ss_smin),
          ss_sin: (siftCliParams.ss_sin === '' ? siftCliParams.ss_sin = siftCliParamsDefault.ss_sin : siftCliParams.ss_sin),
          thresh_dog: (siftCliParams.thresh_dog === '' ? siftCliParams.thresh_dog = siftCliParamsDefault.thresh_dog : siftCliParams.thresh_dog),
          thresh_edge: (siftCliParams.thresh_edge === '' ? siftCliParams.thresh_edge = siftCliParamsDefault.thresh_edge : siftCliParams.thresh_edge),
          ori_nbins: (siftCliParams.ori_nbins === '' ? siftCliParams.ori_nbins = siftCliParamsDefault.ori_nbins : siftCliParams.ori_nbins),
          ori_thresh: (siftCliParams.ori_thresh === '' ? siftCliParams.ori_thresh = siftCliParamsDefault.ori_thresh : siftCliParams.ori_thresh),
          ori_lambda: (siftCliParams.ori_lambda === '' ? siftCliParams.ori_lambda = siftCliParamsDefault.ori_lambda : siftCliParams.ori_lambda),
          descr_nhist: (siftCliParams.descr_nhist === '' ? siftCliParams.descr_nhist = siftCliParamsDefault.descr_nhist : siftCliParams.descr_nhist),
          descr_nori: (siftCliParams.descr_nori === '' ? siftCliParams.descr_nori = siftCliParamsDefault.descr_nori : siftCliParams.descr_nori),
          descr_lambda: (siftCliParams.descr_lambda === '' ? siftCliParams.descr_lambda = siftCliParamsDefault.descr_lambda : siftCliParams.descr_lambda),
          verb_keys: (siftCliParams.verb_keys === '' ? siftCliParams.verb_keys = siftCliParamsDefault.verb_keys : siftCliParams.verb_keys),
          verb_ss: (siftCliParams.verb_ss === '' ? siftCliParams.verb_ss = siftCliParamsDefault.verb_ss : siftCliParams.verb_ss)
        }
      })
        .then((res) => {
          console.log(res.data)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
    reset (e) {
      Object.assign(this.siftCliParams, siftCliParamsDefault)
    }
  }
}
</script>
