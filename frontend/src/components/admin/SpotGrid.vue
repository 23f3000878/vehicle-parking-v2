<!-- components/admin/SpotGrid.vue -->
<template>
  <button
    v-for="spot in spots"
    :key="spot.id"
    :class="[
      'btn',
      spot.status === 'A' ? 'btn-outline-success' : 'btn-outline-danger',
    ]"
    @click="$emit('spot-selected', spot)"
  >
    {{ spot.spot_number }}
  </button>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "../../services/axios";
import { defineProps } from "vue";

const props = defineProps(["lotId"]);
const spots = ref([]);

onMounted(async () => {
  const res = await axios.get(`/admin/lots/${props.lotId}/spots`);
  spots.value = res.data.spots;
});
</script>
