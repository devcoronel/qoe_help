var msg = document.getElementById("msg")

let mynode = document.getElementById("id-node");
let mydays = document.getElementById("id-days");


const myform = document.getElementById("form_sumary");

myform.addEventListener("submit", function (e) {
	e.preventDefault();
		
	const formData = new FormData(this);

	fetch("/sumario", {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {

			if (data.msg) {
				console.log(data.msg)
				document.getElementById("msg").value = data.msg
				
			} else {
				console.log("There was an error")
				
			}
		})
		.catch(err => {
			console.log("There was an error")
			
		})
	}	
);
