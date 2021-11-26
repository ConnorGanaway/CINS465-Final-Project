/*
const Counter = {
  data() {
    return {
      counter: 0
    }
  },
  mounted() {
    setInterval(() => {
      this.counter++
    }, 1000)
  }
}

counterapp = Vue.createApp(Counter).mount('#counter')
*/

const Counter = {
    data() {
      return {
        counter : 0
      }
    },
    methods: {
       increment : function(){
           this.counter += 1
       },
       decrement : function(){
           this.counter -= 1
       }
    }
}


counterapp = Vue.createApp(Counter).mount('#counter')
