function startIntro(){
    var intro = introJs();
    intro.setOptions({
      steps: [
        {
          intro: "Hello! This is ~Tangelo~, the daily app designed for Princeton students. \n\n Let's get started!"
        },
        {
          element: document.querySelector('#step1'),
          intro: "This is your personalized Tangelo dashboard."
        },
        {
          element: document.querySelector('[widget-id="1"]'),
          intro: "And this is your first widget."
        },
      ]
    });

    intro.start();
}
