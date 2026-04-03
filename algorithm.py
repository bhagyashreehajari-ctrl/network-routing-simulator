# ================= MAX-MIN SAFEST PATH =================
import heapq

def safest_path_maxmin(graph, source, target):
    heap = [(-float('inf'), source, [])]
    visited = set()

    while heap:
        min_cap, node, path = heapq.heappop(heap)
        min_cap = -min_cap

        if node in visited:
            continue

        visited.add(node)
        path = path + [node]

        if node == target:
            return path, min_cap

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                weight = graph[node][neighbor]['weight']
                new_min = min(min_cap, weight)
                heapq.heappush(heap, (-new_min, neighbor, path))

    return None, 0


# ================= MERGE SORT =================
def merge_sort(routes):
    if len(routes) <= 1:
        return routes

    mid = len(routes) // 2
    left = merge_sort(routes[:mid])
    right = merge_sort(routes[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ================= BINARY SEARCH =================
def binary_search(routes, target):
    low, high = 0, len(routes) - 1

    while low <= high:
        mid = (low + high) // 2
        if routes[mid][0] == target:
            return routes[mid]
        elif routes[mid][0] < target:
            low = mid + 1
        else:
            high = mid - 1

    return None