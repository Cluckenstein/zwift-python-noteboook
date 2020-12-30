function postWorkout(){
    $.ajax({
        type : 'POST',
        cache : false,
        //url : "{{url_for('tester')}}",
        url: "http://reihn.synology.me:5000/ploter/",  
        data : {'ftp' : document.getElementById('ftp').value,
                'name' : document.getElementById('workoutName').value,
                'description' : document.getElementById('workoutDescription').value,
                'string' : document.getElementById('workoutGen').value,
                'generate' : 0},
        dataType: 'json',
        success : function(response)
        {   
            console.log(typeof response)
            if (typeof response == 'object') {
                console.log(response)
                //fig = JSON.parse(response);
                plot = document.getElementById('plot')
                Plotly.newPlot(plot, response,{}) 
            }
        }
    });
}

function postWorkoutGenerate(){
    var date = new Date();
    var tag = date.toISOString().slice(0,23).replace(/-/g,"-").replace(":","-");
    $.ajax({
        type : 'POST',
        cache : false,
        //url : "{{url_for('tester')}}",
        url: "http://reihn.synology.me:5000/generator/",  
        data : {'ftp' : document.getElementById('ftp').value,
                'name' : document.getElementById('workoutName').value,
                'description' : document.getElementById('workoutDescription').value,
                'string' : document.getElementById('workoutGen').value,
                'generate' : tag},
        dataType: 'json',
        success : function(response)
        {   
            console.log(typeof response)
            console.log(response)
            if (typeof response == 'object') {
                console.log(response)
                //fig = JSON.parse(response);
                plot = document.getElementById('plot')
                Plotly.newPlot(plot, response,{}) 

                if (document.getElementById('workoutName').value == ''){
                    var link = tag + '-new Workout';
                } else {
                    var link = tag + '-' +document.getElementById('workoutName').value;
                }
                var url = "http://reihn.synology.me:5000/zwo_download/" + link + ".zwo";
                /**
                var win = window.open("http://localhost:5000/zwo_download/" + link + ".zwo", '_blank');
                
                Object.assign(document.createElement('a'), {
                    target: '_blank',
                    href: url,
                  }).click(); */
                window.open(url);
            }
           
        }
    });
}

window.onload = function() {
	// setup the button click
	document.getElementById("button_show").onclick = function() {
        console.log('posting  box')
		postWorkout()
    };
    
    document.getElementById("button_gen").onclick = function() {
        console.log('posting  box and generating file')
		postWorkoutGenerate()
	};
}


