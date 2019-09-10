<template lang="html">
  <div>
    <div id="myModal" class="modal">
      <span class="close">&times;</span>
      <img class="modal-content" id="img01">
      <p id="keypoint_caption"></p>
    </div>
    <p class="tab_content_header q-title text-h4">
      Step {{ step_number + ': ' + step_name}}
    </p>
    <div
      class="q-gutter-md column items-start"
      v-for="(octave, o_number) in step"
      :key="'octave_' + o_number"
    >
      <div>
        <p class="octave_headline">
          Octave: {{ parseInt(o_number) + 1 }}
        </p>
        <div class="scale_container">
          <div
            class="keypoint_image"
            v-for="(scale, s_number) in octave"
            :key="'scale_' + s_number"
          >
            <q-img
              :src="'http://localhost:5000/' + scale.scale + '?' + scale.randomUuid"
              spinner-color="white"
              @click="zoomImg"
              style="width: 360px"
              :class="'octave_' + o_number + ' ' + 'scale_' + s_number"
              :data-stepName="step_name"
              :data-stepNumber="step_number"
            >
              <div class="absolute-bottom-right text-subtitle2">
                {{ parseInt(s_number) + 1 }}
              </div>
            </q-img>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { QImg } from 'quasar'

export default {
  components: {
    QImg
  },
  props: {
    step: Object,
    defaultWidth: Number,
    step_number: Number,
    step_name: String
  },
  methods: {
    zoomImg (img) {
      var classes = img.target.parentElement.className.split(' ')
      var octaveOfImage = parseInt(classes[2].split('_')[1]) + 1
      var scaleOfImage = parseInt(classes[3].split('_')[1]) + 1
      var stepOfImage = img.target.parentElement.dataset.stepname
      var stepNumberOfImage = img.target.parentElement.dataset.stepnumber
      document.getElementById('keypoint_caption').innerHTML = 'Step ' +
      stepNumberOfImage + ': ' + stepOfImage + '<br />Octave: ' + octaveOfImage + ' - Scale: ' + scaleOfImage

      var modal = document.getElementById('myModal')
      var modalImg = document.getElementById('img01')
      modal.style.display = 'block'
      var srcUrl = img.srcElement.previousSibling.style.backgroundImage
      var src = srcUrl.substring(srcUrl.lastIndexOf('http'), srcUrl.lastIndexOf(')'))
      modalImg.src = src
      modal.onclick = function () {
        if (modal.style.display === 'block') modal.style.display = 'none'
        else modal.style.display = 'block'
      }
    }
  }
}
</script>

<style lang="css">
  #keypoint_caption {
    text-align: center;
    margin-top: 10px;
    font-size: 18pt;
    color: white;
  }

  .keypoint_image {
    margin-right: 15px;
    margin-bottom: 15px;
    transition: all .2s ease-in-out;
    width: 360px;
  }

  .keypoint_image:hover {
    transform: scale(1.03);
    z-index: 1;
  }

  .octave_headline {
    margin-bottom: 0;
    font-size: 14pt;
  }

  .scale_container {
    display: flex;
    flex-wrap: wrap;
  }

  .modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 9; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
  }

  .modal-content {
    margin: auto;
    display: block;
    width: 80%;
    max-width: 50%;
  }

  .modal-content, #caption {
    animation-name: zoom;
    animation-duration: 0.6s;
  }

  @keyframes zoom {
    from {transform:scale(0)}
    to {transform:scale(1)}
  }

  .close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #f1f1f1;
    font-size: 40px;
    font-weight: bold;
    transition: 0.3s;
  }

  .close:hover,
  .close:focus {
    color: #bbb;
    text-decoration: none;
    cursor: pointer;
  }

  @media only screen and (max-width: 700px){
    .modal-content {
      width: 100%;
    }
  }
</style>
