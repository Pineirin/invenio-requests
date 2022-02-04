import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from "semantic-ui-react";
import ReactDOM from "react-dom";

const element = document.getElementById("request-actions");

export const RequestActions = () =>{
  return ReactDOM.createPortal(<Button positive> I am an action</Button>, element);
}
