<template>
    <div class="anim">
    <lottie :options="defaultOptions" :height="300" :width="300" 
    v-on:animCreated="handleAnimation"/>
</div>
</template>
<script>
import Lottie from './lottie.vue';
// import Lottie from 'vue-lottie';
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
                autoplay: false,
                loop: "2"},
        };
    },
    methods: {
        handleAnimation: function (anim) {
            this.ltanim = anim;
            // this.ltanim.play();
            // this.ltanim.stop();
            // t = anim.getDuration(false);
            // console.log('anim dur: ' + t);
        },
        ssplay: function () {
            console.log('ssplay');
            this.ltanim.play();
            // this.ltanim.playSegments(0,2,false);
        },
        ssstop: function () {
            // wait(1500);
            console.log('stop');
            this.ltanim.stop();
        },
        sspause: function () {
            console.log('pause');
            this.ltanim.pause();
        },
        ssreload: function () {
            console.log('anim reload');
            this.ltanim.loadAnimation({
                path: animationData.default,
                loop: false,
                autoplay: true
            });
        }
    },
    mounted() {
        // this.ssstop();
    },
    mqtt: {
        'webdev/on' (data, topic) {
            this.ssplay();
            console.log('received:' + data);
            // setTimeout(this.sspause(), 1500);
        },
        'webdev/off' (data, topic) {
            this.sspause();
            console.log('receive stop:' + data);
        }
    }
}
</script>
