var student_input = [];
var subjects = [];

var fr = new FileReader();
var selectedSubject = "";
fr.onload = function () {
    text = fr.result;
    lines = text.split("\n");
    student_info = [];
    importedSubjects = [];
    subjectList = document.getElementById("subject-list");
    for (var i = 1; i < lines[0].length - 2; i ++) {
        if (lines[i] != undefined) {
            student_info.push({
                "id": lines[i].split(", ")[0],
                "courses": lines[i].split(", ").slice(1)
            });
            for (var j = 0; j < lines[i].split(", ").slice(1).length; j ++) {
                if (!(importedSubjects.indexOf(lines[i].split(", ").slice(1)[j]) > -1)) { //js black magic OwOno
                    importedSubjects.push(lines[i].split(", ").slice(1)[j]);
                    listItem = document.createElement("li");
                    listItem.innerHTML = lines[i].split(", ").slice(1)[j];
                    listItem.subject = lines[i].split(", ").slice(1)[j];
                    listItem.onclick = function () {
                        selectedSubject = this.subject;
                        console.log(selectedSubject);
                    }
                    removeButton = document.createElement("button");
                    removeButton.innerHTML = "-";
                    removeButton.id = "remove-button";
                    removeButton.onclick = function () {
                        this.parentElement.parentElement.removeChild(this.parentElement);
                    };
                    listItem.appendChild(removeButton);
                    subjectList.appendChild(listItem);
                }
            }
        }
    }

}

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
    f = importButton.files.item(0);
    fr.readAsText(f);
}
