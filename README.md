# 🧭 Pathfinding Visualizer

An interactive **Pathfinding Algorithm Visualizer** built in **Python (Pygame)** that helps visualize how different algorithms find the shortest path between two points — just like how **Google Maps** finds routes between locations.

---

## 🚀 Features

- 🎯 Visualizes multiple pathfinding algorithms:
  - **A\*** (A-Star) → Fastest and most accurate
  - **Dijkstra’s Algorithm**
  - **Breadth-First Search (BFS)**
  - **Depth-First Search (DFS)**
- 🧱 Create barriers and obstacles freely
- 🟩 Start and end node placement
- 🟨 Real-time animation of algorithm progress
- 🧹 Clear grid instantly
- 🖱️ Easy mouse interaction
- 🖥️ Responsive UI with legend box (works on laptops)

---

## 🧠 Algorithms Used

| Algorithm | Type | Optimal | Weighted | Notes |
|------------|-------|----------|-----------|--------|
| **A\*** | Heuristic | ✅ Yes | ✅ Yes | Combines Dijkstra + Greedy |
| **Dijkstra’s** | Weighted | ✅ Yes | ✅ Yes | Expands all nodes equally |
| **BFS** | Unweighted | ✅ Yes | ❌ No | Explores level by level |
| **DFS** | Unweighted | ❌ No | ❌ No | Goes deep before wide |

---

## 🎮 Controls

| Key / Action | Description |
|---------------|-------------|
| **Left Click** | Place Start, End, or Barriers |
| **Right Click** | Remove Node |
| **1** | Run **A\*** Algorithm |
| **2** | Run **Dijkstra’s** Algorithm |
| **3** | Run **BFS** Algorithm |
| **4** | Run **DFS** Algorithm |
| **SPACE** | Start Visualization |
| **C** | Clear Grid |
| **Exit Button** | Close Window |

---

## 🧰 Tech Stack

- **Language:** Python 3.12+
- **Library:** [Pygame](https://www.pygame.org/)
- **IDE:** VS Code

---

## ⚙️ Installation & Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/pathfinding-visualizer.git
   cd pathfinding-visualizer
