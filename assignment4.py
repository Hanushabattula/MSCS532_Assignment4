import random
import time


# ============================================================
# PART 1: HEAPSORT
# ============================================================

def heapify(arr, n, i):
    """
    Restores the max-heap property for the subtree rooted at i.
    """

    # Assume the current node contains the largest value
    largest = i

    # Calculate the locations of the left and right children
    left = 2 * i + 1
    right = 2 * i + 2

    # Check whether the left child is larger than the current node
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check whether the right child is larger
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If a child is larger, swap it with the parent
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        # Continue restoring the heap below the swapped position
        heapify(arr, n, largest)


def heapsort(arr):
    """
    Sorts a list in ascending order using a max-heap.
    The list is modified in place.
    """

    n = len(arr)

    # Build the max-heap.
    # The last non-leaf node is located at n // 2 - 1.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Move the largest element from the root to the end.
    # After every extraction, reduce the active heap size.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]

        # Restore the heap property in the remaining heap
        heapify(arr, end, 0)

    return arr


# ============================================================
# RANDOMIZED QUICKSORT
# Used for the empirical comparison with Heapsort
# ============================================================

def randomized_quicksort(arr):
    """
    Returns a new sorted list using Randomized Quicksort.
    """

    # A list with zero or one element is already sorted
    if len(arr) <= 1:
        return arr

    # Randomly choose a pivot
    pivot = random.choice(arr)

    # Divide the values into three groups
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    # Recursively sort the smaller and greater partitions
    return (
        randomized_quicksort(less)
        + equal
        + randomized_quicksort(greater)
    )


# ============================================================
# MERGE SORT
# Used for the empirical comparison with Heapsort
# ============================================================

def merge(left, right):
    """
    Combines two sorted lists into one sorted list.
    """

    result = []
    i = 0
    j = 0

    # Compare elements from the two halves
    while i < len(left) and j < len(right):

        if left[i] <= right[j]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    # Add any values that remain in either half
    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort(arr):
    """
    Returns a new sorted list using Merge Sort.
    """

    # Base case
    if len(arr) <= 1:
        return arr

    # Divide the list into two halves
    middle = len(arr) // 2

    left_half = merge_sort(arr[:middle])
    right_half = merge_sort(arr[middle:])

    # Merge the two sorted halves
    return merge(left_half, right_half)


# ============================================================
# SORTING CORRECTNESS TESTS
# ============================================================

def run_correctness_tests():
    """
    Confirms that all three sorting algorithms return
    the expected result.
    """

    print("=" * 65)
    print("SORTING CORRECTNESS TESTS")
    print("=" * 65)

    test_array = [12, 4, 7, 1, 9, 3, 10]

    expected = sorted(test_array)

    # Heapsort modifies the list, so use a copy
    heap_result = test_array.copy()
    heapsort(heap_result)

    # Quicksort and Merge Sort return new lists
    quick_result = randomized_quicksort(test_array.copy())
    merge_result = merge_sort(test_array.copy())

    print("Original Array:       ", test_array)
    print("Expected Result:      ", expected)
    print("Heapsort Result:      ", heap_result)
    print("Randomized Quicksort: ", quick_result)
    print("Merge Sort Result:    ", merge_result)

    print("\nHeapsort correct:", heap_result == expected)
    print("Quicksort correct:", quick_result == expected)
    print("Merge Sort correct:", merge_result == expected)


# ============================================================
# EDGE-CASE TESTING
# ============================================================

def run_edge_case_tests():
    """
    Tests Heapsort with unusual inputs that can expose
    implementation errors.
    """

    print("\n" + "=" * 65)
    print("EDGE CASE TESTS")
    print("=" * 65)

    cases = {
        "Empty list": [],
        "One element": [5],
        "Two elements": [2, 1],
        "All duplicates": [4, 4, 4, 4],
        "Already sorted": [1, 2, 3, 4, 5],
        "Reverse sorted": [5, 4, 3, 2, 1],
        "Negative numbers": [3, -1, 0, -7, 2]
    }

    for name, data in cases.items():

        test_data = data.copy()

        # Sort the test case with Heapsort
        heapsort(test_data)

        # Compare against Python's sorted result
        passed = test_data == sorted(data)

        print(f"{name}: {passed}")


