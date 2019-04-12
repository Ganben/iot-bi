<template>
  <div id="lineChart" style="width:100%;height:100%"></div>
</template>
<script>
  import echarts from 'echarts'

  export default {
    name: 'lineChart',
    props: {
      chartOptions: Object,
      chartData: Object

    },
    data() {
      return {
        l_legend: [],
        l_series: []
      };
    },
    methods: {
      init() {
        let option = {
        title: {
          text: 'Last Week'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                  backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
          data: this.l_legend
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: this.l_series
        }
        
    },
    updateData (data) {
      this.l_series.clear();
      this.l_series = data;
    },
    mounted () {
      this.init()
    }
  }
}
</script>