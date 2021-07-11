import Vue from 'vue'
import {
  LMap,
  LTileLayer,
  LMarker,
  LCircleMarker,
  LCircle,
  LControlZoom,
  LControl,
} from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'

Vue.component(LMap)
Vue.component(LTileLayer)
Vue.component(LMarker)
Vue.component('LCircleMarker', LCircleMarker)
Vue.component('LCircle', LCircle)
Vue.component('LControlZoom', LControlZoom)
Vue.component('LControl', LControl)
