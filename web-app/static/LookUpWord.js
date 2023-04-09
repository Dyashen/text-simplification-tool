const callPythonFunctionLookUp = async (word, context) => {
  try {
    const response = await fetch(
      `http://localhost:5000/look-up-word?word=${word}&context=${context}`
    );
    return (result = await response.json());
  } catch (error) {
    console.error(error);
  }
};

//
document.addEventListener("DOMContentLoaded", () => {
  const spans = document.querySelectorAll(".word");
  spans.forEach((span) => {
    span.addEventListener("click", async (event) => {
      sentence_of_origin = span.closest(".sentence");
      var context = "";
      for (const child of sentence_of_origin.children) {
        context = context + " " + child.textContent;
      }

      const word = event.target.textContent;
      const response = await callPythonFunctionLookUp(word, context);
      var dazzle = document.querySelector(".dazzle");
      var p = document.createElement("p");
      var p2 = document.createElement("p");
      var text = document.createTextNode(JSON.stringify(response.result));
      var prompt = document.createTextNode(JSON.stringify(response.prompt));
      p.appendChild(prompt);
      dazzle.appendChild(p);
      p2.appendChild(text);
      dazzle.appendChild(p2);
    });
  });
});
