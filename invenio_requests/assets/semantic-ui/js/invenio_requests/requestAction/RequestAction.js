import React, { Component } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { RequestActions } from "../request/RequestActions";

class RequestAction extends Component {
  accept = async (event) => {
    const { acceptRequest, request } = this.props;
    const format = "html";
    const content = "First test";
    console.log(event.target.value);
    if (!content) return;

    try {
      await acceptRequest({ content, format, request });
      //TODO
    } catch (error) {
      // TODO
    }
  };

  decline = async (event) => {
    const { declineRequest, request } = this.props;
    const format = "html";
    const content = "First test";
    console.log(event.target.value);
    if (!content) return;

    try {
      await declineRequest({ content, format, request });
      //TODO
    } catch (error) {
      // TODO
    }
  };

  cancel = async (content, format) => {
    const { cancelRequest, request } = this.props;
    if (!content) return;

    try {
      await cancelRequest({ content, format, request });
      //TODO
    } catch (error) {
      // TODO
    }
  };

  render() {
    const { action, request } = this.props;

    return (
      <Overridable id="RequestAction.layout" event={action}>
        <RequestActions
          request={request}
          accept={this.accept}
          decline={this.decline}
          cancel={this.cancel}
        />
      </Overridable>
    );
  }
}

RequestAction.propTypes = {
  action: PropTypes.object,
  acceptRequest: PropTypes.func,
  declineRequest: PropTypes.func,
  cancelRequest: PropTypes.func,
};

RequestAction.defaultProps = {
  action: {},
};

export default Overridable.component("RequestAction", RequestAction);
