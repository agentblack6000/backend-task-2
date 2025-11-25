def shortest_path(start_station, end_station):
    from .models import Connection
    connections = Connection.objects.filter(line__is_active=True)

    graph = {}
    for connection in connections:
        if connection.start_station not in graph:
            graph[connection.start_station] = []
        
        if connection.destination_station not in graph:
            graph[connection.destination_station] = []
        
        graph[connection.start_station].append([connection.destination_station, connection])
        graph[connection.destination_station].append([connection.start_station, connection])
    

    queue = [(start_station, [])]
    visited = set()

    while queue:
        current_station, path = queue.pop(0)

        if current_station in visited:
            continue

        visited.add(current_station)

        if current_station == end_station:
            total_cost = sum(connection.cost for connection in path)
            total_distance = sum(connection.distance for connection in path)
            return total_cost, total_distance, path
        
        try:
            for neighbouring_station, neighbouring_connection in graph[current_station]:
                if neighbouring_station not in visited:
                    queue.append((neighbouring_station, path + [neighbouring_connection]))
        except KeyError:
            pass

    raise ValueError(f"No possible route")
    

