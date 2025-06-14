<template>
  <form @submit.prevent="submit">
    <input v-model="text" placeholder="Écris ton message..." />
    <button type="submit">Envoyer</button>
  </form>
</template>

<script>
export default {
  data: () => ({ text: '' }),
  methods: {
    submit() {
      if (this.text.trim()) {
        this.$emit('send', this.text);
        this.text = '';
      }
    }
  }
};
</script>