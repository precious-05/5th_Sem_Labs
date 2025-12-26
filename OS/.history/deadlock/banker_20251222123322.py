# =====================================================
# OPERATING SYSTEM PROJECT
# Topic: Deadlock Avoidance & Recovery
# Algorithm: Banker's Algorithm
# Mode: CLI Based
# Language: Python
# =====================================================


# -----------------------------------------------------
# BANKER'S ALGORITHM (SAFETY CHECK)
# -----------------------------------------------------
def bankers_algorithm(processes, available, max_need, allocated):

    num_processes = len(processes)      # Total number of processes
    num_resources = len(available)      # Total number of resource types

    # -------------------------------------------------
    # STEP 1: Calculate NEED matrix
    # NEED = MAX - ALLOCATION
    # -------------------------------------------------
    need = []

    for i in range(num_processes):          # i = process index
        need_row = []

        for j in range(num_resources):      # j = resource index
            # Formula:
            # need[i][j] = max_need[i][j] - allocated[i][j]

            # Dry run example:
            # i = 1 , j = 2
            # need[1][2] = max_need[1][2] - allocated[1][2]

            value = max_need[i][j] - allocated[i][j]
            need_row.append(value)

        need.append(need_row)

    # -------------------------------------------------
    # STEP 2: Initialize Finish and Work
    # -------------------------------------------------
    finish = [False] * num_processes
    # finish[i] = False means process Pi is not completed yet

    work = available.copy()
    # work initially contains available resources
    # Example: work = [3, 3, 2]

    safe_sequence = []


    # -------------------------------------------------
    # STEP 3: Find Safe Sequence
    # -------------------------------------------------
    while len(safe_sequence) < num_processes:

        allocated_in_this_cycle = False

        for i in range(num_processes):

            # Check only unfinished processes
            if finish[i] == False:

                # Condition:
                # need[i][j] <= work[j] for all resources j

                can_execute = True

                for j in range(num_resources):

                    # Dry run example:
                    # need[2][1] <= work[1]

                    if need[i][j] > work[j]:
                        can_execute = False
                        break

                # -------------------------------------------------
                # If process can execute safely
                # -------------------------------------------------
                if can_execute:

                    # Assume process Pi completes execution
                    for j in range(num_resources):

                        # Release allocated resources back to work
                        # work[j] = work[j] + allocated[i][j]

                        # Dry run example:
                        # work[0] = work[0] + allocated[2][0]

                        work[j] += allocated[i][j]

                    finish[i] = True
                    safe_sequence.append(processes[i])
                    allocated_in_this_cycle = True

        # -------------------------------------------------
        # If no process could be allocated in this cycle
        # -------------------------------------------------
        if not allocated_in_this_cycle:
            return False, []

    return True, safe_sequence


# -----------------------------------------------------
# DEADLOCK DETECTION
# -----------------------------------------------------
def detect_deadlock(available, allocated, request):

    num_processes = len(allocated)
    num_resources = len(available)

    work = available.copy()
    finish = [False] * num_processes

    while True:
        progress = False

        for i in range(num_processes):

            if finish[i] == False:

                can_finish = True

                for j in range(num_resources):

                    # Dry run example:
                    # request[3][1] <= work[1]

                    if request[i][j] > work[j]:
                        can_finish = False
                        break

                if can_finish:

                    # Release resources
                    for j in range(num_resources):
                        work[j] += allocated[i][j]

                    finish[i] = True
                    progress = True

        if not progress:
            break

    # Processes which could not finish are deadlocked
    deadlocked = []

    for i in range(num_processes):
        if finish[i] == False:
            deadlocked.append(i)

    return deadlocked


# -----------------------------------------------------
# DEADLOCK RECOVERY
# -----------------------------------------------------
def recover_deadlock(deadlocked, allocated, available):

    print("\nDeadlock detected.")
    print("Recovering system...\n")

    for p in deadlocked:
        print(f"Terminating Process P{p}")

        for j in range(len(available)):

            # Release resources of terminated process
            # available[j] = available[j] + allocated[p][j]

            # Dry run example:
            # available[2] = available[2] + allocated[3][2]

            available[j] += allocated[p][j]

    print("\nResources released.")
    print("System recovered.")


# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------
def main():

    processes = ["P0", "P1", "P2", "P3", "P4"]

    # Available resources
    available = [3, 3, 2]

    # Maximum required resources
    max_need = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    # Currently allocated resources
    allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    print("-----------Running Banker's Algorithm------------\n")

    safe, sequence = bankers_algorithm(
        processes, available, max_need, allocated
    )

    if safe:
        print("System is in SAFE STATE")
        print("Safe Sequence:", " -> ".join(sequence))

    else:
        print("System is in UNSAFE STATE")

        # Build request matrix
        request = []

        for i in range(len(processes)):
            row = []
            for j in range(len(available)):
                # request[i][j] = max_need[i][j] - allocated[i][j]
                row.append(max_need[i][j] - allocated[i][j])
            request.append(row)

        deadlocked = detect_deadlock(
            available, allocated, request
        )

        recover_deadlock(deadlocked, allocated, available)


# -----------------------------------------------------
# PROGRAM ENTRY POINT
# -----------------------------------------------------
if __name__ == "__main__":
    main()
