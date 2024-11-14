import heapq


def process_line(line,graph,heuristic): 

    temp = line.split() 
    key = temp[0]  #splitted list first value is a location
    heuristic[key] = int(temp[1]) #2nd value heuristic of that location
    graph[key] = []

    for i in range(2,len(temp),2):
        dest = temp[i]
        weight = int(temp[i+1])
        graph[key].append((dest,weight))


def make_graph(graph,heuristic):
    
    with open("lab1.txt","r") as inp:
        while True:
            ln = inp.readline()
            if ln != "":
                process_line(ln,graph,heuristic)
            else:
                #print(graph,sep=" =>")
                #print(heuristic)
                break
    inp.close()
    

def path_construct(came_from,current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    #print(path)
    return path  

    

def aStar(start,goal,graph,heu):

    visited = set()  
    parent = {}
    pq = []  #priority queue
    g_values = {}

    fn = heu[start] + 0
    g_values[start] = 0  # g value 0 of start node
    heapq.heappush(pq, (fn,start)) #inserting starting node to PQ

    while True:
        
        _,current = heapq.heappop(pq) #dequeueing lowest f valued node
        visited.add(current)

        if current == goal:
            #print()
            #print(g_values)
            return path_construct(parent,current),g_values[goal]
         
        for location,cost in graph[current]: 
            tentative = cost + g_values[current] 

            if (location not in visited) or tentative < g_values[location]: 
                """If the child node is not visited then we set the g_value and calculate fn value
                OR if we find a better path to visit the child node we update the g_value
                push to the priority queue each time
                """
                parent[location] = current
                g_values[location] =  tentative
                
                fn = g_values[location] + heu[location]                    
                heapq.heappush(pq,(fn,location))


if __name__ == '__main__': 

    graph = {}
    heuristic = {} 
    make_graph(graph,heuristic)
    #print(heuristic)
    #print()
    #print(graph)
    start = "Arad"
    end = "Bucharest"
    #end = "Oradea"
    #end = "Neamt"
    #end = "Craiova"
    
    try:
        path,distance = aStar(start,end,graph,heuristic)
        print("Path:",path[0],end="")
        for i in path[1:]:
            print("->"+i,end="")
        print(f"\nDistance: {distance} km")
    except:
        print("Path not found")
        
