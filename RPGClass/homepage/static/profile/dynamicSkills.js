var courseSelect;

window.onload = function() {
    courseSelect = document.getElementByID('dropdown');
    console.log(courseSelect);
}

function changeSelectedCourse(objDropDown){
    console.log(objDropDown);
    var objHidden = document.getElementById("classSelector");
    objHidden.value = objDropDown.value;
    var a = objHidden.value;
    courseDisplay.innerHTML = a || "";
}

function addSkill(){
    var ul = document.getElementById("skill-list");
    var candidate = document.getElementById("skill-candidate");
    var li = document.createElement("li");

    li.setAttribute('id',candidate.value);
    li.appendChild(document.createTextNode(candidate.value));

    ul.appendChild(li);
    document.getElementById("skill-list").appendChild(li);
    linebreak = document.createElement("br");
    ul.appendChild(linebreak);

    var droplist = document.getElementById("skill-drop");
    var option = document.createElement("option");
    option.text = li.textContent;
    droplist.add(option);
}

function removeSkill(){
    var ul = document.getElementById("skill-list");
    var candidate = document.getElementById("skill-candidate");
    var li = document.getElementById(candidate.value);
 
    ul.removeChild(li)

    var droplist = document.getElementById("skill-drop");
    var option = document.createElement("option");
    option.text = li.textContent;
    droplist.remove(option);
}

