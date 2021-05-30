import React from 'react';
import ReactDOM from 'react-dom';
import Pet from "./Pet";

const App = () => {
  return React.createElement("div", {}, [
    React.createElement("h1", { id: "first-title" }, "Try this!"),
    React.createElement(Pet, {
      name: "Trial 1",
      type: "Test 1",
      Last: "Sub-test 1",
    }),
    React.createElement(Pet, {
      name: "Trial 2",
      type: "Test 2",
      Last: "Sub-test 2",
    }),
    React.createElement(Pet, {
      name: "Trial 3",
      type: "Test 3",
      Last: "Sub-test 3",
    }),
  ]);
};

ReactDOM.render(React.createElement(App), document.getElementById("root"));
