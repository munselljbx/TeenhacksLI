var student_input = [];
var subjects = [];
function submitStudents() {
  var new_id = document.getElementById("student-id").value;
  var new_courses = document.getElementById("student-courses").value;
  student_input.push(new_input);
  console.log(student_input);
}
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
}

function submitCSV() {
    importButton = document.getElementById("importButton");
    f = importButton.files.get(0);
    console.log(f);
}
