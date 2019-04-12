<template>
  <div>
    <p>{{ msg }}</p>
    <lot></lot>
  </div>
  
</template>

<script>
import axios from 'axios';
import VueLot from '@/components/VueLot.vue';

export default {
  name: 'Homepg',
  data() {
    return {
      msg: 'Hello!',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/api/home';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch();
    },
  },
  created() {
  },
  components: {
    'lot': VueLot
  }
};
</script>
