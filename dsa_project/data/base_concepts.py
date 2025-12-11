# base_concepts.py
# Manual foundational dataset for the semi-automatic DSA Knowledge Graph
# These definitions are enriched later via scraping + auto-relations.

BASE_CONCEPTS = {

    # ------------------------------------------------------------
    # LINEAR STRUCTURES
    # ------------------------------------------------------------
    "array": {
        "name": "Array",
        "type": "linear_structure",
        "category": "data_structure",
        "basic_ops": ["access", "update", "insert", "delete"],
        "principle": "Contiguous memory block",
        "description": "A basic linear structure storing elements in contiguous memory."
    },

    "matrix": {
        "name": "Matrix",
        "type": "2d_array",
        "category": "data_structure",
        "basic_ops": ["row_access", "col_access", "transform"],
        "principle": "2D array stored in row-major or column-major order.",
        "description": "A two-dimensional array structure used for tabular representation."
    },

    "sequential_list": {
        "name": "Sequential List",
        "type": "array_based_list",
        "category": "data_structure",
        "basic_ops": ["insert", "delete", "search"],
        "principle": "List implemented using arrays.",
        "description": "A list stored as a dynamic array supporting sequential access."
    },

    "linked_list": {
        "name": "Singly Linked List",
        "type": "linked_structure",
        "category": "data_structure",
        "basic_ops": ["insert", "delete", "traverse", "search"],
        "principle": "Nodes connected via next pointers.",
        "description": "A dynamic list of nodes where each node links to the next."
    },

    "doubly_linked_list": {
        "name": "Doubly Linked List",
        "type": "linked_structure",
        "category": "data_structure",
        "basic_ops": ["insert", "delete", "traverse_forward", "traverse_backward"],
        "principle": "Nodes linked with both next and prev pointers.",
        "description": "A linked list with bidirectional traversal capability."
    },

    "circular_linked_list": {
        "name": "Circular Linked List",
        "type": "linked_structure",
        "category": "data_structure",
        "basic_ops": ["insert", "delete", "loop_traverse"],
        "principle": "Last node points back to head.",
        "description": "A linked list where the last node links back to the first node."
    },

    "general_list": {
        "name": "General List",
        "type": "adt",
        "category": "data_structure",
        "basic_ops": ["insert", "delete", "search"],
        "principle": "An abstract list supporting linear or non-linear storage.",
        "description": "An abstract list structure with varying implementations."
    },

    "generalized_list": {
        "name": "Generalized List",
        "type": "nested_list",
        "category": "data_structure",
        "basic_ops": ["depth", "evaluate", "flatten"],
        "principle": "List whose elements can be atoms or sub-lists.",
        "description": "A recursive list structure composed of atoms and sublists."
    },

    # ------------------------------------------------------------
    # STACK & QUEUE
    # ------------------------------------------------------------
    "stack": {
        "name": "Stack",
        "type": "linear_structure",
        "category": "data_structure",
        "basic_ops": ["push", "pop", "top", "is_empty"],
        "principle": "LIFO (Last-In-First-Out)",
        "description": "A linear structure supporting LIFO access."
    },

    "queue": {
        "name": "Queue",
        "type": "linear_structure",
        "category": "data_structure",
        "basic_ops": ["enqueue", "dequeue", "front", "is_empty"],
        "principle": "FIFO (First-In-First-Out)",
        "description": "A linear structure supporting FIFO access."
    },


    # ------------------------------------------------------------
    # HASHING
    # ------------------------------------------------------------
    "hash_table": {
        "name": "Hash Table",
        "type": "mapping_structure",
        "category": "data_structure",
        "basic_ops": ["insert", "delete", "search"],
        "principle": "Maps keys to values using a hash function.",
        "description": "An associative array using hashing and collision resolution."
    },


    # ------------------------------------------------------------
    # SPARSE STRUCTURES
    # ------------------------------------------------------------
    "sparse_matrix": {
        "name": "Sparse Matrix",
        "type": "matrix_structure",
        "category": "data_structure",
        "basic_ops": ["store", "retrieve", "add", "multiply"],
        "principle": "Optimized storage for matrices with many zeros.",
        "description": "A matrix stored using compressed formats like COO or CSR."
    },

    "coo_format": {
        "name": "COO Format",
        "type": "sparse_representation",
        "category": "data_structure",
        "basic_ops": ["store", "iterate"],
        "principle": "Stores triples (row, col, value).",
        "description": "Sparse matrix representation using coordinate lists."
    },

    "csr_format": {
        "name": "CSR Format",
        "type": "sparse_representation",
        "category": "data_structure",
        "basic_ops": ["row_pointer", "compressed_storage"],
        "principle": "Compressed Sparse Row representation.",
        "description": "Efficient sparse matrix structure for row-wise operations."
    },


    # ------------------------------------------------------------
    # TREE STRUCTURES
    # ------------------------------------------------------------
    "tree": {
        "name": "Tree",
        "type": "hierarchical_structure",
        "category": "data_structure",
        "basic_ops": ["traverse", "depth", "height"],
        "principle": "Hierarchical structure of nodes and children.",
        "description": "A non-linear structure consisting of nodes in parent-child relationships."
    },

    "binary_tree": {
        "name": "Binary Tree",
        "type": "tree_structure",
        "category": "data_structure",
        "basic_ops": ["preorder", "inorder", "postorder"],
        "principle": "Each node has at most two children.",
        "description": "A tree where each node has up to two children."
    },

    "bst": {
        "name": "Binary Search Tree",
        "type": "tree_structure",
        "category": "data_structure",
        "basic_ops": ["insert", "delete", "search"],
        "principle": "Left subtree < root < right subtree.",
        "description": "A binary tree supporting fast search operations."
    },

    "avl_tree": {
        "name": "AVL Tree",
        "type": "balanced_tree",
        "category": "data_structure",
        "basic_ops": ["rotate_LL", "rotate_RR", "rotate_LR", "rotate_RL"],
        "principle": "Self-balancing BST with height constraints.",
        "description": "A balanced BST ensuring logarithmic height."
    },

    "huffman_tree": {
        "name": "Huffman Tree",
        "type": "compression_tree",
        "category": "data_structure",
        "basic_ops": ["encode", "decode"],
        "principle": "Optimal prefix coding.",
        "description": "A tree used for optimal prefix-based compression."
    },


    # ------------------------------------------------------------
    # GRAPH STRUCTURES
    # ------------------------------------------------------------
    "graph": {
        "name": "Graph",
        "type": "network_structure",
        "category": "data_structure",
        "basic_ops": ["add_vertex", "add_edge", "remove_vertex", "remove_edge"],
        "principle": "Vertices connected via edges.",
        "description": "A non-linear data structure representing relationships."
    },

    "adjacency_matrix": {
        "name": "Adjacency Matrix",
        "type": "graph_representation",
        "category": "data_structure",
        "basic_ops": ["edge_lookup", "update"],
        "principle": "Matrix representation of graph edges.",
        "description": "A 2D matrix used to represent edge connections."
    },

    "adjacency_list": {
        "name": "Adjacency List",
        "type": "graph_representation",
        "category": "data_structure",
        "basic_ops": ["traverse_neighbors"],
        "principle": "Each vertex stores a list of neighbors.",
        "description": "A memory-efficient graph representation."
    },

    "union_find": {
        "name": "Union-Find",
        "type": "disjoint_set_structure",
        "category": "data_structure",
        "basic_ops": ["find", "union"],
        "principle": "Partition data into disjoint subsets.",
        "description": "A structure used for connectivity and MST algorithms."
    },


    # ------------------------------------------------------------
    # ALGORITHMS (SEARCHING)
    # ------------------------------------------------------------
    "linear_search": {
        "name": "Linear Search",
        "type": "search_algorithm",
        "category": "algorithm",
        "basic_ops": ["scan"],
        "principle": "Sequential search over elements.",
        "description": "A simple search algorithm that scans elements one by one."
    },

    "binary_search": {
        "name": "Binary Search",
        "type": "search_algorithm",
        "category": "algorithm",
        "basic_ops": ["mid_compare", "divide"],
        "principle": "Divide search space by half.",
        "description": "Efficient search on sorted arrays."
    },

    # ------------------------------------------------------------
    # ALGORITHMS (SORTING)
    # ------------------------------------------------------------
    "bubble_sort": {
        "name": "Bubble Sort",
        "type": "sorting_algorithm",
        "category": "algorithm",
        "basic_ops": ["swap", "compare"],
        "principle": "Repeatedly swap adjacent elements if out of order.",
        "description": "Simple but inefficient sorting method."
    },

    "merge_sort": {
        "name": "Merge Sort",
        "type": "sorting_algorithm",
        "category": "algorithm",
        "basic_ops": ["split", "merge"],
        "principle": "Divide-and-conquer sorting algorithm.",
        "description": "Efficient stable sorting method using recursion."
    },

    "quick_sort": {
        "name": "Quick Sort",
        "type": "sorting_algorithm",
        "category": "algorithm",
        "basic_ops": ["partition", "recursive_sort"],
        "principle": "Divide around pivot element.",
        "description": "Fast divide-and-conquer sorting method."
    },


    # ------------------------------------------------------------
    # GRAPH ALGORITHMS
    # ------------------------------------------------------------
    "bfs": {
        "name": "Breadth-First Search",
        "type": "graph_algorithm",
        "category": "algorithm",
        "basic_ops": ["enqueue", "visit"],
        "principle": "Level-order exploration.",
        "description": "Graph traversal visiting nodes in breadth-first order."
    },

    "dfs": {
        "name": "Depth-First Search",
        "type": "graph_algorithm",
        "category": "algorithm",
        "basic_ops": ["push", "visit"],
        "principle": "Explore depth first.",
        "description": "Graph traversal exploring depth-first paths."
    },

    "dijkstra": {
        "name": "Dijkstra Algorithm",
        "type": "shortest_path_algorithm",
        "category": "algorithm",
        "basic_ops": ["relax", "extract_min"],
        "principle": "Find shortest paths with non-negative weights.",
        "description": "Algorithm computing minimal distances from source."
    },

    "bellman_ford": {
        "name": "Bellman-Ford Algorithm",
        "type": "shortest_path_algorithm",
        "category": "algorithm",
        "basic_ops": ["relax"],
        "principle": "Handles negative weights.",
        "description": "Algorithm computing shortest paths including negative weights."
    },


    # ------------------------------------------------------------
    # RECURSION ALGORITHMS
    # ------------------------------------------------------------
    "recursion": {
        "name": "Recursion",
        "type": "programming_technique",
        "category": "algorithm",
        "basic_ops": ["call", "base_case"],
        "principle": "Function calling itself.",
        "description": "A method where a function solves a problem by calling itself."
    },

    "factorial_recursive": {
        "name": "Recursive Factorial",
        "type": "recursive_algorithm",
        "category": "algorithm",
        "basic_ops": ["call", "multiply"],
        "principle": "n! = n * (n-1)!",
        "description": "Classic recursive definition of factorial."
    },

    "fibonacci_recursive": {
        "name": "Recursive Fibonacci",
        "type": "recursive_algorithm",
        "category": "algorithm",
        "basic_ops": ["call", "sum"],
        "principle": "fib(n) = fib(n-1) + fib(n-2)",
        "description": "Tree-shaped recursive computation of Fibonacci numbers."
    }
}
