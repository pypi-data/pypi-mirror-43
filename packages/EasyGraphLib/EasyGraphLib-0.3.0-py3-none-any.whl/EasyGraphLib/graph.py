from collections import deque

class weighted_graph:
    def __init__(self):
        self.graph, self.weights, self.parents = {}, {}, {}
        self.__graph_struct = {"graph":self.graph, "weights":self.weights, "parents":self.parents}

    def add_node(self, node_, connections_ = None, weights_ = None):
        ''' Adding node from childs or without childs \n
            Input: node_ tuple(str or int)/ str or int/ None, connections_ -- // --, weights_ tuple(int or float)/ int or float/ None.'''
        if connections_ == None and weights_ == None:
            self.graph[node_] = {}
        elif connections_ != None and weights_ == None or connections_ == None and weights_ != None:
            raise SyntaxError('Graph error: Error Graph syntax. You can\'t use this function with only one parameter.')
        else:
            if not isinstance(weights_, int) and not isinstance(connections_, str):
                if len(connections_) != len(weights_):
                    raise ValueError('Graph error: connections and weights len not equal.')
                else:
                    self.graph[node_] = {}
                    for child_index in range(len(connections_)):
                        self.graph[node_][connections_[child_index]] = weights_[child_index]
            else:
                self.graph[node_] = {}
                self.graph[node_][connections_] = weights_

    def add_connections(self, node_, connections_, weights_):
        ''' Adding childs/child to node. \n
            Input: node_ tuple(str or int)/ str or int, connections_ -- // --, weights_ tuple(int or float)/ int or float.'''
        if not isinstance(weights_, int) and not isinstance(connections_, str):
            if self.graph.get(node_):
                if len(connections_) != len(weights_):
                    raise ValueError('Graph error: connections and weights len not equal.')
                else:
                    for connection_index in range(len(connections_)):
                        self.graph[node_][connections_[connection_index]] = weights_[connection_index]
            else:
                raise ValueError('Graph error: Node not exist.')
        else:
            if self.graph.get(node_):
                self.graph[node_][connections_] = weights_
            else:
                raise ValueError('Graph error: Node not exist.')
    
    def update_connection(self, node_, connection_, weight_):
        ''' Update child in node. \n
            Input: node_ - str or int, connection_ - str or int,  weight_ - int or float.'''
        if isinstance(weight_, int) and isinstance(connection_, str):
            if self.graph.get(node_) and self.graph.keys():
                if self.graph[node_].get(connection_):
                    self.graph[node_][connection_] = weight_
                else:
                    raise ValueError('Graph error: connection not exist.')
            else:
                raise ValueError('Graph error: Node not exist.')
        else:
            raise ValueError('Graph error: Unknown parameters.')
    
    def remove_node(self, node_):
        ''' Removing node_ with childs. \n
            Input: node_ - str or int '''
        if self.graph.get(node_):
            self.graph.pop(node_, None)
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def remove_connection(self, node_, connection_):
        ''' Removing childs in node. \n
            Input: node_ - str or int, connection_ - str or int '''
        if self.graph.get(node_):
            if self.graph[node_].get(connection_):
                self.graph[node_].pop(connection_, None)
            else:
                raise ValueError('Graph error: connection not exist.')
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def compile_graph(self):
        ''' Returns Graph struct with weights and parents. '''
        self.weights, self.parents = self.__makeweights(self), self.__makeparents(self)
        self.__graph_struct = {"graph":self.graph, "weights":self.weights, "parents":self.parents}
        return self.__graph_struct

    @staticmethod
    def __makeweights(self, start_node = 0, end_node = None):
        result, graph_keys, end_node = {}, [], len(self.graph) - 1
        for key in self.graph.keys():
            graph_keys.append(key)

        for child in self.graph[graph_keys[start_node]].keys():
            result[child] = self.graph[graph_keys[start_node]][child]
        result[graph_keys[end_node]] = float("inf")
        return result

    @staticmethod
    def __makeparents(self, start_node = 0, end_node = None):
        result, graph_keys, end_node = {}, [], len(self.graph) - 1
        for key in self.graph.keys():
            graph_keys.append(key)
    
        for child in self.graph[graph_keys[start_node]].keys():
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
    
    def add_node(self, node_, connections_ = None, values_ = None):
        ''' Adding node from childs or without childs \n
            Input: node_ tuple(str or int)/ str or int/ None, connections_ -- // --, values_ tuple(int or float)/ int or float/ None.'''
        if connections_ == None and values_ == None:
            self.__graph[node_] = {}
        elif connections_ != None and values_ == None or connections_ == None and values_ != None:
            raise SyntaxError('Graph error: Error Graph syntax. You can\'t use this function with only one parameter.')
        else:
            if not isinstance(values_, int or bool) and not isinstance(connections_, str):
                if len(connections_) != len(values_):
                    raise ValueError('Graph error: connections and values len not equal.')
                else:
                    self.__graph[node_] = {}
                    for child_index in range(len(connections_)):
                        self.__graph[node_][connections_[child_index]] = values_[child_index]
            else:
                self.__graph[node_] = {}
                self.__graph[node_][connections_] = values_

    def add_connections(self, node_, connections_, values_):
        ''' Adding childs/child to node. \n
            Input: node_ tuple(str or int)/ str or int, connections_ -- // --, values_ tuple(int or float)/ int or float.'''
        if not isinstance(values_, int or bool) and not isinstance(connections_, str):
            if self.__graph.get(node_):
                if len(connections_) != len(values_):
                    raise ValueError('Graph error: connections and weights len not equal.')
                else:
                    for connection_index in range(len(connections_)):
                        self.__graph[node_][connections_[connection_index]] = values_[connection_index]
            else:
                raise ValueError('Graph error: Node not exist.')
        else:
            if self.__graph.get(node_):
                self.__graph[node_][connections_] = values_
            else:
                raise ValueError('Graph error: Node not exist.')
    
    def update_connection(self, node_, connection_, value_):
        ''' Update child in node. \n
            Input: node_ - str or int, connection_ - str or int,  value_ - int or float.'''
        if isinstance(value_, int or bool) and isinstance(connection_, str):
            if self.__graph.get(node_) and self.__graph.keys():
                if self.__graph[node_].get(connection_):
                    self.__graph[node_][connection_] = value_
                else:
                    raise ValueError('Graph error: connection not exist.')
            else:
                raise ValueError('Graph error: Node not exist.')
        else:
            raise ValueError('Graph error: Unknown parameters.')
    
    def remove_node(self, node_):
        ''' Removing node_ with childs. \n
            Input: node_ - str or int '''
        if self.__graph.get(node_):
            self.__graph.pop(node_, None)
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def remove_connection(self, node_, connection_):
        ''' Removing childs in node. \n
            Input: node_ - str or int, connection_ - str or int '''
        if self.__graph.get(node_):
            if self.__graph[node_].get(connection_):
                self.__graph[node_].pop(connection_, None)
            else:
                raise ValueError('Graph error: connection not exist.')
        else:
            raise ValueError('Graph error: Node not exist.')
    
    def get_graph(self):
        return self.__graph
    
    def wide_search(self, node_, condition = True):
        search_queue, searched = deque(), [] # Создаём очередь и массив, хранящий прошедших очередь
        search_queue += self.__graph[node_] # Задаём начальную очередь
        while search_queue: # Пока очередь не кончилась
            person = search_queue.popleft() # Извлекаем первого из очереди
            if not person in searched: # Проверяем не был ли элемент в очереди
                if self.__graph[node_][person] == condition: # Какая нибудь проверка
                    return True, (node_, person)
                else:
                    if self.__graph.get(person): # Проверяем имеет ли узел связи
                        search_queue += self.__graph[person] # Добавляем в очередь соседей
                    searched.append(person) # Добавляем в проверенные
        return False, ()

class tree(object):
    pass

class binary_tree(object):
    pass