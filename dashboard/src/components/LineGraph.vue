<template>
  <!-- <div id="lineChart" style="width:100%;height:100%"></div> -->
  <v-chart :options="lines" />
</template>
<script>
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/line'
import 'echarts/lib/component/polar'
import 'echarts/lib/component/title'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/polar'
import 'echarts/lib/chart/bar'
import axios from 'axios'

export default {
  name: 'lineChart',
  components: {
    'v-chart': ECharts
  },
  data() {
    return {
      lines: {
        title: {
                text: 'Activity History'
            },
            tooltip: {},
            legend: {
                data:['Total Activities']
            },
            xAxis: {
                data: []
            },
            yAxis: {},
            series: []
      }
    };
  },
  methods: {
    getChartData() {
      const path='http://www.aishe.org.cn:5000/api/linchart';
      axios.get(path)
        .then((res) => {
          this.lines.xAxis.data = res.data.xs;
          this.lines.series.push(res.data.serie);
        })
        .catch();
    },
    init() {
      
    }
  },
  created() {
    this.getChartData();
  },
  mqtt: {
    'webdev/on' (data, topic) {
      // console.log(data);
      // this.lines.series[0].data[6] += 1;
      var last = this.lines.series.pop();
      // console.log(''+last);
      var lasta = last.data.pop();
      lasta ++;
      last.data.push(lasta);
      this.lines.series.push(last);
    }
  }
}
</script>
