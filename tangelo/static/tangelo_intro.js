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
        {
          element: document.querySelector('#left-menu-toggle'),
          intro: "Click here to search for available widgets.",
        },
        {
          element: document.querySelector('#widget-follow-list'),
          intro: "And click on your favorites to follow! We have everything ranging from a personalized daily poem and Princeton News, to updates from student groups.",
          position: "right"
        },
        {
          element: document.querySelector('#right-menu-toggle'),
          intro: "Click here to manage your widgets and create your own."
        },
        {
          element: document.querySelector('#trash'),
          intro: "If you're ready to let go of a widget, simply drag it here!."
        },
      ]
    });
    intro.onbeforechange(function () {

        if (this._currentStep === 4 || this._currentStep === 6) {
              $('.introjs-helperNumberLayer').addClass('introjs-stepno-top-visible');
        } else {
              $('.introjs-helperNumberLayer').removeClass('introjs-stepno-top-visible');
        }

        if (this._currentStep === 4) {
            if (document.querySelector("#wrapper").classList.contains('left-toggled')) {
                document.querySelector("#left-menu-toggle").click();
            }
        }

        if (this._currentStep === 6) {
            if (document.querySelector("#wrapper").classList.contains('right-toggled')) {
                document.querySelector("#right-menu-toggle").click();
            }
        }
    });

    intro.start();
}
