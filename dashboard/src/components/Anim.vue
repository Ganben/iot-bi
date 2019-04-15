<template>
    <div class="anim">
    <lottie :options="defaultOptions" :height="300" :width="300" 
    v-on:animCreated="handleAnimation"/>
</div>
</template>
<script>
import Lottie from 'vue-lottie';
import * as animationData from '@/assets/5212-loading.json';

export default {
    name: 'Anim',
    components: {
        'lottie': Lottie
    },
    data() {
        return {
            defaultOptions: { 
                animationData: animationData.default,
                // renderer: 'html',
                loop: false},
        };
    },
    methods: {
        handleAnimation: function (anim) {
            this.anim = anim;
            this.anim.play();
            // this.anim.stop();
        },
        play: function () {
            this.anim.play();
        }
    },
}
</script>
