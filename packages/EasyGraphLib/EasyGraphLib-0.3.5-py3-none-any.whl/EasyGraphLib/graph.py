from collections import deque

class weighted_graph:
    def __init__(self):
        self.__graph, self.__weights, self.__parents, self.__type = {}, {}, {}, "w graph object"
        self.__graph_struct = {"graph":self.__graph, "weights":self.__weights, "parents":self.__parents}

    def add_node(self, node_, connections_ = None, weights_ = None, add_con_nodes = True):
        ''' Adding node from connections or without connections \n
            Input: node_ tuple(str or int)/ str or int/ None, connections_ -- // --, weights_ tuple(int or float)/ int or float/ None.'''
        if not node_ in self.__graph.keys():
            if connections_ == None and weights_ == None:
                self.__graph[node_] = {}
            elif connections_ != None and weights_ == None or connections_ == None and weights_ != None:
                raise SyntaxError('Graph error: Error Graph syntax. You can\'t use this function with only one parameter.')
            else:
                if isinstance(weights_, tuple) and isinstance(connections_, tuple):
                    if len(connections_) != len(weights_):
                        raise ValueError('Graph error: connections and weights len not equal.')
                    else:
                        self.__graph[node_] = {}
                        for child_index in range(len(connections_)):
                            if self.__graph.get(connections_[child_index]) is None and add_con_nodes:
                                self.add_node(connections_[child_index])
                            self.__graph[node_][connections_[child_index]] = weights_[child_index]
                else:
                    self.__graph[node_] = {}
                    self.__graph[node_][connections_] = tuple(weights_)
                    if self.__graph.get(connections_) is None and add_con_nodes:
                        self.add_node(connections_)

    def add_connections(self, node_, connections_, weights_, add_con_nodes = True):
        ''' Adding connections/connection to node. \n
            Input: node_ tuple(str or int)/ str or int, connections_ -- // --, weights_ tuple(int or float)/ int or float.'''
        if node_ in self.__graph.keys():
            if isinstance(weights_, tuple) and isinstance(connections_, tuple):
                if len(connections_) != len(weights_):
                    raise ValueError('Graph error: connections and weights len not equal.')
                else:
                    for connection_index in range(len(connections_)):
                        self.__graph[node_][connections_[connection_index]] = weights_[connection_index]
                        if self.__graph.get(connections_[connection_index]) is None and add_con_nodes:
                            self.add_node(connections_[connection_index])
            else:
                self.__graph[node_][connections_] = weights_
                if self.__graph.get(connections_) is None and add_con_nodes:
                    self.add_node(connections_)
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def update_connection(self, node_, connection_, weight_):
        ''' Update connection in node. \n
            Input: node_ - str or int, connection_ - str or int,  weight_ - int or float.'''
        if isinstance(weight_, int) and isinstance(connection_, str):
            if node_ in self.__graph.keys():
                if connection_ in self.__graph[node_].keys():
                    self.__graph[node_][connection_] = weight_
                else:
                    raise ValueError('Graph error: connection not exist.')
            else:
                raise ValueError('Graph error: Node not exist.')
        else:
            raise ValueError('Graph error: Unknown parameters.')
    
    def remove_node(self, node_):
        ''' Removing node_ with connections. \n
            Input: node_ - str or int '''
        if node_ in self.__graph.keys():
            self.__graph.pop(node_, None)
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def remove_connection(self, node_, connection_):
        ''' Removing connection in node. \n
            Input: node_ - str or int, connection_ - str or int '''
        if node_ in self.__graph.keys():
            if connection_ in self.__graph[node_].keys():
                self.__graph[node_].pop(connection_, None)
            else:
                raise ValueError('Graph error: connection not exist.')
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def compile_graph(self):
        ''' Returns Graph struct with weights and parents. '''
        self.weights, self.parents = self.__makeweights(self), self.__makeparents(self)
        self.__graph_struct = {"graph":self.__graph, "weights":self.weights, "parents":self.parents}
        return self.__graph_struct, self.__type

    @staticmethod
    def __makeweights(self, start_node = 0, end_node = None):
        result, graph_keys, end_node = {}, [], len(self.__graph) - 1
        for key in self.__graph.keys():
            graph_keys.append(key)

        for child in self.__graph[graph_keys[start_node]].keys():
            result[child] = self.__graph[graph_keys[start_node]][child]
        result[graph_keys[end_node]] = float("inf")
        return result

    @staticmethod
    def __makeparents(self, start_node = 0, end_node = None):
        result, graph_keys, end_node = {}, [], len(self.__graph) - 1
        for key in self.__graph.keys():
            graph_keys.append(key)
    
        for child in self.__graph[graph_keys[start_node]].keys():
            result[child] = graph_keys[start_node]
        result[graph_keys[end_node]] = None
        return result
    
    def __find_lowest_weight(self, weights, processed): # Поиск минимальной стоимости
        lowest_weight, lowest_weight_node = float("inf"), None
        for node in weights:
            weight = weights[node]
            if weight < lowest_weight and node not in processed:
                lowest_weight = weight
                lowest_weight_node = node
        return lowest_weight_node

    #Dijkstra algorythm for finding the nearest way in graph
    def find_tnw_d(self, input_graph = None):
        ''' Search for the shortest distance to the desired vertex using the Dijkstra algorithm. \n
            Returns a sheet with vertices ascending, and the length of the path. \n
            Input: dict({"graph":, "weights":, "parents":}) or None'''
        if input_graph is None:
            input_graph = self.__graph_struct
        processed = [] # Проверенные вершины
        node = self.__find_lowest_weight(input_graph["weights"], processed) # Вершина с минимальной ценой
        while node is not None:
            weight = input_graph["weights"][node] # Достаём цену
            neighbours = input_graph["graph"][node] # Достаём соседние вершины
            for n in neighbours.keys(): # Проходимся по соседним вершинам
                new_weight = weight + neighbours[n] # Пишем новую цену, учитывая текущую цену и цену до соседа
                if input_graph["weights"][n] > new_weight: # Если новая цена дешевле предыдущей
                    input_graph["weights"][n] = new_weight # Задаём новую цену
                    input_graph["parents"][n] = node # Добавляем родителя
            processed.append(node) # Добавляем вершину в проверенные
            node = self.__find_lowest_weight(input_graph["weights"], processed) # Достаём новую вершину
            
        path, parents = [], list(input_graph["parents"].keys())
        end = parents[len(parents) - 1]
        del parents
        while True:
            path.append(end)
            if input_graph["parents"].get(end) is None:
                break
            end = input_graph["parents"][end]
        path.reverse()
        return path, input_graph["weights"][path[len(path) - 1]]
        


