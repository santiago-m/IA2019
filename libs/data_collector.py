import sys
sys.path.append('../aima-python')
import time
import multiprocessing 
from generic_heuristics import *
from search import *
from search_algorithms import *

class DataCollector:

    @staticmethod
    def run_fun(function, args, result):
        res = function(*args)
        result.put(res)

    @staticmethod
    def run_for_seconds(function, args, seconds):
        solution = None
        solution_time = -1
        result = multiprocessing.Queue()

        # Start function in process
        p = multiprocessing.Process(target=DataCollector.run_fun, args=(function, args, result))

        init = time.time()
        p.start()
        # Wait for 10 seconds or until process finished
        p.join(seconds)
        end = time.time()

        # If thread is not still alive
        if (not p.is_alive()):
            #print(result)
            solution = result.get()
            if (solution):
                solution_time = end - init

        # Terminate
        p.terminate()
        p.join()

        return (solution, solution_time)


    @staticmethod
    def collect_greedy_best_first(puzzles, size, iterations, timeout):
        if (iterations < 1):
            return None

        manhattan_solutions = []
        manhattan_lengths = []
        manhattan_times = []

        misplaced_solutions = []
        misplaced_lengths = []
        misplaced_times = []

        gaschnig_solutions = []
        gaschnig_lengths = []
        gaschnig_times = []

        max_manh_gasch_solutions = []
        max_manh_gasch_lengths = []
        max_manh_gasch_times = []

        ''' ------------------------------------ Greedy Best First Search with Manhattan as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(greedy_best_first_graph_search, (p, NPuzzleHeuristics(size).manhattan), timeout)
            if timed_run_result[1] == -1:
                manhattan_solutions.append(timed_run_result[0])
            else:
                manhattan_solutions.append(timed_run_result[0].solution())
            manhattan_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        ''' ------------------------------------ Greedy Best First Search with Misplaced_Tiles as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(greedy_best_first_graph_search, (p, NPuzzleHeuristics(size).misplaced_tiles), timeout)
            if timed_run_result[1] == -1:
                misplaced_solutions.append(timed_run_result[0])
            else:
                misplaced_solutions.append(timed_run_result[0].solution())
            misplaced_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        ''' ------------------------------------ Greedy Best First Search with Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(greedy_best_first_graph_search, (p, NPuzzleHeuristics(size).gaschnig), timeout)
            if timed_run_result[1] == -1:
                gaschnig_solutions.append(timed_run_result[0])
            else:
                gaschnig_solutions.append(timed_run_result[0].solution())
            gaschnig_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        ''' ------------------------------------ Greedy Best First Search with Max_Manhattan_Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(greedy_best_first_graph_search, (p, NPuzzleHeuristics(size).max_manhattan_gaschnig), timeout)
            if timed_run_result[1] == -1:
                max_manh_gasch_solutions.append(timed_run_result[0])
            else:
                max_manh_gasch_solutions.append(timed_run_result[0].solution())
            max_manh_gasch_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        return ( ('Manhattan', manhattan_solutions, manhattan_times), ('Misplaced Tiles', misplaced_solutions, misplaced_times), ('Gaschnig', gaschnig_solutions, gaschnig_times), ('Max Manhattan Gaschnig', max_manh_gasch_solutions, max_manh_gasch_times) )

    @staticmethod
    def collect_best_first_tree(puzzles, size, iterations, timeout):
        if (iterations < 1):
            return None

        manhattan_solutions = []
        manhattan_lengths = []
        manhattan_times = []

        misplaced_solutions = []
        misplaced_lengths = []
        misplaced_times = []

        gaschnig_solutions = []
        gaschnig_lengths = []
        gaschnig_times = []

        max_manh_gasch_solutions = []
        max_manh_gasch_lengths = []
        max_manh_gasch_times = []

        ''' ------------------------------------ Greedy Best First Search with Manhattan as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(best_first_tree_search, (p, NPuzzleHeuristics(size).manhattan), timeout)
            if timed_run_result[1] == -1:
                manhattan_solutions.append(timed_run_result[0])
            else:
                manhattan_solutions.append(timed_run_result[0].solution())
            manhattan_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        ''' ------------------------------------ Greedy Best First Search with Misplaced_Tiles as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(best_first_tree_search, (p, NPuzzleHeuristics(size).misplaced_tiles), timeout)
            if timed_run_result[1] == -1:
                misplaced_solutions.append(timed_run_result[0])
            else:
                misplaced_solutions.append(timed_run_result[0].solution())
            misplaced_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        ''' ------------------------------------ Greedy Best First Search with Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(best_first_tree_search, (p, NPuzzleHeuristics(size).gaschnig), timeout)
            if timed_run_result[1] == -1:
                gaschnig_solutions.append(timed_run_result[0])
            else:
                gaschnig_solutions.append(timed_run_result[0].solution())
            gaschnig_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        ''' ------------------------------------ Greedy Best First Search with Max_Manhattan_Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(best_first_tree_search, (p, NPuzzleHeuristics(size).max_manhattan_gaschnig), timeout)
            if timed_run_result[1] == -1:
                max_manh_gasch_solutions.append(timed_run_result[0])
            else:
                max_manh_gasch_solutions.append(timed_run_result[0].solution())
            max_manh_gasch_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''

        return ( ('Manhattan', manhattan_solutions, manhattan_times), ('Misplaced Tiles', misplaced_solutions, misplaced_times), ('Gaschnig', gaschnig_solutions, gaschnig_times), ('Max Manhattan Gaschnig', max_manh_gasch_solutions, max_manh_gasch_times) )

    @staticmethod
    def collect_astar_search(puzzles, size, iterations, timeout):
        if iterations < 1:
            return None
    
        manhattan_solutions = []
        manhattan_lengths = []
        manhattan_times = []
    
        misplaced_solutions = []
        misplaced_lengths = []
        misplaced_times = []
    
        gaschnig_solutions = []
        gaschnig_lengths = []
        gaschnig_times = []
    
        max_manh_gasch_solutions = []
        max_manh_gasch_lengths = []
        max_manh_gasch_times = []
        
        ''' ------------------------------------ A* Search with Manhattan as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(fixed_astar_search, (p, NPuzzleHeuristics(size).manhattan), timeout)
            if timed_run_result[1] == -1:
                manhattan_solutions.append(timed_run_result[0])
            else:
                manhattan_solutions.append(timed_run_result[0].solution())
            manhattan_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
            
        ''' ------------------------------------ A* Search with Misplaced_Tiles as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(fixed_astar_search, (p, NPuzzleHeuristics(size).misplaced_tiles), timeout)
            if timed_run_result[1] == -1:
                misplaced_solutions.append(timed_run_result[0])
            else:
                misplaced_solutions.append(timed_run_result[0].solution())
            misplaced_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
            
        ''' ------------------------------------ A* Search with Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(fixed_astar_search, (p, NPuzzleHeuristics(size).gaschnig), timeout)
            if timed_run_result[1] == -1:
                gaschnig_solutions.append(timed_run_result[0])
            else:
                gaschnig_solutions.append(timed_run_result[0].solution())
            gaschnig_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
        
        ''' ------------------------------------ A* Search with Max_Manhattan_Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(fixed_astar_search, (p, NPuzzleHeuristics(size).max_manhattan_gaschnig), timeout)
            if timed_run_result[1] == -1:
                max_manh_gasch_solutions.append(timed_run_result[0])
            else:
                max_manh_gasch_solutions.append(timed_run_result[0].solution())
            max_manh_gasch_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
    
        return ( ('Manhattan', manhattan_solutions, manhattan_times), ('Misplaced Tiles', misplaced_solutions, misplaced_times), ('Gaschnig', gaschnig_solutions, gaschnig_times), ('Max Manhattan Gaschnig', max_manh_gasch_solutions, max_manh_gasch_times) )

    @staticmethod
    def collect_astar_tree_search(puzzles, size, iterations, timeout):
        if iterations < 1:
            return None
    
        manhattan_solutions = []
        manhattan_lengths = []
        manhattan_times = []
    
        misplaced_solutions = []
        misplaced_lengths = []
        misplaced_times = []
    
        gaschnig_solutions = []
        gaschnig_lengths = []
        gaschnig_times = []
    
        max_manh_gasch_solutions = []
        max_manh_gasch_lengths = []
        max_manh_gasch_times = []
        
        ''' ------------------------------------ A* Search with Manhattan as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(astar_tree_search, (p, NPuzzleHeuristics(size).manhattan), timeout)
            if timed_run_result[1] == -1:
                manhattan_solutions.append(timed_run_result[0])
            else:
                manhattan_solutions.append(timed_run_result[0].solution())
            manhattan_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
            
        ''' ------------------------------------ A* Search with Misplaced_Tiles as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(astar_tree_search, (p, NPuzzleHeuristics(size).misplaced_tiles), timeout)
            if timed_run_result[1] == -1:
                misplaced_solutions.append(timed_run_result[0])
            else:
                misplaced_solutions.append(timed_run_result[0].solution())
            misplaced_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
            
        ''' ------------------------------------ A* Search with Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(astar_tree_search, (p, NPuzzleHeuristics(size).gaschnig), timeout)
            if timed_run_result[1] == -1:
                gaschnig_solutions.append(timed_run_result[0])
            else:
                gaschnig_solutions.append(timed_run_result[0].solution())
            gaschnig_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
        
        ''' ------------------------------------ A* Search with Max_Manhattan_Gaschnig as Heuristic. -----------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(astar_tree_search, (p, NPuzzleHeuristics(size).max_manhattan_gaschnig), timeout)
            if timed_run_result[1] == -1:
                max_manh_gasch_solutions.append(timed_run_result[0])
            else:
                max_manh_gasch_solutions.append(timed_run_result[0].solution())
            max_manh_gasch_times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
    
        return ( ('Manhattan', manhattan_solutions, manhattan_times), ('Misplaced Tiles', misplaced_solutions, misplaced_times), ('Gaschnig', gaschnig_solutions, gaschnig_times), ('Max Manhattan Gaschnig', max_manh_gasch_solutions, max_manh_gasch_times) )


    @staticmethod
    def collect_iterative_deepening(puzzles, size, iterations, timeout):
        if iterations < 1:
            return None
    
        solutions = []
        times = []
        
        ''' ---------------------------------------------- Iterative Deepening Search. -------------------------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(iterative_deepening_search, (p,), timeout)
            if timed_run_result[1] == -1:
                solutions.append(timed_run_result[0])
            else:
                solutions.append(timed_run_result[0].solution())
            times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
    
        return ('-', solutions, times)

    @staticmethod
    def collect_iterative_deepening_graph(puzzles, size, iterations, timeout):
        if iterations < 1:
            return None
    
        solutions = []
        times = []
        
        ''' ---------------------------------------------- Iterative Deepening Search. -------------------------------------------------------'''
        for p in puzzles:
            timed_run_result = DataCollector.run_for_seconds(iterative_deepening_graph_search, (p,), timeout)
            if timed_run_result[1] == -1:
                solutions.append(timed_run_result[0])
            else:
                solutions.append(timed_run_result[0].solution())
            times.append(timed_run_result[1])
        ''' ----------------------------------------------------------------------------------------------------------------------------------- '''
    
        return ('-', solutions, times)