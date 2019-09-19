<template>
  <div class="input_container">
    <div class="q-pa-md">
      <form @submit.prevent.stop="submit" @reset.prevent.stop="reset" class="q-gutter-md">
        <div class="input-picture">
          <picture-input
            ref="pictureInput"
            @change="onChange"
            width="300"
            height="300"
            margin="16"
            zIndex="0"
            accept="image/jpeg,image/png"
            size="10"
            buttonClass="btn"
            :customStrings="{
              upload: '<h1>Bummer!</h1>',
              drag: 'Input image</br>(optional)',
              change: 'Change image'
            }">
          </picture-input>
          <div class="image_type">*Only .png files are allowed.</div>
        </div>

        <div class="">
          <div class="input-category-header flex-box">
            <div class="flex-box-column">
              <div class="flex-child">
                <h4>Quantity</h4>
                <div class="input-child-headline">Number of octaves</div>
                <q-input class="input-child-field" v-model="siftCliParams.ss_noct" filled type="text" hint="How many octaves should be produced?" />
                <div class="input-child-headline">Number of intervalls per octave</div>
                <q-input class="input-child-field" v-model="siftCliParams.ss_nspo" filled type="text" hint="Sets the value 'S'. " />
              </div>
            </div>
            <div class="flex-box-column">
              <div class="flex-child">
                <h4>Image</h4>
                <div class="input-child-headline">Sampling distance</div>
                <q-input class="input-child-field" v-model="siftCliParams.ss_dmin" filled type="text" hint="Distance between sample points (pixels)" />
                <div class="input-child-headline">Blur Level</div>
                <q-input class="input-child-field" v-model="siftCliParams.ss_smin" filled type="text" hint="Sets the Gaussian value (sigma) for blurring an image" />
                <div class="input-child-headline">Blur Level in Input Image</div>
                <q-input class="input-child-field" v-model="siftCliParams.ss_sin" filled type="text" hint="Level of blur in the input image" />
              </div>
            </div>
            <div class="flex-box-column">
              <div class="flex-child">
                <h4>Threshold</h4>
                <div class="input-child-headline">DoG</div>
                <q-input class="input-child-field" v-model="siftCliParams.thresh_dog" filled type="text" hint="Threshold over the DoG response" />
                <div class="input-child-headline">Principle curvature ratio</div>
                <q-input class="input-child-field" v-model="siftCliParams.thresh_edge" filled type="text" hint="Threshold over the ratio of principal curvature"/>
                <div class="input-child-headline">Threshold for orientation histogram</div>
                <q-input class="input-child-field" v-model="siftCliParams.ori_thresh" filled type="text" hint="Threshold for considering local maxima in the orientation histogram"/>
              </div>
            </div>
            <div class="flex-box-column">
              <div class="flex-child">
                <h4>Orientation</h4>
                <div class="input-child-headline">Locality of gradient</div>
                <q-input class="input-child-field" v-model="siftCliParams.ori_lambda" filled type="text" hint="Sets how local is the analysis of the gradient distribution" />
                <div class="input-child-headline">Number of bins in orientation histogram</div>
                <q-input class="input-child-field" v-model="siftCliParams.ori_nbins" filled type="text" hint="Number of bins in the orientation histogram" />
              </div>
            </div>
            <div class="flex-box-column">
              <div class="flex-child">
                <h4>Descriptor</h4>
                <div class="input-child-headline">Number of histograms</div>
                <q-input class="input-child-field" v-model="siftCliParams.descr_nhist" filled type="text" hint="Number of histograms per dimension" />
                <div class="input-child-headline">Number of bins in histogram</div>
                <q-input class="input-child-field" v-model="siftCliParams.descr_nori" filled type="text" hint="Number of bins in each histogram" />
                <div class="input-child-headline">Locality of Descriptor</div>
                <q-input class="input-child-field" v-model="siftCliParams.descr_lambda" filled type="text" hint="Sets how local is the analysis of the gradient distribution" />
              </div>
            </div>
          </div>
        </div>

        <div class="sift_cli_buttons q-gutter-md row items-start">
          <!-- <q-toggle v-model="drawType" /> -->
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
          <q-btn id="sift_cli_button_execute" label="Run Sift Algorithm" type="submit" color="primary" />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { QInput } from 'quasar'
import axios from 'axios'
import PictureInput from 'vue-picture-input'

