<template>
  <v-row>
    <v-col cols="12" md="6">
      <v-card class="elevation-0">
        <v-card-title class="headline"> Linear Regression </v-card-title>
        <v-card-text>
          <v-form ref="linearForm" v-model="valid" lazy-validation>
            <v-text-field
              v-model="size"
              :rules="sizeRules"
              label="Size"
              required
            ></v-text-field>

            <v-text-field
              v-model="distance"
              :rules="distanceRules"
              label="Distance from city center"
              required
            ></v-text-field>

            <v-text-field
              v-model="rooms"
              :rules="roomsRules"
              label="Number of rooms"
              required
            ></v-text-field>

            <v-select
              v-model="old_new"
              :items="items"
              :rules="[(v) => !!v || 'Item is required']"
              label="Build period"
              required
            ></v-select>

            <v-btn :disabled="!valid" class="mr-4" @click="predict_linear">
              Predict
            </v-btn>

            <v-btn class="mr-4" @click="reset"> Reset Form </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card class="elevation-0">
        <v-card-title class="headline"> k-Nearest Neighbors </v-card-title>
        <v-card-text>
          <v-form ref="knnForm" v-model="validKnn" lazy-validation>
            <v-text-field
              v-model="knn_size"
              :rules="sizeRules"
              label="Size"
              required
            ></v-text-field>

            <v-text-field
              v-model="knn_distance"
              :rules="distanceRules"
              label="Distance from city center"
              required
            ></v-text-field>

            <v-text-field
              v-model="knn_rooms"
              :rules="roomsRules"
              label="Number of rooms"
              required
            ></v-text-field>

            <v-select
              v-model="knn_old_new"
              :items="items"
              :rules="[(v) => !!v || 'Item is required']"
              label="Build period"
              required
            ></v-select>

            <v-btn :disabled="!validKnn" class="mr-4" @click="predict_knn">
              Predict
            </v-btn>

            <v-btn class="mr-4" @click="reset_knn"> Reset Form </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card class="elevation-0">
        <v-card-title class="headline">
          Linear Regression Prediction
        </v-card-title>
        <v-card-text>
          <l-map
            style="height: 500px; width: 100%"
            :zoom="zoom"
            :center="center"
            :options="{ zoomControl: false }"
          >
            <l-control-zoom position="bottomright"></l-control-zoom>
            <l-control position="topleft">
              <v-card v-if="regression_result !== null">
                <v-card-text>
                  <!-- <p>
                    {{ parseInt(regression_result).toLocaleString() }} &euro;
                  </p> -->
                  <v-simple-table>
                    <template #default>
                      <tbody>
                        <tr>
                          <td
                            colspan="2"
                            style="text-align: center"
                            class="headline"
                          >
                            {{ parseInt(regression_result).toLocaleString() }}
                            &euro;
                          </td>
                        </tr>
                        <tr>
                          <td>Size</td>
                          <td>{{ size }}</td>
                        </tr>
                        <tr>
                          <td>Rooms</td>
                          <td>{{ rooms }}</td>
                        </tr>
                        <tr>
                          <td>Distance from center</td>
                          <td>{{ distance }}</td>
                        </tr>
                        <tr>
                          <td>Build period</td>
                          <td>{{ old_new }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>

                  <!-- <p>Size: {{ size }}</p>
                  <p>Distance from center: {{ distance }}</p>
                  <p>Rooms: {{ rooms }}</p>
                  <p>Build perion: {{ old_new }}</p> -->
                </v-card-text>
              </v-card>
            </l-control>
            <l-tile-layer :url="url"></l-tile-layer>
            <l-circle-marker :lat-lng="center" :radius="2" color="#66D2D6" />
            <l-circle
              v-if="regression_result !== null"
              :lat-lng="center"
              :radius="parseFloat(distance) * 1000"
              color="#FBC740"
              fill-color="#FBC740"
            />
          </l-map>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card class="elevation-0">
        <v-card-title class="headline"> k-Nearest Neighbors </v-card-title>
        <v-card-text>
          <l-map
            style="height: 500px; width: 100%"
            :zoom="zoom"
            :center="center"
            :options="{ zoomControl: false }"
          >
            <l-control-zoom position="bottomright"></l-control-zoom>
            <l-control position="topleft">
              <v-card v-if="knn_result !== null">
                <v-card-text>
                  <v-simple-table>
                    <template #default>
                      <tbody>
                        <tr>
                          <td
                            colspan="2"
                            style="text-align: center"
                            class="headline"
                          >
                            {{ parseInt(knn_result).toLocaleString() }}
                            &euro;
                          </td>
                        </tr>
                        <tr>
                          <td>Size</td>
                          <td>{{ knn_size }}</td>
                        </tr>
                        <tr>
                          <td>Rooms</td>
                          <td>{{ knn_rooms }}</td>
                        </tr>
                        <tr>
                          <td>Distance from center</td>
                          <td>{{ knn_distance }}</td>
                        </tr>
                        <tr>
                          <td>Build period</td>
                          <td>{{ knn_old_new }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-card-text>
              </v-card>
            </l-control>
            <l-tile-layer :url="url"></l-tile-layer>
            <l-circle-marker :lat-lng="center" :radius="2" color="#66D2D6" />
            <l-circle
              v-if="knn_result !== null"
              :lat-lng="center"
              :radius="parseFloat(knn_distance) * 1000"
              color="#FBC740"
              fill-color="#FBC740"
            />
          </l-map>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { LMap, LTileLayer } from 'vue2-leaflet'
export default {
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      url: 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
      zoom: 13,
      center: [44.8159136, 20.4607347],
      valid: true,
      validKnn: true,
      size: '',
      knn_size: '',
      sizeRules: [
        (v) => !!v || 'Size is required',
        (v) => (v && !isNaN(v)) || 'Size must be a number',
      ],
      knn_distance: '',
      distance: '',
      distanceRules: [
        (v) => !!v || 'Distance is required',
        (v) => (v && !isNaN(v)) || 'Distance must be a number',
      ],
      knn_rooms: '',
      rooms: '',
      roomsRules: [
        (v) => !!v || 'Rooms is required',
        (v) => (v && !isNaN(v)) || 'Rooms must be a number',
      ],
      knn_old_new: null,
      old_new: null,
      items: ['Old', 'New', 'No data'],
      regression_result: null,
      knn_result: null,
    }
  },
  methods: {
    reset() {
      this.$refs.linearForm.reset()
    },
    reset_knn() {
      this.$refs.knnForm.reset()
    },
    async predict_linear() {
      const form = {
        size: this.size,
        distance: this.distance,
        rooms: this.rooms,
        old: this.old_new === 'Old' ? 1 : 0,
        new: this.old_new === 'New' ? 1 : 0,
        nodata: this.old_new === 'No data' ? 1 : 0,
      }
      const result = await this.$axios.post('/linear_regression', form)
      this.regression_result = result.data
    },
    async predict_knn() {
      const form = {
        size: this.knn_size,
        distance: this.knn_distance,
        rooms: this.knn_rooms,
        old_new: this.mapOldNew(),
      }
      const result = await this.$axios.post('/knn', form)
      this.knn_result = result.data
    },
    mapOldNew() {
      if (this.knn_old_new === 'Old') {
        return -1
      }
      if (this.knn_old_new === 'New') {
        return 1
      }
      if (this.knn_old_new === 'No data') {
        return 0
      }
    },
  },
}
</script>
