from extensions import cache
from flask import g
def delete_lots_cache():
    from .admin import get_filtered_lots
    cache.delete_memoized(get_filtered_lots)
    cache.delete(f'availability-graph-{g.current_user.id}')
    cache.delete(f'lots-revenue-graph-{g.current_user.id}')


def delete_spots_cache():
    from .admin import find_spots_by_lot, find_all_spots,find_occupied_spots
    cache.delete_memoized(find_spots_by_lot)
    cache.delete_memoized(find_all_spots)
    cache.delete_memoized(find_occupied_spots)
    cache.delete(f'occupancy-graph-{g.current_user.id}')