# ============================================================
# PERFORMANCE MEASUREMENT
# ============================================================

def measure_time(sort_function, data, runs=5):
    """
    Measures the median execution time over several runs.
    A fresh copy of the data is used for every run.
    """
    times = []

    for _ in range(runs):
        test_data = data.copy()

        start_time = time.perf_counter()
        sort_function(test_data)
        end_time = time.perf_counter()

        times.append(end_time - start_time)

    times.sort()
    return times[len(times) // 2]

def run_sorting_benchmarks():
    """
    Compares Heapsort, Randomized Quicksort, and Merge Sort
    on multiple input sizes and input distributions.
    """

    # Larger sizes make the growth trend easier to observe
    input_sizes = [1000, 5000, 10000, 20000]

    print("\n" + "=" * 65)
    print("SORTING PERFORMANCE COMPARISON")
    print("Median of 5 runs")
    print("=" * 65)

    for size in input_sizes:

        # Random values
        random_data = [
            random.randint(1, size * 5)
            for _ in range(size)
        ]

        # Already sorted values
        sorted_data = list(range(size))

        # Values in descending order
        reverse_data = list(range(size, 0, -1))

        datasets = {
            "Random": random_data,
            "Sorted": sorted_data,
            "Reverse Sorted": reverse_data
        }

        print(f"\nInput Size: {size}")

        for name, data in datasets.items():

            # Measure each algorithm using the same dataset
            heapsort_time = measure_time(
                heapsort,
                data
            )

            quicksort_time = measure_time(
                randomized_quicksort,
                data
            )

            mergesort_time = measure_time(
                merge_sort,
                data
            )

            print(f"\n{name} Dataset:")
            print(
                f"Heapsort:             "
                f"{heapsort_time:.6f} seconds"
            )
            print(
                f"Randomized Quicksort: "
                f"{quicksort_time:.6f} seconds"
            )
            print(
                f"Merge Sort:           "
                f"{mergesort_time:.6f} seconds"
            )


# ============================================================
# PART 2: TASK CLASS
# ============================================================

class Task:
    """
    Represents a task that can be placed in the priority queue.

    Each task stores:
    - task ID
    - priority
    - arrival time
    - deadline
    """

    def __init__(
        self,
        task_id,
        priority,
        arrival_time=0,
        deadline=None
    ):

        self.task_id = task_id
        self.priority = priority
        self.arrival_time = arrival_time
        self.deadline = deadline

    def __repr__(self):

        return (
            f"Task(id={self.task_id}, "
            f"priority={self.priority}, "
            f"arrival={self.arrival_time}, "
            f"deadline={self.deadline})"
        )


# ============================================================
# MAX-HEAP PRIORITY QUEUE
# ============================================================

class MaxHeapPriorityQueue:
    """
    Priority queue implemented using a binary max-heap.

    A higher numeric priority means that the task should
    be processed before a task with a lower priority.
    """

    def __init__(self):

        # Python list used to represent the binary heap
        self.heap = []


    def is_empty(self):
        """
        Checks whether the queue contains any tasks.

        Time complexity: O(1)
        """

        return len(self.heap) == 0


    def _parent(self, index):

        return (index - 1) // 2


    def _left_child(self, index):

        return 2 * index + 1


    def _right_child(self, index):

        return 2 * index + 2


    def _swap(self, first, second):

        self.heap[first], self.heap[second] = (
            self.heap[second],
            self.heap[first]
        )


    def insert(self, task):
        """
        Inserts a task into the priority queue and moves
        it upward until the max-heap property is restored.

        Time complexity: O(log n)
        """

        # Add the new task at the end of the heap
        self.heap.append(task)

        index = len(self.heap) - 1

        # Compare the task with its parent
        while index > 0:

            parent = self._parent(index)

            # Stop when heap order is correct
            if (
                self.heap[index].priority
                <= self.heap[parent].priority
            ):
                break

            # Move the higher-priority task upward
            self._swap(index, parent)

            index = parent


    def extract_max(self):
        """
        Removes and returns the task with the highest priority.

        Time complexity: O(log n)
        """

        # Nothing can be removed from an empty queue
        if self.is_empty():
            return None

        # The root contains the maximum-priority task
        highest_priority_task = self.heap[0]

        # Remove the last task
        last_task = self.heap.pop()

        # If tasks remain, move the last task to the root
        # and restore the heap property
        if not self.is_empty():

            self.heap[0] = last_task

            self._heapify_down(0)

        return highest_priority_task


    def _heapify_down(self, index):
        """
        Moves a task downward until the max-heap property
        is restored.
        """

        size = len(self.heap)

        while True:

            largest = index

            left = self._left_child(index)
            right = self._right_child(index)

            # Check the left child
            if (
                left < size
                and self.heap[left].priority
                > self.heap[largest].priority
            ):
                largest = left

            # Check the right child
            if (
                right < size
                and self.heap[right].priority
                > self.heap[largest].priority
            ):
                largest = right

            # Stop when the current task is already largest
            if largest == index:
                break

            # Move the larger child upward
            self._swap(index, largest)

            index = largest


    def _find_task_index(self, task_id):
        """
        Searches the heap for a task with a matching ID.

        Time complexity: O(n)
        """

        for index, task in enumerate(self.heap):

            if task.task_id == task_id:
                return index

        return -1


    def increase_key(self, task_id, new_priority):
        """
        Raises the priority of an existing task.

        The task search is O(n), while moving the task
        upward is O(log n). Therefore, this implementation
        has an overall complexity of O(n).
        """

        index = self._find_task_index(task_id)

        # Task was not found
        if index == -1:
            return False

        # increase_key should not lower a priority
        if new_priority < self.heap[index].priority:
            return False

        # Apply the new priority
        self.heap[index].priority = new_priority

        # Move the task upward if necessary
        while index > 0:

            parent = self._parent(index)

            if (
                self.heap[index].priority
                <= self.heap[parent].priority
            ):
                break

            self._swap(index, parent)

            index = parent

        return True


    def decrease_key(self, task_id, new_priority):
        """
        Lowers the priority of an existing task.

        The task search is O(n), and restoring heap order
        is O(log n). Overall complexity is O(n).
        """

        index = self._find_task_index(task_id)

        # Task was not found
        if index == -1:
            return False

        # decrease_key should not increase a priority
        if new_priority > self.heap[index].priority:
            return False

        # Apply the lower priority
        self.heap[index].priority = new_priority

        # A lower priority may require moving downward
        self._heapify_down(index)

        return True


# ============================================================
# PRIORITY QUEUE TESTS
# ============================================================

def run_priority_queue_tests():
    """
    Tests the required priority queue operations.
    """

    print("\n" + "=" * 65)
    print("PRIORITY QUEUE OPERATION TESTS")
    print("=" * 65)

    queue = MaxHeapPriorityQueue()

    # Verify the new queue begins empty
    print(
        "Queue initially empty:",
        queue.is_empty()
    )

    # Create several tasks
    task1 = Task(
        "T1",
        priority=3,
        arrival_time=0,
        deadline=10
    )

    task2 = Task(
        "T2",
        priority=5,
        arrival_time=1,
        deadline=8
    )

    task3 = Task(
        "T3",
        priority=2,
        arrival_time=2,
        deadline=15
    )

    task4 = Task(
        "T4",
        priority=4,
        arrival_time=3,
        deadline=12
    )

    # Insert the tasks
    queue.insert(task1)
    queue.insert(task2)
    queue.insert(task3)
    queue.insert(task4)

    print("\nHeap after insertions:")
    print(queue.heap)

    # Increase T3 from priority 2 to priority 6
    print("\nIncrease T3 priority from 2 to 6:")

    increased = queue.increase_key(
        "T3",
        6
    )

    print("Operation successful:", increased)
    print(queue.heap)

    # Decrease T2 from priority 5 to priority 1
    print("\nDecrease T2 priority from 5 to 1:")

    decreased = queue.decrease_key(
        "T2",
        1
    )

    print("Operation successful:", decreased)
    print(queue.heap)

    # Remove tasks in priority order
    print("\nExtraction order:")

    while not queue.is_empty():

        task = queue.extract_max()

        print(task)

    # Test extraction from an empty queue
    print(
        "\nExtract from empty queue returns None:",
        queue.extract_max() is None
    )


# ============================================================
# SIMPLE PRIORITY SCHEDULER SIMULATION
# ============================================================

def run_scheduler_simulation():
    """
    Demonstrates a priority-based task scheduling application.

    Tasks arrive at different times. At each time step,
    newly arrived tasks are inserted into the max-heap.
    The scheduler processes the available task with the
    highest priority and records completion time,
    waiting time, and whether the deadline was met.
    """

    print("\n" + "=" * 65)
    print("PRIORITY SCHEDULER SIMULATION")
    print("=" * 65)

    tasks = [
        Task(
            "Job-A",
            priority=2,
            arrival_time=0,
            deadline=5
        ),

        Task(
            "Job-B",
            priority=5,
            arrival_time=1,
            deadline=4
        ),

        Task(
            "Job-C",
            priority=3,
            arrival_time=1,
            deadline=3
        ),

        Task(
            "Job-D",
            priority=4,
            arrival_time=2,
            deadline=7
        ),

        Task(
            "Job-E",
            priority=1,
            arrival_time=3,
            deadline=4
        )
    ]

    queue = MaxHeapPriorityQueue()

    current_time = 0
    completed_tasks = []

    # Continue until every task has been processed
    while len(completed_tasks) < len(tasks):

        # Insert every task that arrives at this time
        for task in tasks:

            if task.arrival_time == current_time:

                queue.insert(task)

                print(
                    f"Time {current_time}: "
                    f"{task.task_id} arrived "
                    f"(priority {task.priority})"
                )

        # Process the highest-priority available task
        if not queue.is_empty():

            selected_task = queue.extract_max()

            print(
                f"Time {current_time}: "
                f"Processing {selected_task.task_id} "
                f"(priority {selected_task.priority})"
            )

            # Each task takes one time unit to process
            completion_time = current_time + 1

            # Waiting time is time spent waiting before execution
            waiting_time = (
                current_time
                - selected_task.arrival_time
            )

            # Check whether completion occurs by the deadline
            met_deadline = (
                selected_task.deadline is None
                or completion_time <= selected_task.deadline
            )

            completed_tasks.append(
                (
                    selected_task.task_id,
                    selected_task.priority,
                    selected_task.arrival_time,
                    waiting_time,
                    completion_time,
                    selected_task.deadline,
                    met_deadline
                )
            )

        else:

            print(
                f"Time {current_time}: "
                f"No task available"
            )

        current_time += 1

    print("\nScheduler Results")

    print(
        "Task | Priority | Arrival | Waiting | "
        "Completion | Deadline | Met Deadline"
    )

    for result in completed_tasks:

        task_id = result[0]
        priority = result[1]
        arrival = result[2]
        waiting = result[3]
        completion = result[4]
        deadline = result[5]
        met_deadline = result[6]

        print(
            f"{task_id:5} | "
            f"{priority:8} | "
            f"{arrival:7} | "
            f"{waiting:7} | "
            f"{completion:10} | "
            f"{deadline:8} | "
            f"{met_deadline}"
        )

    # Calculate summary statistics
    deadlines_met = sum(
        1
        for result in completed_tasks
        if result[6]
    )

    total_waiting_time = sum(
        result[3]
        for result in completed_tasks
    )

    average_waiting_time = (
        total_waiting_time / len(completed_tasks)
    )

    print(
        f"\nTasks meeting deadlines: "
        f"{deadlines_met}/{len(completed_tasks)}"
    )

    print(
        f"Average waiting time: "
        f"{average_waiting_time:.2f} time units"
    )

# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # Verify sorting correctness first
    run_correctness_tests()

    # Check unusual sorting inputs
    run_edge_case_tests()

    # Compare the three sorting algorithms
    run_sorting_benchmarks()

    # Test every required priority queue operation
    run_priority_queue_tests()

    # Demonstrate a practical scheduling application
    run_scheduler_simulation()