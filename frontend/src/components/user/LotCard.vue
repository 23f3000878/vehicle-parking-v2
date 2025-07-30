<template>
  <div class="card shadow-sm">
    <div class="card-body">
      <h5 class="card-title text-success">{{ lot.name }}</h5>
      <p class="card-text">
        Location: {{ lot.location }}<br />
        Price: ₹{{ lot.price }}/hr<br />
        Available: {{ lot.available_spots }} / {{ lot.total_spots }}
      </p>

      <div class="d-flex flex-wrap gap-2 mb-2">
        <button
          v-for="spot in spots"
          :key="spot.id"
          class="btn"
          :class="
            spot.status === 'A'
              ? 'btn-outline-success'
              : 'btn-outline-secondary disabled'
          "
          @click="handleBook(spot)"
        >
          Spot {{ spot.spot_number }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import axios from "../../services/axios";

const props = defineProps({ lot: Object });
const emit = defineEmits(["book"]);

const spots = ref([]);

const fetchSpots = async () => {
  const res = await axios.get(`/user/lots/${props.lot.id}/spots`);
  spots.value = res.data.spots;
};

watch(() => props.lot.id, fetchSpots);
onMounted(fetchSpots);

const handleBook = (spot) => {
  if (spot.status === "A") {
    emit("book", props.lot, spot);
  }
};
</script>
