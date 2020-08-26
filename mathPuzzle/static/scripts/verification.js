"use strict"
async function getSchoolClasses(school_id){
	let response = await fetch(`http://127.0.0.1:8000/api/school_classes/${school_id}`);
	let json
	if (response.ok){
		json =  await response.json();
	}else{
		alert("Ошибка HTTP: " + response.status);
	}
	return json.answer;
}

function addSchoolClasses(schoolClasses, schoolClassesArr, ){
	console.log(schoolClassesArr);
		for(let i = 0; i < schoolClassesArr.length; i++){
			let schoolClass = schoolClassesArr[i];
			schoolClasses.add(new Option(schoolClass[1], schoolClass[0]));
		}
}

function schoolChanged(){
	let school = document.getElementById("school_select");
	let schoolClasses = document.getElementById("school_class_select");
	if (school.value == -1){
		schoolClasses.disabled = true;
		schoolClasses.length = 1
	}else{
		schoolClasses.length = 1
		schoolClasses.disabled = false;
		getSchoolClasses(school.value).then(schoolClassesArr => addSchoolClasses(schoolClasses, schoolClassesArr))
		
	}
}
function onLoad(){
	let school = document.getElementById("school_select");
	schoolChanged();
	school.onchange = schoolChanged;
}

document.addEventListener("DOMContentLoaded", onLoad);
