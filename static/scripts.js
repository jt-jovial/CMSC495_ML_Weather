function select(input) {
    let value = input.value;
    //reset form
    let df = document.getElementById("dynamic-form");
    let dl = document.getElementById("daylight-form");
    let bt = document.getElementById("execute-button");
    df.innerHTML = "<p id=\"dynamic-form\"></p>"
    dl.innerHTML = "<p id=\"daylight-form\"></p>"
    bt.innerHTML = "<p id=\"execute-button\"></p>"

    form_maker(value);
}

function day_input(in_bool) {
    let insertpoint = document.getElementById("daylight-form");
    let DAYLIGHT = document.createElement("input");

    if (in_bool === "true") {
        DAYLIGHT.setAttribute("type", "text");
        DAYLIGHT.setAttribute("name", "daylight");
        DAYLIGHT.setAttribute("id", "daylight");
        DAYLIGHT.setAttribute("form", "ak-form");
        let DAYNUMTEXT = document.createTextNode("How many daylight hours would you prefer? (3.5-22): ");
        insertpoint.appendChild(DAYNUMTEXT);
        insertpoint.append(DAYLIGHT);
    }
    else {
        insertpoint.innerHTML = "<p id=\"daylight-form\"></p>"
    }
}

function form_maker(input) {
    function temp_form() {
        // Create a form dynamically
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        // Create an input element for temperature
        let TEMP = document.createElement("input");
        TEMP.setAttribute("type", "text");
        TEMP.setAttribute("name", "temp");
        TEMP.setAttribute("placeholder", "Degrees");

        // Create a selection element for daylight hours
        let DAY = document.createElement("select");
        DAY.setAttribute("name", "day-check");
        DAY.setAttribute("id", "day-check");
        DAY.setAttribute("form", "ak-form");
        DAY.add(new Option("No", "false", true));
        DAY.add(new Option("Yes", "true", false));

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "temp_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        // Append the temp input to the form
        let TEMPTEXT = document.createTextNode("What is your preferred temperature? (Fahrenheit): ")
        form.appendChild(TEMPTEXT);
        form.append(TEMP);
        form.innerHTML += "<br><br>";

        // Append the daylight select to the form
        let DAYTEXT = document.createTextNode("Do you have a preference with regards to number of daylight hours?")
        form.appendChild(DAYTEXT);
        form.innerHTML += "<br>";
        form.append(DAY);

        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);
        document.getElementById("day-check").addEventListener(
            "change", function() {day_input(this.value);}, false);
    }

    function day_form() {
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        day_input("true")

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "day_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);
    }

    function snow_form() {
        // Create a form dynamically
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        // Create an input element for snowfall
        let SNOW = document.createElement("input");
        SNOW.setAttribute("type", "text");
        SNOW.setAttribute("name", "snow");
        SNOW.setAttribute("form", "ak-form");
        SNOW.setAttribute("placeholder", "Inches");

        // Create a selection element for daylight hours
        let DAY = document.createElement("select");
        DAY.setAttribute("name", "day-check");
        DAY.setAttribute("id", "day-check");
        DAY.setAttribute("form", "ak-form");
        DAY.add(new Option("No", "false", true));
        DAY.add(new Option("Yes", "true", false));

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "snow_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        // Append the temp input to the form
        let SNOWTEXT = document.createTextNode("How much accumulated snow would you like to see? (0-24in): ")
        form.appendChild(SNOWTEXT);
        form.append(SNOW);
        form.innerHTML += "<br><br>";

        // Append the daylight select to the form
        let DAYTEXT = document.createTextNode("Do you have a preference with regards to number of daylight hours?")
        form.appendChild(DAYTEXT);
        form.innerHTML += "<br>";
        form.append(DAY);

        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);
        document.getElementById("day-check").addEventListener(
            "change", function() {day_input(this.value);}, false);
    }

    function light_form() {
        // Create a form dynamically
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        // Create a selection element for daylight hours
        let DAY = document.createElement("select");
        DAY.setAttribute("name", "day-check");
        DAY.setAttribute("id", "day-check");
        DAY.setAttribute("form", "ak-form");
        DAY.add(new Option("No", "false", true));
        DAY.add(new Option("Yes", "true", false));

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "light_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        // Append the temp input to the form
        let LIGHTTEXT = document.createTextNode("The best time to see the Northern Lights is between August and April.")
        form.appendChild(LIGHTTEXT);
        form.innerHTML += "<br><br>";

        // Append the daylight select to the form
        let DAYTEXT = document.createTextNode("Do you have a preference with regards to number of daylight hours?")
        form.appendChild(DAYTEXT);
        form.innerHTML += "<br>";
        form.append(DAY);

        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);
        document.getElementById("day-check").addEventListener(
            "change", function() {day_input(this.value);}, false);
    }

    switch (input) {
        case "temp":
            temp_form();
            break;
        case "daylight":
            day_form();
            break;
        case "snowfall":
            snow_form();
            break;
        case "northernlights":
            light_form();
            break;
        default:
            //return nothing
            let form = document.createElement("form");
            document.getElementById("dynamic-form")
                .appendChild(form);
    }
}