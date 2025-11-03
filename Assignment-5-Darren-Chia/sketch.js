//Assignment 5 Darren Chia
// Magama color palette, triangle/circle overlap, variation of step 6 animated
let canvasWidth = 800;
let canvasHeight = 600;
let cellWidth = 800 / 8;
let cellHeight = 600 / 6;

// Animation variables
let animationMode = 'rotating';
let rotationAngle = 0;
let pulseAmount = 0;
let colorOffset = 0;
let appearProgress = 0;

// Dropdown selector
let selector;

// Magma style palette 
let palette = [
  "#000004","#120a32","#2b0b5b","#51127c",
  "#6c1d81","#8c2d7c","#a83a73","#c24e67",
  "#d86358","#ea7b48","#f3953f","#f9b43b",
  "#f9cf43","#f6e85a","#fcf7a0","#fefbd7"
];

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  ellipseMode(CENTER);

  selector = select('#animationSelect');
  if (selector) selector.changed(changeAnimation);
}

function draw() {
  background(0);

  updateAnimationVariables();
  rotationAngle += 0.02; // rotate whole cell

  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 6; j++) {
      let colorIndex = (8 * j + i) % palette.length;

      // cell center
      let cx = i * cellWidth + cellWidth / 2;
      let cy = j * cellHeight + cellHeight / 2;

      push();
      translate(cx, cy);
      rotate(rotationAngle);

      // Draw both shapes per cell
      drawMultipleCircles(0, 0, cellWidth * 0.95, colorIndex, 16);
      drawMultipleTriangles(0, 0, cellWidth,       colorIndex, 16);

      pop();
    }
  }
}

function updateAnimationVariables() {
  switch (animationMode) {
    case 'pulsing':
      pulseAmount = sin(frameCount * 0.05) * 20;
      break;
    case 'colorShift':
      colorOffset = (colorOffset + 0.1) % palette.length;
      break;
    case 'appearing':
      appearProgress = (sin(frameCount * 0.02) + 1) / 2; 
      break;
  }
}

function changeAnimation() {
  animationMode = selector.value();
  rotationAngle = 0;
  pulseAmount = 0;
  colorOffset = 0;
  appearProgress = 0;
}

// Helper function to draw circles and triangles

function drawCircle(x, y, diameter, fillColor, strokeColor) {
  fill(fillColor);
  stroke(strokeColor);
  strokeWeight(2);
  ellipse(x, y, diameter, diameter);
}

function drawTriangle(x, y, size, fillColor, strokeColor) {
  fill(fillColor);
  stroke(strokeColor);
  strokeWeight(1);
  const half = size / 2;
  triangle(
    x, y - half,       
    x - half, y + half, 
    x + half, y + half  
  );
}



function drawMultipleCircles(centerX, centerY, diameter, colorIndex, number) {
  let angle = TWO_PI / number;

  let currentDiameter = diameter;
  let currentColorIndex = colorIndex;
  if (animationMode === 'pulsing') currentDiameter = diameter + pulseAmount;
  if (animationMode === 'colorShift')
    currentColorIndex = floor((colorIndex + colorOffset) % palette.length);

  const base = color(palette[currentColorIndex]);
  const fillColor   = color(red(base), green(base), blue(base), 18);
  const strokeColor = color(red(base), green(base), blue(base), 40);

  for (let i = 0; i < number; i++) {
    if (animationMode === 'appearing' && i / number > appearProgress) continue;

    const newX = sin(angle * i) * currentDiameter / 4 + centerX;
    const newY = cos(angle * i) * currentDiameter / 4 + centerY;
    drawCircle(newX, newY, currentDiameter / 2, fillColor, strokeColor);
  }
}

function drawMultipleTriangles(centerX, centerY, diameter, colorIndex, number) {
  const angle = TWO_PI / number;

  const baseSize = diameter * 0.9;
  let currentSize = baseSize;
  let currentColorIndex = colorIndex;

  if (animationMode === 'pulsing') currentSize = baseSize + pulseAmount;
  if (animationMode === 'colorShift')
    currentColorIndex = floor((colorIndex + colorOffset) % palette.length);

  const base = color(palette[currentColorIndex]);
  const fillColor   = color(red(base), green(base), blue(base), 45);
  const strokeColor = color(red(base), green(base), blue(base), 90);

  for (let i = 0; i < number; i++) {
    if (animationMode === 'appearing' && i / number > appearProgress) continue;

    const newX = sin(angle * i) * diameter / 4 + centerX;
    const newY = cos(angle * i) * diameter / 4 + centerY;
    drawTriangle(newX, newY, currentSize / 2, fillColor, strokeColor);
  }
}

