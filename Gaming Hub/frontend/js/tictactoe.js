let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameActive = true;
let score = 0;

const statusText = document.getElementById("status");
const scoreText = document.getElementById("score");
const usernameText = document.getElementById("username");
const cells = document.querySelectorAll(".cell");

// ===============================
// FETCH USER NAME FROM SESSION
// ===============================
async function loadUser() {
  const res = await fetch("http://localhost:5000/api/user/dashboard", {
    credentials: "include"
  });

  if (!res.ok) {
    window.location.href = "login.html";
    return;
  }

  const data = await res.json();
  usernameText.textContent = data.user.name;
}

loadUser();

// ===============================
// WINNING CONDITIONS
// ===============================
const winningCombinations = [
  [0,1,2], [3,4,5], [6,7,8],
  [0,3,6], [1,4,7], [2,5,8],
  [0,4,8], [2,4,6]
];

// ===============================
// HANDLE CELL CLICK
// ===============================
cells.forEach(cell => {
  cell.addEventListener("click", () => {
    const index = cell.getAttribute("data-index");

    if (board[index] !== "" || !gameActive) return;

    board[index] = currentPlayer;
    cell.textContent = currentPlayer;

    checkResult();
  });
});

// ===============================
// CHECK GAME RESULT
// ===============================
function checkResult() {
  let roundWon = false;

  for (let condition of winningCombinations) {
    const [a, b, c] = condition;

    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      roundWon = true;
      break;
    }
  }

  if (roundWon) {
    statusText.textContent = `Player ${currentPlayer} wins!`;
    score++;
    scoreText.textContent = score;
    gameActive = false;
    return;
  }

  if (!board.includes("")) {
    statusText.textContent = "Game Draw!";
    gameActive = false;
    return;
  }

  currentPlayer = currentPlayer === "X" ? "O" : "X";
}

// ===============================
// RESTART GAME
// ===============================
function restartGame() {
  board = ["", "", "", "", "", "", "", "", ""];
  gameActive = true;
  currentPlayer = "X";
  statusText.textContent = "";

  cells.forEach(cell => cell.textContent = "");
}

// ===============================
// BACK TO DASHBOARD
// ===============================
function goBack() {
  window.location.href = "dashboard.html";
}
