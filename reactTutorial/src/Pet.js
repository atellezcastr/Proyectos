import React from 'react';

const Pet = (props) => {
    return React.createElement("div", {}, [
      React.createElement("h2", {}, props.name),
      React.createElement("h3", {}, props.type),
      React.createElement("h3", {}, props.Last),
    ]);
  };

export default Pet;