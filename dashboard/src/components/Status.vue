<template>
<el-col>
    <el-badge :value="item.ct" class="badgeitem" type="primary" v-for="item in items">
        <!-- <el-col> -->
        <span>
        <el-button v-if="item.st" size="small" class="el-icon-circle-check"> {{item.id}}</el-button>
        <el-button v-else size="small" class="el-icon-sold-out"> {{item.id}}</el-button>
        </span>
        <!-- </el-col> -->
    </el-badge>
</el-col>
</template>
<script>
import axios from 'axios'

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
        const path = 'http://aishe.org.cn:5000/api/status';
        axios.get(path)
          .then((res) => {
              this.items = res.data;
          })
          .catch((error) => {
              console.error('renew data error');
          });
    }
  },
  mounted() {
    this.getStatus();
  },
  mqtt: {
    'webdev/on' (data, topic) {
      console.log('receive:'+data)
      for (var i =0; i < this.items.length; i++) {
        if (this.items[i].id == data.devicepin) {
          this.items[i].ct = data.counts;
          break;
        }
      }
    }
  }
}
</script>
<style>
.badgeitem {
    margin-top: 10px;
    margin-right: 26px;
}
</style>
