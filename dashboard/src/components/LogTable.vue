<template>
<div>
<el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="time"
        label="Time"
        width="180">
      </el-table-column>
      <el-table-column
        prop="devicepin"
        label="Device"
        width="380">
      </el-table-column>
      <el-table-column prop="counts"
      label="Counts"
      width="120">
      </el-table-column>
    </el-table>
</div>
</template>
<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
// import  myApi  from '@/axios.js'

export default {
  name: 'LogTable',
  props: {

  },
  data() {
      return {
        tableData:[
            {"time":"11:10:11", "devicepin": "12341234", "counts": 2},
            {"time":"12:10:11", "devicepin": "12341234", "counts": 1}
        ]
      };
  },
  methods: {
    getLogs() {
        const path = 'http://aishe.org.cn/api/logacts';
        const conf = this.axiosconfig();
        axios.get(path, conf)
          .then((res) => {
              this.tableData = res.data;
          })
          .catch((error) => {
              console.error('renew data error');
              console.error('' + error);
          });
    },
    ...mapGetters([
      'axiosconfig'
    ])
  },
  mounted() {
    this.getLogs();
  },
  mqtt: {
      'webdev/log' (data, topic) {
         console.log('rec:' + topic +':' + data);
         this.tableData.unshift(JSON.parse(data));
         console.log('len: '+ this.tableData);
      }
  }
}
</script>