var siftCliParamsDefault = {
  ss_noct: '3', // number of octaves
  ss_nspo: '3', // number of scales per octave
  ss_dmin: '0.5', // the sampling distance in the first octave
  ss_smin: '0.8', // blur level on the seed image
  ss_sin: '0.5', // assumed level of blur in the input image
  thresh_dog: '0.03', // threshold over the DoG response
  thresh_edge: '10', // threshold over the ratio of principal curvature
  ori_nbins: '36', // number of bins in the orientation histogram
  ori_thresh: '0.8', // threshold for considering local maxima in the orientation histogram
  ori_lambda: '1.5', // sets how local is the analysis of the gradient distribution
  descr_nhist: '4', // number of histograms per dimension
  descr_nori: '8', // number of bins in each histogram
  descr_lambda: '16', // sets how local the descriptor is
  verb_keys: '1', // flag to output the intermediary sets of keypoints
  verb_ss: '1' // flag to output the scalespaces (Gaussian and DoG)
}

export default {
  components: {
    QInput,
    PictureInput
  },
  data () {
    return {
      siftCliParams: Object.assign({}, siftCliParamsDefault),
      drawType: true
    }
  },
  methods: {
    siftCli_execute (inputImageName = 'adam1.png') {
      this.$eventBus.$emit('showLoader') // Beginn
      this.$store.inputImageName = inputImageName.split('.').slice(0, -1).join('.')
      document.getElementById('sift_cli_button_execute').disabled = true
      var siftCliParams = this.siftCliParams
      axios.get('http://localhost:5000/sift_cli/execute', {
        params: {
          inputImageName: inputImageName,
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
        .then(() => {
          console.log('SIFT finished.')
          this.$eventBus.$emit('buildGallery', this.drawType)
        })
        .catch((error) => {
          console.error(error)
          this.$eventBus.$emit('hideLoader')
          document.getElementById('sift_cli_button_execute').disabled = false
        })
    },
    submit () {
      if (this.image) {
        var file = this.image
        var formData = new FormData()
        formData.append('file', file)
        const config = {
          headers: {
            'Content-type': 'multipart/form-data'
          }
        }
        axios.post('http://localhost:5000/sift_cli/upload_image', formData, config)
          .then((res) => {
            var filename = res.data
            if (filename) {
              console.log('Image: ' + filename + ' uploaded successfully ✨')
              console.log('Start SIFT with uploaded image ✨')
              this.siftCli_execute(filename)
            }
          })
          .catch((error) => {
            console.error(error)
          })
      } else {
        console.log('Start SIFT with default image (adam1.png) ✨')
        this.siftCli_execute()
      }
    },
    reset () {
      Object.assign(this.siftCliParams, siftCliParamsDefault) // Resets the parameter values
      this.drawType = true
      this.image = ''
      this.$refs.pictureInput.removeImage()
    },
    onChange () {
      if (this.$refs.pictureInput.file) {
        this.image = this.$refs.pictureInput.file
      } else {
        console.log('FileReader API not supported: use the <form>, Luke!')
      }
    }
  }
}
</script>

<style>
  .input-picture {
    margin-bottom: 50px;
  }

  .input-container-collection {
    display: flex;
    flex-direction: row;
  }

  .input-container {
    margin-right: 50px;
    margin-bottom: 50px;
    display: block;
    flex: 0 1 auto;
  }

  .input-container-box {
    display: flex;
    flex-direction: column;
  }

  .input_container .items-start {
    display: -webkit-inline-flex !important;
    flex: 1;
  }

  .sift_cli_buttons {
    position: fixed;
    right: 0;
    top: 0;
    margin-right: 32px;
  }

  .image_type {
    text-align: center;
    padding-top: 5px;
    color: #d2d2d2;
    font-variant: super;
  }

  .input-category-header {
    margin-bottom: 50px;
    margin-top: 0;
  }

  .flex-box {
    display: flex;
    flex-direction: row;
    text-align: center;
    flex-wrap: wrap;
  }

  .flex-box-column {
    display: flex;
    flex-direction: column;
    flex: 1;
    flex-wrap: wrap;
    margin-right: 15px;
    margin-left: 15px;
    border-radius: 55pt;
    background-color: #f4f4f4;
    align-self: flex-start;
  }

  .flex-child {
    flex: 1;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 50px;
  }

  .flex-child h4 {
    margin-bottom: 15px;
  }

  .input-child {
    margin-bottom: 50px;
  }

  .input-child-headline {
    font-size: 16pt;
    margin-bottom: 0;
  }

  .input-child-field {
    margin-top: 15px;
    margin-bottom: 75px;
  }
</style>
