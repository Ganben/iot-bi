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
import axios from 'axios'

export default {
  name: 'LogTable',
  props: {

  },
  data() {
      return {
        tableData:[
            {"time":"11:10:11", "di": "12341234"},
            {"time":"12:10:11", "di": "12341234"}
        ]
      };
  },
  methods: {
    getLogs() {
        const path = 'http://aishe.org.cn/api/logacts';
        axios.get(path)
          .then((res) => {
              this.tableData = res.data;
          })
          .catch((error) => {
              console.error('renew data error');
          });
    }
  },
  mounted() {
    getLogs();
  },
  mqtt: {
      'webdev/+' (data, topic) {

      }
  }
}
</script>