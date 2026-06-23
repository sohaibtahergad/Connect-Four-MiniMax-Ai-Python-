# Connect 4 with AI (Minimax & Alpha-Beta Pruning)

A desktop Connect 4 game built in Python using **Pygame**. The project features an interactive Graphical User Interface (GUI), adjustable AI difficulty settings, and real-time performance metrics (search time, nodes evaluated, and move utility values).

This project was developed as part of a 1st-year university computer science assignment to demonstrate game theory algorithms, heuristic evaluation, and GUI state management.

---

##  Features

* **Human vs. AI Gameplay:** Play against an intelligent agent optimized using adversarial search techniques.
* **Dynamic Difficulty Slider:** Adjust the AI's lookahead depth dynamically via an in-game GUI slider (Depth 1 to 7).
* **Performance Tracking Dashboard:** Displays execution analytics for every move:
* **Iterations (Nodes):** The total number of board states analyzed.
* **Time taken:** Engine computation time in milliseconds (`ms`).
* **Move Value:** The exact heuristic evaluation score calculated for the chosen branch.


* **Clean Visuals:** Responsive grid layout built on Pygame with real-time turn animations and accurate match-end states (Win/Loss/Draw notifications).

---

##  Core Algorithms & Architecture

###  The AI Engine

The backbone of the AI is a **Minimax Algorithm** enhanced with **Alpha-Beta Pruning**. Alpha-Beta pruning optimizes the search tree by short-circuiting branches that cannot possibly influence the final decision, drastically lowering execution time at deeper lookaheads.

###  Heuristic Evaluation Function

When the engine reaches the specified search limit (`DEPTH == 0`), it scores the board using a localized heuristic evaluation sequence (`score_board`):

* **Center Column Control:** Prioritizes drops in the center column to maximize horizontal and diagonal alignment options.
* **Window Scanning:** Slides a 4-slot window horizontally, vertically, and diagonally across the board to evaluate positional weight:
* 4-in-a-row (AI) $\rightarrow$ **+100,000** (Instant Win State)
* 3-in-a-row + 1 Empty $\rightarrow$ **+5**
* 2-in-a-row + 2 Empty $\rightarrow$ **+2**
* Opponent 3-in-a-row (Block Hazard) $\rightarrow$ **-4**



---

##  Prerequisites & Installation

Ensure you have Python 3.x installed on your system. You will also need `pygame`.

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME

```


2. **Install dependencies:**
```bash
pip install pygame

```


3. **Run the game:**
```bash
python main.py

```



---

##  How To Play

1. **Set Difficulty:** Launch the game and adjust the green slider to select your desired AI lookahead depth. Click **SELECT** to confirm.
2. **Make a Move:** Hover your cursor over the column grid and click inside the column boundaries where you want to drop your piece.
3. **AI Turn:** The game freezes input momentarily while displaying `AI thinking...` and plotting the optimized response based on your selected algorithm depth.
4. **Play Again:** Upon a win, loss, or tie, view your historical match summary (Total time & iterations calculated) and click **Play again** to reset.

---

##  Project Structure

```text
├── main.py          # Complete application code containing Game Engine, Minimax, and Pygame UI logic
└── README.md        # Documentation
* [ ] **Bitboards:** Implement bitwise operations for board representations to accelerate win detection and move-generation.
* [ ] **Transposition Tables:** Cache previously evaluated board states using Zobrist hashing to avoid duplicate sub-tree processing.
* [ ] **Move Ordering:** Sort moves (e.g., assessing center columns first) to trigger alpha-beta cutoffs significantly earlier in the recursive loop.
