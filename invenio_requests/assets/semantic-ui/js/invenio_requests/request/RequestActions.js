import React, { Component } from "react";
import { Button, Modal, Form, Header } from "semantic-ui-react";
import ReactDOM from "react-dom";

const element = document.getElementById("request-actions");

const modal = (func, actionName, positive) => {
  const placeholder = actionName + " comment";
  return (
    <>
      <Modal
        as={Form}
        onSubmit={(e) => func(e)}
        trigger={
          positive ? (
            <Button positive>{actionName}</Button>
          ) : (
            <Button negative>{actionName}</Button>
          )
        }
        size="tiny"
      >
        <Modal.Content>
          <Form.Input
            label={actionName}
            type="text"
            placeholder={placeholder}
          />
        </Modal.Content>
        <Modal.Actions>
          <Button color="red" icon="times" content="Close" />
          <Button
            type="submit"
            color="green"
            icon="check"
            content={actionName}
          />
        </Modal.Actions>
      </Modal>
    </>
  );
};

const buttons = (request, accept, decline, cancel) => {
  return (
    <>
      {modal(accept, "Accept", true)}
      {modal(decline, "Decline", false)}
      {modal(cancel, "Cancel", false)}
    </>
  );
};

export const RequestActions = ({ request, accept, decline, cancel }) => {
  return ReactDOM.createPortal(
    buttons(request, accept, decline, cancel),
    element
  );
};
