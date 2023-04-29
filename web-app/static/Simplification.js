/* --- */
document.addEventListener("DOMContentLoaded", () => {
  const spans = document.querySelectorAll(".verb, .adj, .noun, .aux");
  spans.forEach((span) => {
    span.addEventListener("click", async (event) => {
      const radioButton = document.querySelector("#explainWords");
      if (!radioButton.checked) {
        return;
      }
      let leftSideTag = span.closest("p");
      let rightSideTag = leftSideTag.nextElementSibling;
      sentence_of_origin = span.closest(".sentence");

      var context = "";
      for (const child of sentence_of_origin.children) {
        context = context + " " + child.textContent;
      }
      const word = event.target.textContent;
      const response = await fetch(`http://localhost:5000/look-up-word`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ word: word, sentence: context }),
      });
      result = await response.json();
      rightSideTag.textContent +=
        result.word + ":" + "\n" + result.result + "\n\n";
    });
  });
});

/* --- */
async function syntacticSimplification() {
  var selectedText = window.getSelection().toString();
  if (selectedText == "" || selectedText == null) {
    return;
  }

  var dazzle = document.querySelector(".dazzle");
  var p = document.createElement("p");
  var p2 = document.createElement("p");
  var text = document.createTextNode("Zinsbouw vereenvoudigen...");
  var prompt = document.createTextNode("...");
  p.appendChild(prompt);
  dazzle.appendChild(p);
  p2.appendChild(text);
  dazzle.appendChild(p2);
  const response = await fetch(`http://localhost:5000/simplify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: selectedText, key: "sc" }),
  });
  result = await response.json();
  prompt.nodeValue = JSON.stringify(result.prompt);
  text.nodeValue = JSON.stringify(result.result);
}

/* --- */
function insertAfter(newNode, existingNode) {
  existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

/* --- */
document.addEventListener("DOMContentLoaded", () => {
  const spans = document.querySelectorAll(".sentence");
  spans.forEach((span) => {
    span.addEventListener("click", async (event) => {
      const radioButton = document.querySelector("#simplifySentences"); // get reference to radio button
      if (!radioButton.checked) {
        return;
      }

      sentence_of_origin = span.closest(".sentence");
      var context = "";
      for (const child of sentence_of_origin.children) {
        context = context + " " + child.textContent;
      }
      const response = await fetch(`http://localhost:5000/simplify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: context, key: "sc" }),
      });
      result = await response.json();
      var p = document.createElement("p");
      newNode = document.createTextNode(JSON.stringify(result.result));
      p.append(newNode);
      insertAfter(p, span);
      sentence_of_origin.innerHTML = "<del>" + context + "</del>";
      parent = sentence_of_origin.parent;
    });
  });
});

//
async function personalizedSimplification() {
  let checkedValues = [];
  let checkboxes = document.querySelectorAll(
    '.personalisation input[type="checkbox"]'
  );
  checkboxes.forEach((checkbox) => {
if (checkbox.checked) {checkedValues.push(checkbox.name);}});

  if (checkedValues.length == 0) {return;}

  var selectedText = window.getSelection().toString();
  var selectedChoices = checkedValues;
  var prompt = document.createTextNode("Gepersonaliseerde tekst ophalen...");
  var text = document.createTextNode("...");
  var dazzle = document.querySelector(".dazzle");
  var p = document.createElement("p");
  var p2 = document.createElement("p");

  p.appendChild(prompt);
  dazzle.appendChild(p);
  p2.appendChild(text);
  dazzle.appendChild(p2);

  const response = await fetch(`http://localhost:5000/personalized-simplify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: selectedText, choices: selectedChoices }),
  });

  result = await response.json();
  prompt.nodeValue = JSON.stringify(result.prompt);
  text.nodeValue = JSON.stringify(result.result);
}


async function askGPT() {
  var promptText = window.prompt("Wat wil je veranderen aan deze tekst? Start met 'Maak deze tekst...'")
  var selectedText = window.getSelection().toString();
  var fullPrompt = promptText + '///\n' + selectedText; 
  var prompt = document.createTextNode("Gepersonaliseerde tekst ophalen...");
  var text = document.createTextNode("...");
  var dazzle = document.querySelector(".dazzle");
  var p = document.createElement("p");
  var p2 = document.createElement("p");

  p.appendChild(prompt);
  dazzle.appendChild(p);
  p2.appendChild(text);
  dazzle.appendChild(p2);

  const response = await fetch(`http://localhost:5000/personalized-simplify-custom-prompt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: selectedText, prompt: fullPrompt }),
  });

  result = await response.json();
  console.log(result);
  prompt.nodeValue = JSON.stringify(result.prompt);
  text.nodeValue = JSON.stringify(result.result);
}

async function emptyChat() {
  const dazzleDiv = document.querySelector(".dazzle");
  dazzleDiv.innerHTML = "";
}