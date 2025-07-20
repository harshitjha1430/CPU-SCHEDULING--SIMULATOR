# 🖥️ CPU Scheduling Simulator

A Python-based simulator for key CPU scheduling algorithms:

- First Come First Served (FCFS)
- Round Robin (RR) (with customizable Time Quantum)
- Shortest Job First (SJF) – both Preemptive and Non-Preemptive

The simulator calculates and displays:

- Completion Time
- Turnaround Time
- Waiting Time
- Gantt Chart

---

## 📌 Features

- Simulates FCFS, SJF (Preemptive & Non-Preemptive), and Round Robin
- User-defined Time Quantum for Round Robin
- Takes arrival and burst time inputs
- Computes:
  - Completion Time (CT)
  - Turnaround Time (TAT = CT - Arrival Time)
  - Waiting Time (WT = TAT - Burst Time)
- Displays a clean textual Gantt chart

---

## ⚙️ How It Works

1. User inputs:
   - Number of processes
   - Arrival time and burst time for each process
   - Choice of scheduling algorithm
   - Time quantum (for Round Robin)

2. The program performs:
   - Simulation of the chosen scheduling method
   - Calculation of CT, TAT, WT
   - Gantt chart generation

---

## 🛠️ How to Run

### Requirements

- Python 3.x

### Run Command

`