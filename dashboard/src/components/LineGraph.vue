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
  props: {
    chartOption: Object,
    chartData: Object
  },
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
                data: ["Mon","Tue","Wed","Thr","Fri","Sat"]
            },
            yAxis: {},
            series: [{
                name: 'Activites',
                type: 'bar',
                data: [566, 2210, 3561, 1421, 2020, 1992]
            }]
      }
    }
  },
  methods: {
    getChartData() {
      const path='http://www.aish.org.cn:5000/api/linchart';
      axios.get(path)
        .then((res) => {
          this.chartData = res.data;
        })
        .catch();
    },
    init() {
      
    }
  },
  created() {
    // getChartData();
  }
}
</script>
