function runConversion(fromUnit, toUnit, amount, history = []) {
  if (fromUnit === toUnit) {
    // return the amount if you're converting a unit to itself
    return amount;
  }
  // recursively search for a way to convert the two units
  if (toUnit in ConversionFunctions[fromUnit]) {
    // a conversion is available
    return ConversionFunctions[fromUnit][toUnit](amount);
  }
  // try to runConversion with every possible conversion
  for (let [conversion, conversionFunction] of Object.entries(ConversionFunctions[fromUnit])) {
    if (!history.includes(conversion)) {
      let result = runConversion(conversion, toUnit, conversionFunction(amount), history.concat([fromUnit]));
      if (result !== null) {
        return result;
      }
    }
  }
  return null;
}

const liveConversionInput = document.getElementById("live-conversion-input");

function showConversion(fromUnit, toUnit) {
  document.getElementById("live-conversion").style.display = "block";
  document.getElementById("from-unit").textContent = SpecialPlurals[fromUnit] || fromUnit + "s";
  document.getElementById("to-unit").textContent = SpecialPlurals[toUnit] || toUnit + "s";

  function updateConversion() {
    let num = parseFloat(this.value);
    if (isNaN(num)) {
      document.getElementById("after-conversion").textContent = "0";
    } else {
      let conversionResult = runConversion(fromUnit, toUnit, num);
      let writtenResult = conversionResult;
      if (conversionResult === 0) {
        writtenResult = "0";
      }
      document.getElementById("after-conversion").textContent = writtenResult || "not convertable to";
    }
  }
  updateConversion.call(liveConversionInput);
  liveConversionInput.oninput = updateConversion;
}

function generateConversions(units) {
  return units.map(unit => {
    let unitClone = Object.assign({}, unit);
    if (unitClone.type === "answer") {
      // add a question "To what unit?"
      // after To what unit?, run the conversion
      unitClone.nextQuestion = {
        "To what unit?": units.map(unit2 => {
          let unit2Clone = Object.assign({}, unit2);
          if (unit2Clone.type === "answer") {
            // add a function to show the actual conversion
            unit2Clone.nextFunction = () => {
              showConversion(unitClone.text, unit2Clone.text)
            };
          }
          return unit2Clone;
        })
      };
    }
    return unitClone;
  });
}

const QuestionTree = {
  "What is measured?": [{
      type: "answer",
      text: "Length",
      nextQuestion: {
        "What unit are you converting?": generateConversions(LengthUnits)
      }
    },
    {
      type: "answer",
      text: "Temperature",
      nextQuestion: {
        "What unit are you converting?": generateConversions(TemperatureUnits)
      }
    },
    {
      type: "answer",
      text: "Speed",
      nextQuestion: {
        "What unit are you converting?": generateConversions(SpeedUnits)
      }
    },
    {
      type: "answer",
      text: "Time",
      nextQuestion: {
        "What unit are you converting?": generateConversions(TimeUnits)
      }
    },
    {
      type: "answer",
      text: "Mass",
      nextQuestion: {
        "What unit are you converting?": generateConversions(MassUnits)
      }
    },
    {
      type: "answer",
      text: "Volume",
      nextQuestion: {
        "What unit are you converting?": generateConversions(VolumeUnits)
      }
    }
  ]
};

const unitSelector = document.getElementById("unit-selector");

function renderQuestion(question) {
  let questionName = Object.keys(question)[0];
  let answersAndCategories = question[questionName];
  let questionElem = document.createElement("div");
  questionElem.className = "question";
  let questionTitle = document.createElement("p");
  questionTitle.textContent = questionName;
  questionElem.appendChild(questionTitle);
  for (let answerOrCategory of answersAndCategories) {
    if (answerOrCategory.type === "answer") {
      // this is an answer
      let answerElem = document.createElement("button");
      answerElem.className = "answer";
      answerElem.textContent = answerOrCategory.text;
      // add a click listener
      answerElem.addEventListener("click", () => {
        // deactivate all other answers
        for (let elem of questionElem.children) {
          if (elem.classList.contains("answer")) {
            elem.classList.remove("active");
          }
        }
        // activate the answer element
        answerElem.classList.add("active");
        // remove all questions after this one
        let questionsAfter = [];
        let questionAfter = questionElem.nextElementSibling;
        while (questionAfter !== null) {
          questionsAfter.push(questionAfter);
          questionAfter = questionAfter.nextElementSibling;
        }
        for (let question of questionsAfter) {
          unitSelector.removeChild(question);
        }
        // render the next question OR run the next function
        if (answerOrCategory.nextQuestion) {
          renderQuestion(answerOrCategory.nextQuestion);
        } else if (answerOrCategory.nextFunction) {
          answerOrCategory.nextFunction();
        }
      });
      questionElem.appendChild(answerElem);
    } else if (answerOrCategory.type === "category") {
      // this is a category
      let categoryElem = document.createElement("p");
      categoryElem.className = "answer-category";
      categoryElem.textContent = answerOrCategory.text;
      questionElem.appendChild(categoryElem);
    }
  }
  unitSelector.appendChild(questionElem);
}

renderQuestion(QuestionTree);