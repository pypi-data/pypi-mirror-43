# EasyGraphLib

This is a simple package for working with graphs in Python 3.

Tasks:
- [x] Add weighted graph.
- [x] Add unweighted graph.
- [ ] Add tree's.

"class weighted_graph" methods:  
    
*  **add_node**("node name", "connect or connections", "values for con/con's") - add node with connections and values  
    
*  **add_connections**("node name", "connection or connections", "values for con/con's") - add connections.  
    
*  **update_connection**("node name", "connection", "value") - update connection value.  
    
*  **remove_node**("node name") - remove node with connections.  
    
*  **remove_connection**("node name", "connection") - remove connection from node.  
    
*  **compile_graph()** - Compile EasyGraphLib struct.  
    
*  **find_tnw_d**("EasyGraphLib struct") - Dijkstra algorythm.  

    ```python
    import easygraphlib as egl

    wg = egl.weighted_graph() # Creating weighted graph
    wg.add_node("start", ("a","b"), (6,2)) # Adding node with connections.
    wg.add_connections("start", "c", 3) # Adding connection.
    wg.add_node("c", ("a", "fin"), (2, 2))
    wg.update_connection("start", "c", 4) # Update connection.
    wg.add_node("a", ("fin"), (1))
    wg.add_node("b", ("a", "fin"), (3, 5))
    wg.add_node("fin") # Node without connections.

    graph = wg.compile_graph() # Compile EasyGraphLib struct.
    print(graph, wg.find_tnw_d())

    wg.remove_node("c") # Removing node.
    wg.remove_connection("b", "a") # Removing connection from node.
    graph = wg.compile_graph() # Compile EasyGraphLib struct.
    print(graph)  # You can't use wg.find_tnw_d() with this graph.
    ```

"class unweighted_graph" methods:  
    
*  **add_node**("node name", "connect or connections", "values for con/con's") - add node with connections and values
   
*   **add_connections**("node name", "connection or connections", "values for con/con's") - add connections.
    
*  **update_connection**("node name", "connection", "value") - update connection value.
    
*  **remove_node**("node name") - remove node with connections.
    
*  **remove_connection**("node name", "connection") - remove connection from node.
    
*  **get_graph()**
    
*  **wide_search("node name", "value", "condition")**

    ```python
    import easygraphlib as egl

    wg = egl.unweighted_graph() # Creating weighted graph
    wg.add_node("John", ("David","Mike"), (False, False)) # Adding node with connections.
    wg.add_connections("John", "Leonard", False) # Adding connection.
    wg.add_node("Leonard", ("David", "Josh"), (False, True))
    wg.update_connection("Jonh", "Leonard", False) # Update connection.
    wg.add_node("David", ("Josh"), (True))
    wg.add_node("Mike", ("David", "Josh"), (False, True))

    graph = wg.get_graph() # Get graph.
    print(graph, wg.wide_search("David", True))

    wg.remove_node("Leonard") # Removing node.
    wg.remove_connection("Mike", "David") # Removing connection from node.
    graph = wg.get_graph() # Compile EasyGraphLib struct.
    print(graph, wg.wide_search("Mike"))
    ```