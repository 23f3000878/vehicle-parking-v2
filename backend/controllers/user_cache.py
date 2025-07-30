from extensions import cache
from flask import g

def delete_user_cache():
    from .user import find_all_spots, find_lots,find_lot_status
    cache.delete_memoized(find_all_spots)
    cache.delete_memoized(find_lots)
    cache.delete_memoized(find_lot_status)
    cache.delete(f"parking-history:{g.current_user.id}")