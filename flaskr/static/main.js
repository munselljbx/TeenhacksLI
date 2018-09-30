var student_input = [];
var room_input = [];
function submitStudents() {
  var new_id = document.getElementById("student-id").value;
  var new_courses = document.getElementById("student-courses").value;
  student_input.push(new_input);
  console.log(student_input);
}
function submitRooms() {
  new_id = document.getElementById("room-id").value;
  new_courses = document.getElementById("room-courses").value;
  var room = {
    id: new_id,
    courses: new_courses
  };
  room_input.push(room);
  console.log(room_input);
}
function submitInfo() {

}
