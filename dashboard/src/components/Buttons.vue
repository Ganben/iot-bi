<template>
  <div class="button">
<el-button @click="publish" type="primary">Button</el-button>
  </div>
</template>

<script>
export default {
  name: 'Buttons',
  props: {
    msg: String
  },
  methods: {
    publish () {
      console.log('click button');
      this.$mqtt.publish('VueMqtt/dev', 'button msg');
    }
  },
}
</script>