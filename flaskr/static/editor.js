window.onload = function () {

canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");

gridX = 10;
gridY = 10;
rectWidth = canvas.width / gridX;
rectHeight = canvas.height / gridY;
grid = [];

for (var x = 0; x < gridX; x ++) {
    grid.push([]);
    for (var y = 0; y < gridY; y ++) {
        grid[x].push({id: "", subjects: []});
        ctx.strokeStyle = "black";
        ctx.rect(x * rectWidth, y * rectHeight, (x*rectWidth) + rectWidth, (y*rectHeight) + rectHeight);
        ctx.stroke();
    }
}
}
