import Vue from 'vue'
import Vuex from 'vuex'
import VueZoomer from 'vue-zoomer'

import example from './module-example'

Vue.use(Vuex)
Vue.use(VueZoomer)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      example
    },
    state: {
      image: ''
    }
  })

  return Store
}
