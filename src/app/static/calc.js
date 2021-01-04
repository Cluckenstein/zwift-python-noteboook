function postWorkout(){
    
    $.ajax({
        type : 'POST',
        cache : false,
        url: "/ploter/",  
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
                plot = document.getElementById('plot')
                Plotly.newPlot(plot, response,{}) 
            }
        }
    });
}

function postWorkoutGenerate(tag){
    //var date = new Date();
    //var tag = date.toISOString().slice(0,23).replace(/-/g,"-").replace(":","-");
    $.ajax({
        type : 'POST',
        cache : false,
        url: "/generator/",  
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

                
                //var url = "/zwo_download/" + link + ".zwo";
                //window.open(url);
            }
           
        }
    });
}

function postWorkoutExample(){
    var ex_string = "ramp(600,50,65,90)\ninter(5, 45, 100, 300, 65)\nadd(300, 50, 80)\nramp(600, 65,50)\ntext(1,'let the games begin')";
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
                plot = document.getElementById('plot_example')
                Plotly.newPlot(plot, response,{}) 
            }
        }
    });
}

function postWorkoutGenerateExample(tag){
    //var date = new Date();
    //var tag = date.toISOString().slice(0,23).replace(/-/g,"-").replace(":","-");

    var ex_string = "ramp(600,50,65,90)\ninter(5, 45, 100, 300, 65)\nadd(300, 50, 80)\nramp(600, 65,50)\ntext(1,'let the games begin')";
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
                plot = document.getElementById('plot_example')
                Plotly.newPlot(plot, response,{}) 

                //var link = tag + '-Example_Workout';
                //var url = "/zwo_download/" + link + ".zwo";
                //window.open(url);
            }
           
        }
    });
}

window.onload = function() {
	document.getElementById("button_show").onclick = function() {
        console.log('posting box')
		postWorkout()
    };
    
    document.getElementById("button_gen").onclick = function() {
        console.log('posting box and generating file')

        var date = new Date();
        var tag = date.toISOString().slice(0,23).replace(/-/g,"-").replace(":","-");

        if (document.getElementById('workoutName').value == ''){
            var link = tag + '-new Workout';
        } else {
            var link = tag + '-' +document.getElementById('workoutName').value;
        }
        var url = "/zwo_download/" + link + ".zwo";
        window.open(url);

		postWorkoutGenerate(tag);
    };

    document.getElementById("button_show_example").onclick = function() {
        console.log('posting box')
		postWorkoutExample()
    };
    
    document.getElementById("button_gen_example").onclick = function() {
        console.log('posting box and generating file')

        var date = new Date();
        var tag = date.toISOString().slice(0,23).replace(/-/g,"-").replace(":","-");
        var link = tag + '-Example_Workout';
        var url = "/zwo_download/" + link + ".zwo";
        window.open(url);
        
		postWorkoutGenerateExample(tag);
    };
    /** 
    document.getElementById("button_example").onclick = function() {
        window.location.href = "/example";
    };
    */ 
}


