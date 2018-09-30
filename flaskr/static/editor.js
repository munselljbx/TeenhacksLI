/*function canvasClick () {
    coords = canvas.relMouseCoords(event);
    getBox(event.pageX, event.pageY, grid);
}*/

function selectRoom() {
    placingMode = "room";
}
function selectHallway() {
    placingMode = "hall";
}
function selectStair() {
    placingMode = "stair";
}
function selectEmpty() {
    placingMode = "empty";
}
function autoAssign() {
    for (var i = 0; i < grid.length; i ++) {
        for (var j = 0; j < grid[i].length; j ++) {
            grid[i][j].id = i.toString() + j.toString();
            console.log(grid);
        }
    }
}

function submitInfo() {

}

/*
function relMouseCoords(event){
    var totalOffsetX = 0;
    var totalOffsetY = 0;
    var canvasX = 0;
    var canvasY = 0;
    var currentElement = this;

    do{
        totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
        totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
    }
    while(currentElement = currentElement.offsetParent)

    canvasX = event.pageX - totalOffsetX;
    canvasY = event.pageY - totalOffsetY;

    return {x:canvasX, y:canvasY}
}
HTMLCanvasElement.prototype.relMouseCoords = relMouseCoords;
*/
window.onload = function () {
    function getBox (x, y, grid) {
        for (var i = 0; i < grid.length; i ++) {
            for (var j = 0; j < grid[i].length; j ++) {
                box = grid[i][j];
                if (x > box.x && x < box.x + rectWidth && y > box.y && y < box.y + rectHeight) {
                    grid[i][j].type = placingMode;
                    console.log(box.x);
                    grid[i][j].id = document.getElementById("set-id").value;
                    grid[i][j].subjects.push(selectedSubject);
                    if (placingMode == "room") {
                        ctx.fillStyle = "black";
                    }
                    if (placingMode == "hall") {
                        ctx.fillStyle = "blue";
                    }
                    if (placingMode == "stair") {
                        ctx.fillStyle = "red";
                    }
                    if (placingMode == "empty") {
                        ctx.fillStyle = "white";
                    }
                    ctx.fillRect(box.x, box.y, rectWidth, rectHeight);
                }
            }
        }
    }
canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");
function on_canvas_click(ev) {
    var x = ev.clientX - canvas.offsetLeft;
    var y = ev.clientY - canvas.offsetTop;
    getBox(x, y, grid);

}
canvas.addEventListener('click', on_canvas_click, false);
placingMode = "empty";

gridX = 10;
gridY = 10;
rectWidth = canvas.width / gridX;
rectHeight = canvas.height / gridY;
grid = [];

for (var x = 0; x < gridX; x ++) {
    grid.push([]);
    for (var y = 0; y < gridY; y ++) {
        grid[x].push({id: "", subjects: [], type: "empty", x: x * rectWidth, y: y * rectHeight});
        ctx.strokeStyle = "black";
        ctx.lineWidth = 0.1;
        ctx.rect(x * rectWidth, y * rectHeight, (x*rectWidth) + rectWidth, (y*rectHeight) + rectHeight);
        ctx.stroke();
    }
}
}
