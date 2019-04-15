<template>
    <el-row>
        <el-row>
        <el-col :span="8">
        <Anim />
        </el-col>
        <el-col :span="16">
            <Status />
        </el-col>
        </el-row>
    <el-row>
        <LineGraph />
    </el-row>
        <el-row>
        <LogTable />
        </el-row>
        
    </el-row>
</template>
<script>

import Anim from '@/components/Anim.vue'
import Status from '@/components/Status.vue'
import LogTable from '@/components/LogTable.vue'
import LineGraph from '@/components/LineGraph.vue'
// mqtt


export default {
    name: 'MqController',
    components: {
        Anim,
        Status,
        LogTable,
        LineGraph
    },
    methods: {
    
    },
    mounted() {
        // this.$mqtt.subscribe('VueMqtt/#')
    }

    // mqtt: {
    //     'VueMqtt/+' (data, topic) {
    //         this.Anim.play();
    //     }
    // }
}
</script>
