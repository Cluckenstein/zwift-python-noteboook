function postWorkout(){
    var ex_string = "add(600,[50,65],90)\ninter(5, 45, 100, 300, 65)\nadd(300, 50, 80)\nadd(600, [65,50])\ntext(1,'let the games begin')";
    $.ajax({
        type : 'POST',
        cache : false,
        url: "/ploter/",  
        data : {'ftp' : '300',
                'name' : 'Example_Workout',
                'description' : 'Put anything you like in here!',
                'string' : ex_string,
                'generate' : 0},
        dataType: 'json',
        success : function(response)
        {   
            console.log(typeof response)
            if (typeof response == 'object') {
                console.log(response)
                plot = document.getElementById('plot')
                Plotly.newPlot(plot, response,{}) 
            }
        }
    });
}

function postWorkoutGenerate(){
    var date = new Date();
    var tag = date.toISOString().slice(0,23).replace(/-/g,"-").replace(":","-");

    var ex_string = "add(600,[50,65])\ninter(5, 45, 100, 300, 65)\nadd(300, 50)\nadd(600, [65,50])\ntext(1,'let the games begin')";
    $.ajax({
        type : 'POST',
        cache : false,
        url: "/generator/",  
        data : {'ftp' : '300',
                'name' : 'Example_Workout',
                'description' : 'Put anything you like in here!',
                'string' : ex_string,
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

                var link = tag + '-Example_Workout';
                var url = "/zwo_download/" + link + ".zwo";
                window.open(url);
            }
           
        }
    });
}

window.onload = function() {
	document.getElementById("button_show").onclick = function() {
        console.log('posting  box')
		postWorkout()
    };
    
    document.getElementById("button_gen").onclick = function() {
        console.log('posting  box and generating file')
		postWorkoutGenerate()
    };
}


