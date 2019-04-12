<template>
<div>
    <div class="separator">
      <md-badge :md-content="count">
        <md-button class="md-icon-button">
          <md-icon>{{ msg }}</md-icon>
        </md-button>
      </md-badge>
    </div>
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
      msg: 'H',
      count: 12,
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
