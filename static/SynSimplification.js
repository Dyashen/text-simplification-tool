const callPythonFunctionSyntacticSimplification = async (text) => {
  try {
    const response = await fetch(
      `http://localhost:5000/syntactic-simplify?text=${text}`
    );
    return (result = await response.json());
  } catch (error) {
    console.error('couldnt perform good handling', error);
    return error;
  }
};

//
async function syntacticSimplification() {
  //
  var dazzle = document.querySelector(".dazzle");
  var p = document.createElement("p");
  var p2 = document.createElement("p");

  //
  var text = document.createTextNode("Zinsbouw vereenvoudigen...");
  var prompt = document.createTextNode("...");
  p.appendChild(prompt);
  dazzle.appendChild(p);
  p2.appendChild(text);
  dazzle.appendChild(p2);

  //
  var selectedText = window.getSelection().toString();
  const response = await callPythonFunctionSyntacticSimplification(
    selectedText
  );
  prompt.nodeValue = JSON.stringify(response.prompt);
  text.nodeValue = JSON.stringify(response.result);
}

//
function insertAfter(newNode, existingNode) {
  console.log(newNode, existingNode);
  console.log(existingNode.parent, existingNode.nextSibling);
  existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

// simplify sentence structure
document.addEventListener("DOMContentLoaded", () => {
  const spans = document.querySelectorAll(".sentence");
  spans.forEach((span) => {
    span.addEventListener("click", async (event) => {
      sentence_of_origin = span.closest(".sentence");

      //
      var context = "";
      for (const child of sentence_of_origin.children) {
        context = context + " " + child.textContent;
      }

      //
      const response = await callPythonFunctionSyntacticSimplification(context);
      var p = document.createElement("p");
      newNode = document.createTextNode(JSON.stringify(response.result));

      //
      p.append(newNode);
      insertAfter(p, span);

      //
      sentence_of_origin.innerHTML = "<del>" + context + "</del>";
      parent = sentence_of_origin.parent;
    });
  });
});
