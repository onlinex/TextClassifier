// ParticlesJS Config.
particlesJS("particles-js", {
    "particles": {
      "number": {
        "value": 80,
        "density": {
          "enable": false,
          "value_area": 700 } },
  
  
      "color": {
        "value": "#fff" },
  
      "shape": {
        "type": "circle",
        "stroke": {
          "width": 0,
          "color": "#003" },
  
        "polygon": {
          "nb_sides": 5 } },
  
  
      "opacity": {
        "value": 0.5,
        "random": false,
        "anim": {
          "enable": false,
          "speed": 0.1,
          "opacity_min": 0.1,
          "sync": false } },
  
  
      "size": {
        "value": 3,
        "random": true,
        "anim": {
          "enable": false,
          "speed": 10,
          "size_min": 0.1,
          "sync": false } },
  
  
      "line_linked": {
        "enable": true,
        "distance": 150,
        "color": "#003",
        "opacity": 0.4,
        "width": 1 },
  
      "move": {
        "enable": true,
        "speed": 2,
        "direction": "none",
        "random": false,
        "straight": false,
        "out_mode": "out",
        "bounce": false,
        "attract": {
          "enable": false,
          "rotateX": 600,
          "rotateY": 1200 } } },
  

    
    "interactivity": {
      "detect_on": "canvas",
      "events": {
        "onhover": {
          "enable": false,
          "mode": "grab" },
  
        "onclick": {
          "enable": false,
          "mode": "push" },
  
        "resize": true },
  
      "modes": {
        "grab": {
          "distance": 140,
          "line_linked": {
            "opacity": 1 } },
  
  
        "bubble": {
          "distance": 400,
          "size": 40,
          "duration": 2,
          "opacity": 8,
          "speed": 3 },
  
        "repulse": {
          "distance": 200,
          "duration": 0.4 },
  
        "push": {
          "particles_nb": 4 },
  
        "remove": {
          "particles_nb": 2 } } },
  
  
  
    "retina_detect": true });


///////////////////////////////////////

function setNumbers(val) {
    $(".progress").each(function(){
        var $bar = $(this).find(".bar");
        var $val = $(this).find("span");

        // round
        var perc = parseInt(val, 10);

        $({p:0}).animate({p:perc}, {
        duration: 2200,
        easing: "swing",
        step: function(p) {
            $bar.css({
            transform: "rotate("+ (45+(p*1.8)) +"deg)", // 100%=180° so: ° = % * 1.8
            // 45 is to add the needed rotation to have the green borders at the bottom
            });
            $val.text(''.concat(p|0, '%'));
        }
        });
    });
}

///////////////////////////////////////

/* zingchart.min.js */

function setChartConfig(val) {

  keys = Object.keys(val);
  values = Object.values(val).map(element => parseInt(element * 100, 10));
  len = keys.length;

  return {
    type: 'radar',
    plot: {
      aspect: 'area',
      animation: {
        effect: 3,
        sequence: 1,
        speed: 700
      }
    },
    scaleV: {
      values: "0:100:1", // Set min/max/step.
      visible: false
    },
    scaleK: {
      values: '0:'+String(len-1)+':1', // from - to - step
      labels: keys,
      guide: {
        alpha: 0.3,
        backgroundColor: "#c5c5c5 #718eb4"
      }
    },
    series: [
      {
        values: values
      }
    ]
  };
}

function renderChart(val) {
  zingchart.render({
    id: 'RadarChart',
    data: setChartConfig(val),
    height: '100%',
    width: '100%'
  });
}