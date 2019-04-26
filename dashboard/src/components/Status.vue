<template>
<el-col>
     <span v-for="item in items" :key="item">
     <el-badge :value="item.ct" class="badgeitem" type="primary">
        <!-- <el-col> -->
        <span>
        <el-button v-if="item.st" size="small" class="el-icon-circle-check"> {{item.id}}</el-button>
        <el-button v-else size="small" class="el-icon-sold-out"> {{item.id}}</el-button>
        </span>
        <!-- </el-col> -->
    </el-badge>
     </span>
</el-col>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import axios from 'axios'
// import http from '@/axios.js'


export default {
  name: 'status',
  props: {

  },
  data() {
      return {
        items:[
            {"id":1, "st": 1, "ct": 120},
            {"id":2, "st": 0, "ct": 90}
        ]
      };
  },
  methods: {
    getStatus() {
        const path = 'http://aishe.org.cn/api/status';
        const tk = this.axiosconfig();
        axios.get(path, tk)
          .then((res) => {
              this.items = res.data;
          })
          .catch((error) => {
              console.error('renew data error' + error);
          });
    },
    ...mapActions([
      'authGet'
    ]),
    ...mapGetters([
      'axiosconfig',
      'axconfs'
    ])
  },
  mounted() {
    this.getStatus();
  },
  mqtt: {
    // 'webdev/on' (data, topic) {
    //   console.log('receive:'+ topic + ':' + data)
    //   for (var i =0; i < this.items.length; i++) {
    //     if (this.items[i].id == data.devicepin) {
    //       this.items[i].ct = data.counts;
    //       break;
    //     }
    //   }
    // }
  }
}
</script>
<style>
.badgeitem {
    margin-top: 10px;
    margin-right: 26px;
}
</style>
