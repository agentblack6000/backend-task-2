import heapq
from decimal import Decimal


def shortest_path(start_station, end_station):
    """
    Finds the shortest path from start_station to end_station using Dijkstra's algorithm.
    Returns (total_distance, total_cost, connection_list) along the shortest path.
    Total cost is calculated after the path is found.
    Raises ValueError if no path exists.
    """
    from .models import Station, Connection

    # Build graph from active connections only
    # Graph format: {station_id: [(neighbor_id, distance, connection_id), ...]}
    graph = {}
    connections = Connection.objects.filter(line__is_active=True)

    # Map connection IDs to Connection objects for easy retrieval later
    connection_map = {conn.id: conn for conn in connections}

    for conn in connections:
        # Bidirectional edges
        graph.setdefault(conn.start_station_id, []).append(
            (conn.destination_station_id, float(conn.distance), conn.id)
        )
        graph.setdefault(conn.destination_station_id, []).append(
            (conn.start_station_id, float(conn.distance), conn.id)
        )

    start_id = start_station.id
    end_id = end_station.id

    # Priority queue: (total_distance, current_station_id, path_of_connection_ids, path_of_station_ids)
    heap = [(0, start_id, [], [start_id])]
    visited = set()

    while heap:
        total_distance, current, conn_path, path_stations = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)

        if current == end_id:
            # Convert connection IDs back to Connection objects
            connections_list = [connection_map[cid] for cid in conn_path]
            # Calculate total cost after the path is found
            total_cost = Decimal(sum(c.cost for c in connections_list))
            return total_cost, total_distance, connections_list

        for neighbor, distance, conn_id in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(
                    heap,
                    (
                        total_distance + distance,
                        neighbor,
                        conn_path + [conn_id],
                        path_stations + [neighbor],
                    ),
                )

    raise ValueError(f"No route possible from {start_station} to {end_station}")
