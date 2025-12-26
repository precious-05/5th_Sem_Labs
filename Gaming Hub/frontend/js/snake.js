const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const box = 20;
let snake;
let direction;
let food;
let score;
let game;

// ===============================
// LOAD USER FROM SESSION
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
  document.getElementById("username").textContent = data.user.name;
}

loadUser();

// ===============================
// START GAME
// ===============================
function startGame() {
  snake = [{ x: 9 * box, y: 10 * box }];
  direction = "RIGHT";
  score = 0;

  food = {
    x: Math.floor(Math.random() * 19) * box,
    y: Math.floor(Math.random() * 19) * box
  };

  document.getElementById("score").textContent = score;
  document.getElementById("status").textContent = "";

  clearInterval(game);
  game = setInterval(draw, 150);
}

document.addEventListener("keydown", changeDirection);

// ===============================
// CHANGE DIRECTION
// ===============================
function changeDirection(event) {
  if (event.key === "ArrowLeft" && direction !== "RIGHT") direction = "LEFT";
  else if (event.key === "ArrowUp" && direction !== "DOWN") direction = "UP";
  else if (event.key === "ArrowRight" && direction !== "LEFT") direction = "RIGHT";
  else if (event.key === "ArrowDown" && direction !== "UP") direction = "DOWN";
}

// ===============================
// DRAW GAME
// ===============================
function draw() {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw Snake
  for (let i = 0; i < snake.length; i++) {
    ctx.fillStyle = i === 0 ? "lime" : "green";
    ctx.fillRect(snake[i].x, snake[i].y, box, box);
  }

  // Draw Food
  ctx.fillStyle = "red";
  ctx.fillRect(food.x, food.y, box, box);

  // Snake Head Position
  let headX = snake[0].x;
  let headY = snake[0].y;

  if (direction === "LEFT") headX -= box;
  if (direction === "UP") headY -= box;
  if (direction === "RIGHT") headX += box;
  if (direction === "DOWN") headY += box;

  // Eat Food
  if (headX === food.x && headY === food.y) {
    score++;
    document.getElementById("score").textContent = score;

    food = {
      x: Math.floor(Math.random() * 19) * box,
      y: Math.floor(Math.random() * 19) * box
    };
  } else {
    snake.pop();
  }

  let newHead = { x: headX, y: headY };

  // Game Over Conditions
  if (
    headX < 0 || headY < 0 ||
    headX >= canvas.width || headY >= canvas.height ||
    collision(newHead, snake)
  ) {
    clearInterval(game);
    document.getElementById("status").textContent = "Game Over!";
    return;
  }

  snake.unshift(newHead);
}

// ===============================
// COLLISION CHECK
// ===============================
function collision(head, body) {
  for (let i = 0; i < body.length; i++) {
    if (head.x === body[i].x && head.y === body[i].y) {
      return true;
    }
  }
  return false;
}

// ===============================
// BUTTONS
// ===============================
function restartGame() {
  startGame();
}

function goBack() {
  window.location.href = "dashboard.html";
}

// Start initially
startGame();
