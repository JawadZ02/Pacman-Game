# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    frontier = util.Stack()
    frontier.push([problem.getStartState(), []])
    explored = set()
    actions = []
    
    while frontier:
        state, actions = frontier.pop()
        explored.add(state)

        if problem.isGoalState(state):
            return actions
            # return list of actions
        
        for nextState, action, stepCost in problem.getSuccessors(state):
            if nextState not in explored:
                nextActions = actions + [action]
                frontier.push([nextState, nextActions])
        
    return -1
    
    # util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    frontier = util.Queue()
    frontier.push([problem.getStartState(), []])
    explored = set()
    actions = []
    
    while frontier:
        state, actions = frontier.pop()
        explored.add(state)

        if problem.isGoalState(state):
            return actions
            # return list of actions
        
        for nextState, action, stepCost in problem.getSuccessors(state):
            stateInFrontier = (nextState in (states[0] for states in frontier.list))
            if nextState not in explored and not stateInFrontier:
                nextActions = actions + [action]
                frontier.push([nextState, nextActions])
        
    return -1
    
    # util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    frontier = util.PriorityQueue()
    frontier.push([problem.getStartState(), []], 0)
    explored = set()
    actions = []
    
    while frontier:
        state, actions = frontier.pop()
        explored.add(state)

        if problem.isGoalState(state):
            return actions
            # return list of actions
        
        for nextState, action, stepCost in problem.getSuccessors(state):

            # for each successor state, we must check if it is already in the frontier
            # if it is, then we must compare the existing cost with the new cost
            # and accordingly we decide to keep one of them

            stateInFrontier = (nextState in (states[2][0] for states in frontier.heap))

            if nextState not in explored and not stateInFrontier:
                nextActions = actions + [action]
                nextCost = problem.getCostOfActions(nextActions)
                frontier.push([nextState, nextActions], nextCost)

            elif nextState not in explored and stateInFrontier:
                for states in frontier.heap:
                    if states[2][0] == nextState:
                        existingCost = problem.getCostOfActions(states[2][1])
                
                nextActions = actions + [action]
                nextCost = problem.getCostOfActions(nextActions)

                if nextCost < existingCost:
                    frontier.update([nextState, nextActions], nextCost)
        
    return -1
    
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

from util import PriorityQueue
class NewPriorityQueueWithFunction(PriorityQueue):
    
    # implemented a version of PriorityQueueWithFunction
    # which pushes and updates with parameters problem, state (item), heuristic
    # to match priorityFunction call with parameters problem, state (item), heuristic

    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, problem, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(problem, item, heuristic))

    def update(self, problem, item, heuristic, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(problem, item, heuristic)

def priorityFunction(problem, state, heuristic):
    # priority function is f(n) = g(n) + h(n)
    return problem.getCostOfActions(state[1]) + heuristic(state[0], problem)

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    frontier = NewPriorityQueueWithFunction(priorityFunction)
    frontier.push(problem, [problem.getStartState(), []], heuristic)
    explored = set()
    actions = []
    
    while frontier:
        state, actions = frontier.pop()
        explored.add(state)

        if problem.isGoalState(state):
            return actions
            # return list of actions
        
        for nextState, action, stepCost in problem.getSuccessors(state):
            
            # for each successor state, we must check if it is already in the frontier
            # if it is, then we must compare the existing cost with the new cost
            # and accordingly we decide to keep one of them
            
            stateInFrontier = (nextState in (states[2][0] for states in frontier.heap))

            if nextState not in explored and not stateInFrontier:
                nextActions = actions + [action]
                frontier.push(problem, [nextState, nextActions], heuristic)

            elif nextState not in explored and stateInFrontier:
                for states in frontier.heap:
                    if states[2][0] == nextState:
                        existingTotalCost = priorityFunction(problem, [states[2][0], states[2][1]], heuristic)
                        
                nextActions = actions + [action]
                nextTotalCost = priorityFunction(problem, [nextState, nextActions], heuristic)

                if nextTotalCost < existingTotalCost:
                    frontier.update(problem, [nextState, nextActions], heuristic, nextTotalCost)
        
    return -1
    
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
