var student_input = [];
var subjects = [];
function submitStudents() {
  var new_id = document.getElementById("student-id").value;
  var new_courses = document.getElementById("student-courses").value;
  var student = {
    id: new_id,
    courses: new_courses
  };
  room_input.push(student);
  console.log(student_input);
}
<<<<<<< HEAD
function submitSubjects() {
    subjectNameElement = document.getElementById("room-id");
    subjectName = subjectNameElement.value;
    subjects.push(subjectName);
    subjectNameElement.value = "";

    subjectList = document.getElementById("subject-list");
    listItem = document.createElement("li");
    listItem.innerHTML = subjectName;
    removeButton = document.createElement("button");
    removeButton.innerHTML = "-";
    removeButton.id = "remove-button";
    removeButton.onclick = function () {
        this.parentElement.parentElement.removeChild(this.parentElement);
    };
    listItem.appendChild(removeButton);
    subjectList.appendChild(listItem);
=======
function submitRooms() {
  var new_id = document.getElementById("room-id").value;
  var new_courses = document.getElementById("room-courses").value;
  var room = {
    id: new_id,
    courses: new_courses
  };
  room_input.push(room);
  console.log(room_input);
>>>>>>> d8014ece8a3e9e4d157032934d980cd123baad32
}

function submitCSV() {
    importButton = document.getElementById("importButton");
    f = importButton.files.get(0);
    console.log(f);
}
