// Create a slider, pass in the ID of the <div>
// containing the <input>
function slider(s_id) {

    // assemble the tag id's we'll need later
    var range       = '#'+s_id;
    var inputRange  = '#input-'+s_id;
    var labelsRange = '#labels-'+s_id;

    var getTrackStyle = function (elem) {  
        var curVal = elem.value;
        // The number of stops determines the multiplier
        // below. For example, if there are 7 stops in
        // total then there will be 6 blank spaces between
        // them. So if 100% is the total length then:
        //      100 / 6 = 16.666666667% 
        var step = 100 / ($(inputRange).attr('max') - 1);
        // 
        var seltrack = (curVal - 1) * step;
        
        // Set active label
        $(labelsRange+' li').removeClass('active selected');
        var curLabel = $(labelsRange).find('li:nth-child(' + curVal + ')');
        curLabel.addClass('active selected');
        curLabel.prevAll().addClass('selected');

        console.log('getTrackStyle - '+labelsRange+' = '+curLabel.data('stop'));

        // Change background gradient.....
        // provide the necessary styling to create a 
        // colored line to the left of the selected stop.
        // and use the background color of the parent element to
        // set the background behind the unselected track.
        var style = range+' {background: linear-gradient(to right, var(--slider-active-color) 0%, var(--slider-active-color) ' + seltrack + '%, '+$(range).parent().css('background-color')+' ' + seltrack + '%, '+$(range).parent().css('background-color')+' 100%);}\n';

// NOTE: This breaks the sliders, the unselected line will disappear
// when a stop is selected. Not sure why, requires further investigation.
//
//        var prefs = ['webkit-slider-runnable-track', 'moz-range-track', 'ms-track'];
//        var prefs = ['ms-track'];
//        for (var i = 0; i < prefs.length; i++) {
//            style += range+' input::-' + prefs[i] + ' {background: linear-gradient(to right, var(--slider-active-color) 0%, var(--slider-active-color) ' + seltrack + '%, '+$(range).parent().css('background-color')+' ' + seltrack + '%, '+$(range).parent().css('background-color')+' 100%);}\n';
//        }

        console.log('getTrackStyle - style = ['+style+']');
        return style;
    };

    var sheet = document.createElement('style');
    document.body.appendChild(sheet);
    
    // when a stop is selected apply the necessary
    // styling and get the usable value of the stop.
    $(inputRange).on('input', function () {
        sheet.textContent = getTrackStyle(this);
    });

    // Change input value on label click
    $(labelsRange+' li').on('click', function () {
        var index = $(this).index();
        $(inputRange).val(index + 1).trigger('input');
    });
};