class unweighted_graph(object):
    def __init__(self):
        self.__graph = {}
        self.__type = "uw_graph object"
    
    def add_node(self, node_, value_ = None, connections_ = None, add_con_nodes = True):
        ''' Adding node from connections or without connections, and creating nodes for connections if not exist. \n
            Input: node_ tuple(str or int)/ str or int/ None, connections_ -- // --, values_ tuple(int or float)/ int or float/ None.'''
        if not node_ in self.__graph.keys():
            if connections_ == None:
                self.__graph[node_] = {}
                self.__graph[node_]["value"] = value_
                self.__graph[node_]["connections"] = tuple()
            else:
                if isinstance(connections_, tuple):
                    self.__graph[node_], new_connections = {}, []
                    for connection in connections_:
                        new_connections.append(connection)
                        if self.__graph.get(connection) is None and add_con_nodes:
                            self.add_node(connection, False)
                    self.__graph[node_]["value"] = value_
                    self.__graph[node_]["connections"] = tuple(new_connections)
                else:
                    self.__graph[node_], new_connections = {}, []
                    new_connections.append(connections_)
                    self.__graph[node_]["value"] = value_
                    self.__graph[node_]["connections"] = tuple(new_connections)
                    if self.__graph.get(connections_) is None and add_con_nodes:
                        self.add_node(connections_, False)
        else:
            raise ValueError('Graph error: Node already exist.')

    def add_connections(self, node_, connections_, add_con_nodes = True):
        ''' Adding connections/connection to node, and creating nodes if. \n
            Input: node_ tuple(str or int)/ str or int, connections_ -- // --, values_ tuple(int or float)/ int or float.'''
        current_connections, new_connections = list(self.__graph[node_]["connections"]), []
        if node_ in self.__graph.keys():
            if isinstance(connections_, tuple):
                for connection in connections_:
                    new_connections.append(connection)
                    if self.__graph.get(connection) is None and add_con_nodes:
                        self.add_node(connection, False)
                self.__graph[node_]["connections"] = tuple(current_connections + new_connections)
            else:
                current_connections.append(connections_)
                self.__graph[node_]["connections"] = tuple(current_connections)
                if self.__graph.get(connections_) is None and add_con_nodes:
                    self.add_node(connections_, False)
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def update_value(self, node_, value_):
        ''' Update value in node. \n
            Input: node_ - str or int,  value_ - int or bool.'''
        if node_ in self.__graph.keys():
            self.__graph[node_]["value"] = value_
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def remove_node(self, node_):
        ''' Removing node_ with connections. \n
            Input: node_ - str or int '''
        if node_ in self.__graph.keys():
            self.__graph.pop(node_, None)
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def remove_connection(self, node_, connection_):
        ''' Removing connections in node. \n
            Input: node_ - str or int, connection_ - str or int'''
        if node_ in self.__graph.keys():
            if connection_ in self.__graph[node_].keys():
                self.__graph[node_].pop(connection_, None)
            else:
                raise ValueError('Graph error: connection not exist.')
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def get_graph(self):
        return self.__graph, self.__type
    
    def wide_search(self, node_, condition = True):
        search_queue, searched = deque(), [] # Создаём очередь и массив, хранящий прошедших очередь
        search_queue += self.__graph[node_] # Задаём начальную очередь
        while search_queue: # Пока очередь не кончилась
            node = search_queue.popleft() # Извлекаем первого из очереди
            if not node in searched: # Проверяем не был ли элемент в очереди
                if self.__graph[node_]["value"] == condition: # Какая нибудь проверка
                    return True, (node_, node)
                else:
                    if self.__graph.get(node): # Проверяем имеет ли узел связи
                        search_queue += self.__graph[node] # Добавляем в очередь соседей
                    searched.append(node) # Добавляем в проверенные
        return False, ()

class tree(object):
    pass

class binary_tree(object):
    pass