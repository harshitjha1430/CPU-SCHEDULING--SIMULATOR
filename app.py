from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# FCFS Algorithm
def calculate_fcfs(processes):
    processes.sort(key=lambda x: x['arrival_time'])  # Sort by arrival time
    current_time = 0
    results = []
    for process in processes:
        start_time = max(current_time, process['arrival_time'])
        completion_time = start_time + process['burst_time']
        turnaround_time = completion_time - process['arrival_time']
        waiting_time = turnaround_time - process['burst_time']
        results.append({
            "PID": process['pid'],
            "Arrival Time": process['arrival_time'],
            "Burst Time": process['burst_time'],
            "Completion Time": completion_time,
            "Turnaround Time": turnaround_time,
            "Waiting Time": waiting_time
        })
        current_time = completion_time
    return results

def calculate_sjf(processes, preemptive=False):
    if not preemptive:
        # Non-preemptive logic
        processes.sort(key=lambda x: (x['arrival_time'], x['burst_time']))
        current_time = 0
        results = []
        for process in processes:
            start_time = max(current_time, process['arrival_time'])
            completion_time = start_time + process['burst_time']
            turnaround_time = completion_time - process['arrival_time']
            waiting_time = turnaround_time - process['burst_time']
            results.append({
                "PID": process['pid'],
                "Arrival Time": process['arrival_time'],
                "Burst Time": process['burst_time'],
                "Completion Time": completion_time,
                "Turnaround Time": turnaround_time,
                "Waiting Time": waiting_time
            })
            current_time = completion_time
        return results

    # Preemptive SJF (SRTF)
    remaining_times = {p['pid']: p['burst_time'] for p in processes}
    arrival_times = {p['pid']: p['arrival_time'] for p in processes}
    completed = set()
    results = []
    current_time = 0

    while len(completed) < len(processes):
        # Filter processes that have arrived but not completed
        available_processes = [p for p in processes if p['arrival_time'] <= current_time and p['pid'] not in completed]

        if available_processes:
            # Find process with shortest remaining time
            ongoing_process = min(available_processes, key=lambda p: remaining_times[p['pid']])
            pid = ongoing_process['pid']

            # Execute the process for 1 time unit
            remaining_times[pid] -= 1
            current_time += 1

            # Check if the process is completed
            if remaining_times[pid] == 0:
                completed.add(pid)
                completion_time = current_time
                turnaround_time = completion_time - arrival_times[pid]
                waiting_time = turnaround_time - ongoing_process['burst_time']

                results.append({
                    "PID": pid,
                    "Arrival Time": arrival_times[pid],
                    "Burst Time": ongoing_process['burst_time'],
                    "Completion Time": completion_time,
                    "Turnaround Time": turnaround_time,
                    "Waiting Time": waiting_time
                })
        else:
            # No process is ready; increment time
            current_time += 1

    return results


def calculate_round_robin(processes, quantum):
    queue = []  # Queue to manage processes
    results = []  # List to store results
    remaining_burst_times = {p['pid']: p['burst_time'] for p in processes}  # Dictionary for remaining burst times
    current_time = 0  # Start from time 0

    # First, add all processes to the queue
    queue.extend(processes)  # Add all processes to the queue initially

    while queue:
        # Get the first process from the queue
        process = queue.pop(0)
        pid = process['pid']
        
        # Wait until the arrival time of the process is matched with the current time
        if current_time < process['arrival_time']:
            # If the current time is less than the arrival time, move time forward
            current_time = process['arrival_time']
        
        # Execute the process for a maximum of quantum time
        execution_time = min(quantum, remaining_burst_times[pid])
        remaining_burst_times[pid] -= execution_time  # Reduce remaining burst time
        current_time += execution_time  # Increase current time by execution time

        if remaining_burst_times[pid] == 0:  # If the process is completed
            completion_time = current_time
            turnaround_time = completion_time - process['arrival_time']
            waiting_time = turnaround_time - process['burst_time']
            results.append({
                "PID": pid,
                "Arrival Time": process['arrival_time'],
                "Burst Time": process['burst_time'],
                "Completion Time": completion_time,
                "Turnaround Time": turnaround_time,
                "Waiting Time": waiting_time
            })
        else:
            # Re-queue the process if it's not finished
            queue.append(process)

    return results


@app.route("/")
def home():
    return render_template("scheduling_simulator.html")

@app.route('/schedule/fcfs', methods=['POST'])
def schedule_fcfs():
    data = request.get_json()
    processes = data['processes']
    result = calculate_fcfs(processes)  # Replace with your actual scheduling function
    quantum = data.get('quantum', 0)
    preemptive = data.get('preemptive', False)  
    return render_template("results.html", algorithm="FCFS", results=result,preemptive=preemptive,quantum=quantum)

@app.route('/schedule/sjf', methods=['POST'])
def schedule_sjf():
    data = request.get_json()
    processes = data['processes']
    quantum = data.get('quantum', 0)
    preemptive = data.get('preemptive', False)  # Default to False if not provided
    
    result = calculate_sjf(processes, preemptive)  # Replace with your actual scheduling function
    return render_template("results.html", algorithm="SJF", results=result, preemptive=preemptive,quantum=quantum)

@app.route('/schedule/round_robin', methods=['POST'])
def schedule_round_robin():
    data = request.get_json()
    processes = data['processes']
    preemptive = data.get('preemptive', False)
    quantum = data.get('quantum', 0)  # Default to 0 if not provided
    result = calculate_round_robin(processes, quantum)  # Replace with your actual scheduling function
    return render_template("results.html", algorithm="Round Robin", results=result,quantum=quantum,preemptive=preemptive)


if __name__ == '__main__':
    app.run(debug=True)
