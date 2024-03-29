// Take Tour: CustomerList.
function startTourForList() {
  var tour = introJs();

  tour.setOptions({
    showBullets: false,
    showStepNumbers: false,
    doneLabel: 'Next page',
    steps: [
      {
        element: '#step-1',
        intro: "Your cutomers will be listed here. They will appear here once \
                you will add them.",
        position: 'top'
      },
      {
        element: '#step-2',
        intro: "Let's add one.",
        position: 'left'
      }
    ]
  });

  // Go to the next page.
  tour.oncomplete(function() {
    window.location.href = customersCreateURI + '?tour=true';
  });

  tour.start();
}

// Take Tour: CustomerCreate.
function startTourForCreate() {
  var tour = introJs();

  tour.setOptions({
    showBullets: false,
    showStepNumbers: false,
    doneLabel: 'Next page',
    steps: [
      {
        element: '#step-1',
        intro: "Create your customer by filling up the fields. First and last \
                names are required. All other fields are optional.",
        position: 'top'
      },
      {
        element: '#step-2',
        intro: "Add amounts for customer. Still opportunity? Already \
                closed-win? Or closed-lost? Choose what you want. Let's add \
                one.",
        position: 'left'
      }
    ]
  });

  // Go to the next page.
  tour.oncomplete(function() {
    window.location.href = reportsURI + '?tour=true';
  });

  $('html, body').scrollTop(0);

  tour.start();
}
